#built in
import time
import random
from dataclasses import dataclass

#dependencies
import numpy as np

#internal
from heartrate_monitor import HeartrateMonitor
from shocker import Shocker

def map_value(value, min_val, max_val, target_min, target_max):
    # Figure out how 'wide' each range is
    left_span = max_val - min_val
    right_span = target_max - target_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - min_val) / float(left_span)

    # Convert the 0-1 range into a value in the right range
    return target_min + (value_scaled * right_span)

@dataclass
class hr_data:
    unfiltered: float = 0
    filtered: float = 0
    low: float = 0
    high: float = 0
    change: float = 0
    is_increasing: bool = False

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
        self.last_data = hr_data()

        #shocker stuff
        self.shocker = Shocker('Pishock')
        self.mode = 0       # 0 is shock 1 is vibrate 2 is beep, same as pishock api 
        self.shocker_id = 0
        self.is_allowed_to_shock = True
        self.shock_timeblock_duration_s = 60
        self.last_shock_time = time.perf_counter()
        self.shock_duration = 500
        self.min_punishable_spike = 20
        self.max_punishable_spike = 40
        self.max_intensity = 50
        self.min_intensity = 10
        self.max_retries = 5
        self.retries_left = 0
        self.luck_numerator = 1
        self.luck_denomenator = 5
       
    def increase_luck_numerator(self):
        self.luck_numerator = min(self.luck_numerator + 1, self.luck_denomenator)
    def reset_luck(self):
        self.luck_numerator = 1
    def test_shock(self):
        self.shocker.shock(self.shocker_id, 500, 5)

    #sends auth information through to the heartrate monitor object
    def configure_devices(self, pulse_code, pishock_code):
        self.hr.set_auth(pulse_code)
        self.shocker.set_auth_header(pishock_code)

    #how long after a shock is sent before we can send another one
    def set_timeblock(self, new_duration):
        self.shock_timeblock_duration_s = new_duration

    def configure_settings(self, low_spike, high_spike, window_size, low_shock, high_shock, duration, block_duration, set_chance):
        self.min_punishable_spike = low_spike
        self.max_punishable_spike = high_spike
        self.history_window_size = window_size
        self.min_intensity = low_shock
        self.max_intensity = high_shock
        self.shock_duration = duration
        self.shock_timeblock_duration_s = block_duration
        self.starting_chance = set_chance

    # remove heartrate data from history
    def clear_history(self):
        self.history = []

    def heartrate_input(self):
        data = hr_data()
        data.unfiltered = self.hr.poll_montior()
        print(data.unfiltered)
        data.filtered = self.update_filter_window(data.unfiltered)
        print(f"filtered: {data.filtered}")
        self.history.append(data.filtered)
        if len(self.history) > self.history_window_size:
            self.history.pop(0)
        data.low, data.high, data.change, data.is_increasing = self.get_historic_hr_difference()
        

    def reset_shock_blocker(self):
        if time.perf_counter() - self.last_shock_time > self.shock_timeblock_duration_s:
            self.is_allowed_to_shock = True
    
    def is_shock_deserved(self) -> bool:    
        # bool whether we need to send shock
        if not self.last_data.is_increasing:
            return False
        if (self.last_data.change) < self.min_punishable_spike:
            return False
        if not self.is_allowed_to_shock:
            print("Tried to shock but blocked by blocker")
            return False
        return True

    def is_unlucky(self):
        chance_val = self.luck_numerator / self.luck_denomenator
        if random.random() > chance_val:
            self.increase_luck_numerator()
            print("You got lucky")
            self.is_allowed_to_shock = False
            self.last_shock_time = time.perf_counter()
            return False
        else:
            print(f"unlucky, get zapped")
            self.reset_luck()
            self.is_allowed_to_shock = False
            self.last_shock_time = time.perf_counter()
            return True
    
    def shocker_output(self):
        #generate information about the shock we need to send
        sanitized_delta = min(self.last_data.c, self.max_punishable_spike)
        intensity = self.convert_jump_amount_to_intensity(sanitized_delta)

        #send shock
        self.shocker.shock(self.shocker_id, self.shock_duration, intensity)
        self.is_allowed_to_shock = False
        self.last_shock_time = time.perf_counter()

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

    def store_shocker_device_id(self):
        self.shocker_id = self.shocker.get_shocker_id()
    


    def update_filter_window(self, new_reading):
        #Base constraints these are the human limits
        if new_reading < 30 or new_reading > 220:
            return self.buffer[-1] if self.buffer else 72.0  # Fallback to last known good value or default
        self.buffer.append(new_reading)
        if len(self.buffer) > self.filter_window_size:
            self.buffer.pop(0)
            
        #Extract median from current rolling window
        median = np.median(self.buffer)
        
        #Check for sudden spikes relative to the rolling median
        if abs(new_reading - median) > self.max_deviation:
            # Replace spike in buffer with median so it doesn't skew future calculations
            self.buffer[-1] = median
            return median
            
        return float(new_reading)

    def convert_jump_amount_to_intensity(self, jump_amount):
        intensity_value = int(map_value(jump_amount, self.min_punishable_spike, self.max_punishable_spike, 1, self.max_intensity))
        return intensity_value