# Dual-AI Permanent Operating Contract

## 👑 THE CORE OPERATING RULES

> **1. Output Delivery Protocol**:
> Whenever `/gpt` or `/gptdeep` is invoked:
> 1. You get the **100% completely raw, exact, word-for-word, uncompressed output** from ChatGPT directly from `bridge/report.md`. Zero summaries, zero truncation, zero filtering.
> 2. **Immediately following the verbatim response**, Antigravity provides a **concise 3–7 line brief** summarizing key takeaways, actionable decisions, and next steps.

---

### 🛡️ Core Operating Directives:

1. **Single-Thread Continuity (No Arbitrary New Chats)**:
   * Maintain conversation inside the **exact same persistent thread** for the project (`Instagram Automation Framework...` under folder `gemini-gpt-bridge`).
   * **URL**: `https://chatgpt.com/c/6a9345aa-9174-83e9-a64e-4a5b5db0c999`
   * **NEVER open new chats** unless explicitly commanded by the user or when formally switching to a brand new project.

2. **Zero-Pollution Attachment Lifecycle**:
   * **NEVER attach images to architectural or text prompts**.
   * Only attach files when the user or task explicitly requests image editing or analysis based on that specific file.
   * `bridge/attachments.json` and attached images are **auto-deleted immediately** upon file upload so no stale files linger to pollute future prompts.

3. **100% Raw Image Extraction (Zero Cropping / Zero Alteration)**:
   * When ChatGPT generates an image, the bridge downloads the **exact raw binary directly from OpenAI's CDN** (e.g. 1.89 MB untouched PNG).
   * **NEVER crop, resize, downsample, or slice** the generated images with Pillow or CSS screen grabs.

4. **Strict AI Role Division**:
   * **ChatGPT**: Sole authority for deep research, strategic reasoning, art prompts, and DALL-E image generation.
   * **Antigravity (Gemini)**: Responsible for local code execution, file management, builds, device automation, and testing.
   * **Obedience**: When ChatGPT prescribes architecture or design specs, Antigravity follows them completely.

5. **Clean Session Architecture (No Mobile Private API)**:
   * Do not use private mobile reverse-engineered APIs (`instagrapi`) that trigger checkpoints.
   * Use official Web session browser contexts with automated keep-alive sentinels.
