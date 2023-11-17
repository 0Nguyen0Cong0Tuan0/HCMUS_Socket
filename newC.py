import socket
import os
import base64
from datetime import datetime

HEADER = 1024
FORMAT = "utf-8"
BOUNDARY = "------------5sWLTDpPOowcnjH7yr7J87Aq"
MIME_VERSION = "1.0"
USER_AGENT = "Mozilla Thunderbird"
CONTENT_LANGUAGE = "en-US"
BCC_NOTICE = "undisclosed-recipients: ;"
CONTENT_TYPE = "text/plain; charset=UTF-8; format=flowed"
CONTENT_TXT = "text/plain; charset=UTF-8; name="
CONTENT_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document; name="
CONTENT_PDF = "application/pdf; name="
CONTENT_JPG = "image/jpeg; name="
CONTENT_ZIP = "application/x-zip-compressed; name="
CONTENT_TRANSFER_ENCODING = "7bit"
NOTICE = "This is a multi-part message in MIME format."
SEND_CONTENT = False

def get_Email_To(mails_address_to):
    To = input("TO: ").split(',')
    To = [email.strip() for email in To]
    mails_address_to.extend(To)

def get_Email_Cc(mails_address_cc):
    Cc = input("CC: ").split(',')
    Cc = [email.strip() for email in Cc]
    mails_address_cc.extend(Cc)
    
def get_Email_Bcc(mails_address_bcc):
    Bcc = input("BCC: ").split(',')
    Bcc = [email.strip() for email in Bcc]
    mails_address_bcc.extend(Bcc)

def get_Attached_File():
    attach_files_path = []
    files_input = input("Attach files: ").split(',')
    if files_input == ['']:
        return []
    else:
        attach_files_path.extend([file_path.strip() for file_path in files_input])
        new_path = get_Valid_File(attach_files_path)
        return new_path

def get_Valid_File(attach_files):  
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

#----------------------------
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

def attach_txt_in_email(file_path):
    if os.path.exists(file_path):
        return encode_and_header_attach_file(file_path, CONTENT_TXT)
    else:
        print("The file does not exist")
        return ""
    
def attach_docx_in_email(file_path):
    if os.path.exists(file_path):
        return encode_and_header_attach_file(file_path, CONTENT_DOCX)
    else:
        print("The file does not exist")
        return ""

def attach_pdf_in_email(file_path):
    if os.path.exists(file_path):
        return encode_and_header_attach_file(file_path, CONTENT_PDF)
    else:
        print("The file does not exist")
        return ""

def attach_image_in_email(file_path):
    if os.path.exists(file_path):
        return encode_and_header_attach_file(file_path, CONTENT_JPG)
    else:
        print("The file does not exist")
        return ""

def attach_zip_in_email(file_path):
    if os.path.exists(file_path):
        return encode_and_header_attach_file(file_path, CONTENT_ZIP)
    else:
        print("The file does not exist")
        return ""

#----------------------------
def send_header(server_socket, From, Type):
    server_socket.send("EHLO [127.0.0.1]\r\n".encode())
    response = server_socket.recv(HEADER).decode()
    if not response.startswith('250'):
        raise Exception(f"Error sending EHLO: {response}")
    
    server_socket.send(f"MAIL FROM:<{From}>\r\n".encode())
    response = server_socket.recv(HEADER).decode()
    if not response.startswith('250'):
        raise Exception(f"Error sending mail address: {response}")
    
    for type in Type:
        server_socket.send(f"RCPT TO:<{type}>\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")
    
    server_socket.send("DATA\r\n".encode())
    response = server_socket.recv(HEADER).decode()
    if not response.startswith('354'):
        raise Exception(f"Error sending data: {response}")

def send_header_normal_mail(server_socket):
    current_time = datetime.now()
    time_format = current_time.strftime("Date: %a, %d %b %Y %H:%M:%S +0700")
    server_socket.send(f"{time_format}\r\n".encode())

    server_socket.send(f"MIME-Version: {MIME_VERSION}\r\n".encode())
    server_socket.send(f"User-Agent: {USER_AGENT}\r\n".encode())
    server_socket.send(f"Content-Language: {CONTENT_LANGUAGE}\r\n".encode())

def send_header_attached_file_mail(server_socket):
    server_socket.send(f"Content-Type: multipart/mixed; boundary=\"{BOUNDARY}\"\r\n".encode())
    send_header_normal_mail(server_socket)

#----------------------------
def send_normal_mail(server_socket, email_data, content):
    email_data += f"Content-Type: {CONTENT_TYPE}\r\nContent-Transfer-Encoding: {CONTENT_TRANSFER_ENCODING}\r\n\r\n{content}\r\n\r\n"
    server_socket.sendall(f"{email_data}.\r\n".encode())

    response = server_socket.recv(HEADER).decode()
    if not response.startswith('250'):
            raise Exception(f"Error sending email: {response}")

def check_send_content(email_data, server_socket, content):
    global SEND_CONTENT
    if not SEND_CONTENT:
        send_content_of_attached_mail(email_data, server_socket, content)
        SEND_CONTENT = True

def send_content_of_attached_mail(email_data, server_socket, content):
    email_data += f"\r\n{NOTICE}\r\n--{BOUNDARY}\r\nContent-Type: {CONTENT_TYPE}\r\nContent-Transfer-Encoding: {CONTENT_TRANSFER_ENCODING}\r\n\r\n{content}\r\n\r\n"
    server_socket.sendall(f"{email_data}".encode())
    server_socket.send(f"--{BOUNDARY}".encode())

def send_txt_file(server_socket, email_data, file, content):
    check_send_content(email_data, server_socket, content)
    server_socket.send(f"{attach_txt_in_email(file)}".encode())    
    
def send_docx_file(server_socket, email_data, file, content):
    check_send_content(email_data, server_socket, content)
    server_socket.send(f"{attach_docx_in_email(file)}".encode())    

def send_pdf_file(server_socket, email_data, file, content):
    check_send_content(email_data, server_socket, content)
    server_socket.send(f"{attach_pdf_in_email(file)}".encode())    

def send_image_file(server_socket, email_data, file, content):
    check_send_content(email_data, server_socket, content)
    server_socket.send(f"{attach_image_in_email(file)}".encode())    

def send_zip_file(server_socket, email_data, file, content):
    check_send_content(email_data, server_socket, content)
    server_socket.send(f"{attach_zip_in_email(file)}".encode())    

def send_all_file(server_socket, attach_files, email_data, content):
    send_header_attached_file_mail(server_socket)
    for index, file in enumerate(attach_files):
        if file.endswith('.txt'):
            send_txt_file(server_socket, email_data, file, content)
        if file.endswith('.docx'):
            send_docx_file(server_socket, email_data, file, content)
        elif file.endswith('.pdf'):
            send_pdf_file(server_socket, email_data, file, content)
        elif file.endswith('.jpg'):
            send_image_file(server_socket, email_data, file, content)
        elif file.endswith('.zip'):
            send_zip_file(server_socket, email_data, file, content)
        
        if index == len(attach_files) - 1:
            continue
        else:
            server_socket.send(f"--{BOUNDARY}".encode())

    server_socket.send(f"--{BOUNDARY}--\r\n.\r\n".encode())   
    response = server_socket.recv(HEADER).decode()
    if not response.startswith('250'):
            raise Exception(f"Error sending email: {response}")

#----------------------------
def send_email_to(From, To, subject, content, attach_files):
    check_attach_file = bool(attach_files)

    to_address = ', '.join(To)
    email_data = f"To: {to_address}\r\nFrom: {From}\r\nSubject: {subject}\r\n"

    with socket.create_connection(("127.0.0.1", 2225)) as server_socket:
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('220'):
            raise Exception(f"Error connecting to server: {response}")
        
        send_header(server_socket, From, To)
        
        if check_attach_file == True:
            send_all_file(server_socket, attach_files, email_data, content)
        else:
            send_header_normal_mail(server_socket)
            send_normal_mail(server_socket, email_data, content)
        
        server_socket.send("QUIT".encode()) 

def send_email_cc(From, Cc, subject, content, attach_files):
    check_attach_file = bool(attach_files)

    cc_address = ', '.join(Cc)
    email_data = f"Cc: {cc_address}\r\nFrom: {From}\r\nSubject: {subject}\r\n"

    with socket.create_connection(("127.0.0.1", 2225)) as server_socket:
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('220'):
            raise Exception(f"Error connecting To server: {response}")
        
        send_header(server_socket, From, Cc)

        if check_attach_file == True:
            send_all_file(server_socket, attach_files, email_data, content)
        else:
            send_header_normal_mail(server_socket)
            send_normal_mail(server_socket, email_data, content)
        
        server_socket.send("QUIT".encode()) 

def send_email_bcc(From, Bcc, subject, content, attach_files):
    check_attach_file = bool(attach_files)

    email_data = f"From: {From}\r\nSubject: {subject}\r\nTo: {BCC_NOTICE}\r\n"

    with socket.create_connection(("127.0.0.1", 2225)) as server_socket:
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('220'):
            raise Exception(f"Error connecting to server: {response}")
        
        send_header(server_socket, From, Bcc)

        if check_attach_file == True:
            send_all_file(server_socket, attach_files, email_data, content)
        else:
            send_header_normal_mail(server_socket)
            send_normal_mail(server_socket, email_data, content)
        
        server_socket.send("QUIT".encode()) 
        
def send_email(mails_address_to, mails_address_cc, mails_address_bcc, From, subject, content, attach_files_path):
    if any(email.strip() for email in mails_address_to):
        send_email_to(From, mails_address_to, subject, content, attach_files_path)
    if any(email.strip() for email in mails_address_cc):
        send_email_cc(From, mails_address_cc, subject, content, attach_files_path)
    if any(email.strip() for email in mails_address_bcc):
        send_email_bcc(From, mails_address_bcc, subject, content, attach_files_path)

#----------------------------
def run_send_mail_program():
    mails_address_to = []
    mails_address_cc = []
    mails_address_bcc = []
    
    #From = input("From: ")
    From = "nctuan22@clc.fitus.edu.vn"

    get_Email_To(mails_address_to)
    get_Email_Cc(mails_address_cc)
    get_Email_Bcc(mails_address_bcc)
   
    subject = input("Subject: ")
    content = input("Content: ")

    attach_files_path = get_Attached_File()

    send_email(mails_address_to, mails_address_cc, mails_address_bcc, From, subject, content, attach_files_path)

def main():
    run_send_mail_program()
    
if __name__ == "__main__":
    main()
