import requests
from autoclose.config.settings import OPSGENIE_API_KEY

# CONFIG
API_KEY = OPSGENIE_API_KEY
BASE = 'https://api.opsgenie.com/v2'
HEADERS = {
    'Authorization': f'GenieKey {API_KEY}',
    'Content-Type': 'application/json'
}

def fetch_open_alerts():
    url = f'{BASE}/alerts'
    params = {'query': 'status:open', 'limit': 50}
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json().get('data', [])

def fetch_alert_detail(alert_id):
    url = f'{BASE}/alerts/{alert_id}'
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json().get('data', {})

def main():
    alerts = fetch_open_alerts()
    print(f"✅ Found {len(alerts)} open alerts.")
    for a in alerts:
        alert_id = a.get('id')
        detail = fetch_alert_detail(alert_id)
        print(f"🔹 ID: {alert_id}")
        print(f"📝 Message: {detail.get('message')}")
        print(f"📘 Description: {detail.get('description') or '— (none)'}")
        print(f"🧾 Details: {detail.get('details') or {}}")
        details = detail.get('details')
        print(details.get('networkName'))
        print("-" * 50)

if __name__ == '__main__':
    main()
