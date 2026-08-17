# TaskVision

> **The Lens that sees your world and guides your hands.**

TaskVision is a SPECS spatial experience built for the **CLAD Summer Hackathon — Week 2: "Guide"** ([lenslist.co/clad-summer-hackathon](https://lenslist.co/clad-summer-hackathon)), developed with **CLAD (Closed Loop Agentic Development) in Lens Studio**.

Look at something real, tap, and the glasses figure out what it is — then generate a live, step-by-step spatial guide floating in your field of view to help you complete a real-world task with it. No phone, no search, no decisions. Your glasses see the problem and stream the solution.

## How It Works

The experience runs a vision-in-the-loop pipeline: the SPECS **CameraModule** captures what the user is looking at, the frame is sent to an AI vision service through the **InternetModule (Fetch API)** and a lightweight relay, the response (identified object + generated task plan) comes back as structured JSON, and a **world-locked spatial UI** renders the step-by-step guide directly over the real world. Steps advance hands-free via **Interaction Kit** gestures, and progress persists through **Snap Cloud** so a paused task resumes exactly where it left off.

| Layer | Technology |
|---|---|
| Platform | SPECS (Snap AR glasses), Lens Studio 5.22+ |
| AI development workflow | CLAD (Claude Code + Lens Studio MCP server) |
| Vision pipeline | CameraModule → relay service → AI vision/LLM API |
| Spatial UI | World-locked panels, UI Kit, glass-morphism materials |
| Input | Interaction Kit (palm tap to advance, wrist flick for menu) |
| Persistence | Snap Cloud (JSON: active task, step index, completion flags) |
| Progress feedback | Segmented progress ribbon, per-step countdown rings, completion VFX |

## Repository Structure

```
taskvision/
├── README.md              # This file
├── docs/
│   ├── ARCHITECTURE.md    # Full system architecture and pipeline design
│   ├── BUILD_GUIDE.md     # Step-by-step build instructions (CLAD prompt sequence)
│   └── DEMO_SCRIPT.md     # Shot-by-shot demo video script
├── src/
│   └── tasks/
│       └── tasks.json     # Task definitions: "What's in my kitchen?", "Diagnose my plant", "Fix-it mode"
├── scripts/
│   └── vision_relay.py    # Example relay service (camera frame → AI → structured guide)
└── prompt_log.md          # The complete CLAD prompt log used during development
```

## The Guide Week Fit

The theme asks for *"a spatial experience that guides people to learn, complete, or improve a real-world task."* TaskVision answers it at the system level rather than the content level: instead of shipping one hardcoded guide, it **generates a guide from whatever the world shows it**. The three flagship modes demonstrate this:

1. **What's in my kitchen?** — glance at your counter, and the glasses identify your ingredients and generate a recipe guide on the spot.
2. **Diagnose my plant** — point at a wilting leaf, get the problem and a recovery guide anchored to the plant.
3. **Fix-it mode** — point at the broken thing (bike chain, router with a red light), get the correct fix as spatial steps.

## CLAD Prompt Log

The full development prompt log — the actual prompts used with CLAD to scaffold, build, iterate, and test this project — lives in `prompt_log.md`. It documents the closed loop in action: prompt → build → test → fix → refine.

## Author

**Michael Ikwuka (@mikeymontaz)** — Snapchat, TikTok, Instagram, Discord

*Built with CLAD in Lens Studio. No Spectacles hardware required to develop.*
