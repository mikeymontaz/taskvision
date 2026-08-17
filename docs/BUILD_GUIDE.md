# TaskVision — Build Guide (Step-by-Step)

This guide takes you from a fresh machine to a working TaskVision Lens, using CLAD for the heavy lifting. Designed for the phone-only builder running a cloud Windows PC via RDP.

## Step 1 — Set Up the Build Machine

On the cloud Windows PC (or any Windows 11 machine):

1. Download and install **Lens Studio 5.22+** from https://ar.snap.com/download
2. Open Lens Studio → Home → select **SPECS** → **Base Template** → File → Save As → `TaskVision`
3. Install **Claude Code** (or Codex/Cursor) and sign in
4. Follow the CLAD setup guide to connect the AI tool to the Lens Studio MCP server: https://developers.specs.com/docs/clad/setup/setup-ai/claude-code-setup
5. In Project Settings, enable **Allow Experimental API** (needed for camera + internet together)

On your phone: install an RDP/remote desktop client (e.g., Microsoft Remote Desktop, RustDesk, or the cloud provider's own app) and connect to the cloud PC.

## Step 2 — Run the CLAD Prompt Sequence

Open Claude Code connected to the Lens Studio project and run the prompts from `prompt_log.md` in order, starting with Prompt 1 (scaffold) through Prompt 9 (content + polish). Copy-paste them verbatim — each builds on the last.

## Step 3 — Build the Vision Relay

The relay is a small Python service that receives the captured frame and returns a TaskGuide JSON. A starter implementation is in `scripts/vision_relay.py`:

```
python scripts/vision_relay.py
```

It expects an environment variable `AI_SERVICE_URL` (or an OpenAI-compatible key) and exposes `POST /analyze` taking `{ "mode": "...", "frame_base64": "..." }`. Swap in any vision-capable model (GPT-4o, Gemini, Claude with vision). Host it on any always-on host with a public HTTPS URL — the relay is what makes the Lens smart.

## Step 4 — Configure the Endpoint

In the Lens project settings JSON, set `relayEndpoint` to your relay's HTTPS URL. Test the full loop in the SPECS simulator: mode select → capture (mocked frame in simulator) → response → step rendering → timer → completion.

## Step 5 — The Closed Loop Pass

Run Prompt 10 (test loop). Let CLAD iterate until zero console errors. This pass is the most important artifact for judging — it is the literal "Loop" in Closed Loop Agentic Development.

## Step 6 — Record the Demo Video

Follow `DEMO_SCRIPT.md` for the shot list. Record the simulator screen (screen capture software works fine on the cloud PC — the recording happens on the machine, not your phone). Upload to Google Drive or WeTransfer with public link sharing.

## Step 7 — Push & Submit

```
git add . && git commit -m "TaskVision complete" && git push
```

Fill the submission form at https://lenslist.co/clad-summer-hackathon with:

| Field | Value |
|---|---|
| Project name | TaskVision |
| Repo link | https://github.com/mikeymontaz/taskvision |
| Video link | your Drive/WeTransfer link |
| Prompt log link | https://github.com/mikeymontaz/taskvision/blob/main/prompt_log.md |
| Description | the pitch below |

## Project Description (paste into form)

> TaskVision is a vision-in-the-loop spatial experience for SPECS that turns "what do I do with this?" into a guided, hands-free workflow. Point your glasses at something real — ingredients on your counter, a wilting plant, a broken bike chain — tap to capture, and TaskVision's AI pipeline identifies the object and generates a step-by-step spatial guide rendered as world-locked cards in your field of view. Steps advance with palm-tap gestures, each step can carry a countdown timer and checklist, and progress persists through Snap Cloud so a paused task resumes exactly where you left off. It was built end-to-end with CLAD in Lens Studio: the prompt log documents the full closed loop, from scaffold through the vision relay integration to the final test-and-fix pass that landed on zero simulator errors. Built by Michael Ikwuka (@mikeymontaz) for the CLAD Summer Hackathon, Week 2: Guide.

**Deadline: Sunday, Aug 23, 2026, night (PT). Submit before then. Good luck.**
