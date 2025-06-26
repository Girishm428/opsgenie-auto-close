# autoclose/config/config_loader.py
import json
from pathlib import Path
from platformdirs import user_config_dir

APP_NAME = "OpsGenieAutoClose"
CONFIG_DIR = Path(user_config_dir(APP_NAME, appauthor=False))
SETTINGS_FILE = CONFIG_DIR / "settings.json"

def load_settings():
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_setting(key, default=None):
    return load_settings().get(key, default)
