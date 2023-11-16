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
    return num_ids

def extract_email_info(response):
    lines = response.splitlines()[1:]

    second_boundary = False
    meet_notice = False
    email_info = ''
    subject = ''
    sender = ''

    for line in lines:
        if line.strip().startswith((NOTICE, NOTICE_1)):
            meet_notice = True
            continue
        if line.strip().startswith(BOUNDARY) and not second_boundary:
            second_boundary = True
            continue
        if line.strip().startswith(BOUNDARY) and (second_boundary or line.strip().startswith('.')):
            break
        if line.strip().startswith('.'):
            break
        if line.strip().startswith('From: '):
            start_index = line.find('<') + 1
            end_index = line.find('>', start_index)
            sender += line[start_index:end_index].strip()
        if line.strip().startswith('Subject: ') and meet_notice:
            email_info += line
            subject = line.strip()[9:]
        elif line.strip().startswith('Subject: '):
            email_info += line + '\n'
            subject = line.strip()[9:]
        else:
            email_info += line + '\n'

    return email_info, sender, subject

# def save_status_of_mail(sender, subject, type):
#     email_filename = os.path.join(f"{sender}, {subject}.msg")

#     existing_status = set()
    
#     STATUS_FILE = os.path.join(SAVE_FOLDER, 'status_file.txt')
    
#     if os.path.exists(STATUS_FILE):
#         with open(STATUS_FILE, 'r') as status_file:
#             existing_status = set(status_file.read().splitlines())

#     if type == 1:
#         if email_filename not in existing_status:
#             email_status = "unread"
#             with open(STATUS_FILE, 'a') as status_file:
#                 status_file.write(f"file_{email_filename}, {email_status}\n")
#         elif not os.path.exists(STATUS_FILE):
#             with open(STATUS_FILE, 'w') as status_file:
#                 status_file.write(f"file_{email_filename}, {email_status}\n")
#     else:
#         if email_filename not in existing_status:
#             email_status = "unread"
#             with open(STATUS_FILE, 'a') as status_file:
#                 status_file.write(f"no_file_{email_filename}, {email_status}\n")
#         elif not os.path.exists(STATUS_FILE):
#             with open(STATUS_FILE, 'w') as status_file:
#                 status_file.write(f"no_file_{email_filename}, {email_status}\n")

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

        nums_ids = extract_email_ids(uidl_response)
        for num_id in nums_ids:
            download_content_email_pop3(server_socket, num_id, SAVE_FOLDER)
            download_email_pop3(server_socket, num_id, SAVE_FOLDER)

def download_content_email_pop3(server_socket, num_id, SAVE_FOLDER):
    server_socket.send(f"RETR {num_id}\r\n".encode())
    response = receive_all(server_socket).decode()

    email_info, sender, subject = extract_email_info(response)
    
    #save_status_of_mail(sender, subject, 0)

    email_filename = os.path.join(SAVE_FOLDER, f"no_file_{sender}, {subject}.msg")
    with open(email_filename, 'w') as email_file:
        email_file.write(email_info)
    
def download_email_pop3(server_socket, num_id, SAVE_FOLDER):
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
    
    #save_status_of_mail(sender, subject, 1)
    
    email_filename = os.path.join(SAVE_FOLDER, f"file_{sender}, {subject}.msg")
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

