"""
main.py
AI Shield Scanner — lightweight API.
No database. No auth. Just run it and start scanning.

Start:  uvicorn main:app --reload --port 8000
UI:     http://localhost:8000
Docs:   http://localhost:8000/docs
"""
import logging
import asyncio
import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

import backend.Detection as detection
import backend.Scanner  as scanner
from backend.Prompt_library import get_all_categories, get_prompts, PromptCategory, Prompt

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s  %(message)s")
logger = logging.getLogger("aishield")

_scan_store: dict[str, dict] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading semantic detection model…")
    await detection.load_model()
    logger.info("AI Shield Scanner ready.")
    yield


app = FastAPI(
    title="AI Shield Scanner",
    version="1.0.0",
    description="Automated prompt injection & data leakage scanner for AI chatbots.",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Serve the custom UI at / ──────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_ui():
    ui_path = os.path.join(os.path.dirname(__file__), "scanner_ui.html")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h2>UI not found — place scanner_ui.html next to main.py</h2>", status_code=404)


# ── Models ────────────────────────────────────────────────────────────────────
class ExtraPrompt(BaseModel):
    id: str = "CUSTOM"
    text: str
    description: str = "Custom prompt"
    severity: str = "medium"


class ScanRequest(BaseModel):
    endpoint_url: str
    api_key: str = ""
    model_name: str = "gpt-4o"
    categories: Optional[list[str]] = None
    intensity: str = "medium"
    max_prompts: Optional[int] = None
    extra_prompts: Optional[list[ExtraPrompt]] = None   # ← custom prompts from UI

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "endpoint_url": "https://api.openai.com/v1/chat/completions",
                "api_key": "sk-...",
                "model_name": "gpt-4o",
                "categories": ["direct_injection", "jailbreak"],
                "intensity": "medium",
                "extra_prompts": [
                    {"id": "CUSTOM-1", "text": "My own attack prompt here", "description": "Custom test", "severity": "high"}
                ]
            }]
        }
    }


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["meta"], include_in_schema=False)
async def health():
    return {"status": "ok", "semantic_model_loaded": detection._model is not None}


# ── Scan endpoints ─────────────────────────────────────────────────────────────
@app.post("/scan", tags=["scan"])
async def start_scan(req: ScanRequest):
    """Run a full scan. Custom prompts in extra_prompts are appended to the library."""
    try:
        # Build extra Prompt objects from UI custom prompts
        extras: list[Prompt] = []
        for ep in (req.extra_prompts or []):
            extras.append(Prompt(
                id=ep.id,
                category=PromptCategory.DIRECT_INJECTION,   # custom → treated as injection
                text=ep.text,
                description=ep.description,
                severity=ep.severity,
                tags=["custom"],
            ))

        result = await scanner.run_scan(
            endpoint_url=req.endpoint_url,
            api_key=req.api_key,
            model_name=req.model_name,
            categories=req.categories,
            intensity=req.intensity,
            max_prompts=req.max_prompts,
            extra_prompts=extras,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    scan_id = result["summary"]["scan_id"]
    _scan_store[scan_id] = result
    return result


@app.get("/scan/{scan_id}/fails", tags=["scan"])
async def get_failures(scan_id: str):
    """Return only FAIL results from a scan."""
    result = _scan_store.get(scan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Scan not found.")
    fails = [r for r in (result.get("results") or []) if r["label"] == "fail"]
    return {"scan_id": scan_id, "fail_count": len(fails), "fails": fails}


@app.delete("/scan/{scan_id}", tags=["scan"])
async def delete_scan(scan_id: str):
    """Remove a scan from memory."""
    if scan_id not in _scan_store:
        raise HTTPException(status_code=404, detail="Scan not found.")
    del _scan_store[scan_id]
    return {"deleted": scan_id}


@app.get("/scans", tags=["scan"])
async def list_scans():
    """List all scan results in memory."""
    return {
        "scans": [
            {
                "scan_id":  sid,
                "status":   data.get("status", "completed"),
                "severity": data.get("summary", {}).get("overall_severity") if data.get("summary") else None,
                "score":    data.get("summary", {}).get("max_score") if data.get("summary") else None,
            }
            for sid, data in _scan_store.items()
        ]
    }