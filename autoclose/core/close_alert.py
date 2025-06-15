from autoclose.config.settings import OPSGENIE_API_INTEGRATION_KEY
from autoclose.loggers.log_cli import setup_logger
import opsgenie_sdk
from opsgenie_sdk.rest import ApiException

logger = setup_logger("autoclose.opsgenie")

class CloseAlert:
    def __init__(self, opsgenie_api_key=OPSGENIE_API_INTEGRATION_KEY):
        self.conf = opsgenie_sdk.configuration.Configuration()
        self.conf.api_key['Authorization'] = opsgenie_api_key

        self.api_client = opsgenie_sdk.api_client.ApiClient(configuration=self.conf)
        self.alert_api = opsgenie_sdk.AlertApi(api_client=self.api_client)
        logger.info("Successfully connected to OpsGenie")   

    def close_alert(self, alert_id):
        body = opsgenie_sdk.CloseAlertPayload(
            user='AutoCloser',
            note='Auto-closed: CPU usage normalized.',
            source='python sdk'
        )
        try:
            close_response = self.alert_api.close_alert(identifier=alert_id, close_alert_payload=body)
            logger.info(f"Closed alert {alert_id}")
            print(close_response)
            return close_response
        except ApiException as err:
            logger.error(f"Exception when calling AlertApi->close_alert: {err}")
            print(f"Exception: {err}")


# Run test
# if __name__ == "__main__":
#     client = CloseAlert()
#     client.close_alert("9753b2b2-1c94-4fdd-ab42-a4c96fbfab97-1749993162941")
