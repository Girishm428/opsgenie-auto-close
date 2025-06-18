from autoclose.loggers.log_cli import setup_logger
from autoclose.core.elastic_connect import elastic_connect

logger = setup_logger(__name__)

# === CHECK METRIC IN ELASTICSEARCH ===
def current_cpu_usage(host):
    es = elastic_connect()
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

    return value


def current_cpu_usage_for_hosts(host_list):
    es = elastic_connect()
    index_name = "metricbeat-7*"
    results = []

    for host in host_list:
        if not host:
            logger.warning("Skipping None or empty hostname.")
            results.append(None)
            continue

        query = {
            "size": 1,
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

        try:
            result = es.search(index=index_name, body=query)
            hits = result["hits"]["hits"]
            if hits:
                value = hits[0]["_source"]["system"]["load"]["norm"]["5"]
                logger.info(f"system.load.norm.5 for {host}: {value}")
                results.append(value)
            else:
                logger.info(f"No data found for host {host}.")
                results.append(None)
        except Exception as e:
            logger.error(f"Error querying Elasticsearch for {host}: {e}")
            results.append(None)

    return results
