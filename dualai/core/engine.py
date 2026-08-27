import os
import time
from typing import Tuple
from playwright.sync_api import sync_playwright, BrowserContext, Page
from dualai.core.config import BridgeConfig
from dualai.core.browser import discover_browser_executable
from dualai.utils.logger import Logger

class ChatGPTDriver:
    def __init__(self, config: BridgeConfig):
        self.config = config
        self.browser_exe = config.browser_path or discover_browser_executable()
        os.makedirs(self.config.profile_dir, exist_ok=True)

    def get_launch_args(self, headless: bool = False) -> dict:
        args = {
            "user_data_dir": self.config.profile_dir,
            "headless": headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-sandbox"
            ],
            "viewport": None
        }
        if self.browser_exe:
            args["executable_path"] = self.browser_exe
        return args

    def authenticate_interactive(self):
        Logger.info("Starting interactive authentication session...")
        Logger.info(f"Target URL: {self.config.chatgpt_url}")
        Logger.info(f"Profile: {self.config.profile_dir}")
        Logger.info("Please log in to your account. Close the browser window when finished.")

        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(**self.get_launch_args(headless=False))
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto(self.config.chatgpt_url, timeout=60000)

            while len(ctx.pages) > 0:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    break
            ctx.close()
        Logger.success("Authentication session saved to profile directory.")

    def submit_and_extract(self, prompt: str, target_url: Optional[str] = None) -> Tuple[bool, str]:
        url = target_url or self.config.chatgpt_url
        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(**self.get_launch_args(headless=self.config.headless))
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            
            if page.url != url and not page.url.startswith("https://chatgpt.com/c/"):
                page.goto(url, timeout=60000)
                time.sleep(3)

            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)

            textarea = page.locator("#prompt-textarea, div[contenteditable='true']").first
            try:
                textarea.wait_for(state="attached", timeout=10000)
                textarea.click(force=True)
                textarea.fill(prompt)
            except Exception:
                page.keyboard.insert_text(prompt)
            time.sleep(0.5)

            send_btn = page.locator("button[data-testid='send-button'], button[aria-label*='Send']").first
            if send_btn.is_visible() and send_btn.is_enabled():
                send_btn.click()
            else:
                page.keyboard.press("Enter")

            Logger.info("Prompt dispatched. Awaiting model completion...")

            stop_btn = page.locator("button[data-testid='stop-button'], button[aria-label*='Stop']")
            time.sleep(4)
            start_time = time.time()
            while time.time() - start_time < self.config.timeout_seconds:
                if not stop_btn.is_visible():
                    time.sleep(3)
                    if not stop_btn.is_visible():
                        break
                time.sleep(1.5)

            time.sleep(2)
            last_msg = page.locator("div[data-message-author-role='assistant']").last
            response = last_msg.inner_text()
            ctx.close()
            return True, response
