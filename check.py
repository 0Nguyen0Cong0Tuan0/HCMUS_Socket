import os
import csv
import re
import base64
import socket

HEADER = 1024
USERNAME = "nguyencongtuan0810@gmail.com"
PASSWORD = "1234567"
SERVER = '127.0.0.1'
PORT = 3335
SAVE_FOLDER = "saved_emails"
BOUNDARY ="--------------"
NOTICE = "This is a multi-part message in MIME format."
NOTICE_1 = "Content-Type: multipart/mixed;"
FOLDER_LIST = ["Inbox", "Project", "Important", "Work", "Spam"]
SUBJECT = ["urgent", "asap", "important", "action required", "critical", "priority", "attention", "dealine", "approval required", "emergency", "important information", "right now"]
SPAM = ['virus', 'hack', 'crack', 'security alert', 'suspicious activity', 
        'unauthorized access', 'account compromise', 'fraud warning', 'phishing attempt',
        'please confirm your identity', 'click here to reset your password', 'verify your account',
        'unusual login activity', 'your account will be suspended', 'bank account verification',
        'important security upadate', 'win a prize', 'win a lottery']

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

def get_sender(response):
    lines = response.splitlines()[1:]
    for line in lines:
        if line.strip().startswith('From: '):
            start_index = line.find('<') + 1
            end_index = line.find('>', start_index)
            sender = line[start_index:end_index].strip()
            break
    return sender

def get_email_content(response):
    start_marker = "Content-Transfer-Encoding: 7bit"
    boundary = "--------------5sWLTDpPOowcnjH7yr7J87Aq"
    dot = "."

    start_index = response.find(start_marker)
    end_index_boundary = response.find(boundary, start_index)
    end_index_dot = response.find(dot, start_index)

    if start_index != -1 and end_index_boundary != -1:
        return response[start_index + len(start_marker):end_index_boundary].strip()
    elif start_index != -1 and end_index_dot != -1:
        return response[start_index + len(start_marker):end_index_dot].strip()

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

def create_filter_folder():
    for folder in FOLDER_LIST:
        file_path = os.path.join(SAVE_FOLDER, folder)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

def create_mails_status(sender, email_id):
    element = [sender, email_id, "unread"]

    file_path = os.path.join(SAVE_FOLDER, 'students.csv')

    if os.path.exists(file_path):
        with open(file_path, "r") as read_file:
            reader = csv.reader(read_file)
            for row in reader:
                if row[:2] == [sender, email_id]:
                    break
            else:
                with open(file_path, "a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(element)
    else:
        with open(file_path, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(element)

def download_email_pop3(server_socket, num_id, email_id, SAVE_FOLDER):
    server_socket.send(f"RETR {num_id}\r\n".encode())
    response = receive_all(server_socket).decode()

    sender = get_sender(response)

    email_filename = os.path.join(SAVE_FOLDER, f"{sender}, {email_id}.msg")
    with open(email_filename, 'wb') as email_file:
        email_file.write(response.encode())
        create_mails_status(sender, email_id)

def take_email(choice):
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

        server_socket.send(f"RETR {choice}\r\n".encode())
        response = receive_all(server_socket).decode()

        mail_content = get_email_content(response)

        return response, mail_content

def show_download_mail():
    email_list = []
    csv_path = os.path.join(SAVE_FOLDER, "students.csv")

    if os.path.exists(csv_path):
        with open(csv_path) as file:
            for line in file:
                sender, mes_id, status = line.strip().split(',')
                email = {"sender": sender, "mes_id": mes_id, "status": status}
                email_list.append(email)

    return email_list


def main():
    download_emails_pop3()
    email_list = show_download_mail()
    create_filter_folder()

    while True:
        for index, mail in enumerate(email_list, start=1):
            print(f'{index} ({mail["status"]}) <{mail["sender"]}> {mail["mes_id"]}')
        
        choice = input("Choose the email you wanna read: ")
        response, content = take_email(choice)
        print(f"Content: {content}")
        
        email_list[int(choice)-1]['status'] = "read"

        if NOTICE in response:
            ans = input(f"The {email_list[int(choice)-1]['mes_id']} has attached files. Do you want to download it? ")
            if ans.lower() == 'y':
                save_attachments(response, email_list[int(choice)-1]['mes_id'])

        choice1 = input("Do you wanna continue (y/n): ")
        while choice1 not in ['y', 'n']:
            print("Invalid Value!!! Try again")
            choice1 = input("Do you wanna continue (y/n): ")

        if choice1 == 'y':
            continue
        elif choice1 == 'n':
            break
    
    csv_path = os.path.join(SAVE_FOLDER, "students.csv")
    if os.path.exists(csv_path):
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for element in email_list:
                content = [element['sender'],element['mes_id'],element['status']]
                writer.writerow(content)

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

