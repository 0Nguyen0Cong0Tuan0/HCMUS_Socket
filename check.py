import base64
import os
import socket

HEADER = 1024
USERNAME = "nctuan22@clc.fitus.edu.vn"
PASSWORD = "123456"
SERVER = '127.0.0.1'
PORT = 3335
SAVE_FOLDER = "saved_emails"
BOUNDARY ="--------------"
NOTICE = "This is a multi-part message in MIME format."
NOTICE_1 = "Content-Type: multipart/mixed;"

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
    num_ids = [line.split()[0] for line in lines]
    email_ids = [line.split()[1] for line in lines]
    return num_ids, email_ids

def extract_email_info(response):
    lines = response.splitlines()[1:]
    second_boundary = False
    meet_notice = False
    email_info = ''
    for line in lines:
        if line.strip().startswith((NOTICE, NOTICE_1)):
            meet_notice = True
            continue
        if line.strip().startswith(BOUNDARY) and not second_boundary:
            second_boundary = True
            continue
        if line.strip().startswith(BOUNDARY) and second_boundary or line.strip().startswith('.'):
            break

        if line.strip().startswith('Subject: ') and meet_notice:
            email_info += line
        else:
            email_info += line + '\n'
    
    return email_info

def download_emails_pop3():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    with socket.create_connection((SERVER, PORT)) as server_socket:
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('+OK Test Mail Server'):
            raise Exception(f"Error connecting to server: {response}")
        
        server_socket.send("CAPA\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('+OK\r\nUIDL'):
            raise Exception(f"Error: {response}")
        
        server_socket.send(f"USER {USERNAME}\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('+OK'):
            raise Exception(f"Error: {response}")

        server_socket.send(f"PASS {PASSWORD}\r\n".encode())
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

        nums_ids, email_ids = extract_email_ids(uidl_response)
        count = 0
        for email_id in email_ids:
            download_email_pop3(server_socket, email_id, nums_ids[count], SAVE_FOLDER)
            count += 1

def download_content_email_pop3(server_socket, email_id, num_id, SAVE_FOLDER):
    server_socket.send(f"RETR {num_id}\r\n".encode())
    response = receive_all(server_socket).decode()

    email_info = extract_email_info(response)

    email_filename = os.path.join(SAVE_FOLDER, f"no_file_{email_id}")
    with open(email_filename, 'w') as email_file:
        email_file.write(email_info)
    
def download_email_pop3(server_socket, email_id, num_id, SAVE_FOLDER):
    server_socket.send(f"RETR {num_id}\r\n".encode())
    response = receive_all(server_socket).decode()
    response = response.splitlines()[1:]

    lines = ''
    for line in response:
        lines += line + '\n'
    
    email_filename = os.path.join(SAVE_FOLDER, f"file_{email_id}")
    with open(email_filename, 'w') as email_file:
        email_file.write(lines)

download_emails_pop3()




