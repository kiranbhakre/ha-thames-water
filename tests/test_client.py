import sys
import os
from pathlib import Path
from unittest.mock import MagicMock

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

# Mock homeassistant before importing the component
# This prevents ModuleNotFoundError when running this script standalone
sys.modules["homeassistant"] = MagicMock()
sys.modules["homeassistant.config_entries"] = MagicMock()
sys.modules["homeassistant.core"] = MagicMock()
sys.modules["homeassistant.helpers"] = MagicMock()
sys.modules["homeassistant.helpers.entity"] = MagicMock()
sys.modules["homeassistant.helpers.typing"] = MagicMock()

import datetime
import logging
from dotenv import load_dotenv
from custom_components.thames_water.thameswaterclient import ThamesWater

# Set up logging
logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

def main():
    # Load environment variables from .env file if it exists
    load_dotenv()

    email = os.getenv("THAMES_WATER_EMAIL")
    password = os.getenv("THAMES_WATER_PASSWORD")
    account_number = os.getenv("THAMES_WATER_ACCOUNT_NUMBER")

    if not all([email, password, account_number]):
        print("Error: Missing environment variables.")
        print("Please set THAMES_WATER_EMAIL, THAMES_WATER_PASSWORD, and THAMES_WATER_ACCOUNT_NUMBER.")
        return

    try:
        print(f"Attempting to authenticate as {email}...")
        client = ThamesWater(email, password, int(account_number))
        print("Authentication successful!")

        # Test fetching usage for the last 7 days
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=10)

        # Note: We need a meter ID. 
        # In a real scenario, this would be discovered or known.
        # For this test, we might need the user to provide a METER_ID too.
        meter_id = os.getenv("THAMES_WATER_METER_ID")
        
        if meter_id:
            print(f"Fetching usage for meter {meter_id} from {start_date.date()} to {end_date.date()}...")
            usage = client.get_meter_usage(int(meter_id), start_date, end_date)
            print(f"Retrieved {len(usage.Lines)} reading lines.")
            for line in usage.Lines:  # Show all readings
                print(f" {usage.TargetUsage} : {line.Label}: {line.Usage} L (Read: {line.Read})")
        else:
            print("No THAMES_WATER_METER_ID provided. Skipping usage fetch test.")

    except Exception as e:
        print(f"An error occurred during testing: {e}")

if __name__ == "__main__":
    main()
