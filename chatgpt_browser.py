import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

# Configure UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def get_brave_path():
    brave_paths = [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe")
    ]
    for path in brave_paths:
        if os.path.exists(path):
            return path
    return None

def load_config():
    config = {
        "automation_mode": "browser",
        "headless_browser": False,
        "browser_profile_dir": "browser_profile",
        "bridge_directory": "bridge",
        "history_directory": "history"
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"Warning: Could not read config.json: {e}", flush=True)
    return config

def dismiss_popups(page):
    """Dismiss common onboarding popups, dialogs, and banners."""
    popup_texts = ["Stay logged in", "Dismiss", "Next", "Done", "Okay", "Let's go", "Got it", "Continue", "Accept", "Close"]
    for text in popup_texts:
        try:
            btn = page.locator(f"button:has-text('{text}'), div[role='button']:has-text('{text}')").first
            if btn.is_visible():
                btn.click()
                time.sleep(0.5)
        except Exception:
            pass

def run_chatgpt_query(prompt_content: str) -> str:
    """
    Automates ChatGPT Web using Playwright persistent browser context with Brave/Chromium.
    """
    config = load_config()
    profile_dir = os.path.join(BASE_DIR, config.get("browser_profile_dir", "browser_profile"))
    headless = config.get("headless_browser", False)
    brave_exe = get_brave_path()

    os.makedirs(profile_dir, exist_ok=True)

    browser_label = "Brave Browser" if brave_exe else "Chromium"
    print(f"\n🌐 [ChatGPT Automation] Launching {browser_label} engine...", flush=True)

    with sync_playwright() as p:
        launch_kwargs = {
            "user_data_dir": profile_dir,
            "headless": headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            "permissions": ["clipboard-read", "clipboard-write"],
            "viewport": None
        }

        if brave_exe:
            launch_kwargs["executable_path"] = brave_exe
        else:
            launch_kwargs["channel"] = "chrome"

        try:
            browser_context = p.chromium.launch_persistent_context(**launch_kwargs)
        except Exception:
            launch_kwargs.pop("executable_path", None)
            launch_kwargs.pop("channel", None)
            browser_context = p.chromium.launch_persistent_context(**launch_kwargs)

        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()

        target_url = config.get("active_thread_url", "https://chatgpt.com/")
        print(f"🔍 Navigating to persistent thread: {target_url} ...", flush=True)
        page.goto(target_url, timeout=60000)
        time.sleep(3)

        # Dismiss any post-login onboarding modals
        dismiss_popups(page)

        # Find prompt input
        print("📝 Locating ChatGPT prompt input...", flush=True)
        textarea = page.locator("#prompt-textarea, div[contenteditable='true']").first
        try:
            textarea.wait_for(state="attached", timeout=15000)
        except Exception:
            dismiss_popups(page)
            textarea.wait_for(state="attached", timeout=15000)

        # Check for attachments
        attachments_file = os.path.join(BASE_DIR, config.get("bridge_directory", "bridge"), "attachments.json")
        attachment_files = []
        if os.path.exists(attachments_file):
            try:
                with open(attachments_file, "r", encoding="utf-8") as af:
                    attachment_files = json.load(af)
            except Exception as e:
                print(f"⚠️ Error reading attachments.json: {e}", flush=True)

        single_attachment = os.path.join(BASE_DIR, config.get("bridge_directory", "bridge"), "attachment.png")
        if not attachment_files and os.path.exists(single_attachment):
            attachment_files = [single_attachment]

        if attachment_files:
            valid_files = [f for f in attachment_files if os.path.exists(f)]
            if valid_files:
                print(f"📎 Attaching {len(valid_files)} reference file(s) to ChatGPT: {valid_files}", flush=True)
                try:
                    file_input = page.locator("input[type='file']").first
                    file_input.set_input_files(valid_files)
                    print("⏳ Waiting for file upload to render thumbnail...", flush=True)
                    # Wait for attachment upload processing
                    print("⏳ Waiting for file upload to finish processing in ChatGPT...", flush=True)
                    time.sleep(3)
                    # Immediately delete attachment definitions so subsequent prompts are never polluted
                    if os.path.exists(attachments_file):
                        try:
                            os.remove(attachments_file)
                        except Exception:
                            pass
                    if os.path.exists(single_attachment):
                        try:
                            os.remove(single_attachment)
                        except Exception:
                            pass
                except Exception as e:
                    print(f"⚠️ File upload warning: {e}", flush=True)

        textarea.click(force=True)
        time.sleep(0.5)

        print("⚡ Injecting prompt from Antigravity...", flush=True)
        try:
            textarea.fill(prompt_content)
        except Exception:
            page.keyboard.insert_text(prompt_content)
            
        time.sleep(1)

        # Count assistant turns before sending to detect NEW response
        initial_assistant_turns = page.locator("[data-message-author-role='assistant']").count()

        # Trigger send
        send_btn_selector = "button[data-testid='send-button'], button[aria-label*='Send']"
        send_btn = page.locator(send_btn_selector).first

        # Wait up to 20 seconds for send button to be enabled (in case file is still uploading)
        for _ in range(20):
            if send_btn.is_visible() and send_btn.is_enabled():
                break
            time.sleep(1)
        
        if send_btn.is_visible() and send_btn.is_enabled():
            send_btn.click(force=True)
        else:
            page.keyboard.press("Enter")
            
        print("🚀 Prompt sent to ChatGPT! Waiting for generation to begin...", flush=True)

        # Wait for generation to start
        stop_btn_selector = "button[data-testid='stop-button'], button[aria-label*='Stop']"
        generation_started = False
        
        for _ in range(30):
            has_stop = page.locator(stop_btn_selector).is_visible()
            turns_now = page.locator("[data-message-author-role='assistant']").count()
            if has_stop or turns_now > initial_assistant_turns:
                generation_started = True
                print("⏳ ChatGPT is generating response...", flush=True)
                break
            time.sleep(1)

        # Wait until generation finishes
        if generation_started:
            start_wait = time.time()
            while time.time() - start_wait < 360:
                if not page.locator(stop_btn_selector).is_visible():
                    time.sleep(3)
                    if not page.locator(stop_btn_selector).is_visible():
                        break
                time.sleep(1.5)
        else:
            print("⚠️ Notice: Generation start not explicitly detected via stop button, waiting 15s...", flush=True)
            time.sleep(15)

        print("✨ Generation completed! Extracting strategic report...", flush=True)
        time.sleep(2)

        result_text = None

        # Strategy 1: Direct DOM extraction (Fastest & Most Reliable)
        try:
            extract_script = """() => {
                const turns = document.querySelectorAll('[data-message-author-role="assistant"]');
                if (turns.length > 0) {
                    const last = turns[turns.length - 1];
                    const md = last.querySelector('.markdown') || last;
                    const text = (md.innerText || md.textContent || "").trim();
                    if (text) return text;
                }
                const articles = document.querySelectorAll('article');
                if (articles.length > 0) {
                    const lastArt = articles[articles.length - 1];
                    const text = (lastArt.innerText || lastArt.textContent || "").trim();
                    if (text) return text;
                }
                return null;
            }"""
            result_text = page.evaluate(extract_script)
        except Exception as e:
            print(f"⚠️ DOM extraction fallback: {e}", flush=True)

        # Strategy 2: Click native copy button as secondary option
        if not result_text or not result_text.strip():
            try:
                copy_btns = page.locator("button[aria-label*='Copy'], button[data-testid*='copy']").all()
                if copy_btns:
                    copy_btns[-1].click(force=True, timeout=2500)
                    time.sleep(0.8)
                    result_text = page.evaluate("() => navigator.clipboard.readText()")
            except Exception as e:
                print(f"⚠️ Copy button fallback: {e}", flush=True)

        # Strategy 3: Check for Generated Image (DALL-E / GPT Images)
        try:
            images = page.locator("[data-message-author-role='assistant'] img, article img, img[alt*='Generated image']").all()
            if images:
                for img in reversed(images):
                    src = img.get_attribute("src")
                    alt = img.get_attribute("alt") or ""
                    if src and ("estuary/content" in src or "oaiusercontent.com" in src or "blob:" in src or "dalle" in src.lower()):
                        # Skip if it is the uploaded input reference image
                        if "don-black-front" in alt.lower() or "reference" in alt.lower():
                            continue
                        print(f"🖼️ Found raw generated image in ChatGPT response. Downloading exact full resolution binary...", flush=True)
                        img_data = page.evaluate("""async (imgElem) => {
                            const res = await fetch(imgElem.src);
                            const blob = await res.blob();
                            return new Promise((resolve) => {
                                const reader = new FileReader();
                                reader.onloadend = () => resolve(reader.result);
                                reader.readAsDataURL(blob);
                            });
                        }""", img.element_handle())
                        if img_data and "base64," in img_data:
                            import base64
                            b64_str = img_data.split("base64,")[1]
                            raw_bytes = base64.b64decode(b64_str)
                            bridge_img_path = os.path.join(BASE_DIR, config.get("bridge_directory", "bridge"), "generated_image.png")
                            with open(bridge_img_path, "wb") as bf:
                                bf.write(raw_bytes)
                            print(f"✅ Saved exact untouched raw image binary to {bridge_img_path} ({len(raw_bytes)} bytes)!", flush=True)
                            break
        except Exception as e:
            print(f"⚠️ Image extraction notice: {e}", flush=True)

        browser_context.close()

        if not result_text or not result_text.strip():
            bridge_img_path = os.path.join(BASE_DIR, config.get("bridge_directory", "bridge"), "generated_image.png")
            if os.path.exists(bridge_img_path):
                result_text = f"✅ Image generated and saved successfully to {bridge_img_path}!"
            else:
                raise RuntimeError("Could not extract assistant message from ChatGPT web interface.")

        return result_text.strip()

def process_prompt_file():
    config = load_config()
    bridge_dir = os.path.join(BASE_DIR, config.get("bridge_directory", "bridge"))
    prompt_file = os.path.join(bridge_dir, "prompt.md")
    report_file = os.path.join(bridge_dir, "report.md")

    if not os.path.exists(prompt_file):
        print(f"❌ prompt.md not found at {prompt_file}", flush=True)
        return

    with open(prompt_file, "r", encoding="utf-8-sig", errors="replace") as f:
        prompt_content = f.read()

    if not prompt_content.strip():
        print("⚠️ prompt.md is empty.", flush=True)
        return

    report = run_chatgpt_query(prompt_content)
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ Successfully wrote strategic report to {report_file}!", flush=True)

if __name__ == "__main__":
    process_prompt_file()
