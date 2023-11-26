from MailLib import *
from tkinter import *
from ttkbootstrap.dialogs import Messagebox
import ttkbootstrap as tb

window_width = 1200
window_height = 700
window_size = str(window_width) + 'x' + str(window_height)
color = "primary"
font_interface = 'GOUDY STOUT'
font_type = 'Arial Greek'

root = tb.Window(themename="darkly")
root.title("MAIL APPLICATION")
root.geometry(window_size)

def create_connection_to_server(entry_info):
    try:
        with socket.create_connection((entry_info['SERVER'], int(entry_info['SMTP']))) as server_socket:
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('220'):
                Messagebox.show_error("Error connecting to server", f"Error: {response}")
            else:
                Messagebox.show_info("", "Connect Successfully!!")
    except ConnectionRefusedError:
        Messagebox.show_error("No connection could be made because the target machine actively refused it!", "Connection Error")
    except Exception as e:
        Messagebox.show_error(f"An unexpected error occurred: {e}", "Error")
    
    server_socket.send("QUIT".encode()) 

def get_info():
    entry_info = {'USERNAME': entry_username.get(), 'EMAIL': entry_email.get(),
                  'PASSWORD': entry_password.get(), 'SERVER': entry_server.get(),
                  'SMTP':entry_SMTP_PORT.get(), 'POP3': entry_POP3_PORT.get()}
    create_connection_to_server(entry_info)

# Create Frame
frame_login = tb.Frame(root, bootstyle=f'{color}', width=900, height=500)
frame_login.pack(pady=100, padx=50)

# Create Label
label_login = tb.Label(frame_login, text="LOGIN", bootstyle=f'inverse {color}',
                       font=(f'{font_interface}', 30, 'bold'))
label_login.grid(row=0, column=1, columnspan=3, pady=10)

labels = ["USERNAME", "EMAIL", "PASSWORD", "SERVER", "SMTP PORT", "POP3 PORT"]

for i, label_text in enumerate(labels, start=1):
    label = tb.Label(frame_login, text=label_text, bootstyle=f'inverse {color}',
                     font=(f'{font_interface}', 12))
    label.grid(row=i, column=0, padx=50, pady=10, sticky="w")

# Create Entry
entry_username = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50)
entry_username.grid(row=1, column=1, padx=50, pady=10)

entry_email = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50)
entry_email.grid(row=2, column=1, padx=50, pady=10)

entry_password = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50, show='*')
entry_password.grid(row=3, column=1, padx=50, pady=10)

entry_server = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50)
entry_server.grid(row=4, column=1, padx=50, pady=10)

entry_SMTP_PORT = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50)
entry_SMTP_PORT.grid(row=5, column=1, padx=50, pady=10)

entry_POP3_PORT = tb.Entry(frame_login, font=(f'{font_type}', 12), width=50)
entry_POP3_PORT.grid(row=6, column=1, padx=50, pady=10)

# Create Button
get_info_button = tb.Button(frame_login, bootstyle="light, outline, inverse", 
                            text='Submit', padding=10, command=get_info)
get_info_button.grid(row=8, columnspan=3, pady=10, padx=50)

mainloop()
