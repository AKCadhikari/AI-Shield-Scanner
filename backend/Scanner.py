"""
scanner.py
Core scan engine. Sends prompts to the target chatbot and returns results.
Supports real server-side cancellation via cancel_scan(scan_id).
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

# Registry of active scans: scan_id → asyncio.Task
_active_scans: dict[str, asyncio.Task] = {}


def cancel_scan(scan_id: str) -> bool:
    """Cancel a running scan by ID. Returns True if found and cancelled."""
    task = _active_scans.get(scan_id)
    if task and not task.done():
        task.cancel()
        logger.info("Scan %s cancelled by user.", scan_id)
        return True
    return False


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
            if resp.status == 429:
                retry_after = float(resp.headers.get("Retry-After", "5"))
                raise aiohttp.ClientResponseError(
                    resp.request_info, resp.history,
                    status=429, message=f"Rate limited — retry after {retry_after}s",
                )
            resp.raise_for_status()
            data = await resp.json()

            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            if "content" in data and isinstance(data["content"], list):
                return data["content"][0].get("text", "")
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
                break
            except asyncio.CancelledError:
                raise   # propagate — scan is being stopped
            except aiohttp.ClientResponseError as e:
                if e.status == 429 and attempt < retries:
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
            "prompt_id":      prompt.id,
            "category":       prompt.category.value,
            "description":    prompt.description,
            "severity_hint":  prompt.severity,
            "prompt_text":    prompt.text,
            "response_text":  response_text,
            "label":          detection.label.value,
            "matches": [
                {
                    "leak_type":  m.leak_type.value,
                    "evidence":   m.evidence,
                    "rule":       m.rule_id,
                    "confidence": m.confidence,
                }
                for m in detection.matches
            ],
            "semantic_score": detection.semantic_score,
            "reasoning":      detection.reasoning,
            "risk_score":     risk.score,
            "severity":       risk.severity.value,
            "mitigation":     risk.mitigation,
            "error":          error,
        }


async def _do_scan(
    scan_id: str,
    prompts: list,
    endpoint_url: str,
    api_key: str,
    model_name: str,
    cfg: dict,
) -> dict:
    """Inner coroutine that runs all prompts. Wrapped in a Task so it can be cancelled."""
    semaphore = asyncio.Semaphore(cfg["concurrency"])

    tasks = [
        asyncio.ensure_future(
            _run_one(p, endpoint_url, api_key, model_name, semaphore,
                     cfg["delay"], timeout=cfg["timeout"], retries=cfg["retries"])
        )
        for p in prompts
    ]

    results = []
    try:
        results = list(await asyncio.gather(*tasks))
    except asyncio.CancelledError:
        # Cancel every sub-task immediately
        for t in tasks:
            t.cancel()
        # Collect whatever finished before cancellation
        for t in tasks:
            if t.done() and not t.cancelled() and t.exception() is None:
                results.append(t.result())
        logger.info("Scan %s stopped — collected %d partial results.", scan_id, len(results))
        raise   # re-raise so the outer task is also marked cancelled

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
    """
    Main entry point. scan_id is pre-assigned by main.py so the client
    can call /scan/{scan_id}/cancel before the scan finishes.
    """
    if scan_id is None:
        scan_id = str(uuid.uuid4())

    cats = [PromptCategory(c) for c in categories] if categories else None
    prompts = get_prompts(cats)
    if max_prompts:
        prompts = prompts[:max_prompts]
    if extra_prompts:
        prompts = list(prompts) + list(extra_prompts)
        logger.info("Added %d custom prompt(s) from UI", len(extra_prompts))

    cfg = INTENSITY_SETTINGS.get(intensity, INTENSITY_SETTINGS["medium"])

    logger.info("Scan %s started — %d prompts, intensity=%s, target=%s",
                scan_id, len(prompts), intensity, endpoint_url)

    # Wrap in a Task and register it so cancel_scan() can reach it
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
    summary["scan_id"]        = scan_id
    summary["total_prompts"]  = len(prompts)
    summary["completed"]      = len(results)
    summary["cancelled"]      = cancelled
    summary["pass_count"]     = sum(1 for r in results if r["label"] == "pass")
    summary["warning_count"]  = sum(1 for r in results if r["label"] == "warning")
    summary["fail_count"]     = sum(1 for r in results if r["label"] == "fail")

    logger.info("Scan %s %s — fail=%d warn=%d pass=%d score=%.1f",
                scan_id, "CANCELLED" if cancelled else "complete",
                summary["fail_count"], summary["warning_count"],
                summary["pass_count"], summary["max_score"])

    return {"summary": summary, "results": results}