from MailLib import *
from manageInfo import ManagerInfoUser

class EmailSendInfo:
    # Lấy thông tin người dùng gửi TO
    # Tách các dấu ',' trong chuỗi string thành kiểu dữ liệu <list> 
    @staticmethod
    def get_email_to(mails_address_to, to_email):
        if to_email is not None:
            to_email = to_email.split(',')
            To = [email.strip() for email in to_email]
            mails_address_to.extend(To)
    
    # Lấy thông tin người dùng gửi CC
    # Tách các dấu ',' trong chuỗi string thành kiểu dữ liệu <list> 
    @staticmethod
    def get_email_cc(mails_address_cc, cc_email):
        if cc_email is not None:
            cc_email = cc_email.split(',')
            Cc = [email.strip() for email in cc_email]
            mails_address_cc.extend(Cc)
    
    # Lấy thông tin người dùng gửi BCC
    # Tách các dấu ',' trong chuỗi string thành kiểu dữ liệu <list> 
    @staticmethod
    def get_email_bcc(mails_address_bcc, bcc_email):
        if bcc_email is not None:
            bcc_email = bcc_email.split(',')
            Bcc = [email.strip() for email in bcc_email]
            mails_address_bcc.extend(Bcc)
    
    # Lấy các đường dẫn của các file đính kèm
    # Nếu list trống [''] (ko có bất cứ đường dẫn nào) thì trả về list rỗng [] 
    @staticmethod
    def get_attached_file(entry_filename):
        if entry_filename == ['']:
            return []
        else:
            return entry_filename
    
    # Tạo universal unique ID cho mail
    @staticmethod
    def generate_message_id():
        return str(uuid.uuid4())
    
    # Tách tên miền (lấy từ '@' đến cuối chuỗi)
    @staticmethod
    def take_domain(From):
        return '@' + From.split('@')[1]

    # Encode tên người dùng (username)
    @staticmethod
    def encode_user_name():
        config = ManagerInfoUser.load_config()
        encoded_name = base64.b64encode(config['NAME'].encode()).decode()
        return f'=?UTF-8?B?{encoded_name}?='

class EmailEncoder:
    # Thực hiện encode file đính kèm
    # Gửi thêm các thông tin của file đính kèm
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

    # đính kèm file txt vào mail
    @staticmethod       
    def attach_txt_in_email(file_path):
        if os.path.exists(file_path):
            return EmailEncoder.encode_and_header_attach_file(file_path, CONTENT_TXT)
        else:
            return ""
    
    # đính kèm file docx vào mail
    @staticmethod
    def attach_docx_in_email(file_path):
        if os.path.exists(file_path):
            return EmailEncoder.encode_and_header_attach_file(file_path, CONTENT_DOCX)
        else:
            return ""

    # đính kèm file pdf vào mail
    @staticmethod
    def attach_pdf_in_email(file_path):
        if os.path.exists(file_path):
            return EmailEncoder.encode_and_header_attach_file(file_path, CONTENT_PDF)
        else:
            return ""
    
    # đính kèm file hình vào mail
    @staticmethod
    def attach_image_in_email(file_path):
        if os.path.exists(file_path):
            return EmailEncoder.encode_and_header_attach_file(file_path, CONTENT_JPG)
        else:
            return ""

    # đính kèm file zip vào mail
    @staticmethod
    def attach_zip_in_email( file_path):
        if os.path.exists(file_path):
            return EmailEncoder.encode_and_header_attach_file(file_path, CONTENT_ZIP)
        else:
            return ""
        
class EmailSender:
    # Gửi các header chung, giao tiếp với server SMTP
    @staticmethod
    def send_header(server_socket, From, Type_to, Type_cc, Type_bcc):
        config = ManagerInfoUser.load_config()
        server_socket.send(f"EHLO [{config['SERVER']}]\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending EHLO: {response}")

        server_socket.send(f"MAIL FROM:<{From}>\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")

        if any(email.strip() for email in Type_to):
            for to_address in Type_to: 
                server_socket.send(f"RCPT TO:<{to_address}>\r\n".encode())
                response = server_socket.recv(HEADER).decode()
                if not response.startswith('250'):
                    raise Exception(f"Error sending mail address: {response}")
                
        if any(email.strip() for email in Type_cc):
            for cc_address in Type_cc: 
                server_socket.send(f"RCPT TO:<{cc_address}>\r\n".encode())
                response = server_socket.recv(HEADER).decode()
                if not response.startswith('250'):
                    raise Exception(f"Error sending mail address: {response}")
        
        if any(email.strip() for email in Type_bcc):
            for bcc_address in Type_bcc: 
                server_socket.send(f"RCPT TO:<{bcc_address}>\r\n".encode())
                response = server_socket.recv(HEADER).decode()
                if not response.startswith('250'):
                    raise Exception(f"Error sending mail address: {response}")

        server_socket.send("DATA\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('354'):
            raise Exception(f"Error sending data: {response}")
    
    # Gửi các header chung cho cả mail có file và ko có file
    @staticmethod
    def send_header_normal_mail(server_socket, From):
        message_id = '<' + EmailSendInfo.generate_message_id() + EmailSendInfo.take_domain(From) + '>'
        server_socket.send(f"Message-ID: {message_id}\r\n".encode())

        current_time = datetime.now()
        time_format = current_time.strftime("Date: %a,%e %b %Y %H:%M:%S +0700")
        server_socket.send(f"{time_format}\r\n".encode())

        server_socket.send(f"MIME-Version: {MIME_VERSION}\r\n".encode())
        server_socket.send(f"User-Agent: {USER_AGENT}\r\n".encode())
        server_socket.send(f"Content-Language: {CONTENT_LANGUAGE}\r\n".encode())

    # Gửi các header nếu như file có file đính kèm
    @staticmethod
    def send_header_attached_file_mail(server_socket, From):
        server_socket.send(f"Content-Type: multipart/mixed; boundary=\"{BOUNDARY}\"\r\n".encode())
        EmailSender.send_header_normal_mail(server_socket, From)

    # Gửi các header nếu như file không có file đính kèm
    @staticmethod
    def send_normal_mail(server_socket, email_data, content):
        email_data += f"Content-Type: {CONTENT_TYPE}\r\nContent-Transfer-Encoding: {CONTENT_TRANSFER_ENCODING}\r\n\r\n{content}\r\n\r\n"
        server_socket.sendall(f"{email_data}.\r\n".encode())

        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
                raise Exception(f"Error sending email: {response}")

    # Gửi nội dung của mail cho server SMTP
    @staticmethod
    def send_content_of_attached_mail(email_data, server_socket, content):
        email_data += f"\r\n{NOTICE}\r\n--{BOUNDARY}\r\nContent-Type: {CONTENT_TYPE}\r\nContent-Transfer-Encoding: {CONTENT_TRANSFER_ENCODING}\r\n\r\n{content}\r\n\r\n"
        server_socket.sendall(f"{email_data}".encode())
        server_socket.send(f"--{BOUNDARY}".encode())

    # Gửi file txt cho server SMTP
    @staticmethod
    def send_txt_file(server_socket, email_data, file, content):
        EmailSender.send_content_of_attached_mail(email_data, server_socket, content)
        server_socket.send(f"{EmailEncoder.attach_txt_in_email(file)}".encode())    
    
    # Gửi file docx cho server SMTP
    @staticmethod
    def send_docx_file(server_socket, email_data, file, content):
        EmailSender.send_content_of_attached_mail(email_data, server_socket, content)
        server_socket.send(f"{EmailEncoder.attach_docx_in_email(file)}".encode())    

    # Gửi file pdf cho server SMTP
    @staticmethod
    def send_pdf_file(server_socket, email_data, file, content):
        EmailSender.send_content_of_attached_mail(email_data, server_socket, content)
        server_socket.send(f"{EmailEncoder.attach_pdf_in_email(file)}".encode())    

    # Gửi file hình cho server SMTP
    @staticmethod
    def send_image_file(server_socket, email_data, file, content):
        EmailSender.send_content_of_attached_mail(email_data, server_socket, content)
        server_socket.send(f"{EmailEncoder.attach_image_in_email(file)}".encode())    

    # Gửi file zip cho server SMTP
    @staticmethod
    def send_zip_file(server_socket, email_data, file, content):
        EmailSender.send_content_of_attached_mail(email_data, server_socket, content)
        server_socket.send(f"{EmailEncoder.attach_zip_in_email(file)}".encode())    

    # Gửi tất cả các file đính kèm đã được người dùng chọn
    @staticmethod
    def send_all_file(server_socket, From, attach_files, email_data, content):
        EmailSender.send_header_attached_file_mail(server_socket, From)
        for index, file in enumerate(attach_files):
            if file.strip().endswith('.txt'):
                EmailSender.send_txt_file(server_socket, email_data, file, content)
            if file.strip().endswith('.docx'):
                EmailSender.send_docx_file(server_socket, email_data, file, content)
            elif file.strip().endswith('.pdf'):
                EmailSender.send_pdf_file(server_socket, email_data, file, content)
            elif file.strip().endswith('.jpg'):
                EmailSender.send_image_file(server_socket, email_data, file, content)
            elif file.strip().endswith('.zip'):
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
    # Gửi mail Bcc 
    # Thực hiện khi người dùng ko có gửi mail To, Cc
    def send_email_bcc(From, Bcc, subject, content, attach_files):
        config = ManagerInfoUser.load_config()
        check_attach_file = bool(attach_files)
        user_name_encode = EmailSendInfo.encode_user_name()

        email_data = f"From: {user_name_encode} <{From}>\r\nSubject: {subject}\r\nTo: {BCC_NOTICE}\r\n"

        with socket.create_connection((config['SERVER'], config['SMTP_PORT'])) as server_socket:
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('220'):
                raise Exception(f"Error connecting to server: {response}")
            
            EmailSender.send_header(server_socket, From, [], [], Bcc)

            if check_attach_file == True:
                EmailSender.send_all_file(server_socket, From, attach_files, email_data, content)
            else:
                EmailSender.send_header_normal_mail(server_socket, From)
                EmailSender.send_normal_mail(server_socket, email_data, content)
            
            server_socket.send("QUIT\r\n".encode())

    # Gửi mail bao gồm gửi To, Cc, Bcc
    def send_email(from_address, to_addresses, cc_addresses, bcc_addresses, subject, content, attach_files):
        config = ManagerInfoUser.load_config()
        check_attach_file = bool(attach_files)
        email_data = ""

        if any(email.strip() for email in to_addresses):
            to_address = ', '.join(to_addresses)
            email_data += f"To: {to_address}\r\n"
        if any(email.strip() for email in cc_addresses):
            cc_address = ', '.join(cc_addresses)
            email_data += f"Cc: {cc_address}\r\n"
        
        if not any(email.strip() for email in to_addresses) and not any(email.strip() for email in cc_addresses):
            EmailClient_Send.send_email_bcc(from_address, bcc_addresses, subject, content, attach_files)
            return

        user_name_encode = EmailSendInfo.encode_user_name()
        
        email_data += f"From: {user_name_encode} <{from_address}>\r\nSubject: {subject}\r\n"
        with socket.create_connection((config['SERVER'], config['SMTP_PORT'])) as server_socket:
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('220'):
                raise Exception(f"Error connecting to server: {response}")

            EmailSender.send_header(server_socket, from_address, to_addresses, cc_addresses, bcc_addresses)
            
            if check_attach_file == True:
                EmailSender.send_all_file(server_socket, from_address, attach_files, email_data, content)
            else:
                EmailSender.send_header_normal_mail(server_socket, from_address)
                EmailSender.send_normal_mail(server_socket, email_data, content)

            server_socket.send("QUIT\r\n".encode()) 

    # Chạy chương trình gửi mail
    @staticmethod
    def run_send_mail_program(entry_to, entry_cc, entry_bcc, entry_subject, entry_content, entry_filename):
        mails_address_to = []
        mails_address_cc = []
        mails_address_bcc = [] 

        From = ManagerInfoUser.load_config()['EMAIL']

        EmailSendInfo.get_email_to(mails_address_to, entry_to)
        EmailSendInfo.get_email_cc(mails_address_cc, entry_cc)
        EmailSendInfo.get_email_bcc(mails_address_bcc, entry_bcc)
    
        subject = entry_subject
        content = entry_content

        attach_files_path = EmailSendInfo.get_attached_file(entry_filename)

        EmailClient_Send.send_email(From, mails_address_to, mails_address_cc, mails_address_bcc, subject, content, attach_files_path)