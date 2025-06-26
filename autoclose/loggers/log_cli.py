#loggers/log_cli.py
import logging
from pathlib import Path
from autoclose.config.logfile import create_log_file
import sys
from autoclose.loggers.config_loader import get_setting

LOG_LEVEL = get_setting("LOG_LEVEL", "INFO")
DRY_RUN = get_setting("DRY_RUN", "False")

# APP_NAME = "OpsGenieAutoClose"
# CONFIG_DIR = Path(user_config_dir(APP_NAME, appauthor=False))  # appauthor=False prevents duplicate folder
# SETTINGS_FILE = CONFIG_DIR / "settings.json"

# def load_settings():
#     try:
#         if SETTINGS_FILE.exists():
#             with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
#                 return json.load(f)
#         return {}
#     except Exception:
#         return {}


# LOG_LEVEL = load_settings().get("LOG_LEVEL")
# DRY_RUN = load_settings().get("DRY_RUN")

print(f"--------------LOG_LEVEL: {LOG_LEVEL}, DRY_RUN: {DRY_RUN}---------------------")

def setup_logger(name=__name__, logfile=None):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        # Console handler with UTF-8 encoding
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.getLevelName(LOG_LEVEL.upper()))

        # Use the log file from logfile.py if no specific logfile is provided
        if logfile is None:
            logfile = create_log_file()
        
        # Ensure the log directory exists
        log_path = Path(logfile)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # File handler with UTF-8 encoding
        file_handler = logging.FileHandler(logfile, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
