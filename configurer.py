from heartrate_monitor import HeartrateMonitor
from shocker import Shocker
import numpy as np
import time

def convert_s_to_ms(s):
    return s*1000

def map_value(value, min_val, max_val, target_min, target_max):
    # Figure out how 'wide' each range is
    left_span = max_val - min_val
    right_span = target_max - target_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - min_val) / float(left_span)

    # Convert the 0-1 range into a value in the right range
    return target_min + (value_scaled * right_span)

class Configlayer:
    def __init__(self, window_size=5, history_size = 30, max_deviation_bpm=20):
        #heart rate stuff
        self.hr = HeartrateMonitor('pulsoid')
        self.filter_window_size = window_size
        self.history_window_size = history_size
        self.raw_hr_data = 0
        self.buffer = []
        self.history = []
        self.max_deviation = 40

        #shocker stuff
        self.shocker = Shocker('Pishock')
        self.shocker_id = 0
        self.is_allowed_to_shock = True
        self.shock_timeblock_duration_s = 60
        self.last_shock_time = time.perf_counter()
        self.shock_duration = 500
        self.min_punishable_spike = 20
        self.max_punishable_spike = 40
        self.max_intensity = 50
        self.min_intensity = 10

    #sends auth information through to the heartrate monitor object
    def configure_hr_connection(self, auth_code):
        self.hr.set_auth(auth_code)

    #how long after a shock is sent before we can send another one
    def set_timeblock(self, new_duration):
        self.shock_timeblock_duration_s = new_duration

    #checks the last 15 seconds of filtered heartrate data and returns the lowest, highest, and the difference between them
    def get_historic_hr_difference(self):
            lowest = min(self.history)
            highest = max(self.history)
            delta = highest - lowest
            print(f"heart rate difference is {delta}")
            if self.history[0] > self.history[-1]:
                print("heartrate decreasing")
                return [lowest, highest, delta, False]
            else:
                print("heartrate increasing")
                return [lowest, highest, delta, True]

    def configure_shocker_connection(self, user, auth, sharecode):
        self.shocker.set_auth_info(user, auth, sharecode)

    def test_hr_display(self):
        data = self.hr.poll_montior()
        return data['data']
    
    #for testing, sends a one second shock at the lowest intensity
    def send_test_shock(self):
        self.shocker.shock(1,1)

    def setup(self):
        data = self.shocker.get_shockers()
        self.shocker_id = data[0]['ShockerId']

    
    def update(self):
        # has the user told us to start polling and shocking
        # should be false when none of the auth information is set up, to avoid crashes
        if not self.is_active:
            return
        #check if we need to remove the blocker
        if time.perf_counter() - self.last_shock_time > self.shock_timeblock_duration_s:
            self.is_allowed_to_shock = True

        current_hr = self.hr.poll_montior()
        print(current_hr)
        filtered_hr = self.update_filter_window(current_hr)
        print(f"filtered: {filtered_hr}")
        self.history.append(filtered_hr)
        if len(self.history) > 10:
            self.history.pop(0)
        history_data = self.get_historic_hr_difference()
        is_increase = history_data[3]
        delta = history_data[2]

        #make sure we are allowed to send a shock
        if not is_increase:
            return
        if (delta) < self.min_punishable_spike:
            return
        if not self.is_allowed_to_shock:
            print("Tried to shock but blocked by blocker")
            return

        #generate information about the shock we need to send
        sanitized_delta = min(delta, self.max_punishable_spike)
        intensity = self.convert_jump_amount_to_intensity(delta)

        #send shock
        self.shocker.vibrate(self.shocker_id, self.shock_duration, intensity)
        self.is_allowed_to_shock = False
        self.last_shock_time = time.perf_counter()
        

    

    def update_filter_window(self, new_reading):
        #Base constraints these are the human limits
        if new_reading < 30 or new_reading > 220:
            return self.buffer[-1] if self.buffer else 72.0  # Fallback to last known good value or default
        self.buffer.append(new_reading)
        if len(self.buffer) > self.filter_window_size:
            self.buffer.pop(0)
            
        # 2. Extract median from current rolling window
        median = np.median(self.buffer)
        
        # 3. Check for sudden spikes relative to the rolling median
        if abs(new_reading - median) > self.max_deviation:
            # Replace spike in buffer with median so it doesn't skew future calculations
            self.buffer[-1] = median
            return median
            
        return float(new_reading)

    def convert_jump_amount_to_intensity(self, jump_amount):
        intensity_value = int(map_value(jump_amount, self.min_punishable_spike, self.max_punishable_spike, 1, self.max_intensity))
        return intensity_value