import datetime
import requests

def log_crm_heartbeat():
    """Logs a heartbeat message and optionally checks the GraphQL API."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Log to /tmp/crm_heartbeat_log.txt
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(message)

    # (Optional) Ping the GraphQL hello endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"}
        )
        if response.status_code == 200:
            log_file.write(f"{timestamp} GraphQL responded OK\n")
        else:
            log_file.write(f"{timestamp} GraphQL check failed ({response.status_code})\n")
    except Exception as e:
        log_file.write(f"{timestamp} GraphQL check error: {e}\n")