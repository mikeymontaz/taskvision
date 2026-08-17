"""TaskVision vision relay — starter implementation.

Receives a camera frame (base64) + mode from the SPECS Lens, calls an
AI vision/LLM service, and returns a structured TaskGuide JSON that the
Lens renderer can display directly.

Usage:
    export AI_SERVICE_URL="https://api.openai.com/v1/chat/completions"
    export AI_API_KEY="sk-..."
    python scripts/vision_relay.py

Exposes: POST /analyze  { "mode": "...", "frame_base64": "...", "use_seed": bool }
         GET  /health
"""

import base64
import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="TaskVision Relay")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

AI_SERVICE_URL = os.environ.get("AI_SERVICE_URL")
AI_API_KEY = os.environ.get("AI_API_KEY")

MODE_PROMPTS = {
    "kitchen": (
        "You are a chef assistant. The image shows ingredients on a kitchen counter. "
        "Identify the ingredients, then generate a simple, delicious recipe that uses them. "
        "Return JSON exactly matching this schema: "
        '{"title": str, "objectName": str, "confidence": float, '
        '"steps": [{"text": str, "durationSeconds": int or null, "checklist": [str] or null}]}'
    ),
    "plant": (
        "You are a plant-care expert. The image shows a houseplant. Diagnose its condition "
        "(health, over/underwatering, light stress, pests) and generate a recovery guide. "
        "Return JSON exactly matching the TaskGuide schema: "
        '{"title": str, "objectName": str, "confidence": float, '
        '"steps": [{"text": str, "durationSeconds": int or null, "checklist": [str] or null}]}'
    ),
    "fixit": (
        "You are a repair technician. The image shows a broken or problematic household object. "
        "Identify the object and the most likely problem, then generate a safe, step-by-step fix. "
        "Return JSON exactly matching the TaskGuide schema: "
        '{"title": str, "objectName": str, "confidence": float, '
        '"steps": [{"text": str, "durationSeconds": int or null, "checklist": [str] or null}]}'
    ),
}

SEED_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "tasks", "tasks.json")


class AnalyzeRequest(BaseModel):
    mode: str
    frame_base64: str | None = None
    use_seed: bool = False


def load_seed(mode: str) -> dict | None:
    try:
        with open(SEED_PATH) as f:
            data = json.load(f)
        guides = data.get("modes", {}).get(mode, {}).get("seedGuides", [])
        return guides[0] if guides else None
    except Exception:
        return None


def call_ai(mode: str, frame_b64: str) -> dict:
    if not AI_SERVICE_URL or not AI_API_KEY:
        raise HTTPException(503, "AI service not configured (set AI_SERVICE_URL + AI_API_KEY)")

    prompt = MODE_PROMPTS.get(mode, MODE_PROMPTS["fixit"])
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{frame_b64}"},
                    },
                ],
            }
        ],
        "max_tokens": 1200,
    }
    resp = requests.post(
        AI_SERVICE_URL,
        headers={"Authorization": f"Bearer {AI_API_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"AI service error: {resp.text[:300]}")

    raw = resp.json()["choices"][0]["message"]["content"]
    # Extract the first JSON object from the response (LLMs may wrap it in markdown)
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start == -1 or end == 0:
        raise HTTPException(502, "AI response did not contain valid JSON")
    return json.loads(raw[start:end])


@app.get("/health")
def health():
    configured = bool(AI_SERVICE_URL and AI_API_KEY)
    return {"status": "ok", "ai_configured": configured}


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    if req.use_seed or req.frame_base64 is None:
        seed = load_seed(req.mode)
        if not seed:
            raise HTTPException(404, f"No seed guide for mode: {req.mode}")
        return seed

    guide = call_ai(req.mode, req.frame_base64)

    # Normalize: ensure steps list exists and required keys present
    guide.setdefault("steps", [])
    for step in guide["steps"]:
        step.setdefault("durationSeconds", None)
        step.setdefault("checklist", None)
    return guide


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
