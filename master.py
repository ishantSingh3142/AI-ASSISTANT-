import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQ_FILE = ROOT / "requirements.txt"
APP_FILE = ROOT / "jarvis2.py"


def ensure_requirements():
    if not REQ_FILE.exists():
        print("requirements.txt not found in project directory.")
        return

    try:
        import speech_recognition  # noqa: F401
        import pyttsx3  # noqa: F401
        import requests  # noqa: F401
        import wikipedia  # noqa: F401
        import screen_brightness_control  # noqa: F401
        print("Dependencies already available.")
    except ModuleNotFoundError:
        print("Installing project dependencies...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQ_FILE)],
            cwd=str(ROOT),
        )


def main():
    ensure_requirements()

    if not APP_FILE.exists():
        print(f"Could not find the app file: {APP_FILE}")
        input("Press Enter to exit...")
        return 1

    print("Starting JARVIS AI Assistant...")
    return subprocess.call([sys.executable, str(APP_FILE)], cwd=str(ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
