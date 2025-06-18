import requests
from autoclose.config.settings import OPSGENIE_API_KEY, OPSGENIE_URL_BASE
from autoclose.loggers.log_cli import setup_logger

logger = setup_logger(__name__)

def fetch_open_alerts():
    headers = {
        'Authorization': f'GenieKey {OPSGENIE_API_KEY}',
        'Content-Type': 'application/json'
    }

    params = {
        'query': 'status:open',
#        'limit': 50  # adjust as needed
    }
    url = f'https://{OPSGENIE_URL_BASE}/v2/alerts'
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        alerts = data.get('data', [])
        logger.info(f"✅ Fetched {len(alerts)} open alert(s).")
        for alert in alerts:
            logger.info(f"- [{alert['priority']}] {alert['message']} (ID: {alert['id']})")
        return alerts
    else:
        logger.error(f"❌ Failed to fetch alerts: {response.status_code} - {response.text}")
        return []






