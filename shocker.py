import requests

#make calls to the pishock api
class Shocker:
    def __init__(self, name):
        self.name = name
        self.username = ''
        self.api_key = ''
        self.share_code = ''
        self.url = "https://api.pishock.com"
        self.auth_head = {
            "X-PiShock-Api-Key": self.api_key,
        }

    def set_auth_info(self, username, key, code):
        self.username = username
        self.api_key = key
        self.share_code = code
        self.auth_head = self.auth_head = {
            "X-PiShock-Api-Key": self.api_key,
        }

    def get_shockers(self):
        endpoint = "/Shockers"
        response = requests.get(self.url+endpoint, headers=self.auth_head)
        data = response.json()
        print(data)
        return data


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
        x = requests.post(self.url+endpoint, json = shock_post, headers=self.auth_head)
        if x.status_code  < 200 or x.status_code > 299:
            print(x.status_code)
            print(x.reason)
            print(x.text)
            return f"Something went wrong  vOv"
        print(x.status_code)
        return f"sent shock at intensity: {intensity} for {duration} milliseconds"

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
            x = requests.post(self.url+endpoint, json = shock_post, headers=self.auth_head)
            if x.status_code  < 200 or x.status_code > 299:
                print(x.status_code)
                print(x.reason)
                print(x.text)
                return f"Something went wrong  vOv"
            print(x.status_code)
            return f"sent vibrate at intensity: {intensity} for {duration} milliseconds"


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
        x = requests.post(self.url+endpoint, json = shock_post, headers=self.auth_head)
        if x.status_code  < 200 or x.status_code > 299:
            print(x.status_code)
            print(x.reason)
            print(x.text)
            return f"Something went wrong  vOv"
        print(x.status_code)
        return f"sent beep for {duration} seconds"
