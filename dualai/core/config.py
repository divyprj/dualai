import os
import json
from dataclasses import dataclass
from typing import Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@dataclass
class BridgeConfig:
    chatgpt_url: str = "https://chatgpt.com/"
    headless: bool = False
    poll_interval: float = 1.5
    timeout_seconds: int = 180
    browser_path: Optional[str] = None
    profile_dir: str = os.path.join(ROOT_DIR, "browser_profile")
    prompt_file: str = os.path.join(ROOT_DIR, "bridge", "prompt.md")
    report_file: str = os.path.join(ROOT_DIR, "bridge", "report.md")
    history_dir: str = os.path.join(ROOT_DIR, "history")

    @classmethod
    def load(cls) -> "BridgeConfig":
        cfg_path = os.path.join(ROOT_DIR, "config.json")
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(
                    chatgpt_url=data.get("chatgpt_url", "https://chatgpt.com/"),
                    headless=data.get("headless", False),
                    poll_interval=float(data.get("poll_interval_seconds", 1.5)),
                    timeout_seconds=int(data.get("timeout_seconds", 180)),
                    browser_path=data.get("browser_path")
                )
            except Exception:
                pass
        return cls()
