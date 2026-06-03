"""
scanner.py
Core scan engine. Auto-detects provider from the endpoint URL.
Supports: OpenAI-compatible, Anthropic, Google Gemini, Ollama, Cohere.
User just pastes their endpoint URL — no manual provider selection needed.
"""
from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Optional

import aiohttp

from backend.Prompt_library import get_prompts, PromptCategory, Prompt
from backend.Detection import analyse, Label
from backend.Risk_scoring import score as risk_score, aggregate

logger = logging.getLogger("aishield")

INTENSITY_SETTINGS = {
    "low":    {"concurrency": 1, "delay": 2.0},
    "medium": {"concurrency": 3, "delay": 0.5},
    "high":   {"concurrency": 5, "delay": 0.1},
}

_active_scans: dict[str, asyncio.Task] = {}


def cancel_scan(scan_id: str) -> bool:
    task = _active_scans.get(scan_id)
    if task and not task.done():
        task.cancel()
        logger.info("Scan %s cancelled by user.", scan_id)
        return True
    return False


# ── Auto-detect provider from URL ────────────────────────────────────────────

def _detect_provider(endpoint_url: str) -> str:
    url = endpoint_url.lower()
    if "anthropic.com" in url:
        return "anthropic"
    if "generativelanguage.googleapis.com" in url:
        return "gemini"
    if "localhost:11434" in url or "127.0.0.1:11434" in url or "ollama" in url:
        return "ollama"
    if "cohere.ai" in url or "cohere.com" in url:
        return "cohere"
    # OpenAI, Azure, OpenRouter, Together, any OpenAI-compatible
    return "openai"


# ── Build request per provider ────────────────────────────────────────────────

def _build_request(provider: str, model_name: str, api_key: str,
                   endpoint_url: str, prompt_text: str):
    """Returns (final_url, headers, payload)."""

    if provider == "anthropic":
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }
        payload = {
            "model": model_name,
            "max_tokens": 512,
            "messages": [{"role": "user", "content": prompt_text}],
        }
        return endpoint_url, headers, payload

    if provider == "gemini":
        # Key goes in URL query param; model goes in the URL path not the body
        url = endpoint_url
        if api_key and "key=" not in url:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}],
            "generationConfig": {"maxOutputTokens": 512, "temperature": 0.0},
        }
        return url, headers, payload

    if provider == "ollama":
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt_text}],
            "stream": False,
        }
        return endpoint_url, headers, payload

    if provider == "cohere":
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": model_name,
            "message": prompt_text,
            "max_tokens": 512,
            "temperature": 0,
        }
        return endpoint_url, headers, payload

    # Default: OpenAI-compatible
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt_text}],
        "max_tokens": 512,
        "temperature": 0,
    }
    return endpoint_url, headers, payload


# ── Parse response per provider ───────────────────────────────────────────────

def _parse_response(provider: str, data: dict) -> str:
    if provider == "anthropic":
        content = data.get("content", [])
        if isinstance(content, list) and content:
            return content[0].get("text", "")

    elif provider == "gemini":
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            reason = data.get("promptFeedback", {}).get("blockReason", "")
            return f"[Blocked: {reason}]" if reason else str(data)

    elif provider == "ollama":
        msg = data.get("message", {})
        if isinstance(msg, dict):
            return msg.get("content", "")
        return data.get("response", str(data))

    elif provider == "cohere":
        return data.get("text", str(data))

    # OpenAI-compatible — also used as final fallback
    if "choices" in data:
        choice = data["choices"][0]
        if "message" in choice:
            return choice["message"].get("content", "")
        if "text" in choice:
            return choice["text"]

    # Anthropic-style fallback
    if "content" in data and isinstance(data["content"], list):
        return data["content"][0].get("text", "")

    if "completion" in data:
        return data["completion"]

    return str(data)


# ── HTTP call ─────────────────────────────────────────────────────────────────

async def _call_chatbot(
    endpoint_url: str,
    api_key: str,
    model_name: str,
    prompt_text: str,
    timeout: int = 30,
) -> str:
    provider = _detect_provider(endpoint_url)
    url, headers, payload = _build_request(
        provider, model_name, api_key, endpoint_url, prompt_text
    )

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=timeout)
    ) as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if not resp.ok:
                try:
                    err = await resp.json(content_type=None)
                    msg = (
                        err.get("error", {}).get("message")   # OpenAI
                        or err.get("message")                  # Anthropic / Gemini
                        or err.get("detail")                   # FastAPI
                        or str(err)
                    )
                except Exception:
                    msg = await resp.text()
                raise ValueError(f"HTTP {resp.status} ({provider}): {str(msg)[:300]}")

            data = await resp.json(content_type=None)
            return _parse_response(provider, data)


# ── Per-prompt worker ─────────────────────────────────────────────────────────

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
            response_text = await _call_chatbot(
                endpoint_url, api_key, model_name, prompt.text
            )
        except asyncio.CancelledError:
            raise
        except Exception as e:
            error = str(e)
            logger.warning("Prompt %s failed: %s", prompt.id, e)

        detection = analyse(response_text)
        risk = risk_score(
            category=prompt.category.value,
            severity_hint=prompt.severity,
            num_matches=len(detection.matches),
            semantic_score=detection.semantic_score,
        )
        await asyncio.sleep(delay)

        return {
            "prompt_id":      prompt.id,
            "category":       prompt.category.value,
            "description":    prompt.description,
            "severity_hint":  prompt.severity,
            "prompt_text":    prompt.text,
            "response_text":  response_text,
            "label":          detection.label.value,
            "matches": [
                {"leak_type": m.leak_type.value, "evidence": m.evidence,
                 "rule": m.rule_id, "confidence": m.confidence}
                for m in detection.matches
            ],
            "semantic_score": detection.semantic_score,
            "reasoning":      detection.reasoning,
            "risk_score":     risk.score,
            "severity":       risk.severity.value,
            "mitigation":     risk.mitigation,
            "error":          error,
        }


# ── Scan orchestrator ─────────────────────────────────────────────────────────

async def _do_scan(scan_id, prompts, endpoint_url, api_key, model_name, cfg):
    semaphore = asyncio.Semaphore(cfg["concurrency"])
    tasks = [
        asyncio.ensure_future(
            _run_one(p, endpoint_url, api_key, model_name, semaphore, cfg["delay"])
        )
        for p in prompts
    ]
    results = []
    try:
        results = list(await asyncio.gather(*tasks))
    except asyncio.CancelledError:
        for t in tasks:
            t.cancel()
        for t in tasks:
            if t.done() and not t.cancelled() and t.exception() is None:
                results.append(t.result())
        logger.info("Scan %s stopped — %d partial results.", scan_id, len(results))
        raise
    return results


async def run_scan(
    endpoint_url: str,
    api_key: str = "",
    model_name: str = "gpt-4o",
    categories: Optional[list[str]] = None,
    intensity: str = "medium",
    max_prompts: Optional[int] = None,
    extra_prompts: Optional[list] = None,
    scan_id: Optional[str] = None,
) -> dict:
    if scan_id is None:
        scan_id = str(uuid.uuid4())

    provider = _detect_provider(endpoint_url)
    logger.info("Auto-detected provider: %s", provider)

    cats = [PromptCategory(c) for c in categories] if categories else None
    prompts = get_prompts(cats)
    if max_prompts:
        prompts = prompts[:max_prompts]
    if extra_prompts:
        prompts = list(prompts) + list(extra_prompts)

    cfg = INTENSITY_SETTINGS.get(intensity, INTENSITY_SETTINGS["medium"])
    logger.info("Scan %s started — %d prompts, provider=%s, intensity=%s",
                scan_id, len(prompts), provider, intensity)

    loop = asyncio.get_event_loop()
    scan_task = loop.create_task(
        _do_scan(scan_id, prompts, endpoint_url, api_key, model_name, cfg)
    )
    _active_scans[scan_id] = scan_task

    cancelled = False
    results = []
    try:
        results = await scan_task
    except asyncio.CancelledError:
        cancelled = True
    finally:
        _active_scans.pop(scan_id, None)

    summary = aggregate(results)
    summary["scan_id"]       = scan_id
    summary["total_prompts"] = len(prompts)
    summary["completed"]     = len(results)
    summary["cancelled"]     = cancelled
    summary["provider"]      = provider
    summary["pass_count"]    = sum(1 for r in results if r["label"] == "pass")
    summary["warning_count"] = sum(1 for r in results if r["label"] == "warning")
    summary["fail_count"]    = sum(1 for r in results if r["label"] == "fail")

    logger.info("Scan %s %s — fail=%d warn=%d pass=%d",
                scan_id, "CANCELLED" if cancelled else "complete",
                summary["fail_count"], summary["warning_count"], summary["pass_count"])

    return {"summary": summary, "results": results}