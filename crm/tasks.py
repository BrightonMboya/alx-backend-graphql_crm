from celery import shared_task
from datetime import datetime
import requests

@shared_task
def generate_crm_report():
    query = """
    query {
      customersCount
      ordersCount
      totalRevenue
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json().get("data", {})
            customer_count = data.get("customersCount", 0)
            order_count = data.get("ordersCount", 0)
            revenue = data.get("totalRevenue", 0.0)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report_line = f"{timestamp} - Report: {customer_count} customers, {order_count} orders, {revenue} revenue\n"

            with open("/tmp/crm_report_log.txt", "a") as log_file:
                log_file.write(report_line)

        else:
            with open("/tmp/crm_report_log.txt", "a") as log_file:
                log_file.write(f"Error: GraphQL returned status {response.status_code}\n")

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as log_file:
            log_file.write(f"Exception occurred: {str(e)}\n")
