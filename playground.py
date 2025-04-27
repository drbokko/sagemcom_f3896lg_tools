#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
from modem import ModemApiInterface
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S"  # Date format
)

modem_ip = "192.168.1.1"
modem = ModemApiInterface(f"http://{modem_ip}")
modem.verbose = False

# modem.verbose = False
free_endpoints = ["system/softwareupdate",
                  "system/firstinstall",
                  "system/languages", 
                  "system/localization",
                  "system/modemmode",
                  "system/gateway/provisioning",
                  "system/ui/screens",
                  "cablemodem/registration",
                  "cablemodem/eventlog",
                  "cablemodem/state_",
                  "cablemodem/upstream",
                  "cablemodem/downstream",
                  "cablemodem/upstream/primary_",
                  "cablemodem/downstream/primary_",
                  "cablemodem/serviceflows",
                  "mta/lines",
                  "wifi/band2g/state_",
                  "wifi/band5g/state_"]

logging.info("Testing free endpoints")
for i in free_endpoints:
    result = modem.rest_api_get(i)

password_file_path = os.path.expanduser("~/.cable_modem.pwd")
try:
    with open(password_file_path, "r") as pwd_file:
        modem_password = pwd_file.read().strip()
except FileNotFoundError:
    logging.critical(f"Password file not found: {password_file_path}")
    exit(1)

modem.obtain_token(password=modem_password)
# Protected, need to figure out how to use the token
protected_endpoints = ["wifi/capabilities",
                       "wifi/band2g/state",
                       "wifi/band2g/config",
                       "wifi/band2g/guest/config",
                       "wifi/band5g/state",
                       "wifi/band5g/config",
                       "wifi/band5g/guest/config",
                       "cablemodem/state",
                       "network/hosts?connectedOnly=true", ]
logging.info("Testing protected endpoints")
for i in protected_endpoints:
    result = modem.rest_api_get(i, headers=modem.authorization_bearer())
# "Connection": "keep-alive",


# Example usage


if modem.token:
    modem.revoke_token()
