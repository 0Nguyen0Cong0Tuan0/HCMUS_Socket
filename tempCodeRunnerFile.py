from tkinter import *
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

# Create Frame
frame_menu = tb.Frame(root, bootstyle=f'{color}', width=900, height=500)
frame_menu.pack(pady=100, padx=50)

# Create Label
label_menu = tb.Label(frame_menu, text="MENU", bootstyle=f'inverse {color}',
                      font=(f'{font_interface}', 25, 'bold'))
label_menu.grid(row=0, column=1, columnspan=3, pady=10, padx=100)

# Create Send Email Button
get_send = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                     text='SEND EMAIL', padding=10, command=lambda: open_send_email_window(root))
get_send.grid(row=1, columnspan=3, pady=10, padx=50)

def open_send_email_window(parent):
    # You can implement the logic to open the send email window here
    # For example, you might create a new Toplevel window for sending emails
    send_email_window = Toplevel(parent)
    send_email_window.title("Send Email")
    send_email_window.geometry("600x400")
    # Add widgets and functionality for sending emails in this window

mainloop()