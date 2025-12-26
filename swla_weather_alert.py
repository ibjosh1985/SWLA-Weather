#!/usr/bin/env python3

import sys
import time
import yaml
import traceback
from alerts.nws_alerts import NWSAlertMonitor
from utils.logger import setup_logger

if sys.version_info < (3, 10):
    print("SWLA Weather Alert requires Python 3.10 or newer")
    sys.exit(1)

CONFIG_FILE = "swla_config.yaml"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def main():
    logger = setup_logger()
    config = load_config()

    logger.info("SWLA Weather Alert started (24/7 mode)")

    monitor = NWSAlertMonitor(config, logger)

    while True:
        try:
            monitor.check_alerts()
        except Exception:
            logger.error("Unhandled exception")
            logger.error(traceback.format_exc())
        time.sleep(config.get("poll_interval", 60))

if __name__ == "__main__":
    main()
