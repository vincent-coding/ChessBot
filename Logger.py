from datetime import datetime

class logger:
    def info(text: str) -> None:
        print(f"\033[96m[{datetime.now().strftime('%H:%M:%S')}] INFO: {text}\033[00m")

    def error(text: str) -> None:
        print(f"\033[91m[{datetime.now().strftime('%H:%M:%S')}] ERROR: {text}\033[00m")

    def warning(text: str) -> None:
        print(f"\033[93m[{datetime.now().strftime('%H:%M:%S')}] WARNING: {text}\033[00m")