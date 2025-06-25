from autoclose.handlers.alert_details import get_host_name, get_alert_ids_with_tag
from autoclose.core.elastic_monitor import current_cpu_usage_for_hosts
from autoclose.loggers.log_cli import setup_logger
from autoclose.core.opsgenie_client import OpsGenieClient
from autoclose.config.rules import CPU_CLOUSER_NOTE, CPU_TAG_NAME
from autoclose.config.settings import DRY_RUN

logger = setup_logger(__name__)

def close_alerts_if_cpu_normal(threshold):
    try:
        # Step 1: Fetch alert IDs
        alert_ids = get_alert_ids_with_tag(CPU_TAG_NAME)
        if not alert_ids:
            logger.warning("No alert IDs found.")
            return

        # Step 2: Get hostnames for each alert
        hostnames = get_host_name(alert_ids)
        logger.info(f"Hostnames: {hostnames}")
        # Step 3: Get CPU usage for all hostnames
        cpu_usages = current_cpu_usage_for_hosts(hostnames)
        logger.info(f"CPU usages: {cpu_usages}")
        # Step 4: Close alerts if CPU is below threshold
        for alert_id, hostname, cpu in zip(alert_ids, hostnames, cpu_usages):
            if hostname is None or cpu is None:
                logger.warning(f"Skipping alert {alert_id} due to missing hostname or CPU usage.")
                continue

            if cpu < threshold:
                if DRY_RUN:
                    logger.info(f"[DRY RUN] Would close alert {alert_id} (CPU={cpu} < {threshold}) for host {hostname}")
                else:
                    logger.info(f"CPU for host {hostname} is {cpu}, below threshold. Closing alert {alert_id}.")
                    opsgenie_client = OpsGenieClient()
                    opsgenie_client.close_alert(alert_id, CPU_CLOUSER_NOTE)
            else:
                logger.info(f"CPU for host {hostname} is {cpu}, not closing alert {alert_id}.")
    except Exception as e:
        logger.error(f"Error in close_alerts_if_cpu_normal: {e}")