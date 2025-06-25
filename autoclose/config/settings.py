import json
from pathlib import Path
from autoclose.loggers.log_cli import setup_logger
import json
from pathlib import Path
from platformdirs import user_config_dir

#------------ logger ------------
logger = setup_logger(__name__)

# Set up application configuration directory
APP_NAME = "OpsGenieAutoClose"
CONFIG_DIR = Path(user_config_dir(APP_NAME, appauthor=False))  # appauthor=False prevents duplicate folder
SETTINGS_FILE = CONFIG_DIR / "settings.json"

def ensure_settings_file():
    try:
        # First check if directory exists
        logger.debug("Checking if directory exists: %s", CONFIG_DIR)
        if not CONFIG_DIR.exists():
            logger.info("Directory not found, creating: %s", CONFIG_DIR)
            try:
                CONFIG_DIR.mkdir(parents=True, exist_ok=True)
                logger.info("Successfully created directory: %s", CONFIG_DIR)
            except Exception as e:
                logger.error("Failed to create directory: %s", str(e))
                raise
        else:
            logger.info("Directory already exists: %s", CONFIG_DIR)

        # Now check if settings file exists
        logger.debug("Checking if settings file exists: %s", SETTINGS_FILE)
        if not SETTINGS_FILE.exists():
            logger.info("Settings file not found, creating new one at: %s", SETTINGS_FILE)
            default_settings = {
                "OPSGENIE_API_KEY": "",
                "OPSGENIE_URL_BASE": "",
                "OPSGENIE_API_INTEGRATION_KEY": "",
                "ELASTICSEARCH_URL": "",
                "ELASTICSEARCH_HOST": "",
                "ELASTICSEARCH_PORT": "",
                "ELASTICSEARCH_USERNAME": "",
                "ELASTICSEARCH_PASSWORD": "",
                "ELASTICSEARCH_VERIFY_CERTS": "",
                "ELASTICSEARCH_SSL_SHOW_WARN": "",
                "LOG_LEVEL": "",
                "DRY_RUN": "",
                "SCHEDULER_MINUTES": ""
            }
            try:
                with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(default_settings, f, indent=2)
                logger.info("Successfully created settings file at: %s", SETTINGS_FILE)
                logger.debug("Settings file Resolve if any: %s", SETTINGS_FILE.resolve())
            except Exception as e:
                logger.error("Failed to create settings file: %s", str(e))
                raise
        else:
            logger.info("Settings file already exists at: %s", SETTINGS_FILE)
            logger.debug("Settings file Resolve if any: %s", SETTINGS_FILE.resolve())
            # Verify we can read the file
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    json.load(f)
                logger.info("Successfully verified settings file is readable")
            except Exception as e:
                logger.error("Settings file exists but is not readable: %s", str(e))
                raise

        return SETTINGS_FILE
    except Exception as e:
        logger.error("Failed to create settings file in user config directory: %s", str(e))
        # Fallback to local directory if config directory is not accessible
        local_settings = Path(__file__).parent.parent / "config" / "settings.json"
        logger.info("Attempting to use local settings file at: %s", local_settings)
        
        # Create webui directory if it doesn't exist
        if not local_settings.parent.exists():
            logger.info("Creating webui directory: %s", local_settings.parent)
            local_settings.parent.mkdir(parents=True, exist_ok=True)
        
        if not local_settings.exists():
            logger.info("Creating local settings file at %s", local_settings)
            default_settings = {
                "OPSGENIE_API_KEY": "",
                "OPSGENIE_URL_BASE": "",
                "OPSGENIE_API_INTEGRATION_KEY": "",
                "ELASTICSEARCH_URL": "",
                "ELASTICSEARCH_HOST": "",
                "ELASTICSEARCH_PORT": "",
                "ELASTICSEARCH_USERNAME": "",
                "ELASTICSEARCH_PASSWORD": "",
                "ELASTICSEARCH_VERIFY_CERTS": "",
                "ELASTICSEARCH_SSL_SHOW_WARN": "",
                "LOG_LEVEL": "",
                "DRY_RUN": "",
                "SCHEDULER_MINUTES": ""
            }
            with open(local_settings, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, indent=2)
            logger.info("Created local settings file at %s", local_settings)
        else:
            logger.info("Found existing local settings file at %s", local_settings)
            
        return local_settings

SETTINGS_FILE = ensure_settings_file()

logger.debug("SETTINGS_FILE exists: %s", SETTINGS_FILE.exists())

def load_settings():
    try:
        logger.info("Loading settings from %s...", SETTINGS_FILE)
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        logger.error("Failed to load settings: %s", SETTINGS_FILE)
        return {}
    except Exception as e:
        logger.error("Error loading settings: %s", str(e))
        return {}

settings = load_settings()
logger.debug("Settings loaded successfully")

OPSGENIE_API_KEY = settings.get("OPSGENIE_API_KEY", "")
masked_token = f"{OPSGENIE_API_KEY[:1]}****{OPSGENIE_API_KEY[-1:]}" if OPSGENIE_API_KEY else "(not set)"
logger.debug("OPSGENIE_API_KEY: %s", masked_token)

OPSGENIE_URL_BASE = settings.get("OPSGENIE_URL_BASE", "")
logger.debug("OPSGENIE_URL_BASE: %s", OPSGENIE_URL_BASE)

OPSGENIE_API_INTEGRATION_KEY = settings.get("OPSGENIE_API_INTEGRATION_KEY", "")
masked_token = f"{OPSGENIE_API_INTEGRATION_KEY[:1]}****{OPSGENIE_API_INTEGRATION_KEY[-1:]}" if OPSGENIE_API_INTEGRATION_KEY else "(not set)"
logger.debug("OPSGENIE_API_INTEGRATION_KEY: %s", masked_token)

ELASTICSEARCH_URL = settings.get("ELASTICSEARCH_URL", "")
logger.debug("ELASTICSEARCH_URL: %s", ELASTICSEARCH_URL)

ELASTICSEARCH_HOST = settings.get("ELASTICSEARCH_HOST", "")
logger.debug("ELASTICSEARCH_HOST: %s", ELASTICSEARCH_HOST)

ELASTICSEARCH_PORT = settings.get("ELASTICSEARCH_PORT", "")
logger.debug("ELASTICSEARCH_PORT: %s", ELASTICSEARCH_PORT)

ELASTICSEARCH_USERNAME = settings.get("ELASTICSEARCH_USERNAME", "")
logger.debug("ELASTICSEARCH_USERNAME: %s", ELASTICSEARCH_USERNAME)

ELASTICSEARCH_PASSWORD = settings.get("ELASTICSEARCH_PASSWORD", "")
masked_token = f"{ELASTICSEARCH_PASSWORD[:1]}****{ELASTICSEARCH_PASSWORD[-1:]}" if ELASTICSEARCH_PASSWORD else "(not set)"
logger.debug("ELASTICSEARCH_PASSWORD: %s", masked_token)

ELASTICSEARCH_VERIFY_CERTS = settings.get("ELASTICSEARCH_VERIFY_CERTS", "")
logger.debug("ELASTICSEARCH_VERIFY_CERTS: %s", ELASTICSEARCH_VERIFY_CERTS)

ELASTICSEARCH_SSL_SHOW_WARN = settings.get("ELASTICSEARCH_SSL_SHOW_WARN", "")
logger.debug("ELASTICSEARCH_SSL_SHOW_WARN: %s", ELASTICSEARCH_SSL_SHOW_WARN)

LOG_LEVEL = settings.get("LOG_LEVEL", "")
logger.debug("LOG_LEVEL: %s", ELASTICSEARCH_SSL_SHOW_WARN)

DRY_RUN = settings.get("DRY_RUN", "")
logger.debug("DRY_RUN: %s", ELASTICSEARCH_SSL_SHOW_WARN)

SCHEDULER_MINUTES = settings.get("SCHEDULER_MINUTES", "")
logger.debug("SCHEDULER_MINUTES: %s", SCHEDULER_MINUTES)


def validate_settings():
    logger.info("Validating started")
    # Load settings fresh
    current_settings = load_settings()
    
    # Check required fields
    required_fields = {
        "OPSGENIE_API_KEY": current_settings.get("OPSGENIE_API_KEY", ""),
        "OPSGENIE_URL_BASE": current_settings.get("OPSGENIE_URL_BASE", ""),
        "OPSGENIE_API_INTEGRATION_KEY": current_settings.get("OPSGENIE_API_INTEGRATION_KEY", ""),
        #"ELASTICSEARCH_URL": current_settings.get("ELASTICSEARCH_URL", ""),
        "ELASTICSEARCH_HOST": current_settings.get("ELASTICSEARCH_HOST", ""),
        "ELASTICSEARCH_PORT": current_settings.get("ELASTICSEARCH_PORT", ""),
        "ELASTICSEARCH_USERNAME": current_settings.get("ELASTICSEARCH_USERNAME", ""),
        "ELASTICSEARCH_PASSWORD": current_settings.get("ELASTICSEARCH_PASSWORD", ""),
        "ELASTICSEARCH_VERIFY_CERTS": current_settings.get("ELASTICSEARCH_VERIFY_CERTS", ""),
        #"ELASTICSEARCH_SSL_SHOW_WARN": current_settings.get("ELASTICSEARCH_SSL_SHOW_WARN", ""),
        #"DRY_RUN": current_settings.get("DRY_RUN", ""),
        # "SCHEDULAR_MINUTES": current_settings.get("SCHEDULAR_MINUTES", ""),
        "LOG_LEVEL": current_settings.get("LOG_LEVEL", "")
    }
    
    # # Log the values we're checking
    # for field, value in required_fields.items():
    #     if field in {"ELASTICSEARCH_PASSWORD", "OPSGENIE_API_INTEGRATION_KEY", "OPSGENIE_API_KEY"} and value:
    #         masked_value = f"{value[:1]}****{value[-1:]}"
    #     else:
    #         masked_value = value
    #     logger.info("Checking %s: %s", field, masked_value)
    
    if not all(required_fields.values()):
        missing = [field for field, value in required_fields.items() if not value]
        logger.error("Missing required settings: %s", ", ".join(missing))
        raise EnvironmentError(f"Missing required settings: {', '.join(missing)}")
    
    logger.info("Settings validated successfully")

def save_settings_to_file(data):
    data = dict(data)
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    logger.info("Settings saved to %s", SETTINGS_FILE)