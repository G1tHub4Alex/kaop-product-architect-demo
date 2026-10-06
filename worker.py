import logging
import os
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
api_url = os.environ.get("API_URL", "http://demo-api:8080/work")
failures = 0

while True:
    try:
        with urlopen(api_url, timeout=2) as response:
            if response.status != 200:
                raise RuntimeError(f"HTTP {response.status}")
        failures = 0
        logging.info("API request succeeded: %s", api_url)
    except (URLError, RuntimeError) as error:
        failures += 1
        logging.error("API request failed (%s/3): url=%s error=%s", failures, api_url, error)
        if failures >= 3:
            logging.error("Exiting after repeated API connection failures")
            sys.exit(1)
    time.sleep(5)
