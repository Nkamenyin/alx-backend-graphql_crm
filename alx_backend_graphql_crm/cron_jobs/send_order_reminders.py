from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import os

# Define GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def main():
    # 1. Calculate date range (last 7 days)
    today = datetime.now()
    seven_days_ago = today - timedelta(days=7)
    start_date = seven_days_ago.strftime("%Y-%m-%d")

    # 2. Configure GraphQL client
    transport = RequestsHTTPTransport(
        url=GRAPHQL_ENDPOINT,
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # 3. Define GraphQL query
    query = gql(
        """
        query GetRecentOrders($startDate: Date!) {
            orders(filter: { orderDate_Gte: $startDate }) {
                id
                customer {
                    email
                }
            }
        }
        """
    )

    # 4. Execute query
    try:
        result = client.execute(query, variable_values={"startDate": start_date})
        orders = result.get("orders", [])

        # 5. Log to file
        log_file = "/tmp/order_reminders_log.txt"
        with open(log_file, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n--- Order reminder run at {timestamp} ---\n")
            if orders:
                for order in orders:
                    order_id = order["id"]
                    customer_email = order["customer"]["email"]
                    f.write(f"Order ID: {order_id}, Email: {customer_email}\n")
            else:
                f.write("No recent orders found.\n")

        print("Order reminders processed!")

    except Exception as e:
        print(f"Error fetching orders: {e}")

if __name__ == "__main__":
    main()