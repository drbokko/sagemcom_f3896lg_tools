#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import json
import os
from modem import ModemApiInterface
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S"  # Date format
)

modem_ip = "192.168.1.1"
modem = ModemApiInterface(f"http://{modem_ip}")
modem.verbose = False

# Fetch logs
logs = modem.rest_api_get("cablemodem/eventlog").get("eventlog")
if not logs:
    logging.warning("No logs found.")
    exit(0)

# Save raw logs to ~/.cable_modem.log
log_file_path = os.path.expanduser("~/.cable_modem.log")
try:
    # Read existing logs if the file exists
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as log_file:
            existing_logs = json.load(log_file)
    else:
        existing_logs = []

    # Append only new logs to the existing logs
    existing_log_set = {json.dumps(entry, sort_keys=True) for entry in existing_logs}
    for log in logs:
        if json.dumps(log, sort_keys=True) not in existing_log_set:
            existing_logs.append(log)

    # Write the updated logs back to the file
    with open(log_file_path, "w") as log_file:
        json.dump(existing_logs, log_file, indent=4)
    logging.info(f"Logs saved to {log_file_path}")
except Exception as e:
    logging.error(f"Failed to save logs to {log_file_path}: {e}")

# ANSI escape code for underlining
UNDERLINE = "\033[4m"
RESET = "\033[0m"

# Process logs into a dictionary
d_log = {i["time"]: {"message": i["message"], "severity": i["priority"]} for i in logs}

# Display logs with color-coded messages
for i in sorted(d_log, reverse=True):
    message = d_log[i]["message"]
    severity = d_log[i]["severity"]
    timestamp = i

    # Check for specific keywords and apply colors
    if "failed to acquire" in message.lower():
        formatted_message = f"{Fore.YELLOW + Style.BRIGHT}{UNDERLINE}{message}{RESET}"
    elif "loss of sync" in message.lower() or "no ranging response" in message.lower():
        formatted_message = f"{Fore.RED + Style.BRIGHT}{UNDERLINE}{message}{RESET}"
    else:
        formatted_message = message

    # Print the log entry
    print(f"{timestamp} - {severity} - {formatted_message}")
