import socket
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import time
import threading
import psutil
import json
import cv2
import numpy as np

HEADER = 64

window_width = 500
window_height = 500
window_size = str(window_width) + "x" + str(window_height)
FORMAT = "utf-8"
global_font = ("Arial", 16)

back_ground_color = "light gray"


class ClientApplication:
    # Constructor
    def __init__(self, root):
        # Create a GUI window
        self.root = root
        # Set color for background of the GUI window
        self.root.configure(bg=back_ground_color)
        self.client = None
        self.HEADER = 64
        self.is_connected = False
        self.is_capturing = False
        self.is_logging = False
        self.display_thread = None
        self.capture_event = threading.Event()
        root.title("Client Application")
        self.root.geometry("500x500")
        self.create_widgets()
        self.root.mainloop()
        # Move the attribute initializations here

    # Create a function to create all the widgets
    def create_widgets(self):
        # Create a Label
        self.label = tk.Label(
            self.root,
            text="Remote Desktop Software",
            font=("Arial Bold", 20),
            bg=back_ground_color,
        )
        self.label.pack(pady=30)

        # Create label with text "Enter IP Address"
        self.ip_label = tk.Label(
            self.root, text="Enter IP Address", font=global_font, bg=back_ground_color
        )
        self.ip_label.place(x=10, y=80)

        # Create a entry that will accept the IP address
        self.ip_entry = tk.Entry(self.root, width=20, font=global_font)
        self.ip_entry.place(x=180, y=80)

        # Create a button that will connect to the server at the right of the entry
        connect_button = tk.Button(
            self.root,
            text="Connect",
            font=global_font,
            command=lambda: self.connect_server(),
            bg="lime",
        )
        connect_button.place(x=380, y=75)
        # Disable the button if the client is already connected to the server
        if self.is_connected:
            connect_button.config(state=tk.DISABLED)

        button_width = 15
        button_height = 2
        x1 = 50
        xDis = 200
        x2 = x1 + xDis
        y1 = 150
        yDis = 80
        y2 = y1 + yDis
        y3 = y2 + yDis

        app_button = tk.Button(
            text="Application",
            font=global_font,
            height=button_height,
            width=button_width,
            command=lambda: self.open_application_window(),
        )
        app_button.place(x=x1, y=y1)

        process_button = tk.Button(
            text="Process",
            font=global_font,
            height=button_height,
            width=button_width,
            command=lambda: self.open_process_window(),
        )
        process_button.place(x=x2, y=y1)

        screen_capture_button = tk.Button(
            text="Screen Capture",
            font=global_font,
            height=button_height,
            width=button_width,
            command=lambda: self.request_capture_screenshot(),
        )
        screen_capture_button.place(x=x1, y=y2)

        keystroke_button = tk.Button(
            text="Keystroke",
            font=global_font,
            height=button_height,
            width=button_width,
            command=lambda: self.open_key_logger_window(),
        )
        keystroke_button.place(x=x2, y=y2)

        # Create a button that will disconnect from the server
        disconnect_button = tk.Button(
            self.root,
            text="Disconnect",
            font=global_font,
            height=button_height,
            width=button_width,
            command=lambda: self.disconnect_server(),
        )
        disconnect_button.place(x=x1, y=y3)

        # Create a button that shuts down the server
        shutdown_button = tk.Button(
            self.root,
            text="Shutdown",
            font=global_font,
            height=button_height,
            width=button_width,
            command=lambda: self.request_shutdown_server(),
        )
        shutdown_button.place(x=x2, y=y3)

        # Create a button that exits the program
        exit_button = tk.Button(
            self.root,
            text="Exit",
            font=global_font,
            bg="red",
            command=lambda: self.root.destroy(),
        )
        exit_button.place(x=430, y=430)

        # Disable the button if the client is not connected to the server

    def send_message(self, message):
        try:
            message_length = len(message)
            header = str(message_length).ljust(64).encode("utf-8")
            self.client.send(header)
            time.sleep(0.1)
            self.client.send(message.encode("utf-8"))
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to send message: {str(e)}")

    # Create a function that connects to the server
    def connect_server(self):
        if self.client:
            tk.messagebox.showerror(
                "Connection Status", "You are already connected to the server!"
            )
            return
        # Get the IP address from the entry
        ip_address = self.ip_entry.get()
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to the server
            self.client.connect((ip_address, 54321))

            # Send a message to the server
            self.send_message("!CONNECT")

            tk.messagebox.showinfo(
                "Connection Status", "Connected to the server successfully!"
            )
            self.is_connected = True
        except Exception as e:
            tk.messagebox.showerror(
                "Connection Status", "Failed to connect to the server!"
            )
            # Close the connection
            if self.client:
                self.client.close()
            print(e)

    # Create a function that disconnects from the server
    def disconnect_server(self):
        if self.client:
            # Send a message to the server
            self.send_message("!DISCONNECT")

            # Close the connection
            self.client.close()
            self.client = None
            self.is_connected = False
            tk.messagebox.showinfo(
                "Disconnection Status", "Disconnected from the server."
            )
        else:
            tk.messagebox.showerror(
                "Disconnection Status", "You are not connected to the server!"
            )

    # Function to open the process window
    def open_process_window(self):
        try:
            if self.is_connected == False:
                tk.messagebox.showerror(
                    "Connection Status", "You are not connected to the server!"
                )
                return
            process_window = tk.Toplevel(self.root)
            process_window.title("Process Management")
            process_window.geometry("500x500")
            process_window.configure(bg=back_ground_color)

            # Vùng hiển thị danh sách tiến trình
            process_scrolledtext = ScrolledText(process_window, wrap=tk.WORD)
            process_scrolledtext.place(x=10, y=100, width=480, height=350)
            process_window.children["scrolledtext"] = process_scrolledtext
            # Tạo các nút điều khiển
            list_button = tk.Button(
                process_window,
                text="Print List",
                command=lambda: self.request_process_list(process_window),
            )
            add_button = tk.Button(
                process_window,
                text="Start Process",
                command=self.request_start_process,
            )
            remove_button = tk.Button(
                process_window,
                text="Close Process",
                command=self.request_stop_process,
            )
            exit_button = tk.Button(
                process_window, text="Exit", command=process_window.destroy, bg="red"
            )
            clear_button = tk.Button(
                process_window,
                text="Clear",
                command=lambda: process_scrolledtext.delete("1.0", tk.END),
            )
            button_width = 80
            button_height = 50
            x1 = 10
            xDis = 100
            x2 = x1 + xDis
            x3 = x2 + xDis
            x4 = x3 + xDis
            x5 = x4 + xDis
            y = 40

            list_button.place(x=x1, y=y, width=button_width, height=button_height)
            add_button.place(x=x2, y=y, width=button_width, height=button_height)
            remove_button.place(x=x3, y=y, width=button_width, height=button_height)
            clear_button.place(x=x4, y=y, width=button_width, height=button_height)
            exit_button.place(x=x5, y=y, width=button_width, height=button_height)

            process_window.mainloop()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to open process window: {str(e)}")

    # Function to open the application window
    def open_application_window(self):
        try:
            if self.is_connected == False:
                tk.messagebox.showerror(
                    "Connection Status", "You are not connected to the server!"
                )
                return
            app_window = tk.Toplevel(self.root)
            app_window.title("Application Management")
            app_window.geometry("500x500")
            app_window.configure(bg=back_ground_color)

            # Vùng hiển thị danh sách tiến trình
            app_scrolledtext = ScrolledText(app_window, wrap=tk.WORD)
            app_scrolledtext.place(x=10, y=100, width=480, height=350)
            app_window.children["scrolledtext"] = app_scrolledtext

            # Tạo các nút điều khiển
            list_button = tk.Button(
                app_window,
                text="Print List",
                command=lambda: self.request_app_list(app_window),
            )
            add_button = tk.Button(
                app_window,
                text="Start App",
                command=self.request_start_app,
            )
            remove_button = tk.Button(
                app_window,
                text="Close App",
                command=self.request_stop_app,
            )
            exit_button = tk.Button(
                app_window, text="Exit", command=app_window.destroy, bg="red"
            )
            clear_button = tk.Button(
                app_window,
                text="Clear",
                command=lambda: app_scrolledtext.delete("1.0", tk.END),
            )
            button_width = 80
            button_height = 50
            x1 = 10
            xDis = 100
            x2 = x1 + xDis
            x3 = x2 + xDis
            x4 = x3 + xDis
            x5 = x4 + xDis
            y = 40

            list_button.place(x=x1, y=y, width=button_width, height=button_height)
            add_button.place(x=x2, y=y, width=button_width, height=button_height)
            remove_button.place(x=x3, y=y, width=button_width, height=button_height)
            clear_button.place(x=x4, y=y, width=button_width, height=button_height)
            exit_button.place(x=x5, y=y, width=button_width, height=button_height)

            app_window.mainloop()
        except Exception as e:
            tk.messagebox.showerror(
                "Error", f"Failed to open application window: {str(e)}"
            )

    # Function to open the key logger window
    def open_key_logger_window(self):
        try:
            if self.is_connected == False:
                tk.messagebox.showerror(
                    "Connection Status", "You are not connected to the server!"
                )
                return
            key_logger_window = tk.Toplevel(self.root)
            key_logger_window.configure(bg=back_ground_color)
            key_logger_window.title("Key Logger")
            key_logger_window.geometry("500x500")

            # Key logger status
            key_logger_scrolledtext = ScrolledText(key_logger_window, wrap=tk.WORD)
            key_logger_scrolledtext.place(x=10, y=100, width=480, height=350)
            key_logger_window.children["scrolledtext"] = key_logger_scrolledtext

            # Tạo các nút điều khiển
            print_button = tk.Button(
                key_logger_window,
                text="Print",
                command=lambda: self.request_print_key_logger(key_logger_window),
            )
            hook_button = tk.Button(
                key_logger_window,
                text="Hook",
                command=lambda: self.request_start_key_logger(key_logger_window),
            )
            unhook_button = tk.Button(
                key_logger_window,
                text="Unhook",
                command=lambda: self.request_stop_key_logger(key_logger_window),
            )
            exit_button = tk.Button(
                key_logger_window,
                text="Exit",
                command=key_logger_window.destroy,
                bg="red",
            )
            clear_button = tk.Button(
                key_logger_window,
                text="Clear",
                command=lambda: key_logger_scrolledtext.delete("1.0", tk.END),
            )
            button_width = 80
            button_height = 50
            x1 = 10
            xDis = 100
            x2 = x1 + xDis
            x3 = x2 + xDis
            x4 = x3 + xDis
            x5 = x4 + xDis
            y = 40

            print_button.place(x=x1, y=y, width=button_width, height=button_height)
            hook_button.place(x=x2, y=y, width=button_width, height=button_height)
            unhook_button.place(x=x3, y=y, width=button_width, height=button_height)
            clear_button.place(x=x4, y=y, width=button_width, height=button_height)
            exit_button.place(x=x5, y=y, width=button_width, height=button_height)

            key_logger_window.mainloop()
        except Exception as e:
            tk.messagebox.showerror(
                "Error", f"Failed to open key logger window: {str(e)}"
            )

    # Function to display the process list
    def display_process_list(self, process_window, process_json):
        try:
            process_list = json.loads(process_json)
            process_listbox = process_window.children["scrolledtext"]

            # Delete the current content of the listbox
            process_listbox.delete("1.0", tk.END)

            # Print number of process
            n = len(process_list)
            process_listbox.insert(tk.END, f"Number of processes: {n}\n")

            # Display the header
            header = f"{'Name':<50}{'PID':<10}\n"
            process_listbox.insert(tk.END, header)
            process_listbox.insert(tk.END, "=" * 60 + "\n")

            # Sort the list by name
            process_list.sort(key=lambda x: x["name"])

            # Display the process list
            for process in process_list:
                process_info = f"{process['name']:<50}{process['pid']:<10}\n"
                process_listbox.insert(tk.END, process_info)
        except Exception as e:
            tk.messagebox.showerror(
                "Error", f"Failed to display process list: {str(e)}"
            )

    # Function to request the process list from the server
    def request_process_list(self, process_window):
        try:
            # Gửi yêu cầu lấy danh sách tiến trình từ server
            self.send_message("!GET_PROCESS_LIST")

            # Nhận danh sách tiến trình dưới dạng JSON
            process_list_length = int(self.client.recv(HEADER).decode(FORMAT))
            process_list_json = self.client.recv(process_list_length).decode(FORMAT)

            # Hiển thị danh sách tiến trình
            self.display_process_list(process_window, process_list_json)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to get process list: {str(e)}")

    # Template function to open a request window
    def open_request_window(self, title_text, label_text, button_text, command_text):
        window = tk.Tk()
        window.configure(bg=back_ground_color)
        window.title(title_text)
        window.geometry("300x100")

        label = tk.Label(
            window, text=label_text, font=global_font, bg=back_ground_color
        )
        label.place(x=10, y=10)

        entry = tk.Entry(window, width=20, font=global_font)
        entry.place(x=10, y=50)

        button = tk.Button(
            window,
            text=button_text,
            font=global_font,
            command=lambda: self.send_message(command_text + " " + entry.get()),
        )
        button.place(x=210, y=45)
        window.mainloop()

    # Function to start a process
    def request_start_process(self):
        self.open_request_window(
            "Start Process", "Enter process name", "Start", "!START_PROCESS"
        )

    # Function to stop a process
    def request_stop_process(self):
        self.open_request_window(
            "Stop Process", "Enter process name", "Stop", "!STOP_PROCESS"
        )

    # Function to request the application list from the server
    def request_app_list(self, app_window):
        try:
            self.send_message("!GET_APP_LIST")

            app_list_length = int(self.client.recv(HEADER).decode(FORMAT))
            app_list_json = self.client.recv(app_list_length).decode(FORMAT)

            self.display_app_list(app_window, app_list_json)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to get app list: {str(e)}")

    # Function to display the application list
    def display_app_list(self, app_window, app_list_json):
        app_list = json.loads(app_list_json)
        app_listbox = app_window.children["scrolledtext"]

        # Delete the current content of the listbox
        app_listbox.delete("1.0", tk.END)

        # Print number of app
        n = len(app_list)
        app_listbox.insert(tk.END, f"Number of apps: {n}\n")

        # Sort the list by name
        app_list.sort(key=lambda x: x["name"])

        # Display the header
        header = f"{'Name':<50}{'Path':<10}\n"
        app_listbox.insert(tk.END, header)
        app_listbox.insert(tk.END, "=" * 60 + "\n")

        # Display the app list
        for app in app_list:
            app_info = f"{app['name']:<50}{app['status']:<10}\n"
            app_listbox.insert(tk.END, app_info)

    # Function to start an application
    def request_start_app(self):
        self.open_request_window("Start App", "Enter app name", "Start", "!START_APP")

    # Function to stop an application
    def request_stop_app(self):
        self.open_request_window("Stop App", "Enter app name", "Stop", "!STOP_APP")

    # Function to start the key logger
    def request_start_key_logger(self, key_logger_window):
        try:
            if self.is_logging:
                tk.messagebox.showerror(
                    "Error", "Key logger is already running! Please stop it first."
                )
                return
            self.is_logging = True
            self.send_message("!START_KEY_LOGGER")
            key_logger_window.children["scrolledtext"].insert(
                tk.END, "Key logger started\n"
            )
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to start key logger: {str(e)}")

    # Function to stop the key logger
    def request_stop_key_logger(self, key_logger_window):
        try:
            if not self.is_logging:
                tk.messagebox.showerror(
                    "Error", "Key logger is not running! Please start it first."
                )
                return
            self.is_logging = False
            self.send_message("!STOP_KEY_LOGGER")
            key_logger_window.children["scrolledtext"].insert(
                tk.END, "Key logger stopped\n"
            )
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to stop key logger: {str(e)}")

    # Function to print the key logger
    def request_print_key_logger(self, key_logger_window):
        try:
            if self.is_logging:
                tk.messagebox.showerror(
                    "Error", "Please stop the key logger before printing!"
                )
                return
            self.send_message("!GET_LOGGED_DATA")
            key_logger_length = int(self.client.recv(HEADER).decode(FORMAT))
            key_logger = self.client.recv(key_logger_length).decode(FORMAT)
            key_logger_window.children["scrolledtext"].insert(tk.END, key_logger)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to print key logger: {str(e)}")

    # Function to shutdown the server
    def request_shutdown_server(self):
        try:
            if not self.is_connected:
                tk.messagebox.showerror("Error", "You are not connected to the server!")
                return
            self.send_message("!SHUTDOWN")
            self.disconnect_server()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to shutdown server: {str(e)}")

    # Function to capture a screenshot
    def request_capture_screenshot(self):
        try:
            if not self.is_connected:
                tk.messagebox.showerror("Error", "You are not connected to the server!")
                return
            self.send_message("!GET_SCREENSHOT")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to capture screenshot: {str(e)}")
        if self.is_capturing:
            tk.messagebox.showerror(
                "Error", "Please stop capturing before capturing a screenshot!"
            )
            return

        # Receive the screenshot and save it to local disk
        try:
            image_length = int.from_bytes(self.client.recv(4), byteorder="big")
            image_data = self.client.recv(image_length)

            # Decode the image then save it to local disk
            img_decode = cv2.imdecode(
                np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR
            )
            img_decode = cv2.cvtColor(img_decode, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(img_decode)

            # Ask the user to choose a location to save the screenshot
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")],
            )

            if file_path:
                image.save(file_path)  # Save the image to the chosen location
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save screenshot: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApplication(root)
