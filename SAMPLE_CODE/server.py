import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import socket
import threading
import time
import cv2
import numpy as np
import psutil
import json
import subprocess
from pynput import keyboard
import os
import pyautogui

FORMAT = "utf-8"
window_width = 700
window_height = 700
window_size = str(window_width) + "x" + str(window_height)


# Server application
class ServerApp:
    # Constructor
    def __init__(self, root):
        self.root = root
        self.root.title("Server Application")
        self.root.geometry(window_size)
        self.root.configure(bg="light gray")
        self.HEADER = 64
        button_width = 15
        button_height = 2
        x1 = 10
        xDis = 150
        x2 = x1 + button_width + xDis
        x3 = x2 + button_width + xDis
        x4 = x3 + button_width + xDis
        y = 20
        # Button that starts the server
        self.start_button = tk.Button(
            root,
            text="Open Server",
            width=button_width,
            height=button_height,
            command=self.start_server,
        )

        self.start_button.place(
            x=x1,
            y=y,
        )
        # Button that stops the server
        self.stop_button = tk.Button(
            root,
            text="Close Server",
            width=button_width,
            height=button_height,
            command=self.stop_server,
        )
        self.stop_button.place(x=x2, y=y)
        # Button that exits the application
        self.exit_button = tk.Button(
            root,
            text="Exit",
            width=button_width,
            height=button_height,
            command=self.root.destroy,
            bg="red",
        )
        self.exit_button.place(x=x4, y=y)

        # Textbox that displays the messages
        self.text_widget = ScrolledText(root, wrap=tk.WORD)
        self.text_widget.place(x=10, y=100, width=680, height=590)

        # Button that clears the textbox
        self.clear_button = tk.Button(
            root,
            text="Clear",
            width=button_width,
            height=button_height,
            command=lambda: self.text_widget.delete("1.0", tk.END),
        )
        self.clear_button.place(x=x3, y=y)

        self.is_running = False
        self.server_socket = None
        self.is_logging = False
        self.logged_data = ""
        self.listener = None
        self.shutdown_in_progress = False
        self.shutdown_cancelled = False
        self.is_capturing = False
        self.capture_thread = None
        self.capture_event = threading.Event()
        self.clients = []

    # Method that starts the server
    def start_server(self):
        if not self.is_running:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = socket.gethostbyname(socket.gethostname())
            server_port = 54321
            self.append_text(f"Starting server on {server_address}:{server_port}\n")

            self.server_socket.bind((server_address, server_port))
            self.server_socket.listen(5)
            self.append_text("Server started. Waiting for connections...\n")
            self.is_running = True
            threading.Thread(target=self.accept_clients).start()
            self.append_text(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")
        else:
            self.append_text("Server is already running\n")

    # Method that accepts clients
    def accept_clients(self):
        while self.is_running:  # Kiểm tra cờ trước khi accept
            try:
                client_socket, client_address = self.server_socket.accept()
                self.clients.append(client_socket)
                self.append_text(f"New connection from {client_address}\n")
                threading.Thread(
                    target=self.handle_client, args=(client_socket,)
                ).start()
                self.append_text(
                    f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n"
                )
            except OSError as e:
                if self.is_running:  # Chỉ xử lý lỗi nếu server vẫn đang chạy
                    self.append_text(f"Error accepting client: {str(e)}\n")
                    continue
                else:
                    break

    # Method that handles a client
    def handle_client(self, client_socket):
        try:
            while True:
                header = client_socket.recv(self.HEADER)
                if not header:
                    break
                message_length = int(header.decode("utf-8").strip())
                if not message_length:
                    break

                message = client_socket.recv(message_length).decode("utf-8")
                if not message:
                    break
                self.append_text(
                    f"Received data from {client_socket.getpeername()}: {message}\n"
                )
                if message == "!CONNECT" or message == "!DISCONNECT":
                    alreadyAppend = True
                if message == "!GET_PROCESS_LIST":
                    process_list = self.get_process_list()
                    json_data = json.dumps(process_list)
                    self.send_message(client_socket, json_data)
                elif message.startswith("!START_PROCESS "):
                    _, process_name = message.split(" ", 1)
                    self.start_process(process_name)
                elif message.startswith("!STOP_PROCESS "):
                    _, process_pid = message.split(" ", 1)
                    self.stop_process(int(process_pid))
                elif message == "!GET_APP_LIST":
                    app_list = self.get_app_list()
                    json_data = json.dumps(app_list)
                    self.send_message(client_socket, json_data)
                elif message.startswith("!START_APP "):
                    _, app_name = message.split(" ", 1)
                    self.start_app(app_name)
                elif message.startswith("!STOP_APP "):
                    _, app_name = message.split(" ", 1)
                    self.stop_app(app_name)
                elif message == "!START_KEY_LOGGER":
                    self.start_logging()
                elif message == "!STOP_KEY_LOGGER":
                    self.stop_logging()
                elif message == "!GET_LOGGED_DATA":
                    self.send_logged_data(client_socket)
                elif message == "!SHUTDOWN":
                    response = tk.messagebox.askyesno(
                        "Shutdown Confirmation",
                        "Do you really want to shut down the server?",
                    )
                    if response:
                        self.shutdown_server()
                elif message == "!START_CAPTURE":
                    self.start_capture(client_socket)
                elif message == "!STOP_CAPTURE":
                    self.stop_capture()
                elif message == "!GET_SCREENSHOT":
                    self.send_screenshot(client_socket)
                elif not alreadyAppend:
                    self.append_text(
                        f"Received data from {client_socket.getpeername()}: {message}\n"
                    )

                # Xử lý dữ liệu nhận được ở đây
                # Ví dụ: kiểm tra dữ liệu nhận được và thực hiện hành động tương ứng

        except Exception as e:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            self.append_text(
                f"Error handling client {client_socket.getpeername()}: {str(e)}\n"
            )
            tk.messagebox.showerror("Error", f"Failed to receive screenshot: {str(e)}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            self.append_text(f"Client {client_socket.getpeername()} disconnected\n")
            self.append_text(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}\n")
            client_socket.close()

    # Method that stops the server
    def stop_server(self):
        if self.server_socket:
            self.is_running = False
            self.server_socket.close()
            self.server_socket = None
            self.append_text("Server stopped.\n")

    # Method that appends text to the textbox
    def append_text(self, text):
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)

    # Method that sends a message to the client
    def send_message(self, client_socket, message):
        message_length = len(message)
        header = str(message_length).ljust(64).encode("utf-8")
        client_socket.send(header)
        time.sleep(0.1)
        client_socket.send(message.encode("utf-8"))

    # Method that gets the list of processes
    def get_process_list(self):
        process_list = []
        for proc in psutil.process_iter(["pid", "name"]):
            process_list.append({"pid": proc.info["pid"], "name": proc.info["name"]})
        return process_list

    # Method that starts a process
    def start_process(self, process_name):
        try:
            subprocess.Popen(process_name, shell=True)
            if app_name[0:5] == "start":
                app_name = app_name[6:]
            self.append_text(f"Started process: {process_name}\n")
            tk.messagebox.showinfo("Info", f"Started process: {process_name}")
        except Exception as e:
            self.append_text(f"Error starting process: {str(e)}\n")

    # Method that stops a process
    def stop_process(self, process_pid):
        try:
            p = psutil.Process(process_pid)
            p.terminate()
            p.wait()
            self.append_text(f"Terminated process: {process_pid}\n")
            tk.messagebox.showinfo("Info", f"Terminated process: {process_pid}")
        except Exception as e:
            self.append_text(f"Error terminating process: {str(e)}\n")

    # Method that gets the list of apps
    def get_app_list(self):
        app_list = []
        for process in psutil.process_iter(attrs=["name", "exe", "status"]):
            if process.info["exe"]:
                app_name = process.info["name"]
                app_status = process.info["status"]
                # Check if the app is already in the list
                is_exist = False
                for app in app_list:
                    if app["name"] == app_name:
                        is_exist = True
                        break
                if not is_exist:
                    app_list.append({"name": app_name, "status": app_status})
        return app_list

    # Method that starts an app
    def start_app(self, app_name):
        try:
            subprocess.Popen(app_name, shell=True)
            if app_name[0:5] == "start":
                app_name = app_name[6:]
            tk.messagebox.showinfo("Info", f"Started app: {app_name}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to start app: {str(e)}")

    # Method that stops an app
    def stop_app(self, app_name):
        try:
            is_exist = False
            app_name = app_name + ".exe"
            for process in psutil.process_iter(attrs=["pid", "name"]):
                if process.info["name"] == app_name:
                    try:
                        p = psutil.Process(process.info["pid"])
                        p.terminate()
                        is_exist = True
                        p.wait()
                    except psutil.NoSuchProcess:
                        pass
            if is_exist:
                tk.messagebox.showinfo("Info", f"Terminated app: {app_name}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to terminate app: {str(e)}")

    # Method that starts logging
    def start_logging(self):
        if not self.is_logging:
            self.is_logging = True
            self.listener = keyboard.Listener(on_press=self.on_press_key)
            self.listener.start()
            self.append_text("Started logging\n")
        else:
            self.append_text("Logging is already started\n")

    # Method that stops logging
    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            if self.listener:
                self.listener.stop()
                self.listener = None
            self.append_text("Stopped logging\n")
        else:
            self.append_text("Logging is already stopped\n")

    # Method that handles key press
    def on_press_key(self, key):
        try:
            self.logged_data += key.char
        except AttributeError:
            if key == keyboard.Key.space:
                self.logged_data += " "
            elif key == keyboard.Key.enter:
                self.logged_data += "\n"

    # Method that sends logged data to the client
    def send_logged_data(self, client_socket):
        self.send_message(client_socket, self.logged_data)
        self.append_text(f"Sent logged data to {client_socket.getpeername()}\n")
        self.logged_data = ""

    # Method that shuts down the server
    def shutdown_server(self):
        self.shutdown_in_progress = True
        self.root.withdraw()  # Ẩn cửa sổ chính

        countdown_window = tk.Toplevel(self.root)
        countdown_label = tk.Label(countdown_window, text="Shutdown in 30 seconds")
        countdown_label.pack()

        cancel_button = tk.Button(
            countdown_window,
            text="Cancel Shutdown",
            command=self.cancel_shutdown,
        )
        cancel_button.pack()

        self.countdown_thread = threading.Thread(
            target=self.perform_countdown, args=(countdown_label,)
        )
        self.countdown_thread.start()

    # Method that performs countdown
    def perform_countdown(self, label):
        for i in range(30, 0, -1):
            if self.shutdown_cancelled:
                break
            label.config(text=f"Shutdown in {i} seconds")
            time.sleep(1)

        if not self.shutdown_cancelled:
            self.perform_shutdown()

    # Method that cancels shutdown
    def cancel_shutdown(self):
        self.shutdown_cancelled = True
        self.root.deiconify()  # Hiện lại cửa sổ chính
        if self.countdown_thread:
            self.countdown_thread.join()

    # Method that performs shutdown
    def perform_shutdown(self):
        os.system("shutdown /s /t 1")

    # Method that sends a screenshot to the client
    def send_screenshot(self, client_socket):
        try:
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            screenshot = cv2.resize(screenshot, (640, 320))
            img_encode = cv2.imencode(".jpg", screenshot)[1]
            image_data = img_encode.tobytes()

            message_length = len(image_data)
            message_length_bytes = message_length.to_bytes(4, byteorder="big")
            client_socket.send(message_length_bytes + image_data)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to send screenshot: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
