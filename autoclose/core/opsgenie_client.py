from autoclose.config.settings import OPSGENIE_API_INTEGRATION_KEY
from autoclose.loggers.log_cli import setup_logger
import opsgenie_sdk
from opsgenie_sdk.rest import ApiException

logger = setup_logger(__name__)

class OpsGenieClient:
    def __init__(self, opsgenie_api_key=OPSGENIE_API_INTEGRATION_KEY):
        self.conf = opsgenie_sdk.configuration.Configuration()
        self.conf.api_key['Authorization'] = opsgenie_api_key

        self.api_client = opsgenie_sdk.api_client.ApiClient(configuration=self.conf)
        self.alert_api = opsgenie_sdk.AlertApi(api_client=self.api_client)
        logger.info("Successfully connected to OpsGenie")   

    def close_alert(self, alert_id, note):
        body = opsgenie_sdk.CloseAlertPayload(
            user='AutoCloser',
            note=note,
            source='python sdk'
        )
        try:
            close_response = self.alert_api.close_alert(identifier=alert_id, close_alert_payload=body)
            logger.info(f"Closed alert {alert_id}")
            return close_response
        except ApiException as err:
            logger.error(f"Exception when calling AlertApi->close_alert: {err}")

    def list_alerts(self):
        query = 'status=open'
        try:
            list_response = self.alert_api.list_alerts(limit=100, offset=0, sort='updatedAt', order='asc', search_identifier_type='name', query=query)
            # logger.info(list_response)
            return list_response
        except ApiException as err:
            logger.error(f"Exception when calling AlertApi->list_alerts: {err}")
   
    def count_alerts(self):
        try:
            count_response = self.alert_api.count_alerts()
            logger.info(count_response)
            return count_response
        except ApiException as err:
            logger.error(f"Exception when calling AlertApi->count__alerts: {err}")

    def get_alert(self, alert_id):
        try:
            get_response = self.alert_api.get_alert(identifier=alert_id, identifier_type='id')
            # logger.info(get_response)
            return get_response
        except ApiException as err:
            logger.error(f"Exception when calling AlertApi->get_alert: {err}")