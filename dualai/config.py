import os
import json
from pathlib import Path
from dataclasses import dataclass

@dataclass
class BridgeConfig:
    project_name: str = "dual-ai"
    version: str = "2.0.0"
    chatgpt_url: str = "https://chatgpt.com/c/6a8ff4bb-926c-83ee-8515-22f7f6e40857"
    headless_browser: bool = False
    browser_profile_dir: str = "browser_profile"
    bridge_directory: str = "bridge"
    history_directory: str = "history"
    poll_interval_seconds: float = 1.5
    verbatim_output: bool = True
    deep_thinking_timeout: int = 300
    standard_timeout: int = 120

    @classmethod
    def load(cls, config_path: str = None) -> "BridgeConfig":
        if not config_path:
            base_dir = Path(__file__).resolve().parent.parent
            config_path = base_dir / "config.json"
        else:
            config_path = Path(config_path)

        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
            except Exception:
                pass
        return cls()
