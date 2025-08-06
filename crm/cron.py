from datetime import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    log_path = "/tmp/crm_heartbeat_log.txt"
    with open(log_path, "a") as log_file:
        log_file.write(message + "\n")

    # Optional: verify GraphQL endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            graphql_data = response.json()
            hello_message = graphql_data.get("data", {}).get("hello", "No response")
            with open(log_path, "a") as log_file:
                log_file.write(f"{timestamp} GraphQL says: {hello_message}\n")
        else:
            with open(log_path, "a") as log_file:
                log_file.write(f"{timestamp} GraphQL error: {response.status_code}\n")
    except Exception as e:
        with open(log_path, "a") as log_file:
            log_file.write(f"{timestamp} GraphQL exception: {str(e)}\n")



def update_low_stock():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_path = "/tmp/low_stock_updates_log.txt"

    mutation = """
    mutation {
      updateLowStockProducts {
        success
        updatedProducts {
          id
          name
          stock
        }
      }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": mutation},
            timeout=10
        )

        with open(log_path, "a") as log_file:
            if response.status_code == 200:
                data = response.json().get("data", {}).get("updateLowStockProducts", {})
                log_file.write(f"\n[{timestamp}] {data.get('success')}\n")
                for product in data.get("updatedProducts", []):
                    line = f"- {product['name']} (New stock: {product['stock']})\n"
                    log_file.write(line)
            else:
                log_file.write(f"\n[{timestamp}] Error {response.status_code} from GraphQL endpoint\n")

    except Exception as e:
        with open(log_path, "a") as log_file:
            log_file.write(f"\n[{timestamp}] Exception: {str(e)}\n")
