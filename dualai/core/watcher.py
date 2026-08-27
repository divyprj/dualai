import os
import time
import signal
import sys
from datetime import datetime
from dualai.core.config import BridgeConfig
from dualai.core.engine import ChatGPTDriver
from dualai.utils.logger import Logger

class BridgeDaemon:
    def __init__(self, config: BridgeConfig):
        self.config = config
        self.driver = ChatGPTDriver(config)
        self.running = True
        os.makedirs(self.config.history_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.config.prompt_file), exist_ok=True)

    def _signal_handler(self, signum, frame):
        Logger.info("Termination signal received. Shutting down daemon...")
        self.running = False

    def run(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        if sys.platform != "win32":
            signal.signal(signal.SIGTERM, self._signal_handler)

        Logger.info("Dual-AI Bridge Daemon active.")
        Logger.info(f"Watching input:  {self.config.prompt_file}")
        Logger.info(f"Writing output:  {self.config.report_file}")
        Logger.info(f"Poll interval:   {self.config.poll_interval}s")

        last_mtime = 0
        if os.path.exists(self.config.prompt_file):
            last_mtime = os.path.getmtime(self.config.prompt_file)

        while self.running:
            try:
                time.sleep(self.config.poll_interval)
                if not os.path.exists(self.config.prompt_file):
                    continue

                mtime = os.path.getmtime(self.config.prompt_file)
                if mtime > last_mtime:
                    last_mtime = mtime
                    with open(self.config.prompt_file, "r", encoding="utf-8") as f:
                        prompt_text = f.read().strip()

                    if not prompt_text or prompt_text.startswith("# Bridge Initialized") or prompt_text.startswith("# Dual-AI"):
                        continue

                    Logger.info(f"Processing updated task prompt ({len(prompt_text)} characters)...")
                    success, response = self.driver.submit_and_extract(prompt_text)
                    if success:
                        # Write atomically
                        tmp_report = self.config.report_file + ".tmp"
                        with open(tmp_report, "w", encoding="utf-8") as f:
                            f.write(f"# ChatGPT Technical Response\n\n**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n{response}\n")
                        if os.path.exists(self.config.report_file):
                            os.remove(self.config.report_file)
                        os.rename(tmp_report, self.config.report_file)

                        # Archive
                        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                        hist_path = os.path.join(self.config.history_dir, f"session_{ts}.md")
                        with open(hist_path, "w", encoding="utf-8") as f:
                            f.write(f"# Prompt\n\n{prompt_text}\n\n---\n\n# Response\n\n{response}\n")

                        Logger.success(f"Synchronized response ({len(response)} characters) to report.md")
            except Exception as e:
                Logger.error(f"Execution error: {e}")
                time.sleep(3)

        Logger.info("Daemon terminated cleanly.")
