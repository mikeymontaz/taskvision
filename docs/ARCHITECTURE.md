# TaskVision — Architecture

## System Overview

TaskVision is a vision-in-the-loop spatial experience for SPECS. The core loop is:

**Look → Tap → Glasses capture the scene → AI identifies the object → AI generates a task guide → Guide renders in-world → User completes steps hands-free → Progress persists**

```
┌─────────────┐   camera frame    ┌──────────────┐   HTTPS POST    ┌──────────────────┐
│   SPECS     │ ────────────────► │  vision      │ ──────────────► │  AI vision/LLM   │
│  Lens (UI)  │                   │  relay       │                 │  service         │
│             │ ◄──────────────── │  service     │ ◄────────────── │                  │
│  step cards │   TaskGuide JSON  │  (Python)    │   structured    │  (vision + text) │
│  progress   │                   └──────────────┘   guide         └──────────────────┘
└──────┬──────┘
       │ gesture events (Interaction Kit)
       ▼
┌──────────────┐
│  Snap Cloud  │  ← persistence: mode, step index, checklist flags
└──────────────┘
```

## Component Map

| Component | Location | Responsibility |
|---|---|---|
| Mode selector | World-locked UI (UI Kit) | Choose vision mode: Kitchen / Plant / Fix-it |
| Capture controller | `src/` scripts | CameraModule still-image capture on palm tap, "capturing..." indicator |
| Vision client | `src/` scripts | InternetModule POST of base64 frame + mode, parse TaskGuide JSON |
| Guide renderer | `src/` scripts | World-locked step cards, checklist toggles, countdown ring shader |
| Progress ribbon | World-locked UI | Segmented per-step progress bar with percentage |
| Session manager | `src/` scripts | Snap Cloud save/restore (resume at exact step) |
| Celebration system | `src/` scripts | Completion VFX + record |
| Vision relay | `scripts/vision_relay.py` | Receives frames, calls AI service, returns structured guide |

## Data Contract (TaskGuide JSON)

```json
{
  "title": "One-Pot Jollof Rice",
  "objectName": "tomatoes, onions, red pepper, rice",
  "confidence": 0.92,
  "steps": [
    {
      "text": "Dice the onions and red pepper",
      "durationSeconds": 180,
      "checklist": ["onions diced", "pepper diced"]
    }
  ]
}
```

The same schema is used by the AI-generated guides and the seed templates in `src/tasks/tasks.json`, so the renderer is mode-agnostic.

## Privacy & Publishing Considerations

Spectacles restricts simultaneous camera and internet access in public Lenses. TaskVision uses the experimental workflow (Project Settings → Allow Experimental API + Extended Permissions in the Spectacles app developer settings), which permits camera + internet together. This is fully valid for the hackathon (Lenses remain draft/test, demo recorded with the permitted "Experimental Mode" watermark).

## Extensibility

Adding a new mode requires no code changes: register the mode in the selector and add a system prompt to the relay service's mode map. The Lens itself is deliberately thin — the intelligence lives in the relay + AI service, which is also why CLAD was able to iterate on the full system so quickly.
