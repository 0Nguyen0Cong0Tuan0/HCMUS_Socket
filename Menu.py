from InterfaceLib import *
from SendPage import SendTab
from ReceivePage import EmailView
from manageInfo import ManagerInfoUser
import threading
import time

#-----  MENU TAB
class MenuTab:
    def __init__(self, parent):
        self.stop_thread = False
        self.config = ManagerInfoUser.load_config()
        self.menu_interface = Toplevel(parent)
        self.menu_interface.title("Menu")
        self.menu_interface.geometry(window_size)

        self.menu()

        time_counter_thread = threading.Thread(target=self.run_time_counter_to_download)
        time_counter_thread.start()

    def menu(self):
        # Create Frame
        frame_menu = tb.Frame(self.menu_interface, bootstyle=f'{color}', width=900, height=500)
        frame_menu.pack(pady=100, padx=50)

        # Create Label
        label_menu = tb.Label(frame_menu, text="MENU", bootstyle=f'inverse {color}',
                            font=(f'{font_interface}', 25, 'bold'))
        label_menu.grid(row=0, column=1, columnspan=3, pady=10, padx=100)

        # Create Send Email Button
        get_send = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='SEND EMAIL', padding=10, command=lambda: SendTab(self.menu_interface))
        get_send.grid(row=1, columnspan=4, pady=10, padx=100)

        get_all_download = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='ALL RECEIVED MAIL', padding=10, command=EmailView.run_received_tab)
        get_all_download.grid(row=2, columnspan=4, pady=10, padx=100)

        get_download = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='DOWNLOAD MAIL', padding=10, command=EmailView.download_tab)
        get_download.grid(row=3, columnspan=4, pady=10, padx=100)

        get_exit = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='EXIT', padding=10, command=self.press_exit)
        get_exit.grid(row=4, columnspan=4, pady=10, padx=100)
    
    def press_exit(self):
        self.stop_thread = True
        self.menu_interface.destroy()
        ManagerInfoUser.reset_config()

    def run_time_counter_to_download(self):
        counter = 0
        while True:
            time.sleep(1)
            counter += 1
            if not self.stop_thread and counter % int(self.config['AUTOLOAD']) == 0:
                EmailView.download_tab()