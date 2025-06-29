from autoclose.loggers.log_cli import setup_logger
from autoclose.handlers.handlers import close_alerts_if_cpu_normal
from autoclose.config.rules import CPU_THRESHOLD_TO_CLOSE
from autoclose.config.settings import validate_settings

logger = setup_logger(__name__)

def main():
    validate_settings()
    close_alerts_if_cpu_normal(CPU_THRESHOLD_TO_CLOSE)

if __name__ == '__main__':
    main()
