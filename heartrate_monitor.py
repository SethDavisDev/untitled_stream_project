import requests
import time

#hold info relevant to the pulsoid api call and make those calls
class HeartrateMonitor:
    def __init__(self, name):
        self.name = name
        self.url = "https://dev.pulsoid.net/api/v1/data/heart_rate/latest"
        self.auth_code = ""

    def set_url(self, new_url):
        self.url = new_url
    
    def set_auth(self, new_code): 
        self.auth_code = new_code

    def poll_montior(self):
        custom_headers = {
            "Authorization": f"Bearer {self.auth_code}",
            "Content-Type": "application/json"
        }
        response = requests.get(self.url, headers=custom_headers)
        if response.content:
            actual = response.json()['data']['heart_rate']
            return int(actual)    