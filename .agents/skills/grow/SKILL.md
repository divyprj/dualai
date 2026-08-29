---
name: grow
description: >-
  Triggered when the user invokes '/grow' or requests continuous multi-AI evolution.
  Executes an autonomous improvement cycle: Consults ChatGPT in Deep Thinking mode,
  feeds the blueprint to local Qwen 2.5 on RTX 3050 for edge critique, and Antigravity
  implements, tests, and deploys the code live without stopping.
---

# `/grow` — Autonomous Tri-AI Continuous Evolution Protocol

When the user types `/grow`:
The system must not stop or ask for trivial permissions. It must execute the continuous Tri-AI evolution loop:

1. **Step 1: Strategic Planning (ChatGPT Deep Thinking)**
   - Query ChatGPT via the persistent Playwright bridge with Deep Thinking directives active.
   - Formulate the next architectural enhancement.
   - Save the raw immutable output into `bridge/report.md`.

2. **Step 2: Edge Brain Review (Qwen 2.5 on RTX 3050)**
   - Query local Qwen on `http://localhost:11434/api/generate` with the ChatGPT specification.
   - Extract the local feasibility critique, hardware optimization, and exact component breakdown.

3. **Step 3: Hands-On Construction (Antigravity / Gemini)**
   - Build or refactor the Python / Batch code in `c:\Dev\aura-os`.
   - Run tests and syntax checks.
   - Hot-reload or restart the supervisor daemon.

4. **Step 4: Live Verification & Progress Report**
   - Verify live services (Ollama, Telegram, ADB, Bridge).
   - Report progress concisely to Divyansh and stand ready for the next evolution step.
