---
name: gpt
description: >-
  Triggered when the user invokes '/gpt' or requests ChatGPT coordination.
  Strictly routes research, reasoning, architecture, visual design prompts, and
  image generation to ChatGPT via the persistent Dual-AI Bridge, obeying ChatGPT's
  directives completely.
---

# /gpt — ChatGPT Coordination & Obedience Skill

When the user invokes `/gpt` or asks for ChatGPT consultation/generation, the agent must strictly execute through the **Dual-AI Bridge**.

## 🎯 Core Operating Principles
1. **ChatGPT as Authority**: Delegate deep research, strategic reasoning, and DALL-E image prompts to ChatGPT.
2. **Absolute Obedience**: If ChatGPT specifies code or architecture, implement its directions faithfully.
3. **Persistent Thread Lock**: Automatically routes prompts to the same project conversation thread.
4. **Folder Separation**: Bridge files live in this bridge folder; application code lives in the project folder.
