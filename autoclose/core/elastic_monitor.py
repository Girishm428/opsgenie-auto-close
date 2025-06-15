from elasticsearch import Elasticsearch, AuthenticationException, ConnectionError, TransportError
from autoclose.loggers.log_cli import setup_logger
from autoclose.config.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD, ELASTICSEARCH_VERIFY_CERTS, ELASTICSEARCH_SSL_SHOW_WARN

logger = setup_logger()

CPU_THRESHOLD = 0.85  # default threshold, could be alert-specific

# === CHECK METRIC IN ELASTICSEARCH ===
def is_cpu_normal(host):
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

    query = {
        "size": 1,  # Only the latest document
        "sort": [{"@timestamp": {"order": "desc"}}],
        "query": {
            "bool": {
                "must": [
                    {"term": {"host.name": host}},
                    {"exists": {"field": "system.load.norm.5"}}
                ]
            }
        }
    }

    index_name = "metricbeat-7*"

    try:
        result = es.search(index=index_name, body=query)
        hits = result["hits"]["hits"]
        if hits:
            value = hits[0]["_source"]["system"]["load"]["norm"]["5"]
            logger.info(f"system.load.norm.5 for {host}: {value}")
        else:
            logger.info(f"No data found for host {host}.")
    except Exception as e:
        logger.error(f"Error querying Elasticsearch: {e}")

    return value < CPU_THRESHOLD


