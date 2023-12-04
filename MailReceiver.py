from MailLib import *
from InterfaceLib import Messagebox
from manageInfo import ManagerInfoUser

class EmailGetter:
    config = ManagerInfoUser.load_config()
    
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

        email_folder = os.path.join(f"{SAVE_FOLDER}_{EmailGetter.config['EMAIL']}", filtered_email)
        email_path = os.path.join(email_folder, f"{sender}, {email_id}")
        with open(email_path, 'wb') as email_file:
            email_file.write(response.encode())
            EmailManager.create_mails_status(sender, email_id, filtered_email)
    
    @staticmethod
    def download_emails_pop3():
        with socket.create_connection((EmailGetter.config['SERVER'], EmailGetter.config['POP3_PORT'])) as server_socket:
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('+OK Test Mail Server'):
                raise Exception(f"Error connecting to server: {response}")
            
            server_socket.send("CAPA\r\n".encode())
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('+OK\r\nUIDL'):
                raise Exception(f"Error: {response}")
            
            server_socket.send(f"USER {EmailGetter.config['EMAIL']}\r\n".encode())
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('+OK'):
                raise Exception(f"Error: {response}")

            server_socket.send(f"PASS {EmailGetter.config['PASSWORD']}\r\n".encode())
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
    def load_filter_config():
        with open('filter.json', 'r') as json_file:
            return json.load(json_file)
        
    @staticmethod
    def create_filter_folder():
        if not os.path.exists(f"{SAVE_FOLDER}_{EmailGetter.config['EMAIL']}"):
            os.makedirs(f"{SAVE_FOLDER}_{EmailGetter.config['EMAIL']}")

        for folder in FOLDER_LIST:
            file_path = os.path.join(f"{SAVE_FOLDER}_{EmailGetter.config['EMAIL']}", folder)
            if not os.path.exists(file_path):
                os.makedirs(file_path)

    @staticmethod
    def filter_email(response):
        filter_config = EmailFilter.load_filter_config()

        sender = EmailGetter.get_sender(response)
        subject = EmailGetter.get_subject_email(response)
        content = EmailGetter.get_email_content(response)


        for folder, keywords in filter_config.items():
            if any(word.lower() == sender.strip().lower() for word in keywords):
                return folder
            elif any(word.lower() in subject.strip().lower() for word in keywords):
                return folder
            elif any(word.lower() in content.strip().lower() for word in keywords):
                return folder
            elif any(word.lower() in subject.strip().lower() or word.lower() in content.strip().lower() for word in keywords):
                return folder
        
        return "INBOX"

class EmailManager:
    @staticmethod
    def create_mails_status(sender, email_id, filtered_email):
        element = [filtered_email, sender, email_id, "unread"]

        file_path = os.path.join(f"{SAVE_FOLDER}_{EmailGetter.config['EMAIL']}", 'list_emails.csv')

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
        csv_path = os.path.join(f"{SAVE_FOLDER}_{EmailGetter.config['EMAIL']}", "list_emails.csv")
        if os.path.exists(csv_path):
            with open(csv_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for element in email_list:
                    content = [element['folder'], element['sender'], element['mes_id'], element['status']]
                    writer.writerow(content)

    @staticmethod
    def update_status_of_mail(email_id, emails_list):
        matching_emails = [email for email in emails_list if email.get('mes_id') == email_id]
        
        if matching_emails: 
            for matching_email in matching_emails:
                matching_email['status'] = "read"

class EmailShow:
    @staticmethod
    def show_download_mail():
        email_list = []
        csv_path = os.path.join(f"{SAVE_FOLDER}_{EmailGetter.config['EMAIL']}", "list_emails.csv")

        if os.path.exists(csv_path):
            with open(csv_path) as file:
                for line in file:
                    folder, sender, mes_id, status = line.strip().split(',')
                    email = {'folder': folder, 'sender': sender, 'mes_id': mes_id, 'status': status}
                    email_list.append(email)

        return email_list