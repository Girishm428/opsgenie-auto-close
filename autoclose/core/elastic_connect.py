from elasticsearch import Elasticsearch, AuthenticationException, ConnectionError, TransportError
from autoclose.config.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD, ELASTICSEARCH_VERIFY_CERTS, ELASTICSEARCH_SSL_SHOW_WARN
from autoclose.loggers.log_cli import setup_logger

logger = setup_logger(__name__)

def elastic_connect():
    es = None
    try:
        es = Elasticsearch(
            hosts=[{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT, 'scheme': "https" }],
            basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
            verify_certs=ELASTICSEARCH_VERIFY_CERTS,
            ssl_show_warn=ELASTICSEARCH_SSL_SHOW_WARN
        )

        if es.ping():
            logger.info("Successfully connected to Elasticsearch")
        else:
            logger.error("Ping failed. Elasticsearch is reachable but didn't respond properly")
    except AuthenticationException as ae:
        logger.error(f"Authentication error: {ae}")
    except ConnectionError as ce:
        logger.error(f"Connection error: {ce}")
    except TransportError as te:
        logger.error(f"Transport error: {te}")
    except Exception as e:
        logger.error(f"General error: {e}")

    return es