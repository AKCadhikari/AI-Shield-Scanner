"""
scanner.py
Core scan engine. Sends prompts to the target chatbot and returns results.
No database. Results are returned as plain Python dicts.
"""
from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Optional

import aiohttp

from backend.api.Prompt_library import get_prompts, PromptCategory, Prompt
from backend.api.Detection import analyse, Label
from backend.api.Risk_scoring import score as risk_score, aggregate, CATEGORY_TO_VULN

logger = logging.getLogger("aishield")

INTENSITY_SETTINGS = {
    "low":    {"concurrency": 1, "delay": 2.0},
    "medium": {"concurrency": 3, "delay": 0.5},
    "high":   {"concurrency": 5, "delay": 0.1},
}


async def _call_chatbot(
    endpoint_url: str,
    api_key: str,
    model_name: str,
    prompt_text: str,
    timeout: int = 30,
) -> str:
    """Send one prompt to the target chatbot and return its response as a string."""
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt_text}],
        "max_tokens": 512,
        "temperature": 0,
    }

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
        async with session.post(endpoint_url, json=payload, headers=headers) as resp:
            resp.raise_for_status()
            data = await resp.json()

            # OpenAI / Anthropic / Azure style
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            # Anthropic Messages API style
            if "content" in data and isinstance(data["content"], list):
                return data["content"][0].get("text", "")
            # Fallback
            return str(data)


async def _run_one(
    prompt: Prompt,
    endpoint_url: str,
    api_key: str,
    model_name: str,
    semaphore: asyncio.Semaphore,
    delay: float,
) -> dict:
    async with semaphore:
        response_text = ""
        error = None

        try:
            response_text = await _call_chatbot(endpoint_url, api_key, model_name, prompt.text)
        except Exception as e:
            error = str(e)
            logger.warning("Prompt %s failed to reach target: %s", prompt.id, e)

        detection = analyse(response_text)

        risk = risk_score(
            category=prompt.category.value,
            severity_hint=prompt.severity,
            num_matches=len(detection.matches),
            semantic_score=detection.semantic_score,
        )

        await asyncio.sleep(delay)

        return {
            "prompt_id":       prompt.id,
            "category":        prompt.category.value,
            "description":     prompt.description,
            "severity_hint":   prompt.severity,
            "prompt_text":     prompt.text,
            "response_text":   response_text,
            "label":           detection.label.value,
            "matches":         [
                {
                    "leak_type":  m.leak_type.value,
                    "evidence":   m.evidence,
                    "rule":       m.rule_id,
                    "confidence": m.confidence,
                }
                for m in detection.matches
            ],
            "semantic_score":  detection.semantic_score,
            "reasoning":       detection.reasoning,
            "risk_score":      risk.score,
            "severity":        risk.severity.value,
            "mitigation":      risk.mitigation,
            "error":           error,
        }


async def run_scan(
    endpoint_url: str,
    api_key: str = "",
    model_name: str = "gpt-3.5-turbo",
    categories: Optional[list[str]] = None,
    intensity: str = "medium",
    max_prompts: Optional[int] = None,
) -> dict:
    """
    Main entry point.

    Parameters
    ----------
    endpoint_url : str   — full URL of the chatbot API e.g. https://api.openai.com/v1/chat/completions
    api_key      : str   — Bearer token (leave blank if none)
    model_name   : str   — model identifier e.g. gpt-4o, claude-3-5-sonnet-20241022
    categories   : list  — which attack categories to test (None = all)
    intensity    : str   — low | medium | high
    max_prompts  : int   — cap total prompts (useful for quick tests)

    Returns
    -------
    dict with summary + full results list
    """
    # Build prompt list
    cats = [PromptCategory(c) for c in categories] if categories else None
    prompts = get_prompts(cats)
    if max_prompts:
        prompts = prompts[:max_prompts]

    cfg = INTENSITY_SETTINGS.get(intensity, INTENSITY_SETTINGS["medium"])
    semaphore = asyncio.Semaphore(cfg["concurrency"])

    logger.info("Scan started — %d prompts, intensity=%s, target=%s",
                len(prompts), intensity, endpoint_url)

    tasks = [
        _run_one(p, endpoint_url, api_key, model_name, semaphore, cfg["delay"])
        for p in prompts
    ]
    results = await asyncio.gather(*tasks)

    summary = aggregate(list(results))
    summary["scan_id"]       = str(uuid.uuid4())
    summary["total_prompts"] = len(results)
    summary["pass_count"]    = sum(1 for r in results if r["label"] == "pass")
    summary["warning_count"] = sum(1 for r in results if r["label"] == "warning")
    summary["fail_count"]    = sum(1 for r in results if r["label"] == "fail")

    logger.info("Scan complete — fail=%d warn=%d pass=%d overall=%s score=%.1f",
                summary["fail_count"], summary["warning_count"], summary["pass_count"],
                summary["overall_severity"], summary["max_score"])

    return {"summary": summary, "results": list(results)}