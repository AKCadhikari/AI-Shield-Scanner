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

from backend.Prompt_library import get_prompts, PromptCategory, Prompt
from backend.Detection import analyse, Label
from backend.Risk_scoring import score as risk_score, aggregate, CATEGORY_TO_VULN

logger = logging.getLogger("aishield")

INTENSITY_SETTINGS = {
    "low":    {"concurrency": 1, "delay": 2.0,  "timeout": 30,  "retries": 1},
    "medium": {"concurrency": 2, "delay": 1.5,  "timeout": 60,  "retries": 2},
    "high":   {"concurrency": 3, "delay": 0.8,  "timeout": 90,  "retries": 3},
}


async def _call_chatbot(
    endpoint_url: str,
    api_key: str,
    model_name: str,
    prompt_text: str,
    timeout: int = 60,
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
            # Handle 429 rate-limit — raise so caller can retry
            if resp.status == 429:
                retry_after = float(resp.headers.get("Retry-After", "5"))
                raise aiohttp.ClientResponseError(
                    resp.request_info, resp.history,
                    status=429, message=f"Rate limited — retry after {retry_after}s",
                )
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
    timeout: int = 60,
    retries: int = 2,
) -> dict:
    async with semaphore:
        response_text = ""
        error = None

        for attempt in range(retries + 1):
            try:
                response_text = await _call_chatbot(
                    endpoint_url, api_key, model_name, prompt.text, timeout=timeout
                )
                error = None
                break   # success
            except aiohttp.ClientResponseError as e:
                if e.status == 429 and attempt < retries:
                    # Exponential back-off: 5s, 10s, 20s …
                    wait = 5 * (2 ** attempt)
                    logger.warning("Rate limited on %s — waiting %ds (attempt %d/%d)",
                                   prompt.id, wait, attempt + 1, retries)
                    await asyncio.sleep(wait)
                else:
                    error = str(e)
                    logger.warning("Prompt %s failed: %s", prompt.id, e)
                    break
            except asyncio.TimeoutError:
                error = f"Request timed out after {timeout}s"
                logger.warning("Prompt %s timed out", prompt.id)
                break
            except Exception as e:
                error = str(e)
                logger.warning("Prompt %s failed to reach target: %s", prompt.id, e)
                break

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
    model_name: str = "gpt-4o",
    categories: Optional[list[str]] = None,
    intensity: str = "medium",
    max_prompts: Optional[int] = None,
    extra_prompts: Optional[list] = None,   # list of Prompt objects from UI custom input
) -> dict:
    """
    Main entry point.

    Parameters
    ----------
    endpoint_url  : str   — full URL of the chatbot API
    api_key       : str   — Bearer token (leave blank if none)
    model_name    : str   — model identifier e.g. gpt-4o
    categories    : list  — which attack categories to test (None = all)
    intensity     : str   — low | medium | high
    max_prompts   : int   — cap total library prompts (custom prompts always included)
    extra_prompts : list  — additional Prompt objects from the UI custom prompt input

    Returns
    -------
    dict with summary + full results list
    """
    # Build prompt list from library
    cats = [PromptCategory(c) for c in categories] if categories else None
    prompts = get_prompts(cats)
    if max_prompts:
        prompts = prompts[:max_prompts]

    # Append any custom prompts from the UI — always run, not subject to max_prompts cap
    if extra_prompts:
        prompts = list(prompts) + list(extra_prompts)
        logger.info("Added %d custom prompt(s) from UI", len(extra_prompts))

    cfg = INTENSITY_SETTINGS.get(intensity, INTENSITY_SETTINGS["medium"])
    semaphore = asyncio.Semaphore(cfg["concurrency"])

    logger.info("Scan started — %d prompts, intensity=%s, target=%s",
                len(prompts), intensity, endpoint_url)

    tasks = [
        _run_one(p, endpoint_url, api_key, model_name, semaphore, cfg["delay"],
                 timeout=cfg["timeout"], retries=cfg["retries"])
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