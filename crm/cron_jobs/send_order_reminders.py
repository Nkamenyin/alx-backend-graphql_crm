#!/usr/bin/env python3
"""
send_order_reminders.py
------------------------
Fetches orders from the GraphQL endpoint that were placed within the last 7 days
and logs each order’s ID and customer email with a timestamp.
"""

import requests
import datetime

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Log file
LOG_FILE = "/tmp/order_reminders_log.txt"

# Define the GraphQL query
query = """
query RecentOrders($since: DateTime!) {
  orders(orderDate_Gte: $since) {
    id
    customer {
      email
    }
  }
}
"""

def fetch_recent_orders():
    """Fetch orders placed within the last 7 days using GraphQL."""
    seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()

    # Define variables for the query
    payload = {
        "query": query,
        "variables": {"since": seven_days_ago}
    }

    response = requests.post(GRAPHQL_URL, json=payload)

    if response.status_code != 200:
        raise Exception(f"Query failed with status {response.status_code}: {response.text}")

    return response.json()["data"]["orders"]

def log_orders(orders):
    """Log orders to a file with timestamps."""
    with open(LOG_FILE, "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for order in orders:
            log_file.write(f"[{timestamp}] Order ID: {order['id']}, Customer: {order['customer']['email']}\n")

def main():
    orders = fetch_recent_orders()
    log_orders(orders)
    print("Order reminders processed!")

if __name__ == "__main__":
    main()