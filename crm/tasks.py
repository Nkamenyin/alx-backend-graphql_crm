import requests
import json
from datetime import datetime
from celery import shared_task

@shared_task
def generate_crm_report():
    """
    Fetch total customers, orders, and revenue via GraphQL
    and log the report to /tmp/crm_report_log.txt
    """
    endpoint = "http://localhost:8000/graphql"
    query = """
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """

    try:
        response = requests.post(endpoint, json={'query': query})
        data = response.json()

        # Extract metrics
        totals = data.get("data", {})
        customers = totals.get("totalCustomers", 0)
        orders = totals.get("totalOrders", 0)
        revenue = totals.get("totalRevenue", 0)

        # Format log entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

        # Write to log file
        with open("/tmp/crm_report_log.txt", "a") as log_file:
            log_file.write(log_entry)

        print("✅ CRM report generated successfully!")

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - ERROR: {e}\n")
        print("❌ Error generating CRM report:", e)
