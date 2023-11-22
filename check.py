import os
import csv
import re
import base64
import socket

HEADER = 1024
USERNAME = 'nguyencongtuan0810@gmail.com'
PASSWORD = '1234567'
SERVER = '127.0.0.1'
PORT = 3335
SAVE_FOLDER = 'saved_emails'
BOUNDARY = '--------------'
NOTICE = 'This is a multi-part message in MIME format.'
NOTICE_1 = 'Content-Type: multipart/mixed;'
FOLDER_LIST = ['Inbox', 'Project', 'Important', 'Work', 'Spam']
IMPORTANT = ['urgent', 'asap', 'important', 'action required', 'critical',
             'priority', 'attention', 'dealine', 'approval required', 'emergency', 
             'important information', 'right now']
SPAM = ['virus', 'hack', 'crack', 'security alert', 'suspicious activity', 
        'unauthorized access', 'account compromise', 'fraud warning', 'phishing attempt',
        'please confirm your identity', 'click here to reset your password', 'verify your account',
        'unusual login activity', 'your account will be suspended', 'bank account verification',
        'important security upadate', 'win a prize', 'win a lottery']
WORK = ['meeting', 'report', 'project update', 'task', 'collaboration', 'discussion', 'schedule', 
        'feedback', 'assignment']
PROJECT = ['nctuan081004@gmail.com']

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

def save_attachments(response, email_id, folder):
    mail_folder = os.path.join(folder, f"{email_id} attachment")
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
            download_email_pop3(server_socket, num_id, email_id)

def create_filter_folder():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    for folder in FOLDER_LIST:
        file_path = os.path.join(SAVE_FOLDER, folder)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

def create_mails_status(sender, email_id, filtered_email):
    element = [filtered_email, sender, email_id, "unread"]

    file_path = os.path.join(SAVE_FOLDER, 'students.csv')

    if os.path.exists(file_path):
        with open(file_path, "r") as read_file:
            reader = csv.reader(read_file)
            for row in reader:
                if row[:3] == [filtered_email, sender, email_id]:
                    break
            else:
                with open(file_path, "a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(element)
    else:
        with open(file_path, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(element)

def get_sender(response):
    lines = response.splitlines()[1:]
    for line in lines:
        if line.strip().startswith('From: '):
            start_index = line.find('<') + 1
            end_index = line.find('>', start_index)
            sender = line[start_index:end_index].strip()
            break
    return sender

def get_subject_email(response):
    lines = response.splitlines()[1:]
    for line in lines:
        if line.strip().startswith("Subject: "):
            subject = line[8:]
            break
    return subject

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

def filter_email(response):
    sender = get_sender(response)
    subject = get_subject_email(response)
    content = get_email_content(response)

    if any(word.lower() == sender.lower() for word in PROJECT):
        return FOLDER_LIST[1]
    elif any(word.lower() in subject.lower() for word in IMPORTANT):
        return FOLDER_LIST[2]
    elif any(word.lower() in content.lower() for word in WORK):
        return FOLDER_LIST[3]
    elif any(word.lower() in subject.lower() or word.lower() in content.lower() for word in SPAM):
        return FOLDER_LIST[4]
    else:
        return FOLDER_LIST[0]

def download_email_pop3(server_socket, num_id, email_id):
    server_socket.send(f"RETR {num_id}\r\n".encode())
    response = receive_all(server_socket).decode()

    sender = get_sender(response)
    filtered_email = filter_email(response)

    email_folder = os.path.join(SAVE_FOLDER, filtered_email)
    email_path = os.path.join(email_folder, f"{sender}, {email_id}.msg")
    with open(email_path, 'wb') as email_file:
        email_file.write(response.encode())
        create_mails_status(sender, email_id, filtered_email)

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
                folder, sender, mes_id, status = line.strip().split(',')
                email = {'folder': folder, 'sender': sender, 'mes_id': mes_id, 'status': status}
                email_list.append(email)

    return email_list

def update_status_of_mail(email_list):
    csv_path = os.path.join(SAVE_FOLDER, "students.csv")
    if os.path.exists(csv_path):
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for element in email_list:
                content = [element['folder'], element['sender'], element['mes_id'], element['status']]
                writer.writerow(content)

def list_folder():
    sub_folders = [folder.name for folder in os.scandir(SAVE_FOLDER) if folder.is_dir()]
    return sub_folders

def list_file(path):
    files = [file.name for file in os.scandir(path) if file.is_file()]
    return files

def path_to_sub_folder(sub_folders, choice):
    path = os.path.join(SAVE_FOLDER, sub_folders[choice - 1])
    return path

def main():
    # create_filter_folder()
    # download_emails_pop3()

    sub_folders = list_folder()
    email_list = show_download_mail()

    while True:
        # for index, mail in enumerate(email_list, start=1):
        #     print(f'{index} ({mail["status"]}) <{mail["sender"]}> {mail["mes_id"]} - {mail["folder"]}')
        
        for index, sub_folder in enumerate(sub_folders, start=1):
            print(f"{index}_{sub_folder}")

        choice_folder = int(input("Choose the folder number you want to read: "))


        folder_path = path_to_sub_folder(sub_folders, choice_folder)
        files = list_file(folder_path)

        for index, file in enumerate(files, start=1):
            print(f"{index}_{file}")
        
        choice_file = int(input("Choose the file number you want ot read: "))

        response, content = take_email(choice_file)
        print(f"Content: {content}")
        
        email_list[int(choice_file)-1]['status'] = "read"

        # if NOTICE in response:
        #     ans = input(f"The {email_list[int(choice)-1]['mes_id']} has attached files. Do you want to download it? ")
        #     if ans.lower() == 'y':
        #         save_attachments(response, email_list[int(choice)-1]['mes_id'], email_list[int(choice)-1]['folder'])

        # choice1 = input("Do you wanna continue (y/n): ")
        # while choice1 not in ['y', 'n']:
        #     print("Invalid Value!!! Try again")
        #     choice1 = input("Do you wanna continue (y/n): ")

        # if choice1 == 'y':
        #     continue
        # elif choice1 == 'n':
        #     break
        break
    
    update_status_of_mail(email_list)

if __name__ == "__main__":
    main()