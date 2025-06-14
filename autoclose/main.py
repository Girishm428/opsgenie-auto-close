from autoclose.core.fetch_open import fetch_open_alerts
from autoclose.core.fetch_alert import fetch_alert_details
from autoclose.loggers.log_cli import setup_logger

logger = setup_logger()

def main():
    alerts = fetch_open_alerts()
    logger.info(f"✅ Found {len(alerts)} open alert(s).\n")

    for alert in alerts:
        alert_id = alert.get('id')
        logger.info(f"🔍 Fetching details for alert ID: {alert_id}...")

        detail = fetch_alert_details(alert_id)
        if detail:
            logger.info("📄 Alert Detail:")
            logger.info(f"  📝 Message: {detail.get('message')}")
            logger.info(f"  🚨 Priority: {detail.get('priority')}")
            logger.info(f"  📌 Status: {detail.get('status')}")
            logger.info(f"  🏷 Tags: {', '.join(detail.get('tags', []))}")
            logger.info(f"  👥 Responders: {[r.get('name') for r in detail.get('responders', [])]}")
            logger.info(f"  📦 Details: {detail.get('details', {})}")
            dt=detail.get('details')
            logger.info(f"  🌐 Network Name: {dt.get('networkName')}")
            logger.info("--------------------------------------------------\n")




if __name__ == '__main__':
    main()
