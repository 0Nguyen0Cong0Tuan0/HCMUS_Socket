from MailLib import *

class EmailGetter:
    @staticmethod
    def get_email_ids(response):
        lines = response.splitlines()[1:-1] 
        num_ids = [line.split()[0] for line in lines]
        email_ids = [line.split()[1] for line in lines]
        return num_ids, email_ids
    
    @staticmethod
    def get_sender(response):
        lines = response.splitlines()[1:]
        for line in lines:
            if line.strip().startswith('From: '):
                start_index = line.find('<') + 1
                end_index = line.find('>', start_index)
                sender = line[start_index:end_index].strip()
                break
        return sender
    
    @staticmethod
    def get_subject_email(response):
        lines = response.splitlines()[1:]
        for line in lines:
            if line.strip().startswith("Subject: "):
                subject = line[8:]
                break
        return subject

    @staticmethod
    def get_email_content(response):
        start_marker = "Content-Transfer-Encoding: 7bit"
        dot = "."

        start_index = response.find(start_marker)
        end_index_boundary = response.find(BOUNDARIES, start_index)
        end_index_dot = response.find(dot, start_index)

        if start_index != -1 and end_index_boundary != -1:
            return response[start_index + len(start_marker):end_index_boundary].strip()
        elif start_index != -1 and end_index_dot != -1:
            return response[start_index + len(start_marker):end_index_dot].strip()

    @staticmethod
    def take_email(files, choice, folder_path):
        response = b""
        path_file = os.path.join(folder_path, files[choice - 1])
        
        with open(path_file, 'rb') as file:
            response = file.read()
        
        return response, EmailGetter.get_email_content(response.decode(FORMAT))  

class EmailDownloader:
    @staticmethod
    def receive_all(socket):
        data = b""
        while not data.endswith(b"\r\n.\r\n"):
            data += socket.recv(HEADER)
        return data
        
    @staticmethod
    def download_email_pop3(server_socket, num_id, email_id):
        server_socket.send(f"RETR {num_id}\r\n".encode())
        response = EmailDownloader.receive_all(server_socket).decode()

        sender = EmailGetter.get_sender(response)
        filtered_email = EmailFilter.filter_email(response)

        email_folder = os.path.join(SAVE_FOLDER, filtered_email)
        email_path = os.path.join(email_folder, f"{sender}, {email_id}")
        with open(email_path, 'wb') as email_file:
            email_file.write(response.encode())
            EmailManager.create_mails_status(sender, email_id, filtered_email)
    
    @staticmethod
    def save_attachments(response, email_id, folder):
        mail_folder = os.path.join(SAVE_FOLDER, folder)
        mail_path = os.path.join(mail_folder, f"{email_id} attachment")
        os.makedirs(mail_path, exist_ok=True)

        attachment_pattern = re.compile(rb'Content-Disposition:.*?attachment; filename="(.*?)"', re.DOTALL)
        attachments = re.finditer(attachment_pattern, response)

        for match in attachments:
            attachment_filename = match.group(1).decode(FORMAT)
            attachment_path = os.path.join(mail_path, f"{attachment_filename}")

            attachment_start = response.find(b'\r\n\r\n', match.end()) + 4
            attachment_end = response.find(b'\r\n\r\n', attachment_start)
            
            with open(attachment_path, 'wb') as attachment_file:
                attachment_data = response[attachment_start:attachment_end]
                encoded_data = base64.b64decode(attachment_data)
                attachment_file.write(encoded_data)

    @staticmethod
    def notice_download_attachment(response):
        if NOTICE.encode() in response:
            while True:
                ans = input(f"The {mes_ID} has attached files. Do you want to download it? ")
                if ans.lower() == 'y' or ans.lower() == 'yes':
                    EmailDownloader.save_attachments(response, mes_ID, matching_emails[0]['folder'])
                    break
                elif ans.lower() == 'n' or ans.lower() == 'no':
                    break
                else:
                    print("Invalid Value!!! Try again")

    @staticmethod
    def download_emails_pop3():
        with socket.create_connection((SERVER, POP3_PORT)) as server_socket:
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

            nums_ids, emails_ids = EmailGetter.get_email_ids(uidl_response)
            for num_id, email_id in zip(nums_ids, emails_ids):
                EmailDownloader.download_email_pop3(server_socket, num_id, email_id)

class EmailFilter:
    @staticmethod
    def create_filter_folder():
        if not os.path.exists(SAVE_FOLDER):
            os.makedirs(SAVE_FOLDER)

        for folder in FOLDER_LIST:
            file_path = os.path.join(SAVE_FOLDER, folder)
            if not os.path.exists(file_path):
                os.makedirs(file_path)

    @staticmethod
    def filter_email(response):
        sender = EmailGetter.get_sender(response)
        subject = EmailGetter.get_subject_email(response)
        content = EmailGetter.get_email_content(response)

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

class EmailManager:
    @staticmethod
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

    @staticmethod
    def update_all_mail(email_list):
        csv_path = os.path.join(SAVE_FOLDER, "students.csv")
        if os.path.exists(csv_path):
            with open(csv_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for element in email_list:
                    content = [element['folder'], element['sender'], element['mes_id'], element['status']]
                    writer.writerow(content)

    @staticmethod
    def update_status_of_mail(files, choice_file, emails_list):
        global mes_ID, matching_emails
        mes_ID = files[choice_file - 1].split(', ')[1]
        matching_emails = [email for email in emails_list if email.get('mes_id') == mes_ID]
            
        if matching_emails:
            for matching_email in matching_emails:
                matching_email['status'] = "read"

class EmailCreator:
    @staticmethod
    def list_folder():
        sub_folders = [folder.name for folder in os.scandir(SAVE_FOLDER) if folder.is_dir()]
        return sub_folders

    @staticmethod
    def list_file(path):
        files = [file.name for file in os.scandir(path) if file.is_file()]
        return files

    @staticmethod
    def path_to_sub_folder(sub_folders, choice):
        path = os.path.join(SAVE_FOLDER, sub_folders[choice - 1])
        return path

class EmailShow:
    @staticmethod
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

    @staticmethod
    def show_list_folders(sub_folders):
        for index, sub_folder in enumerate(sub_folders, start=1):
            print(f"{index}_{sub_folder}")

    @staticmethod
    def show_list_files(files):
        for index, file in enumerate(files, start=1):
            print(f"{index}_{file}")

    @staticmethod
    def show_mail_content(content):
        print(f"Content: {content}")

class EmailSelector:
    @staticmethod
    def choose_folder():
        return int(input("Choose the folder number you want to read: "))

    @staticmethod
    def choose_file():
        return int(input("Choose the file number you want ot read: "))
    
    @staticmethod
    def ask_for_continuing():
        while True:
            choice = input("Do you wanna continue (y/n): ")
            if choice.lower() not in ['y', 'n']:
                print("Invalid Value!!! Try again")
            else:
                return choice

class EmailClient_Download:
    def run_download_mail_program(self):
        EmailFilter.create_filter_folder()
        EmailDownloader.download_emails_pop3()

        emails_list = EmailShow.show_download_mail()

        while True:
            sub_folders = EmailCreator.list_folder()
            EmailShow.show_list_folders(sub_folders)

            choice_folder = EmailSelector.choose_folder()
            folder_path = EmailCreator.path_to_sub_folder(sub_folders, choice_folder)
            
            files = EmailCreator.list_file(folder_path)
            EmailShow.show_list_files(files)

            choice_file = EmailSelector.choose_file()

            response, content = EmailGetter.take_email(files, choice_file, folder_path)
            EmailShow.show_mail_content(content)

            EmailManager.update_status_of_mail(files, choice_file, emails_list)

            EmailDownloader.notice_download_attachment(response)


            choice_continuing = EmailSelector.ask_for_continuing()
            if choice_continuing == 'y':
                continue
            elif choice_continuing == 'n':
                break
        
        EmailManager.update_all_mail(emails_list)




# for index, mail in enumerate(email_list, start=1):
#     print(f'{index} ({mail["status"]}) <{mail["sender"]}> {mail["mes_id"]} - {mail["folder"]}')