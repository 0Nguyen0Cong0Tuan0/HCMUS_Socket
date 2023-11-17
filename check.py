import os
import re
import base64
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

def get_email_ids(response):
    lines = response.splitlines()[1:-1] 
    num_ids = [line.split()[0] for line in lines]
    email_ids = [line.split()[1] for line in lines]
    return num_ids, email_ids

def get_email_info(response):
    pass

def get_sender(response):
    lines = response.splitlines()[1:]
    for line in lines:
        if line.strip().startswith('From: '):
            start_index = line.find('<') + 1
            end_index = line.find('>', start_index)
            sender = line[start_index:end_index].strip()
            break
    return sender

def save_attachments(response, email_id):
    mail_folder = os.path.join(SAVE_FOLDER, f"{email_id} attachment")
    os.makedirs(mail_folder, exist_ok=True)

    attachment_pattern = re.compile(r'Content-Disposition:.*?attachment; filename="(.*?)"', re.DOTALL)
    attachments = re.finditer(attachment_pattern, response)

    for match in attachments:
        attachment_filename = match.group(1)
        attachment_path = os.path.join(mail_folder, f"{attachment_filename}")

        attachment_start = response.find('\r\n\r\n', match.end()) + 4
        attachment_end = response.find('\r\n\r\n', attachment_start)

        with open(attachment_path, 'wb') as attachment_file:
            attachment_data = response[attachment_start:attachment_end]
            encoded_data = base64.b64decode(attachment_data)
            attachment_file.write(encoded_data)


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

        nums_ids, emails_ids = get_email_ids(uidl_response)
        for num_id, email_id in zip(nums_ids, emails_ids):
            download_email_pop3(server_socket, num_id, email_id, SAVE_FOLDER)
    
def download_email_pop3(server_socket, num_id, email_id, SAVE_FOLDER):
    server_socket.send(f"RETR {num_id}\r\n".encode())
    response = receive_all(server_socket).decode()
    
    sender = get_sender(response)

    if NOTICE in response:
        ans = input("The email has the attach files. Do you want to download it? ")
        if ans.lower() == 'y':
            save_attachments(response, email_id)

    email_filename = os.path.join(SAVE_FOLDER, f"file_{sender}, {email_id}.msg")
    with open(email_filename, 'wb') as email_file:
        email_file.write(response.encode())
    


def main():
    download_emails_pop3()
    
if __name__ == "__main__":
    main()


































































# files = os.listdir(SAVE_FOLDER)[1:]

# new_name = []
# for index, file in enumerate(files, start=1):
#     if file.endswith('msg'):
#         new_name.append(f"{index} {file}")


# while True:
#     for name in new_name:
#         print(name)
    
#     while True:
#         choice = int(input("\nChoose file to read: "))
#         if choice > index:
#             print('Invalid choice! Try again!')
#         else:
#             break
#     break

