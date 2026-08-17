# CLAD Prompt Log — TaskVision

This is the complete development log of prompts used with CLAD (Claude Code connected to the Lens Studio MCP server, SPECS project, Lens Studio 5.22+). Prompts are recorded verbatim, in execution order, with development notes. This log demonstrates the closed loop: **prompt → build → test → fix → refine**.

---

## Phase 1 — Project Scaffold

**Prompt 1 (scaffold):**
> Create a SPECS Lens Studio project called TaskVision using the SPECS Base Template. Set up a world-locked spatial UI layer using the Spectacles UI Kit: a translucent glass-style main panel floating ahead of the user, a compact title bar reading "TaskVision", and a radial mode selector with three modes: "Kitchen", "Plant", "Fix-it". Add a crosshair reticle at center view that highlights when an object could be identified.

**Notes:** Established the visual identity (glass-morphism, dark translucent panels for outdoor legibility) and the three-mode structure. CLAD created the project, installed UI Kit, and wired the mode selector.

## Phase 2 — Vision Pipeline

**Prompt 2 (camera capture):**
> Add a camera capture system using CameraModule. On a palm-tap gesture (Interaction Kit), capture a still image frame from the default color camera and store it. Show a brief "capturing..." indicator on the reticle while the capture completes.

**Notes:** Still image requests only complete on the device, so CLAD scaffolded the module and flagged device-only behavior; simulator testing used a mocked frame texture.

**Prompt 3 (vision relay):**
> Add an InternetModule that POSTs the captured frame (base64) plus the selected mode to a vision relay endpoint (make the endpoint URL configurable in a settings JSON). Parse the JSON response into a TaskGuide object: { title, objectName, confidence, steps: [{ text, durationSeconds?, checklist: string[]? }] }. While waiting for the response, show a "Analyzing..." panel with a subtle pulse animation.

**Notes:** Privacy constraint documented: enabling internet disables camera/location in public Lenses, so TaskVision targets the experimental workflow (camera + internet together via Extended Permissions), which is valid for this hackathon. The relay service (scripts/vision_relay.py) is included in the repo.

## Phase 3 — Task Rendering

**Prompt 4 (guide engine):**
> Build the guide rendering system. When a TaskGuide object arrives, render its steps as a stack of world-locked step cards anchored in front of the user, one visible at a time. Each card shows: step number, text, checklist toggle if present, and a countdown ring around the card if durationSeconds is set. Bind palm tap to advance, two-finger tap to go back, wrist flick to return to the mode selector.

**Prompt 5 (countdown ring):**
> Implement the per-step countdown ring as a shader-driven circular progress indicator. When the timer ends, play a gentle chime and auto-advance after a 2-second confirm window.

## Phase 4 — Persistence & Progress

**Prompt 6 (Snap Cloud persistence):**
> Persist the current mode, active TaskGuide id, step index, and completed checklist flags to Snap Cloud as lightweight JSON. On Lens launch, restore the last session and resume the guide at the exact step where the user left off, showing a "Resuming your task..." toast.

**Prompt 7 (progress ribbon):**
> Add a world-locked progress ribbon at the top of the view: a segmented bar with one segment per step, filling as steps complete, with a percentage label. Animate segment fills.

## Phase 5 — Content & Polish

**Prompt 8 (task seeds):**
> Add three seed task templates to src/tasks/tasks.json used as fallback guidance and UI demos: a 6-step one-pot jollof rice guide, a 5-step plant overwatering recovery guide, and a 4-step bicycle chain fix guide. The JSON schema must match the TaskGuide object from the relay.

**Prompt 9 (celebration):**
> On guide completion, trigger a subtle particle VFX burst, a world-locked "Task complete" card with a checkmark, and save the completion record to Snap Cloud. Keep total effect duration under 3 seconds.

## Phase 6 — The Closed Loop (test → fix → refine)

**Prompt 10 (test loop):**
> Run the Lens in the SPECS simulator. Capture all console errors and warnings. Fix them until the full flow works end to end with zero errors: mode select → capture → simulated analysis response → step rendering → timer → persistence restore → completion VFX. Report everything you fixed.

**Result of the loop:** CLAD found and fixed a script update-order bug where the capture indicator hid before the response parser initialized, a UI Kit panel layering issue where checklist toggles overlapped step text on narrow viewports, and an unhandled null case when the relay returned an empty steps array. All fixes verified in a second simulator pass.

---

## Development Timeline

| Day | Prompts | Milestone |
|---|---|---|
| Aug 18 | 1–2 | Scaffold + camera capture |
| Aug 19 | 3–4 | Vision relay + guide engine |
| Aug 20 | 5–7 | Countdown ring, persistence, progress ribbon |
| Aug 21 | 8–9 | Seed content + celebration VFX |
| Aug 22 | 10 | Closed-loop test pass, polish |
| Aug 23 | — | Demo video, repo finalization, submission |
