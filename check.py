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

        nums_ids, emails_ids = extract_email_ids(uidl_response)
        for num_id, email_id in zip(nums_ids, emails_ids):
            download_email_pop3(server_socket, num_id, email_id, SAVE_FOLDER)
    
def download_email_pop3(server_socket, num_id, email_id, SAVE_FOLDER):
    server_socket.send(f"RETR {num_id}\r\n".encode())
    response = receive_all(server_socket).decode()
    response = response.splitlines()[1:]

    lines = ''
    subject = ''
    sender = ''

    for line in response:
        if line.strip().startswith('Subject: '):
            subject += line.strip()[9:]
        if line.strip().startswith('From: '):
            start_index = line.find('<') + 1
            end_index = line.find('>', start_index)
            sender += line[start_index:end_index].strip()
        if line.strip().startswith('.'):
            continue
        lines += line + '\n'

    email_filename = os.path.join(SAVE_FOLDER, f"file_{sender}, {email_id}.msg")
    with open(email_filename, 'w') as email_file:
        email_file.write(lines)

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

