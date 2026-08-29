# 🧠 Dual-AI Bridge (Gemini Antigravity x ChatGPT)

A persistent, bi-directional, sovereign AI coordination bridge between **Google Antigravity** and **ChatGPT**.

Designed for deep architectural reasoning, zero-truncation markdown extraction, and autonomous pair-programming.

---

## ✨ Features

- **100% Verbatim Fidelity**: Guaranteed zero truncation, zero compression, and full markdown preservation.
- **Deep Thinking Mode (`/gptdeep`)**: Extended 300s timeout with automatic reasoning directive injection.
- **Standard Fast Consultation (`/gpt`)**: Fast interactive reasoning queries.
- **Single-Thread Continuity**: Preserves conversation memory across queries inside the same persistent ChatGPT URL.
- **Isolated & Lightweight**: No heavy models, weights, or external runtime requirements—pure Playwright automation.
- **One-Click Control**: Interactive `run.bat` master dashboard.

---

## 🚀 Quick Start

### 1. Setup & Installation
Run the 1-click setup script:
```powershell
setup.bat
```

### 2. Interactive Dashboard
Launch the control dashboard:
```powershell
run.bat
```

### 3. Python API Usage
```python
from dualai.client import DualAIClient

client = DualAIClient()

# Standard Query
success, response = client.query("Explain distributed consensus in 3 paragraphs")

# Deep Thinking Mode Query
success, deep_response = client.query("Design an atomic transactional lock engine", deep_mode=True)
print(deep_response)
```

---

## 📁 Repository Structure

```text
c:\Dev\dual-ai\
├── .agents\skills\
│   ├── gpt\SKILL.md          # /gpt skill definition
│   └── gptdeep\SKILL.md      # /gptdeep skill definition
├── bridge\
│   ├── prompt.md             # Input query buffer
│   └── report.md             # Output verbatim report buffer
├── browser_profile\          # Persistent browser session
├── dualai\
│   ├── browser.py            # Playwright driver
│   ├── client.py             # High-level query API
│   ├── config.py             # Settings loader
│   ├── watcher.py            # Background file watcher
│   └── utils\                # Logger and text cleaner
├── tests\                    # Integrity test suite
├── ARCHITECTURE.md           # Deep system design
├── BRIDGE_PROTOCOL.md        # File IPC protocol
├── RULES.md                  # Non-negotiable operating rules
├── config.json               # System configuration
└── run.bat                   # Interactive dashboard
```

---

## 💖 Sponsor & Support

If this project helps streamline your AI development workflows, you can support ongoing maintenance:

<details>
<summary><b>💖 Sponsor via UPI / Google Pay (Click to expand)</b></summary>
<br>

| Field | Details |
| :--- | :--- |
| **Recipient** | Divyansh Prajapati |
| **UPI ID** | `surajdivyansh104-1@oksbi` |
| **Supported Apps** | Google Pay, PhonePe, Paytm, BHIM, Navi, Any UPI App |

<br>

<p align="center">
  <img src="docs/donate_qr.png" alt="UPI QR Code" width="180" />
</p>

</details>

---

## 📜 License
Created by **Divyansh Prajapati (~DIV)**. Licensed under the [MIT License](LICENSE).
