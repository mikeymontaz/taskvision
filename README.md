# TaskVision

> **The Lens that sees your world and guides your hands.**

TaskVision is a proposed SPECS spatial experience for the **CLAD Summer Hackathon — "Guide"** ([official event page](https://lenslist.co/clad-summer-hackathon)). This repository is a build scaffold and implementation plan; actual CLAD and Lens Studio execution must be completed and documented before describing the Lens as finished.

Look at something real, tap, and the glasses figure out what it is — then generate a live, step-by-step spatial guide floating in your field of view to help you complete a real-world task with it. No phone, no search, no decisions. Your glasses see the problem and stream the solution.

## How It Works

The planned experience uses a vision-in-the-loop pipeline: the SPECS **CameraModule** may capture the current camera frame, an approved network path may send it to an AI service, structured JSON may return, and a spatial UI may render the guide. Camera, internet, permissions, public-Lens eligibility, Interaction Kit behavior, and persistence must be verified in the target Lens Studio/Spectacles environment before implementation claims are made.

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

The development prompt log in `prompt_log.md` is an ordered CLAD workflow template for scaffolding, building, iterating, and testing this project. It is not evidence that these prompts have already been executed; add dated CLAD outputs, screenshots, and test results after each real build session.

## Author

**Michael Ikwuka (@mikeymontaz)** — Snapchat, TikTok, Instagram, Discord

*Designed for CLAD in Lens Studio. Lens Studio execution, device/simulator testing, and final CLAD evidence remain pending.*
