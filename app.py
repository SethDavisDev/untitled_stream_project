import tkinter as tk
import configurer
import time

main_bg = '#RRGGBB'
card_bg = '#RRGGBB'
highlighted_bg = '#RRGGBB'

def explain_block(parent, _title, _paragraph):
    _frame = tk.Frame(parent)
    title = tk.Label(_frame, text=_title)
    paragraph = tk.Label(_frame, text=_paragraph)
    title.pack(anchor='nw')
    paragraph.pack(anchor='nw')
    return _frame

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

# root = tk.Tk()

# connections_frame = tk.Frame(root)
# connections_explain = explain_block(connections_frame, 'Connections', 'API credentials and service authentication.')
# connections_content = tk.Frame(connections_frame)

# auths_frame = tk.Frame(connections_content)
# pulsoid_auth = tk.Frame(auths_frame, bd=3, relief='raised')
# pulse_title_frame = tk.Frame(pulsoid_auth)
# pulsoid_title = tk.Label(pulse_title_frame, text='Pulsoid')
# pulse_entry_frame = tk.Frame(pulsoid_auth)
# token_entry = create_entry(pulse_entry_frame, 'Access Token')

# pulse_title_frame.pack(side='top', expand=True, fill='x')
# pulsoid_title.pack(side='left', anchor='nw')
# pulse_entry_frame.pack(side='top', expand=True, fill='x')
# token_entry.pack(side='left')

# pishock_auth = tk.Frame(auths_frame, bd=3, relief='raised')
# shock_title_frame = tk.Frame(pishock_auth)
# shock_entry_frame = tk.Frame(pishock_auth)
# pishock_title = tk.Label(shock_title_frame, text='PiShock')
# user = create_entry(shock_entry_frame, 'Username')
# api_key = create_entry(shock_entry_frame, 'API Key')
# share_code = create_entry(shock_entry_frame, 'Share Code')
# shock_title_frame.pack(side='top', expand=True, fill='x')
# pishock_title.pack(side='left', anchor='nw')
# shock_entry_frame.pack(side='top', expand=True, fill='x')
# user.pack(side='left')
# api_key.pack(side='left')
# share_code.pack(side='left')



# submit_frame = tk.Frame(connections_content)
# submit_button = tk.Button(submit_frame, text='Submit')


# pishock_auth.pack(side='left', padx=10)
# pulsoid_auth.pack(side='left', padx=10)
# auths_frame.pack()
# submit_button.pack(expand=True, fill='x', anchor='n')
# submit_frame.pack()
# connections_explain.pack(side='left')
# connections_content.pack(side='left')
# connections_frame.pack(fill='x')

# shocker_frame = tk.Frame(root)
# root.mainloop()