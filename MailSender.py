from MailLib import *

def load_config(file_path):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data

config = load_config('account.json')

class EmailSendInfo:
    @staticmethod
    def get_email_to(mails_address_to, to_email):
        if to_email is not None:
            to_email = to_email.split(',')
            To = [email.strip() for email in to_email]
            mails_address_to.extend(To)
    
    @staticmethod
    def get_email_cc(mails_address_cc, cc_email):
        if cc_email is not None:
            cc_email = cc_email.split(',')
            Cc = [email.strip() for email in cc_email]
            mails_address_cc.extend(Cc)
    
    @staticmethod
    def get_email_bcc(mails_address_bcc, bcc_email):
        if bcc_email is not None:
            bcc_email = bcc_email.split(',')
            Bcc = [email.strip() for email in bcc_email]
            mails_address_bcc.extend(Bcc)
    
    @staticmethod
    def get_attached_file(entry_filename):
        if entry_filename == ['']:
            return []
        else:
            new_path = EmailSendInfo.get_valid_file(entry_filename)
            return new_path
    
    @staticmethod
    def get_valid_file(attach_files):  
        count = 0    
        new_attach_files = []

        for file_path in attach_files:
            file_path = file_path.strip()

            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path) / (1024**2)
                if file_size <= 3:
                    new_attach_files.append(file_path)
                else:
                    print(f"The size of the attached file {file_path} is too large")
                    print("Do you want to remove or choose another file? (0: remove, 1: choose): ", end="")

                    while True:
                        choice = int(input())

                        if choice == 0:
                            remove_file = attach_files[count]
                            attach_files = [file for file in attach_files if file is not remove_file]
                            break
                        elif choice == 1:
                            while True:
                                add_file = input("File you want to attach: ")
                                if os.path.exists(add_file):
                                    file_size = os.path.getsize(add_file) / (1024**2)
                                    if file_size <= 3:
                                        new_attach_files.append(add_file)
                                        break
                                    else:
                                        print(f"The size of the attached file {file_path} is too large")
                                else:
                                    print(f"{add_file} does not exist.")
                        else:
                            print("Invalid choice!!! Try again")
            else:
                print(f"{file_path} does not exist.")
                print(f"Do you want to change the file {file_path}? (0: no, 1: yes): ", end="")

                while True:
                    choice_change = int(input())
                    if choice_change == 0:
                        break
                    elif choice_change == 1:
                        while True:
                            add_file = input("File you want to attach: ")
                            if os.path.exists(add_file):
                                file_size = os.path.getsize(add_file) / (1024**2)
                                if file_size <= 3:
                                    new_attach_files.append(add_file)
                                    break
                                else:
                                    print(f"The size of the attached file {file_path} is too large")
                            else:
                                print(f"{add_file} does not exist.")
                        break
                

            count += 1

        return new_attach_files
    
    @staticmethod
    def generate_message_id():
        return str(uuid.uuid4())
    
    @staticmethod
    def take_domain(From):
        return '@' + From.split('@')[1]

    @staticmethod
    def encode_user_name():
        encoded_name = base64.b64encode(config['NAME'].encode()).decode()
        return f'=?UTF-8?B?{encoded_name}?='

class EmailEncoder:
    @staticmethod
    def encode_and_header_attach_file(file_path, content_type):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as at:
                file_content = at.read()

                file_content_encode = base64.b64encode(file_content).decode(FORMAT)

                file_content_with_newlines = '\r\n'.join(file_content_encode[i:i+100] for i in range(0, len(file_content_encode), 100))

                attachment_header = f"\r\nContent-Type: {content_type}\"{os.path.basename(file_path)}\"" \
                                f"\r\nContent-Disposition: attachment; filename=\"{os.path.basename(file_path)}\"" \
                                "\r\nContent-Transfer-Encoding: base64\r\n\r\n"
                return attachment_header + file_content_with_newlines + "\r\n\r\n"

    @staticmethod       
    def attach_txt_in_email(file_path):
        if os.path.exists(file_path):
            return EmailEncoder.encode_and_header_attach_file(file_path, CONTENT_TXT)
        else:
            print("The file does not exist")
            return ""
    
    @staticmethod
    def attach_docx_in_email(file_path):
        if os.path.exists(file_path):
            return EmailEncoder.encode_and_header_attach_file(file_path, CONTENT_DOCX)
        else:
            print("The file does not exist")
            return ""

    @staticmethod
    def attach_pdf_in_email(file_path):
        if os.path.exists(file_path):
            return EmailEncoder.encode_and_header_attach_file(file_path, CONTENT_PDF)
        else:
            print("The file does not exist")
            return ""
    
    @staticmethod
    def attach_image_in_email(file_path):
        if os.path.exists(file_path):
            return EmailEncoder.encode_and_header_attach_file(file_path, CONTENT_JPG)
        else:
            print("The file does not exist")
            return ""

    @staticmethod
    def attach_zip_in_email( file_path):
        if os.path.exists(file_path):
            return EmailEncoder.encode_and_header_attach_file(file_path, CONTENT_ZIP)
        else:
            print("The file does not exist")
            return ""
        
class EmailSender:
    @staticmethod
    def send_header(server_socket, From, Type):
        server_socket.send(f"EHLO {config['SERVER']}\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending EHLO: {response}")

        server_socket.send(f"MAIL FROM:<{From}>\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")

        for to_address in Type:  # Iterate over the list of addresses
            server_socket.send(f"RCPT TO:<{to_address}>\r\n".encode())
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('250'):
                raise Exception(f"Error sending mail address: {response}")

        server_socket.send("DATA\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('354'):
            raise Exception(f"Error sending data: {response}")
    
    @staticmethod
    def send_header_normal_mail(server_socket, From):
        message_id = '<' + EmailSendInfo.generate_message_id() + EmailSendInfo.take_domain(From) + '>'
        server_socket.send(f"Message-ID: {message_id}\r\n".encode())

        current_time = datetime.now()
        time_format = current_time.strftime("Date: %a, %d %b %Y %H:%M:%S +0700")
        server_socket.send(f"{time_format}\r\n".encode())

        server_socket.send(f"MIME-Version: {MIME_VERSION}\r\n".encode())
        server_socket.send(f"User-Agent: {USER_AGENT}\r\n".encode())
        server_socket.send(f"Content-Language: {CONTENT_LANGUAGE}\r\n".encode())

    @staticmethod
    def send_header_attached_file_mail(server_socket, From):
        server_socket.send(f"Content-Type: multipart/mixed; boundary=\"{BOUNDARY}\"\r\n".encode())
        EmailSender.send_header_normal_mail(server_socket, From)

    @staticmethod
    def send_normal_mail(server_socket, email_data, content):
        email_data += f"Content-Type: {CONTENT_TYPE}\r\nContent-Transfer-Encoding: {CONTENT_TRANSFER_ENCODING}\r\n\r\n{content}\r\n\r\n"
        server_socket.sendall(f"{email_data}.\r\n".encode())

        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
                raise Exception(f"Error sending email: {response}")

    @staticmethod
    def check_send_content(email_data, server_socket, content):
        global SEND_CONTENT
        if not SEND_CONTENT:
            EmailSender.send_content_of_attached_mail(email_data, server_socket, content)
            SEND_CONTENT = True

    @staticmethod
    def send_content_of_attached_mail(email_data, server_socket, content):
        email_data += f"\r\n{NOTICE}\r\n--{BOUNDARY}\r\nContent-Type: {CONTENT_TYPE}\r\nContent-Transfer-Encoding: {CONTENT_TRANSFER_ENCODING}\r\n\r\n{content}\r\n\r\n"
        server_socket.sendall(f"{email_data}".encode())
        server_socket.send(f"--{BOUNDARY}".encode())

    @staticmethod
    def send_txt_file(server_socket, email_data, file, content):
        EmailSender.check_send_content(email_data, server_socket, content)
        server_socket.send(f"{EmailEncoder.attach_txt_in_email(file)}".encode())    
    
    @staticmethod
    def send_docx_file(server_socket, email_data, file, content):
        EmailSender.check_send_content(email_data, server_socket, content)
        server_socket.send(f"{EmailEncoder.attach_docx_in_email(file)}".encode())    

    @staticmethod
    def send_pdf_file(server_socket, email_data, file, content):
        EmailSender.check_send_content(email_data, server_socket, content)
        server_socket.send(f"{EmailEncoder.attach_pdf_in_email(file)}".encode())    

    @staticmethod
    def send_image_file(server_socket, email_data, file, content):
        EmailSender.check_send_content(email_data, server_socket, content)
        server_socket.send(f"{EmailEncoder.attach_image_in_email(file)}".encode())    

    @staticmethod
    def send_zip_file(server_socket, email_data, file, content):
        EmailSender.check_send_content(email_data, server_socket, content)
        server_socket.send(f"{EmailEncoder.attach_zip_in_email(file)}".encode())    

    @staticmethod
    def send_all_file(server_socket, From, attach_files, email_data, content):
        EmailSender.send_header_attached_file_mail(server_socket, From)
        for index, file in enumerate(attach_files):
            if file.endswith('.txt'):
                EmailSender.send_txt_file(server_socket, email_data, file, content)
            if file.endswith('.docx'):
                EmailSender.send_docx_file(server_socket, email_data, file, content)
            elif file.endswith('.pdf'):
                EmailSender.send_pdf_file(server_socket, email_data, file, content)
            elif file.endswith('.jpg'):
                EmailSender.send_image_file(server_socket, email_data, file, content)
            elif file.endswith('.zip'):
                EmailSender.send_zip_file(server_socket, email_data, file, content)
            
            if index == len(attach_files) - 1:
                continue
            else:
                server_socket.send(f"--{BOUNDARY}".encode())

        server_socket.send(f"--{BOUNDARY}--\r\n.\r\n".encode())   
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
                raise Exception(f"Error sending email: {response}")
    
class EmailClient_Send:
    def send_email_to(from_address, to_addresses, subject, content, attach_files):
        check_attach_file = bool(attach_files)
        to_address = ', '.join(to_addresses)
        user_name_encode = EmailSendInfo.encode_user_name()
        email_data = f"To: {to_address}\r\nFrom: {user_name_encode} <{from_address}>\r\nSubject: {subject}\r\n"

        with socket.create_connection((config['SERVER'], config['SMTP_PORT'])) as server_socket:
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('220'):
                raise Exception(f"Error connecting to server: {response}")

            EmailSender.send_header(server_socket, from_address, to_addresses)

            if check_attach_file == True:
                EmailSender.send_all_file(server_socket, from_address, attach_files, email_data, content)
            else:
                EmailSender.send_header_normal_mail(server_socket, from_address)
                EmailSender.send_normal_mail(server_socket, email_data, content)

            server_socket.send("QUIT".encode())

    def send_email_cc(from_address, cc_addresses, subject, content, attach_files):
        check_attach_file = bool(attach_files)
        cc_address = ', '.join(cc_addresses)
        email_data = f"Cc: {cc_address}\r\nFrom: {from_address}\r\nSubject: {subject}\r\n"

        with socket.create_connection((config['SERVER'], config['SMTP_PORT'])) as server_socket:
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('220'):
                raise Exception(f"Error connecting To server: {response}")

            EmailSender.send_header(server_socket, from_address, cc_addresses)

            if check_attach_file == True:
                EmailSender.send_all_file(server_socket, from_address, attach_files, email_data, content)
            else:
                EmailSender.send_header_normal_mail(server_socket, from_address)
                EmailSender.send_normal_mail(server_socket, email_data, content)

            server_socket.send("QUIT".encode())
    
    def send_email_bcc(From, Bcc, subject, content, attach_files):
        check_attach_file = bool(attach_files)

        email_data = f"From: {From}\r\nSubject: {subject}\r\nTo: {BCC_NOTICE}\r\n"

        with socket.create_connection((config['SERVER'], config['SMTP_PORT'])) as server_socket:
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('220'):
                raise Exception(f"Error connecting to server: {response}")
            
            EmailSender.send_header(server_socket, From, Bcc)

            if check_attach_file == True:
                EmailSender.send_all_file(server_socket, From, attach_files, email_data, content)
            else:
                EmailSender.send_header_normal_mail(server_socket, From)
                EmailSender.send_normal_mail(server_socket, email_data, content)
            
            server_socket.send("QUIT".encode()) 

    def send_email(mails_address_to, mails_address_cc, mails_address_bcc, From, subject, content, attach_files_path):
        if any(email.strip() for email in mails_address_to):
            EmailClient_Send.send_email_to(From, mails_address_to, subject, content, attach_files_path)
        if any(email.strip() for email in mails_address_cc):
            EmailClient_Send.send_email_cc(From, mails_address_cc, subject, content, attach_files_path)
        if any(email.strip() for email in mails_address_bcc):
            EmailClient_Send.send_email_bcc(From, mails_address_bcc, subject, content, attach_files_path)

    @staticmethod
    def run_send_mail_program(entry_to, entry_cc, entry_bcc, entry_subject, entry_content, entry_filename):
        mails_address_to = []
        mails_address_cc = []
        mails_address_bcc = [] 
    
        #From = input("From: ")
        From = "nguyencongtuan0810@gmail.com"

        EmailSendInfo.get_email_to(mails_address_to, entry_to)
        EmailSendInfo.get_email_cc(mails_address_cc, entry_cc)
        EmailSendInfo.get_email_bcc(mails_address_bcc, entry_bcc)
    
        subject = entry_subject
        content = entry_content

        attach_files_path = EmailSendInfo.get_attached_file(entry_filename)

        EmailClient_Send.send_email(mails_address_to, mails_address_cc, mails_address_bcc, From, subject, content, attach_files_path)

