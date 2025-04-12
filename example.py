from iliadstats import IliadStats
import logging
import time

# Configure logging for the example
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    # Path to the secrets file
    secrets_file_path = "secrets.json"

    # Initialize the IliadStats instance
    ilistats = IliadStats(
        secrets_file_path=secrets_file_path,
        refresh_interval=120  # Optional: Set the refresh interval in seconds
    )

    # Get traffic consumption
    traffic_consumption = ilistats.get_traffic_consumption()
    print(f"Traffic Consumption: {traffic_consumption} GB")

    # Get traffic endowment
    traffic_endowment = ilistats.get_traffic_endowment()
    print(f"Traffic Endowment: {traffic_endowment} GB")

    # Get renewal date
    renewal_date = ilistats.get_renewal_date()
    print(f"Renewal Date: {time.strftime('%d/%m/%Y', renewal_date)}")