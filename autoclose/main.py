# from autoclose.core.fetch_open import fetch_open_alerts
# from autoclose.core.fetch_alert import fetch_alert_details
from autoclose.loggers.log_cli import setup_logger
from autoclose.handlers.alert_details import (
    get_alert_ids,
    get_alert_dict_details,
    get_network_name,
    get_host_name
)

logger = setup_logger(__name__)

def main():
 
    alert_ids = get_alert_ids()
    network_name = get_network_name(alert_ids)
    print(network_name)
    host_name = get_host_name(alert_ids)
    print(host_name)
    # print(alert_ids)

if __name__ == '__main__':
    main()
