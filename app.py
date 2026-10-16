import tkinter as tk
import configurer
import time

main_bg = '#RRGGBB'
card_bg = '#RRGGBB'
highlighted_bg = '#RRGGBB'


def create_entry(parent, name) -> tk.Frame:
    _frame = tk.Frame(parent)
    _label = tk.Label(_frame, text=name)
    _entry = tk.Entry(_frame)
    _label.pack(anchor='nw')
    _entry.pack(anchor='w')
    return _frame


test = configurer.Configlayer()
test.configure_hr_connection('')
test.configure_shocker_connection('', '', '')
test.setup()
while True:
    test.update()
    time.sleep(0.5)