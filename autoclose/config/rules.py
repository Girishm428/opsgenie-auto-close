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
RULES_FILE = CONFIG_DIR / "rules.json"

def ensure_rules_file():
    try:
        # First check if directory exists
        logger.info("Checking if directory exists: %s", CONFIG_DIR)
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
        logger.info("Checking if rules file exists: %s", RULES_FILE)
        if not RULES_FILE.exists():
            logger.info("Rules file not found, creating new one at: %s", RULES_FILE)
            default_settings = {
                "CPU_THRESHOLD_TO_CLOSE": "",
                "CPU_TAG_NAME": "",
                "CPU_CLOUSER_NOTE": "",
            }
            try:
                with open(RULES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(default_settings, f, indent=2)
                logger.info("Successfully created rules file at: %s", RULES_FILE)
                logger.info("Rules file Resolve if any: %s", RULES_FILE.resolve())
            except Exception as e:
                logger.error("Failed to create rules file: %s", str(e))
                raise
        else:
            logger.info("Rules file already exists at: %s", RULES_FILE)
            logger.info("Rules file Resolve if any: %s", RULES_FILE.resolve())
            # Verify we can read the file
            try:
                with open(RULES_FILE, 'r', encoding='utf-8') as f:
                    json.load(f)
                logger.info("Successfully verified rules file is readable")
            except Exception as e:
                logger.error("Rules file exists but is not readable: %s", str(e))
                raise

        return RULES_FILE
    except Exception as e:
        logger.error("Failed to create rules file in user config directory: %s", str(e))
        # Fallback to local directory if config directory is not accessible
        local_rules = Path(__file__).parent.parent / "config" / "rules.json"
        logger.info("Attempting to use local rules file at: %s", local_rules)
        
        # Create webui directory if it doesn't exist
        if not local_rules.parent.exists():
            logger.info("Creating webui directory: %s", local_rules.parent)
            local_rules.parent.mkdir(parents=True, exist_ok=True)
        
        if not local_rules.exists():
            logger.info("Creating local rules file at %s", local_rules)
            default_settings = {
                "CPU_THRESHOLD_TO_CLOSE": "",
                "CPU_TAG_NAME": "",
                "CPU_CLOUSER_NOTE": "",
            }
            with open(local_rules, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, indent=2)
            logger.info("Created local rules file at %s", local_rules)
        else:
            logger.info("Found existing local rules file at %s", local_rules)
            
        return local_rules

RULES_FILE = ensure_rules_file()

logger.info("RULES_FILE exists: %s", RULES_FILE.exists())

def load_rules():
    try:
        logger.info("Loading rules from %s...", RULES_FILE)
        if RULES_FILE.exists():
            with open(RULES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        logger.error("Failed to load rules: %s", RULES_FILE)
        return {}
    except Exception as e:
        logger.error("Error loading rules: %s", str(e))
        return {}

rules = load_rules()
logger.info("Rules loaded successfully")

CPU_THRESHOLD_TO_CLOSE = rules.get("CPU_THRESHOLD_TO_CLOSE", "")
logger.info("CPU_THRESHOLD_TO_CLOSE: %s", CPU_THRESHOLD_TO_CLOSE)

CPU_TAG_NAME = rules.get("CPU_TAG_NAME", "")
logger.info("CPU_TAG_NAME: %s", CPU_TAG_NAME)

CPU_CLOUSER_NOTE = rules.get("CPU_CLOUSER_NOTE", "") 
logger.info("CPU_CLOUSER_NOTE: %s", CPU_CLOUSER_NOTE)


def validate():
    logger.info("Validating started")
    # Load settings fresh
    current_rules = load_rules()
    
    # Check required fields
    required_fields = {
        "CPU_THRESHOLD_TO_CLOSE": current_rules.get("CPU_THRESHOLD_TO_CLOSE", ""),
        "CPU_TAG_NAME": current_rules.get("CPU_TAG_NAME", ""),
        "CPU_CLOUSER_NOTE": current_rules.get("CPU_CLOUSER_NOTE", ""),
    }
    
    # Log the values we're checking
    for field, value in required_fields.items():
        logger.info("Checking %s: %s", field, value)
    
    if not all(required_fields.values()):
        missing = [field for field, value in required_fields.items() if not value]
        logger.error("Missing required rules: %s", ", ".join(missing))
        raise EnvironmentError(f"Missing required rules: {', '.join(missing)}")
    
    logger.info("Rules validated successfully")

def save_rules_to_file(data):
    data = dict(data)
    with open(RULES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    logger.info("Rules saved to %s", RULES_FILE)