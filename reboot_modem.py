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

password_file_path = os.path.expanduser("~/.cable_modem.pwd")
try:
    with open(password_file_path, "r") as pwd_file:
        modem_password = pwd_file.read().strip()
except FileNotFoundError:
    logging.critical(f"Password file not found: {password_file_path}")
    exit(1)


modem_ip = "192.168.1.1"
modem = ModemApiInterface(f"http://{modem_ip}")
modem.obtain_token(password=modem_password)
modem.reboot()
if modem.token:
    modem.revoke_token()
