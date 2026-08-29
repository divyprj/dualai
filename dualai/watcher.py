import os
import sys
import time
from pathlib import Path

from dualai.config import BridgeConfig
from dualai.client import DualAIClient
from dualai.utils.logger import Logger

def run_watcher():
    """Watches bridge/prompt.md and automatically processes queries."""
    base_dir = Path(__file__).resolve().parent.parent
    config = BridgeConfig.load(str(base_dir / "config.json"))
    client = DualAIClient(config)

    prompt_path = base_dir / config.bridge_directory / "prompt.md"
    report_path = base_dir / config.bridge_directory / "report.md"

    Logger.info(f"🚀 Dual-AI Bridge Watcher Active.")
    Logger.info(f"📁 Watching: {prompt_path}")
    Logger.info(f"📄 Output  : {report_path}")
    Logger.info("Ready for prompts from Antigravity...")

    last_processed_hash = None

    while True:
        try:
            if prompt_path.exists() and prompt_path.stat().st_size > 0:
                with open(prompt_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                current_hash = hash(content)
                if content and current_hash != last_processed_hash:
                    # Check if deep mode is requested
                    deep_mode = "[SYSTEM DIRECTIVE: DEEP THINKING" in content or "deep:" in content[:30].lower()
                    Logger.info(f"⚡ New query detected ({len(content)} chars). Processing...")
                    
                    success, resp = client.query(content, deep_mode=deep_mode)
                    last_processed_hash = current_hash
                    Logger.info("Awaiting next prompt...")

            time.sleep(config.poll_interval_seconds)
        except KeyboardInterrupt:
            Logger.info("Watcher stopped by user.")
            break
        except Exception as e:
            Logger.error(f"Watcher error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    run_watcher()
