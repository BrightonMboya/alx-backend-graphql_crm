#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import logging

# Set up logging
log_file = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# Define GraphQL client
transport = RequestsHTTPTransport(
    url='http://localhost:8000/graphql',
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Define the GraphQL query
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

query = gql(f"""
query {{
  orders(orderDate_Gte: "{seven_days_ago}") {{
    id
    customer {{
      email
    }}
  }}
}}
""")

try:
    result = client.execute(query)
    for order in result.get("orders", []):
        order_id = order["id"]
        customer_email = order["customer"]["email"]
        log_entry = f"Order ID: {order_id}, Customer Email: {customer_email}"
        logging.info(log_entry)

    print("Order reminders processed!")

except Exception as e:
    logging.error(f"Failed to fetch or process orders: {e}")
    print("Error occurred while processing order reminders.")
