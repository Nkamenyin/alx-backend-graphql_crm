import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message and optionally checks GraphQL API availability.
    """
    log_file_path = "/tmp/crm_heartbeat_log.txt"

    # Get current time in the required format
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Log the message
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{timestamp} CRM is alive\n")

    # Optional: query GraphQL API
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("""query { hello }""")
        result = client.execute(query)
        print(f"GraphQL heartbeat check: {result}")
    except Exception as e:
        print(f"GraphQL check failed: {e}")

    print("CRM heartbeat logged successfully.")