import base64
import os
import socket

HEADER = 1024
username = "nctuan22@clc.fitus.edu.vn"
password = "123456"
server = '127.0.0.1'
port = 3335
save_folder = "saved_emails"

def receive_all(socket):
    data = b""
    while True:
        chunk = socket.recv(HEADER)
        if not chunk:
            break
        data += chunk
        if data.endswith(b"\r\n.\r\n"):
            break
    return data


def extract_email_ids(response):
    lines = response.splitlines()[1:-1] 
    email_ids = [line.split()[0] for line in lines]
    return email_ids

def download_emails_pop3():
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    with socket.create_connection((server, port)) as server_socket:
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('+OK Test Mail Server'):
            raise Exception(f"Error connecting to server: {response}")
        
        server_socket.send("CAPA\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('+OK\r\nUIDL'):
            raise Exception(f"Error: {response}")
        

        server_socket.send(f"USER {username}\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('+OK'):
            raise Exception(f"Error: {response}")

        server_socket.send(f"PASS {password}\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('+OK'):
            raise Exception(f"Error: {response}")

        server_socket.send("STAT\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('+OK'):
            raise Exception(f"Error: {response}")
        
        server_socket.send("LIST\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('+OK'):
            raise Exception(f"Error: {response}")

        server_socket.send("UIDL\r\n".encode())
        uidl_response = server_socket.recv(HEADER).decode()
        if not uidl_response.startswith('+OK'):
            raise Exception(f"Error: {uidl_response}")

        email_ids = extract_email_ids(uidl_response)
        print(email_ids)
        for email_id in email_ids:
            download_email_pop3(server_socket, email_id, save_folder)

def download_email_pop3(server_socket, email_id, save_folder):
    server_socket.send(f"RETR {email_id}\r\n".encode())
    response = receive_all(server_socket).decode()

    email_filename = os.path.join(save_folder, f"email_{email_id}.txt")
    with open(email_filename, 'w') as email_file:
        email_file.write(response)

download_emails_pop3()




