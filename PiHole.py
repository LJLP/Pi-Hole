"""Module Interacting with the PiHole API"""
import requests
from loguru import logger as log

class PiHole:
    """Class providing all the functionality in this module"""
    def __init__(self, ip_address: str, api_token: str, protocol: str = "https"):
        self.ip_address = ip_address
        self.api_token = api_token
        self.protocol = protocol
        self.sid_token = None
        self.csrf_token = None
        self.headers = {}
        self.authenticate()
        log.debug("PiHole API Class initialized")

    def authenticate(self):
        if not self.protocol or not self.ip_address:
            log.trace("No protocol or IP address provided. Cannot authenticate.")
            return
        
        """
        Authenticate and store the API token.
        """
        url = f"{self.protocol}://{self.ip_address}/api/auth"
        payload = {"password": self.api_token}

        try:
            resp = requests.post(url, json=payload, verify=False, timeout=2.5)
            log.debug(f"Authentication Response: {resp.status_code}, Body: {resp.text}")
            if resp.status_code == 200:
                session = resp.json().get("session", {})
                self.sid_token = session.get("sid")
                self.csrf_token = session.get("csrf")
                if self.sid_token:
                    self.headers = {
                        "X-FTL-SID": f"{self.sid_token}",
                        "X-FTL-CSRF": f"{self.csrf_token}",
                    }
                    log.info("Authentication with PiHole Server successful.")
                else:
                    log.error("Authentication with PiHole Server failed: No valid session token.")
            else:
                log.error("Authentication with PiHole Server failed.")
        except requests.RequestException as e:
            log.error(f"Authentication error: {e}")

    def _make_request(self, method: str, endpoint: str, data: dict = None):
        """
        Helper function to send requests and handle authentication.

        :param method: "GET" or "POST"
        :param endpoint: API endpoint (e.g., "/api/dns/blocking")
        :param data: Optional JSON payload for POST requests
        :return: JSON response or None
        """
        if not self.ip_address or not self.api_token:
            log.trace("No IP address or API token provided. Cannot make request.")
            return None
        

        if not self.sid_token:
            log.error("[Request Error] No valid authentication token. Re-authenticating...")
            self.authenticate()
            if not self.sid_token:
                log.error("[Request Error] Failed to authenticate.")
                return None

        url = f"{self.protocol}://{self.ip_address}{endpoint}"

        try:
            resp = requests.request(method, url, headers=self.headers, json=data, verify=False, timeout=2.5)
            log.debug(f"API Request using {method} at {endpoint} with Response: {resp.status_code}, Body: {resp.text}")

            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 403:
                log.error("[Request ERROR] Authentication token expired or invalid. Re-authenticating...")
                self.authenticate()
                return self._make_request(method, endpoint, data)  # Retry after re-authentication
            log.error(f"[Request Error] Failed request. Status code: {resp.status_code}")
        except requests.RequestException as e:
            log.error(f"[Request Error] Request failed with error: {e}")

        return None

    def get_summary(self):
        """
        Fetch Pi-hole statistics summary.
        """
        return self._make_request("GET", "/api/stats/summary")

    def get_enabled(self) -> bool:
        """
        Get the current blocking status of Pi-hole.
        Returns True if blocking is enabled, False if disabled.
        """
        response = self._make_request("GET", "/api/dns/blocking")

        if not response:
            return None

        blocking_status = response.get("blocking")
        if blocking_status == "enabled":
            log.info("Blocking is enabled.")
            return True
        if blocking_status == "disabled":
            log.info("Blocking is disabled.")
            return False
        log.error("[get_enabled() Error] Unexpected value for blocking status.")
        return None

    def disable(self, time: int) -> bool:
        """
        Disable Pi-hole blocking for a given time (0 = infinite).
        
        :param time: Time in seconds (0 = infinite)
        :return: True if successful, False otherwise
        """
        data = {"blocking": False, "timer": time}  # JSON payload
        response = self._make_request("POST", "/api/dns/blocking", data)

        if response and response.get("blocking") == "disabled":
            log.info("[disable({time})] Succesfully disabled blocking.", time=time)
            return True

        log.error("[disable({time})] Failed to disable blocking.", time=time)
        return False

    def enable(self, time: int) -> bool:
        """
        Enable Pi-hole blocking for a given time (0 = infinite).

        :param time: Time in seconds (0 = infinite)
        :return: True if successful, False otherwise
        """
        data = {"blocking": True, "timer": time}  # JSON payload
        response = self._make_request("POST", "/api/dns/blocking", data)

        if response and response.get("blocking") == "enabled":
            log.info("[enable({time})] Succesfully enabled blocking.", time=time)
            return True

        log.error("[enable({time})] Failed to enable blocking.", time=time)
        return False
