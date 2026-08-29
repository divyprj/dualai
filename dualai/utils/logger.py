import sys
import time
from datetime import datetime

class Logger:
    """Colorized console logger for Dual-AI Bridge operations."""
    @staticmethod
    def _timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def info(cls, message: str):
        print(f"[{cls._timestamp()}] [INFO] {message}", flush=True)

    @classmethod
    def success(cls, message: str):
        print(f"[{cls._timestamp()}] [SUCCESS] 🟢 {message}", flush=True)

    @classmethod
    def warn(cls, message: str):
        print(f"[{cls._timestamp()}] [WARN] ⚠️ {message}", file=sys.stderr, flush=True)

    @classmethod
    def error(cls, message: str):
        print(f"[{cls._timestamp()}] [ERROR] ❌ {message}", file=sys.stderr, flush=True)

    @classmethod
    def deep(cls, message: str):
        print(f"[{cls._timestamp()}] [DEEP THINKING] 🔮 {message}", flush=True)
