import schedule
import time
from autoclose.main import main  # Replace with your actual module
from autoclose.loggers.log_cli import setup_logger
from autoclose.config.settings import SCHEDULER_MINUTES

logger = setup_logger(__name__)

def job():
    logger.info("Running Opsgenie alert checker...")
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}")

# Schedule the job every 5 minutes
schedule.every(SCHEDULER_MINUTES).minutes.do(job)

logger.info("Scheduler started. Running every %s minutes...", SCHEDULER_MINUTES)
job()  # Run immediately at startup

while True:
    schedule.run_pending()
    time.sleep(1)
