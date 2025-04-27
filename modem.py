import requests
import logging
import json
from bs4 import BeautifulSoup  # For parsing HTML content
from requests.exceptions import HTTPError

# Configure logging

class ModemApiInterface:
    def __init__(self, base_url):
        """
        Initialize the ModemPageFetcher class with the API base URL.
        """
        self.base_url = base_url
        self.user = None
        self.password = None
        self.token = None
        self.verbose = True

    def obtain_token(self, password):
        json_response = self.rest_api_post(key="user/login", 
                                          headers={"Connection": "keep-alive"},
                                          payload={"password": password})
        if json_response:
            self.token = json_response.get("created").get("token")
            self.user = json_response.get("created").get("userId")
            self.password = password
            
            logging.info(f"Token obtained successfully -> {self.token}.")
            return self.token
        else:
            logging.critical(f"Failed to obtain token")
            return None

    def authorization_bearer(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}#, "Connection": "keep-alive"}
        else:
            raise ValueError("Token is not set. Please obtain a token first.")
    
    def revoke_token(self):
        """
        Revoke the current token using the modem's API.
        """
        if not self.token:
            logging.error("No token to revoke.")
            return False

        json_response = self.rest_api_delete(key=f"user/{self.user}/token/{self.token}",
                                             headers=self.authorization_bearer())
        if json_response:
            self.token = None
            logging.info("Token successfully revoked.")
        else:
            logging.critical(f"Failed to remove token")
            return None
        
    def reboot(self):
        full_header = self.authorization_bearer()
        full_header.update({"refearer": f"http://{self.base_url}/?page=admin%2Freboot"})
        self.rest_api_post("system/reboot", 
                           headers=full_header,
                           payload={"reboot": {"enable": True}})          





    def _rest_url(self, key):
        return f"{self.base_url}/rest/v1/{key}"

    def rest_api_get(self, key, payload=None, headers=None):
        try:
            logging.info(f"Sending GET to API endpoint: {key}")
            response = requests.get(self._rest_url(key), json=payload, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            if self.verbose:
                pretty_json = json.dumps(json_data, indent=4)
                logging.info(f"Returning:\n{pretty_json}")

            return json_data
    
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send POST to '{self._rest_url(key)}': {e}")
            return None
        
    def rest_api_post(self, key, payload=None, headers=None):
        try:
            logging.info(f"Sending POST to API endpoint: {self._rest_url(key)}")
            response = requests.post(self._rest_url(key), json=payload, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            if  self.verbose:
                pretty_json = json.dumps(json_data, indent=4)
                logging.info(f"Returning:\n{pretty_json}")

            return json_data
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send POST to '{self._rest_url(key)}': {e}")
            return None

    def rest_api_delete(self, key, payload=None, headers=None):
        try:
            logging.info(f"Sending DELETE to API endpoint: {key}")
            response = requests.delete(self._rest_url(key), headers=headers)
            response.raise_for_status()
            #json_data = response.json()
            #if  self.verbose:
            #    pretty_json = json.dumps(json_data, indent=4)
            #    logging.info(f"Returning:\n{pretty_json}")
            #return json_data
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send DELETE to '{self._rest_url(key)}': {e}")
            return None

    