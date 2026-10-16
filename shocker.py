import requests

#make calls to the pishock api
class Shocker:
    def __init__(self, name):
        self.name = name
        self.url = "https://api.pishock.com"
        self.auth_head = {
            "X-PiShock-Api-Key": '',
        }

    def set_auth_header(self, auth_key: str) -> None:
        self.auth_head = self.auth_head = {
            "X-PiShock-Api-Key": auth_key,
        }
        print(self.auth_head)

    def get_api(self, endpoint):
        try:
            response = requests.get(self.url+endpoint, headers=self.auth_head)
            # raise errors for 4xx and 5xx status codes
            response.raise_for_status()

            # process data when things go well
            data = response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            data = {}
        except requests.exceptions.JSONDecodeError as json_err:
            print(f"Json parse error occurred: {json_err}")
            data = {}
        except requests.exceptions.ConnectionError as conn_err:
            # Network failures, DNS issues, refused connections
            print(f"Connection error occurred: {conn_err}")
            data = {}
        except requests.exceptions.Timeout as time_err:
            # Request exceeded specified timeout limit
            print(f"Timeout error occurred: {time_err}")
            data = {}
        except requests.exceptions.RequestException as general_err:
            # Catch-all base class for any requests-related exception
            print(f"An unexpected error occurred: {general_err}")
            data = {}
        return data

    def post_api(self, endpoint, post_data):
        try:
            x = requests.post(self.url+endpoint, json = post_data, headers=self.auth_head)
            x.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"status code: {x.status_code}\nreason:{x.reason}")
            if x.status_code == 401:
                print("API Key is invalid, or user does not have access to requested device.")
            if x.status_code == 404:
                print(f"Could not find device or share")
            if x.status_code == 405:
                print(f"An operation was provided but that share has not allowed the device to perform (such as shocking while shocking is disabled on the share)")
            if x.status_code == 406:
                print(f"Device is not V3 — Please encourage the user to flash V3 on the device or seek tech support assitance")
            if x.status_code == 410:
                print(f"Share is locked")
            if x.status_code == 412:
                print(f"Intensity is out of bounds (<1, >100, higher than max intensity for a shock)")
            if x.status_code == 416:
                print(f"Duration exceeds limits on share, is lower than 16ms (due to legacy concerns) or higher than 15,000ms")
            if x.status_code == 503:
                print(f"Share or Shocker is paused")
        except requests.exceptions.JSONDecodeError as json_err:
            print(f"Json parse error occurred: {json_err}")
        except requests.exceptions.ConnectionError as conn_err:
            # Network failures, DNS issues, refused connections
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as time_err:
            # Request exceeded specified timeout limit
            print(f"Timeout error occurred: {time_err}")
        except requests.exceptions.RequestException as general_err:
            # Catch-all base class for any requests-related exception
            print(f"An unexpected error occurred: {general_err}")
        else: return True

    def get_shocker_id(self) -> str:
        endpoint = "/Shockers"
        data = self.get_api(endpoint)
        if not data or not data[0] or not data[0]['ShockerId']:
            return 'shocker_id_not_found'
        return data[0]['ShockerId']


    def shock(self, shocker_id, duration, intensity):
        endpoint = f"/Shockers/OperateById/{shocker_id}"
        intensity = min(max(0, intensity), 100)
        shock_post = {
            "AgentName": self.name,
            "Operation": 0,
            "Duration": duration,
            "Intensity": intensity,
            "MinimumDuration": 1,
            "MinimumIntensity": 1,
            "IntensityAsPercentage": False
            }
        print(shock_post)
        if self.post_api(endpoint, shock_post):
            return {'success': True, 'text': f"Sent shock at {intensity} for {duration} ms"}
        else: {'success': False, 'text':f"ran into error during api call"}

    def vibrate(self, shocker_id, duration, intensity):
            endpoint = f"/Shockers/OperateById/{shocker_id}"
            intensity = min(max(0, intensity), 100)
            shock_post = {
                "AgentName": self.name,
                "Operation": 1,
                "Duration": duration,
                "Intensity": intensity,
                "MinimumDuration": 1,
                "MinimumIntensity": 1,
                "IntensityAsPercentage": False
                }
            print(shock_post)
            
            if  self.post_api(endpoint, shock_post):
                return {'success': True, 'text': f"sent vibrate at intensity: {intensity} for {duration} milliseconds"}
            else:
                return {'success': False, 'text':f"ran into error during api call"}


    def beep(self, shocker_id, duration):
        endpoint = f"/Shockers/OperateById/{shocker_id}"
        intensity = min(max(0, intensity), 100)
        shock_post = {
            "AgentName": self.name,
            "Operation": 2,
            "Duration": duration,
            "Intensity": 1,
            "MinimumDuration": 100,
            "MinimumIntensity": 1,
            "IntensityAsPercentage": False
            }
        print(shock_post)
        if self.post_api(endpoint, shock_post):
            return {'success': True, 'text': f"Sent beep for {duration} milliseconds"}
        else:
            return {'success': False, 'text':f"ran into error during api call"}
