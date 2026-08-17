# CLAD Prompt Log — TaskVision

This is a proposed, ordered CLAD workflow for TaskVision. The prompts are ready to run in the real Lens Studio environment. Until dated CLAD outputs, project files, screenshots, and test logs are added, this document is a plan rather than evidence of completed execution.

---

## Phase 1 — Project Scaffold

**Prompt 1 (scaffold):**
> Create a SPECS Lens Studio project called TaskVision using the SPECS Base Template. Set up a world-locked spatial UI layer using the Spectacles UI Kit: a translucent glass-style main panel floating ahead of the user, a compact title bar reading "TaskVision", and a radial mode selector with three modes: "Kitchen", "Plant", "Fix-it". Add a crosshair reticle at center view that highlights when an object could be identified.

**Expected result:** Establish the visual identity and three-mode structure. Record the actual CLAD response, generated files, and any setup errors after running this prompt.

## Phase 2 — Vision Pipeline

**Prompt 2 (camera capture):**
> Add a camera capture system using CameraModule. On a palm-tap gesture (Interaction Kit), capture a still image frame from the default color camera and store it. Show a brief "capturing..." indicator on the reticle while the capture completes.

**Verification note:** Camera behavior and simulator support must be confirmed in the target Lens Studio/Spectacles version. Do not claim device or mock testing until a real test log is captured.

**Prompt 3 (vision relay):**
> Add an InternetModule that POSTs the captured frame (base64) plus the selected mode to a vision relay endpoint (make the endpoint URL configurable in a settings JSON). Parse the JSON response into a TaskGuide object: { title, objectName, confidence, steps: [{ text, durationSeconds?, checklist: string[]? }] }. While waiting for the response, show a "Analyzing..." panel with a subtle pulse animation.

**Verification note:** Camera access, internet access, permissions, and public-Lens eligibility are environment-dependent. Confirm them against the official documentation and event rules before implementation. The relay in `scripts/vision_relay.py` is a starter example, not a verified production integration.

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

**Verification status:** Not yet executed. The repository currently contains no Lens Studio project export, CLAD transcript, simulator recording, console log, or dated second-pass evidence. After running this prompt, append the actual errors, fixes, screenshots, and final result here. Do not claim zero errors without that evidence.

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
