import sys
import time
from datetime import datetime

class Logger:
    @staticmethod
    def _timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def info(cls, message: str):
        print(f"[{cls._timestamp()}] [INFO] {message}", flush=True)

    @classmethod
    def warn(cls, message: str):
        print(f"[{cls._timestamp()}] [WARN] {message}", file=sys.stderr, flush=True)

    @classmethod
    def error(cls, message: str):
        print(f"[{cls._timestamp()}] [ERROR] {message}", file=sys.stderr, flush=True)

    @classmethod
    def success(cls, message: str):
        print(f"[{cls._timestamp()}] [SUCCESS] {message}", flush=True)

    @classmethod
    def debug(cls, message: str):
        print(f"[{cls._timestamp()}] [DEBUG] {message}", flush=True)
