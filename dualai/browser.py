import os
import sys
import time
from pathlib import Path
from typing import Optional, Tuple
from playwright.sync_api import sync_playwright

from dualai.config import BridgeConfig
from dualai.utils.logger import Logger
from dualai.utils.text_cleaner import TextCleaner

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def get_brave_path() -> Optional[str]:
    """Auto-detects Brave Browser installation on Windows."""
    candidates = [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe")
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

class ChatGPTBrowser:
    """Manages persistent browser automation for ChatGPT with zero truncation."""
    def __init__(self, config: Optional[BridgeConfig] = None):
        self.config = config or BridgeConfig.load()
        self.base_dir = Path(__file__).resolve().parent.parent
        self.profile_dir = self.base_dir / self.config.browser_profile_dir
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self.brave_exe = get_brave_path()

    def _dismiss_popups(self, page):
        """Dismiss common onboarding modals, banners, and upgrade prompts."""
        popups = ["Stay logged in", "Dismiss", "Next", "Done", "Okay", "Let's go", "Got it", "Continue", "Accept", "Close"]
        for p in popups:
            try:
                btn = page.locator(f"button:has-text('{p}'), div[role='button']:has-text('{p}')").first
                if btn.is_visible():
                    btn.click()
                    time.sleep(0.3)
            except Exception:
                pass

    def query(self, prompt_text: str, deep_mode: bool = False, timeout: Optional[int] = None) -> Tuple[bool, str]:
        """Submits prompt to ChatGPT and extracts 100% complete, uncompressed, verbatim response."""
        if deep_mode:
            prompt_text = (
                "[SYSTEM DIRECTIVE: DEEP THINKING & MAXIMUM REASONING MODE ENGAGED]\n"
                "Execute an exhaustive, step-by-step chain of analysis. Formally evaluate edge cases, "
                "architectural trade-offs, failure modes, and implementation blueprints before delivering the final solution.\n\n"
                f"{prompt_text}"
            )
            max_wait = timeout or self.config.deep_thinking_timeout
            Logger.deep(f"Submitting query in Deep Thinking Mode (Timeout: {max_wait}s)...")
        else:
            max_wait = timeout or self.config.standard_timeout
            Logger.info(f"Submitting query to ChatGPT (Timeout: {max_wait}s)...")

        browser_label = "Brave Browser" if self.brave_exe else "Chromium"
        Logger.info(f"Launching {browser_label} engine...")

        with sync_playwright() as p:
            launch_args = {
                "user_data_dir": str(self.profile_dir),
                "headless": self.config.headless_browser,
                "args": [
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized"
                ],
                "permissions": ["clipboard-read", "clipboard-write"],
                "viewport": None
            }
            if self.brave_exe:
                launch_args["executable_path"] = self.brave_exe
            else:
                launch_args["channel"] = "chrome"

            try:
                context = p.chromium.launch_persistent_context(**launch_args)
            except Exception:
                launch_args.pop("executable_path", None)
                launch_args.pop("channel", None)
                context = p.chromium.launch_persistent_context(**launch_args)

            page = context.pages[0] if context.pages else context.new_page()

            # Target URL
            target_url = self.config.chatgpt_url or "https://chatgpt.com/"
            Logger.info(f"Navigating to conversation thread: {target_url}")
            try:
                page.goto(target_url, timeout=60000)
            except Exception as e:
                Logger.warn(f"Page load warning (continuing): {e}")

            time.sleep(3)
            self._dismiss_popups(page)

            # Locate prompt input
            textarea = page.locator("#prompt-textarea, div[contenteditable='true']").first
            try:
                textarea.wait_for(state="attached", timeout=15000)
            except Exception:
                self._dismiss_popups(page)
                textarea.wait_for(state="attached", timeout=15000)

            textarea.click(force=True)
            time.sleep(0.5)

            # Inject prompt
            Logger.info("Injecting prompt into ChatGPT input...")
            try:
                textarea.fill(prompt_text)
            except Exception:
                page.keyboard.insert_text(prompt_text)

            time.sleep(1)

            # Trigger Send
            send_btn = page.locator("button[data-testid='send-button'], button[aria-label*='Send']").first
            if send_btn.is_visible() and send_btn.is_enabled():
                send_btn.click()
            else:
                page.keyboard.press("Enter")

            Logger.info("Prompt dispatched! Awaiting synthesis...")

            # Wait for generation to start
            time.sleep(3)
            stop_btn_selector = "button[data-testid='stop-button'], button[aria-label*='Stop']"

            for _ in range(15):
                if page.locator(stop_btn_selector).is_visible():
                    Logger.info("ChatGPT is actively generating response...")
                    break
                time.sleep(1)

            # Wait until generation finishes (Stop button disappears)
            start_wait = time.time()
            while time.time() - start_wait < max_wait:
                if not page.locator(stop_btn_selector).is_visible():
                    time.sleep(2)
                    if not page.locator(stop_btn_selector).is_visible():
                        break
                time.sleep(1.5)

            elapsed = time.time() - start_wait
            Logger.success(f"Generation completed in {elapsed:.1f}s! Extracting verbatim report...")
            time.sleep(2)

            # Extract 100% complete verbatim response
            result_text = None

            # Strategy 1: Native Copy Button (guarantees pure, complete markdown)
            try:
                copy_btns = page.locator("button[aria-label*='Copy'], button[data-testid*='copy']").all()
                if copy_btns:
                    copy_btns[-1].click(force=True)
                    time.sleep(0.8)
                    clipboard_text = page.evaluate("navigator.clipboard.readText()")
                    if clipboard_text and len(clipboard_text.strip()) > 20:
                        result_text = clipboard_text.strip()
                        Logger.info("Extracted complete markdown via native clipboard copy.")
            except Exception as e:
                Logger.warn(f"Clipboard extraction fallback: {e}")

            # Strategy 2: DOM message extraction fallback
            if not result_text:
                try:
                    msgs = page.locator("div[data-message-author-role='assistant']").all()
                    if msgs:
                        result_text = msgs[-1].inner_text().strip()
                        Logger.info("Extracted response via assistant DOM element.")
                except Exception as e:
                    Logger.error(f"DOM extraction error: {e}")

            context.close()

            if result_text:
                cleaned = TextCleaner.clean_chatgpt_response(result_text)
                return True, cleaned
            else:
                return False, "Failed to extract response text from ChatGPT page."
