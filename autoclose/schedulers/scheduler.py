import schedule
import time
from autoclose.main import main  # Replace with your actual module
from autoclose.loggers.log_cli import setup_logger

logger = setup_logger()

def job():
    logger.info("⏱ Running Opsgenie alert checker...")
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Error: {e}")

# Schedule the job every 5 minutes
schedule.every(5).minutes.do(job)

logger.info("✅ Scheduler started. Running every 5 minutes...")
job()  # Run immediately at startup

while True:
    schedule.run_pending()
    time.sleep(1)
