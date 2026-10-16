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
        try:
            response = requests.get(self.url, headers=custom_headers)
            response.raise_for_status()
            # process data when things go well
            data = response.json()
        except requests.exceptions.JSONDecodeError as json_err:
            print(f"Json parse error occurred: {json_err}")
            data = {'data': {'heart_rate': 0}}
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            
            data = {'data': {'heart_rate': 0}}
        except requests.exceptions.ConnectionError as conn_err:
            # Network failures, DNS issues, refused connections
            print(f"Connection error occurred: {conn_err}")
            data = {'data': {'heart_rate': 0}}
        except requests.exceptions.Timeout as time_err:
            # Request exceeded specified timeout limit
            print(f"Timeout error occurred: {time_err}")
            data = {'data': {'heart_rate': 0}}
        except requests.exceptions.RequestException as general_err:
            # Catch-all base class for any requests-related exception
            print(f"An unexpected error occurred: {general_err}")
            data = {'data': {'heart_rate': 0}}
        else:
            if 'error_code' in data:
                print(f"error code: {data['error_code']}, message: {data['error_message']}")
                return 0
        return data['data']['heart_rate']