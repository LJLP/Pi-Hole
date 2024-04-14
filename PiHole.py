import requests
from loguru import logger as log

class PiHole:
    def __init__(self, ip_address: str, api_token: str, protocol: str = "http"):
        self.ip_address = ip_address
        self.api_token = api_token
        self.protocol = protocol
        
    def get_summary(self):
        if not self.get_valid_credentials(): return

        try:
            resp = requests.get(f"{self.protocol}://{self.ip_address}/admin/api.php?summaryRaw&auth={self.api_token}", timeout=1.5)
        except Exception as e:
            log.error(e)
            return
        if resp.status_code != 200:
            return
        
        return resp.json()
    
    def disable(self, time: int) -> bool:
        """
        0 for infinite
        """
        if not self.get_valid_credentials(): return

        try:
            resp = requests.get(f"{self.protocol}://{self.ip_address}/admin/api.php?disable={time}&auth={self.api_token}", timeout=1.5)
        except Exception as e:
            log.error(e)
            return
        return resp.status_code == 200

    def get_enabled(self) -> bool:
        if not self.get_valid_credentials(): return

        summary = self.get_summary()
        if summary is None:
            return
        if not isinstance(summary, dict):
            return
        return summary.get("status") == "enabled"
    
    def enable(self) -> bool:
        if not self.get_valid_credentials(): return

        try:
            resp = requests.get(f"{self.protocol}://{self.ip_address}/admin/api.php?enable&auth={self.api_token}", timeout=1.5)
        except Exception as e:
            log.error(e)
            return
        return resp.status_code == 200
    
    def disable(self, time: int) -> bool:
        if not self.get_valid_credentials(): return

        try:
            resp = requests.get(f"{self.protocol}://{self.ip_address}/admin/api.php?disable={time}&auth={self.api_token}", timeout=1.5)
        except Exception as e:
            log.error(e)
            return
        return resp.status_code == 200

    def get_valid_credentials(self) -> bool:
        return None not in [self.ip_address, self.api_token, self.protocol]