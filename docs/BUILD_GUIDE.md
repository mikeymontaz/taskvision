# TaskVision — Build Guide (Step-by-Step)

This guide is a proposed workflow from a fresh machine to a TaskVision Lens, using CLAD for implementation assistance. It is designed for a phone-only builder using a Windows machine through RDP. It does not claim that the Lens is working until each test gate produces evidence.

## Step 1 — Set Up the Build Machine

On a compatible Windows machine, if you obtain one:

1. Download and install **Lens Studio 5.22+** from https://ar.snap.com/download
2. Open Lens Studio → Home → select **SPECS** → **Base Template** → File → Save As → `TaskVision`
3. Install **Claude Code** (or Codex/Cursor) and sign in
4. Follow the current official CLAD setup documentation for your exact Lens Studio version. The previously used `developers.specs.com` URL must be checked against the current official Snap developer documentation before use.
5. In Project Settings, enable **Allow Experimental API** (needed for camera + internet together)

On your phone: install an RDP/remote desktop client (e.g., Microsoft Remote Desktop, RustDesk, or the cloud provider's own app) and connect to the cloud PC.

## Step 2 — Run the CLAD Prompt Sequence

Open Claude Code connected to the Lens Studio project and run the prompts from `prompt_log.md` in order, starting with Prompt 1 (scaffold) through Prompt 9 (content + polish). Copy-paste them verbatim — each builds on the last.

## Step 3 — Build the Vision Relay

The relay is a small Python service that receives the captured frame and returns a TaskGuide JSON. A starter implementation is in `scripts/vision_relay.py`:

```
python scripts/vision_relay.py
```

The starter relay expects `AI_SERVICE_URL` and `AI_API_KEY`, and exposes `POST /analyze` with `{ "mode": "...", "frame_base64": "..." }`. This code has not been connected to a real Lens or a live model in this repository. Before using it, validate the provider’s current API format, configure authentication privately, add HTTPS, and test with a non-sensitive sample image.

## Step 4 — Configure the Endpoint

Only after the relay and Lens integration are implemented should you configure the endpoint. First test the relay independently with a seed response, then test the Lens UI with a mocked response if the target simulator supports it, and finally test camera/network behavior on the intended device or approved environment. Record each result.

## Step 5 — The Closed Loop Pass

Run Prompt 10 only after the preceding prompts have actually been executed. Capture the console output, screenshots, generated project files, and dated CLAD transcript. Only report zero errors if the evidence supports that result.

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
| Description | Use the verified description below only after the Lens is actually built and tested |

## Project Description (paste into form)

> TaskVision is a proposed vision-in-the-loop spatial experience for SPECS that aims to turn "what do I do with this?" into a guided, hands-free workflow. The current public repository contains the concept, implementation plan, seed task content, and a starter relay; Lens Studio execution, CLAD evidence, permissions, device/simulator testing, and final submission assets are still being completed. Built by Michael Ikwuka (@mikeymontaz).

**Deadline:** verify the current date and deadline directly on the official Lenslist submission page before submitting; earlier materials in this repository contain an unverified deadline and should not be relied upon.
