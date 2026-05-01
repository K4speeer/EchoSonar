from pathlib import Path
import os

CONFIG_DIR = Path.home() / ".config" / "echosonar"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
SESSION_FILE = str(CONFIG_DIR / "monitor")


def ensure_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)