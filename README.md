# Dual-AI Bridge (`dualai`)

An autonomous, zero-overhead inter-process communication bridge linking **Google DeepMind's Gemini (Antigravity)** with **OpenAI's Flagship Model (ChatGPT)**.

---

## Architectural Overview

```
 ┌────────────────────────┐
 │  Antigravity (Gemini)  │  <-- Reasoning & Primary Code Execution
 └───────────┬────────────┘
             │  /gpt (File-based IPC or CLI)
             ▼
 ┌────────────────────────┐
 │   DualAI Core Engine   │  <-- Thread Manager, DOM Observer, Persistent Context
 └───────────┬────────────┘
             │  CDP / Playwright Session
             ▼
 ┌────────────────────────┐
 │      ChatGPT Web       │  <-- Strategic Architecture, Deep Research & DALL-E 3
 └────────────────────────┘
```

---

## Quickstart

### 1. Installation & Environment Setup
Run the setup command to configure an isolated Python virtual environment and download browser dependencies:

```bash
# Windows
dualai.bat setup

# Linux / macOS
chmod +x dualai.sh
./dualai.sh setup
```

### 2. Authentication (One-Time)
Launch an interactive session to authenticate your account. Profile cookies and session state are persisted securely in `browser_profile/`:

```bash
# Windows
dualai.bat auth

# Linux / macOS
./dualai.sh auth
```

### 3. Running the Synchronization Daemon
Start the background file-watching daemon:

```bash
# Windows
dualai.bat daemon

# Linux / macOS
./dualai.sh daemon
```

---

## CLI Reference

```
usage: dualai [-h] {setup,auth,daemon,query,doctor} ...

Dual-AI Bridge Infrastructure CLI

commands:
  setup       Install dependencies and Playwright browser binaries
  auth        Launch interactive browser session for one-time authentication
  daemon      Run background synchronization daemon
  query       Execute single-shot prompt directly from the terminal
  doctor      Inspect system health and configuration
```

---

## Antigravity Slash Skill Integration

To enable the `/gpt` slash command inside Antigravity:
1. Copy `skills/gpt/SKILL.md` to `~/.gemini/config/skills/gpt/SKILL.md`.
2. Any request prefixed with `/gpt` will automatically leverage the bridge.
