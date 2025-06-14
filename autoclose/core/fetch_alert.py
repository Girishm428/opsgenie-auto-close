import requests
from autoclose.config.settings import OPSGENIE_API_KEY, OPSGENIE_URL_BASE
from autoclose.loggers.log_cli import setup_logger

logger = setup_logger()

def fetch_alert_details(alert_id):
    headers = {
        'Authorization': f'GenieKey {OPSGENIE_API_KEY}',
        'Content-Type': 'application/json'
    }
    url = f'https://{OPSGENIE_URL_BASE}/v2/alerts/{alert_id}'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.error(f"❌ Failed to fetch alert details for ID {alert_id}: {response.status_code}")
        return None

    return response.json().get('data')


