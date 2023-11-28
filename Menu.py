from InterfaceLib import *
from SendPage import SendTab
from ReceivePage import EmailView

#-----  MENU TAB
class MenuTab:
    # def __init__(self):
    #     self.root = tb.Window(themename="darkly")
    #     self.root.title("MAIL APPLICATION")
    #     self.root.geometry(window_size)
    @staticmethod
    def menu(parent):
        menu_interface = Toplevel(parent)
        menu_interface.title("Menu")
        menu_interface.geometry(window_size)
        # Create Frame
        frame_menu = tb.Frame(menu_interface, bootstyle=f'{color}', width=900, height=500)
        frame_menu.pack(pady=100, padx=50)

        # Create Label
        label_menu = tb.Label(frame_menu, text="MENU", bootstyle=f'inverse {color}',
                            font=(f'{font_interface}', 25, 'bold'))
        label_menu.grid(row=0, column=1, columnspan=3, pady=10, padx=100)

        # Create Send Email Button
        get_send = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='SEND EMAIL', padding=10, command=lambda: SendTab.open_send_email_window(menu_interface))
        get_send.grid(row=1, columnspan=4, pady=10, padx=100)

        get_all_download = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='ALL RECEIVED MAIL', padding=10, command=EmailView.run_received_tab)
        get_all_download.grid(row=2, columnspan=4, pady=10, padx=100)

        get_download = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='DOWNLOAD MAIL', padding=10, command=EmailView.download_tab)
        get_download.grid(row=3, columnspan=4, pady=10, padx=100)

        get_exit = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='EXIT', padding=10, command=menu_interface.destroy)
        get_exit.grid(row=4, columnspan=4, pady=10, padx=100)

