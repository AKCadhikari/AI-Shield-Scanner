"""
main.py
AI Shield Scanner — lightweight API.
No database. No auth. Just run it and start scanning.

Start:  uvicorn main:app --reload --port 8000
Docs:   http://localhost:8000/docs
"""
import logging
import asyncio
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import Detection
import Scanner
from Prompt_library import get_all_categories, get_prompts, PromptCategory

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s  %(message)s")
logger = logging.getLogger("aishield")

# In-memory store for scan results (no DB needed)
_scan_store: dict[str, dict] = {}


# ── Startup: load semantic model ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading semantic detection model…")
    await Detection.load_model()
    logger.info("AI Shield Scanner ready.")
    yield


app = FastAPI(
    title="AI Shield Scanner",
    version="1.0.0",
    description="Automated prompt injection & data leakage scanner for AI chatbots.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ─────────────────────────────────────────────────
class ScanRequest(BaseModel):
    endpoint_url: str
    api_key: str = ""
    model_name: str = "gpt-3.5-turbo"
    categories: Optional[list[str]] = None    # None = all categories
    intensity: str = "medium"                 # low | medium | high
    max_prompts: Optional[int] = None         # cap for quick tests

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "endpoint_url": "https://api.openai.com/v1/chat/completions",
                    "api_key": "sk-...",
                    "model_name": "gpt-4o",
                    "categories": ["direct_injection", "jailbreak"],
                    "intensity": "medium",
                }
            ]
        }
    }


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok", "semantic_model_loaded": Detection._model is not None}


@app.get("/categories", tags=["prompts"])
async def list_categories():
    """Return all available attack categories."""
    return {"categories": get_all_categories()}


@app.get("/prompts", tags=["prompts"])
async def list_prompts(category: Optional[str] = None):
    """List all built-in prompts, optionally filtered by category."""
    cats = [PromptCategory(category)] if category else None
    prompts = get_prompts(cats)
    return {
        "total": len(prompts),
        "prompts": [
            {
                "id":          p.id,
                "category":    p.category.value,
                "description": p.description,
                "severity":    p.severity,
                "tags":        p.tags,
            }
            for p in prompts
        ],
    }


@app.post("/scan", tags=["scan"])
async def start_scan(req: ScanRequest):
    """
    Run a full scan against the target chatbot.
    Returns immediately with the complete results.
    (For large scans use /scan/async instead.)
    """
    try:
        result = await Scanner.run_scan(
            endpoint_url=req.endpoint_url,
            api_key=req.api_key,
            model_name=req.model_name,
            categories=req.categories,
            intensity=req.intensity,
            max_prompts=req.max_prompts,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    scan_id = result["summary"]["scan_id"]
    _scan_store[scan_id] = result
    return result


@app.post("/scan/async", tags=["scan"])
async def start_scan_async(req: ScanRequest):
    """
    Fire-and-forget scan. Returns a scan_id immediately.
    Poll /scan/{scan_id} for results.
    """
    scan_id = f"scan-{__import__('uuid').uuid4()}"
    _scan_store[scan_id] = {"status": "running", "summary": None, "results": None}

    async def _run():
        try:
            result = await Scanner.run_scan(
                endpoint_url=req.endpoint_url,
                api_key=req.api_key,
                model_name=req.model_name,
                categories=req.categories,
                intensity=req.intensity,
                max_prompts=req.max_prompts,
            )
            _scan_store[scan_id] = {"status": "completed", **result}
        except Exception as e:
            _scan_store[scan_id] = {"status": "failed", "error": str(e)}

    asyncio.create_task(_run())
    return {"scan_id": scan_id, "status": "running"}


@app.get("/scan/{scan_id}", tags=["scan"])
async def get_scan(scan_id: str):
    """Get the results of a previous scan."""
    result = _scan_store.get(scan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Scan not found.")
    return result


@app.get("/scan/{scan_id}/fails", tags=["scan"])
async def get_failures(scan_id: str):
    """Return only the FAIL results from a scan — useful for quick review."""
    result = _scan_store.get(scan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Scan not found.")
    if result.get("status") == "running":
        return {"status": "running"}
    fails = [r for r in (result.get("results") or []) if r["label"] == "fail"]
    return {"scan_id": scan_id, "fail_count": len(fails), "fails": fails}


@app.delete("/scan/{scan_id}", tags=["scan"])
async def delete_scan(scan_id: str):
    """Remove a scan result from memory."""
    if scan_id not in _scan_store:
        raise HTTPException(status_code=404, detail="Scan not found.")
    del _scan_store[scan_id]
    return {"deleted": scan_id}


@app.get("/scans", tags=["scan"])
async def list_scans():
    """List all scan IDs currently in memory."""
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