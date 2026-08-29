# 🏛️ DUAL-AI BRIDGE ARCHITECTURE

The Dual-AI Bridge establishes a bidirectional, persistent cognitive pipeline uniting:
1. **Google DeepMind Antigravity (Gemini)**: The local system engineer and compiler.
2. **OpenAI ChatGPT**: The remote reasoning and architectural strategist.

## Component Breakdown:
* **`dualai.browser`**: Playwright browser driver supporting headless and windowed modes with Brave Browser preference.
* **`dualai.client`**: High-level execution API with automatic deep-thinking prompt injection and timeout controls.
* **`dualai.watcher`**: Zero-configuration background daemon watching `bridge/prompt.md`.
* **`dualai.utils.text_cleaner`**: Sanitizer ensuring zero markdown loss and stripping ephemeral UI tokens.
* **`browser_profile/`**: Persistent Chromium user-data directory preserving authentication cookies indefinitely.
