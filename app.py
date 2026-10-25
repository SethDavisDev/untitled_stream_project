import tkinter as tk
import configurer
import time
import random

main_bg = '#RRGGBB'
card_bg = '#RRGGBB'
highlighted_bg = '#RRGGBB'

class LabeledSpin(tk.Frame):
    def __init__(self, master, label_text="Label:", initial_val=1, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.label = tk.Label(self, text=label_text)
        self.spin = tk.Spinbox(self)
        self.set_range(1,100)
        self.set_default(initial_val)
        self.label.pack(side='left')
        self.spin.pack(side='left')

    def get(self):
        return int(self.spin.get())

    def set_default(self, value):
        self.spin.delete(0,'end')
        self.spin.insert(0, value)

    def set_range(self, from_, to):
        self.spin.config(from_=from_, to=to)
    

is_hr_active = False
is_Shock_active = False
is_in_luck_mode = False

def tracker_loop():
    if not is_hr_active:
        return
    if test.is_shock_deserved():
        if not is_in_luck_mode or (is_in_luck_mode and test.is_unlucky()):
            test.shocker_output()
    test.reset_shock_blocker()
    test.heartrate_input()
    root.after(500, tracker_loop)

def save_keys():
    pulse_key = content['pulse_key_entry'].get()
    pishock_key = content['pishock_key_entry'].get()
    test.configure_devices(pulse_key, pishock_key)
    test.store_shocker_device_id()

def save_settings():
    low_spike = content['low_spike'].get()
    high_spike = content['high_spike'].get()
    window_size = content['window_size'].get()
    low_shock = content['low_shock'].get()
    high_shock = content['high_shock'].get()
    block_duration = content['block_duration'].get()
    shock_duration = content['shock_duration'].get()

    test.configure_settings(low_spike, high_spike, window_size, low_shock, high_shock, shock_duration, block_duration)

def start():
    global is_hr_active
    is_hr_active = True
    tracker_loop()

def stop():
    test.clear_history()
    global is_hr_active
    is_hr_active = False

def test_shocker():
    test_intensity = content['test_intensity'].get()
    if test_intensity > 20:
        test_intensity = 10
    test.test_shock(test_intensity)

def test_vibe():
    test_intensity = content['test_intensity'].get()
    if test_intensity > 20:
        test_intensity = 10
    test.send_vibrate(test_intensity)

def randomly_shock():
    if random.random() < 0.2:
        test.test_shock()

def lucky_mode():
    global is_in_luck_mode
    if is_in_luck_mode:
        is_in_luck_mode = False
    else: is_in_luck_mode = True
    content['luck_mode_value'].config(text=f"Gamble Mode is {"ON" if is_in_luck_mode else "OFF"}")

test = configurer.Configlayer()
root = tk.Tk()
content = {}
main_window = tk.Frame(root)
content['keys_frame'] = tk.Frame(main_window)
content['title_frame'] = tk.Frame(content['keys_frame'])
content['entrys_frame'] = tk.Frame(content['keys_frame'])
content['submit_frame'] = tk.Frame(content['keys_frame'])
content['keys_frame_label'] = tk.Label(content['title_frame'], text="API Keys")
content['pulse_frame'] = tk.Frame(content['entrys_frame'])
content['pulse_key_label'] = tk.Label(content['pulse_frame'], text="Pulsoid API Key")
content['pulse_key_entry'] = tk.Entry(content['pulse_frame'])
content['pishock_frame'] = tk.Frame(content['entrys_frame'])
content['pishock_key_label'] = tk.Label(content['pishock_frame'], text="PiShock API Key")
content['pishock_key_entry'] = tk.Entry(content['pishock_frame'])
content['submit_keys'] = tk.Button(content['submit_frame'], text='save_keys', command=save_keys)

content['keys_frame_label'].pack(anchor='s', expand=True, fill='x')
content['title_frame'].pack(side='top', fill='x')

content['pulse_key_label'].pack(side='top')
content['pulse_key_entry'].pack(side='top')
content['pulse_frame'].pack(side='left')
content['pishock_key_label'].pack(side='top')
content['pishock_key_entry'].pack(side='top')
content['pishock_frame'].pack(side='left')
content['entrys_frame'].pack(side='top', fill='x')

content['submit_keys'].pack(side='top',expand=True, fill='x')
content['submit_frame'].pack(side='top', fill='x')

content['keys_frame'].pack()


# configurable settings
content['controls_frame'] = tk.Frame(main_window)
content['settings_frame'] = tk.Frame(content['controls_frame'])
content['low_spike'] = LabeledSpin(content['settings_frame'], 'Spike needed for lowest intensity', initial_val=20)
content['high_spike'] = LabeledSpin(content['settings_frame'], 'Spike needed for highest intensity', initial_val=40)
content['low_shock'] = LabeledSpin(content['settings_frame'], 'Lowest Shock Intensity', initial_val=10)
content['high_shock'] = LabeledSpin(content['settings_frame'], 'Highest Shock Intensity', initial_val=50)
content['shock_duration'] = LabeledSpin(content['settings_frame'], 'Duration of Shock in milliseconds', initial_val=500)
content['shock_duration'].set_range(16, 15000)
content['window_size'] = LabeledSpin(content['settings_frame'], 'window size for spike detection', initial_val=30)
content['window_size'].set_range(10, 40)
content['block_duration'] = LabeledSpin(content['settings_frame'], 'minimum delay between shocks', initial_val=60)
content['block_duration'].set_range(10, 300)

content['buttons_frame'] = tk.Frame(content['controls_frame'])
content['start'] = tk.Button(content['buttons_frame'], text="Start Heart rate Monitoring", command=start)
content['stop'] = tk.Button(content['buttons_frame'], text="Stop Heart rate Monitoring", command=stop)
content['test_shocker'] = tk.Button(content['buttons_frame'], text="Test Shocker", command=test_shocker)
content['test_intensity'] = LabeledSpin(content['buttons_frame'], 'Test intensity', 1)
content['test_intensity'].set_range(1,20)
content['test_vibrate'] = tk.Button(content['buttons_frame'], text="Test Vibrate", command=test.send_vibrate)
content['test_beep'] = tk.Button(content['buttons_frame'], text="Test Beep", command=test.send_beep)
content['luck_mode'] = tk.Button(content['buttons_frame'], text="Toggle Gamble Mode", command=lucky_mode)
content['luck_mode_value'] = tk.Label(content['buttons_frame'], text="Gamble Mode is OFF")
content['lucky'] = tk.Button(content['buttons_frame'], text="I'm Feelin Lucky", command=randomly_shock)


content['start'].pack()
content['stop'].pack()
content['test_shocker'].pack()
content['test_vibrate'].pack()
content['test_beep'].pack()
content['test_intensity'].pack()
content['luck_mode'].pack()
content['luck_mode_value'].pack()
content['lucky'].pack()

content['low_spike'].pack()
content['high_spike'].pack()
content['low_shock'].pack()
content['high_shock'].pack()
content['shock_duration'].pack()
content['shock_duration'].pack()
content['window_size'].pack()
content['block_duration'].pack()
content['submit_settings'] = tk.Button(content['settings_frame'], text='Submit Settings', command=save_settings)
content['submit_settings'].pack()
content['settings_frame'].pack(side='left')
content['buttons_frame'].pack(side='left')
content['controls_frame'].pack(side='top')



main_window.pack()

root.after(5000, tracker_loop)
root.mainloop()