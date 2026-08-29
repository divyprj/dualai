import os
import time
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime

from dualai.config import BridgeConfig
from dualai.browser import ChatGPTBrowser
from dualai.utils.logger import Logger

class DualAIClient:
    """Client for dispatching queries to ChatGPT and saving full-fidelity reports."""

    def __init__(self, config: Optional[BridgeConfig] = None):
        self.config = config or BridgeConfig.load()
        self.base_dir = Path(__file__).resolve().parent.parent
        self.bridge_dir = self.base_dir / self.config.bridge_directory
        self.history_dir = self.base_dir / self.config.history_directory
        self.bridge_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.browser = ChatGPTBrowser(self.config)

    def query(self, prompt: str, deep_mode: bool = False, timeout: Optional[int] = None) -> Tuple[bool, str]:
        """Queries ChatGPT and saves 100% complete, uncompressed verbatim output to report.md."""
        # 1. Write prompt to bridge/prompt.md for auditability
        prompt_file = self.bridge_dir / "prompt.md"
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt)

        # 2. Execute via browser engine
        start_t = time.time()
        success, response = self.browser.query(prompt, deep_mode=deep_mode, timeout=timeout)
        elapsed = time.time() - start_t

        if success:
            # 3. Save verbatim response to bridge/report.md
            report_file = self.bridge_dir / "report.md"
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(response)

            # 4. Save to history for persistent memory
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode_tag = "deep" if deep_mode else "std"
            hist_file = self.history_dir / f"{timestamp_str}_{mode_tag}.md"
            with open(hist_file, "w", encoding="utf-8") as f:
                f.write(f"# Query Timestamp: {datetime.now().isoformat()}\n# Mode: {mode_tag.upper()}\n\n## Prompt:\n{prompt}\n\n## Response:\n{response}\n")

            Logger.success(f"Report saved to {report_file} ({len(response)} chars, {elapsed:.1f}s)")
            return True, response
        else:
            Logger.error(f"Query failed: {response}")
            return False, response
