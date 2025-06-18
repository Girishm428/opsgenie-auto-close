from autoclose.core.opsgenie_client import OpsGenieClient
from autoclose.loggers.log_cli import setup_logger

logger = setup_logger(__name__)

opsgenie_client = OpsGenieClient()
def get_alert_ids():
    try:
        response = opsgenie_client.list_alerts()
        alerts = response.data  # This is a list of BaseAlert objects
        alert_ids = []
        for alert in alerts:
            alert_id = alert.id
            logger.info(f"Alert ID: {alert_id}")
            alert_ids.append(alert_id)
        return alert_ids
    except Exception as e:
        logger.error(f"Error getting alert IDs: {e}")

def get_alert_dict(alert_ids):
    alert_details_list = []
    try:
        for alert_id in alert_ids:
            response = opsgenie_client.get_alert(alert_id)
            alert_details = response.data
            alert_details_dict = alert_details.to_dict()

            logger.info(f"Details for Alert ID {alert_id}:")
            for key, value in alert_details_dict.items():
                logger.info(f"  {key}: {value}")

            alert_details_list.append(alert_details_dict)

        return alert_details_list
    except Exception as e:
        logger.error(f"Error getting alert details: {e}")
        return []

def get_alert_dict_details(alert_ids):
    all_details = []
    try:
        for alert_id in alert_ids:
            response = opsgenie_client.get_alert(alert_id)
            alert_data = response.data.to_dict()

            details = alert_data.get("details", {})
            logger.info(f"Details for Alert ID {alert_id}: {details}")

            all_details .append(details)
    
        return all_details
    except Exception as e:
        logger.error(f"Error fetching alert details: {e}")
        return []

def get_network_name(alert_ids):
    network_name = []
    try:
        for alert_id in alert_ids:
            response = opsgenie_client.get_alert(alert_id)
            alert_data = response.data.to_dict()
            details = alert_data.get("details", {})
            network_name.append(details.get("networkName"))
        return network_name
    except Exception as e:
        logger.error(f"Error fetching network name: {e}")
        return []

def get_host_name(alert_ids):
    host_name = []
    try:
        for alert_id in alert_ids:
            response = opsgenie_client.get_alert(alert_id)
            alert_data = response.data.to_dict()
            details = alert_data.get("details", {})
            host_name.append(details.get("host.name"))
        return host_name
    except Exception as e:
        logger.error(f"Error fetching host name: {e}")
        return []

def get_alert_ids_with_tag(tag_name):
    client = OpsGenieClient()
    try:
        response = client.alert_api.list_alerts(query=f'tags:"{tag_name}" AND status:open', limit=100)
        alert_ids = [alert.id for alert in response.data]
        logger.info(f"Found {len(alert_ids)} alerts with tag '{tag_name}'")
        return alert_ids
    except Exception as e:
        logger.error(f"Error fetching alerts with tag '{tag_name}': {e}")
        return []