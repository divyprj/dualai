import argparse
import sys
import os
import subprocess
from dualai.core.config import BridgeConfig
from dualai.core.browser import discover_browser_executable
from dualai.core.engine import ChatGPTDriver
from dualai.core.watcher import BridgeDaemon
from dualai.utils.logger import Logger

def cmd_setup(args, cfg: BridgeConfig):
    Logger.info("Initializing environment and dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        req_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        Logger.success("Environment setup completed successfully.")
    except Exception as e:
        Logger.error(f"Setup failed: {e}")
        sys.exit(1)

def cmd_auth(args, cfg: BridgeConfig):
    driver = ChatGPTDriver(cfg)
    driver.authenticate_interactive()

def cmd_daemon(args, cfg: BridgeConfig):
    daemon = BridgeDaemon(cfg)
    daemon.run()

def cmd_query(args, cfg: BridgeConfig):
    prompt = " ".join(args.prompt) if args.prompt else ""
    if not prompt:
        Logger.error("Prompt argument required.")
        sys.exit(1)
    driver = ChatGPTDriver(cfg)
    Logger.info(f"Querying: {prompt}")
    success, response = driver.submit_and_extract(prompt)
    if success:
        print("\n" + "="*60 + "\n" + response + "\n" + "="*60)

def cmd_doctor(args, cfg: BridgeConfig):
    Logger.info("Running system diagnostics...")
    print(f"[*] Python:       {sys.version.split()[0]} ({sys.executable})")
    print(f"[*] Platform:     {sys.platform}")
    browser = discover_browser_executable()
    print(f"[*] Browser:      {browser or 'Bundled Chromium'}")
    print(f"[*] Profile Dir:  {cfg.profile_dir} ({'Ready' if os.path.exists(cfg.profile_dir) else 'Empty'})")
    for mod in ["playwright", "PIL", "requests"]:
        try:
            __import__(mod)
            print(f"[*] Module {mod:10s}: OK")
        except ImportError:
            print(f"[*] Module {mod:10s}: MISSING")
    Logger.success("Diagnostics completed.")

def main():
    parser = argparse.ArgumentParser(prog="dualai", description="Dual-AI Bridge Infrastructure CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("setup", help="Install dependencies and Playwright browser binaries")
    subparsers.add_parser("auth", help="Launch interactive browser session for one-time authentication")
    subparsers.add_parser("daemon", help="Run background synchronization daemon")
    
    query_p = subparsers.add_parser("query", help="Execute single-shot prompt directly")
    query_p.add_argument("prompt", nargs="+", help="Prompt text")

    subparsers.add_parser("doctor", help="Inspect system health and configuration")

    args = parser.parse_args()
    cfg = BridgeConfig.load()

    if args.command == "setup":
        cmd_setup(args, cfg)
    elif args.command == "auth":
        cmd_auth(args, cfg)
    elif args.command == "daemon":
        cmd_daemon(args, cfg)
    elif args.command == "query":
        cmd_query(args, cfg)
    elif args.command == "doctor":
        cmd_doctor(args, cfg)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
