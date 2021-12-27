from datetime import datetime

class logger:
    def info(text: str) -> None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] INFO: {text}")

    def error(text: str) -> None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: {text}")

    def warning(text: str) -> None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] WARNING: {text}")