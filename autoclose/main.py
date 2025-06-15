from autoclose.core.fetch_open import fetch_open_alerts
from autoclose.core.fetch_alert import fetch_alert_details
from autoclose.loggers.log_cli import setup_logger
from autoclose.core.elastic_monitor import is_cpu_normal
from autoclose.core.close_alert import CloseAlert

logger = setup_logger()

def main():
    alerts = fetch_open_alerts()
    logger.info(f"Found {len(alerts)} open alert(s).\n")

    for alert in alerts:
        alert_id = alert.get('id')
        logger.info(f"Fetching details for alert ID: {alert_id}")

        detail = fetch_alert_details(alert_id)
        if detail:
            logger.info("Alert Detail:")
            logger.info(f"Message: {detail.get('message')}")
            logger.info(f"Priority: {detail.get('priority')}")
            logger.info(f"Status: {detail.get('status')}")
            logger.info(f"Tags: {', '.join(detail.get('tags', []))}")
            logger.info(f"Responders: {[r.get('name') for r in detail.get('responders', [])]}")
            logger.info(f"Details: {detail.get('details', {})}")
            dt=detail.get('details')
            logger.info(f"Network Name: {dt.get('networkName')}")
            logger.info("--------------------------------------------------\n")
    
    for alert in alerts:
        alert_id = alert.get("id")
        detail = fetch_alert_details(alert_id)
        details = detail.get("details", {})

        host = details.get("host.name")
        logger.info(f"Host: {host}")
        metric = details.get("system.load.norm.5")
        logger.info(f"Metric: {metric}")
        if metric != "cpu":
            continue

        logger.info(f"Checking alert {alert_id} on {host}...")

# Test auto close alert
host = "1.1.1.1"
alert_id = "asdfa-asdfasdf-asdfa-sdfasdf"
if is_cpu_normal(host):
    logger.info(f"CPU usage is normal on {host}")
    logger.info(f"Closing alert {alert_id} on {host}")
    client = CloseAlert()
    client.close_alert(alert_id)
    logger.info(f"Alert {alert_id} closed")
else:
    logger.info(f"CPU usage is not normal on {host}")


if __name__ == '__main__':
    main()
