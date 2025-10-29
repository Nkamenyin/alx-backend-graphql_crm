import requests
import json
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


# --- 1️⃣ Low Stock Update Function ---
def update_low_stock():
    """
    Executes a GraphQL mutation to restock low-stock products and logs the results.
    """
    endpoint = "http://localhost:8000/graphql"
    mutation = """
    mutation {
        updateLowStockProducts {
            message
            updatedProducts {
                name
                stock
            }
        }
    }
    """

    log_file_path = "/tmp/low_stock_updates_log.txt"

    try:
        response = requests.post(endpoint, json={'query': mutation})
        data = response.json()

        # Log to file
        with open(log_file_path, "a") as log:
            timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
            log.write(f"\n[{timestamp}] Low-stock update run\n")

            if "errors" in data:
                log.write(f"Error: {data['errors']}\n")
            else:
                updates = data["data"]["updateLowStockProducts"]["updatedProducts"]
                msg = data["data"]["updateLowStockProducts"]["message"]
                log.write(f"{msg}\n")
                for p in updates:
                    log.write(f"→ {p['name']} restocked to {p['stock']}\n")

        print("Low-stock products updated successfully!")

    except Exception as e:
        with open(log_file_path, "a") as log:
            log.write(f"\n[{datetime.datetime.now()}] ERROR: {str(e)}\n")
        print("Error updating low-stock products:", e)


# --- 2️⃣ CRM Heartbeat Function ---
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