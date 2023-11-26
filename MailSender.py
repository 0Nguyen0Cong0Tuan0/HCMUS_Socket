from MailLib import *
from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog
from MailSender import *

window_width = 1200
window_height = 700
window_size = str(window_width) + 'x' + str(window_height)
color = "primary"
font_interface = 'GOUDY STOUT'
font_type = 'Arial Greek'

class EmailSendInfo:
    @staticmethod
    def get_email_to(mails_address_to, to_email):
        To = [email.strip() for email in to_email]
        mails_address_to.extend(To)
    
    def get_email_cc(mails_address_cc):
        Cc = input("CC: ").split(',')
        Cc = [email.strip() for email in Cc]
        mails_address_cc.extend(Cc)
    
    @staticmethod
    def get_email_bcc(mails_address_bcc):
        Bcc = input("BCC: ").split(',')
        Bcc = [email.strip() for email in Bcc]
        mails_address_bcc.extend(Bcc)
    
    @staticmethod
    def get_attached_file():
        attach_files_path = []
        files_input = input("Attach files: ").split(',')
        if files_input == ['']:
            return []
        else:
            attach_files_path.extend([file_path.strip() for file_path in files_input])
            new_path = EmailSendInfo.get_valid_file(attach_files_path)
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
        encoded_name = base64.b64encode(USERNAME.encode()).decode()
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
        server_socket.send(f"EHLO {SERVER}\r\n".encode())
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

class EmailInterface:
    filename_list = [] 
    @staticmethod
    def open(send_file):
        send_file.filename = filedialog.askopenfilename(
            initialdir="/Socket", title="Select A File", filetypes=(("*", "*"), ("all files", "*.*"))
        )
        EmailInterface.filename_list.append(send_file.filename + '  ')
        EmailInterface.update_label_to()

    @staticmethod
    def update_label_to():
        filenames = ''.join(EmailInterface.filename_list)
        
        max_display_length = 115
        filenames_with_newlines = '\n'.join([filenames[i:i + max_display_length] for i in range(0, len(filenames), max_display_length)])
        my_label_to.config(text=filenames_with_newlines)

    @staticmethod
    def to_tab(send_to_tab):
        # TO LABEL
        label_to = tb.Label(send_to_tab, text="TO", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_to.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        label_subject = tb.Label(send_to_tab, text="SUBJECT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_subject.grid(row=1, column=0, padx=30, pady=10, sticky="w")

        label_content = tb.Label(send_to_tab, text="CONTENT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_content.grid(row=2, column=0, padx=30, pady=10, sticky="w")

        label_file = tb.Label(send_to_tab, text="ATTACHED\n    FILE", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_file.grid(row=3, column=0, padx=30, pady=10, sticky="w")

        # TO ENTRY
        entry_to = tb.Entry(send_to_tab, font=(f'{font_type}', 10), width=100)
        entry_to.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        entry_subject = tb.Entry(send_to_tab, font=(f'{font_type}', 10), width=100)
        entry_subject.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        entry_content = ScrolledText(send_to_tab, height=20, width=116, autohide=True, bootstyle='info round')
        entry_content.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        get_file_button = tb.Button(send_to_tab, bootstyle="light, outline, inverse", 
                        text='Select A File', padding=10, command=lambda: open(send_to_tab))
        get_file_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        global my_label_to
        my_label_to = tb.Label(send_to_tab, text="", bootstyle='light', font=('Helvetica', 10))
        my_label_to.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        submit_mail = tb.Button(send_to_tab, bootstyle="info outline", 
                        text='SUBMIT', padding=10, command=lambda: EmailClient_Send.run_send_mail_program(entry_to.get(), entry_subject.get(), entry_content.get("1.0", "end-1c")))
        submit_mail.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    @staticmethod
    def to_submit():
        pass
    @staticmethod
    def cc_tab(send_cc_tab):
        # CC LABEL
        label_cc = tb.Label(send_cc_tab, text="CC", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_cc.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        label_subject_cc = tb.Label(send_cc_tab, text="SUBJECT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_subject_cc.grid(row=1, column=0, padx=30, pady=10, sticky="w")

        label_content_cc = tb.Label(send_cc_tab, text="CONTENT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_content_cc.grid(row=2, column=0, padx=30, pady=10, sticky="w")

        label_file_cc = tb.Label(send_cc_tab, text="ATTACHED\n    FILE", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_file_cc.grid(row=3, column=0, padx=30, pady=10, sticky="w")

        # CC ENTRY
        entry_cc = tb.Entry(send_cc_tab, font=(f'{font_type}', 10), width=100)
        entry_cc.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        entry_subject_cc = tb.Entry(send_cc_tab, font=(f'{font_type}', 10), width=100)
        entry_subject_cc.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        entry_content_cc = ScrolledText(send_cc_tab, height=20, width=116, autohide=True, bootstyle='info round')
        entry_content_cc.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        get_file_button_cc = tb.Button(send_cc_tab, bootstyle="light, outline, inverse", 
                        text='Select A File', padding=10, command=lambda: open(send_cc_tab))
        get_file_button_cc.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        global my_label_cc
        my_label_cc = tb.Label(send_cc_tab, text="", bootstyle='light', font=('Helvetica', 10))
        my_label_cc.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        submit_mail = tb.Button(send_cc_tab, bootstyle="info outline", 
                        text='SUBMIT', padding=10)
        submit_mail.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    @staticmethod
    def bcc_tab(send_bcc_tab):
        # BCC LABEL
        label_bcc = tb.Label(send_bcc_tab, text="BCC", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_bcc.grid(row=0, column=0, padx=30, pady=10, sticky="w")

        label_subject_bcc = tb.Label(send_bcc_tab, text="SUBJECT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_subject_bcc.grid(row=1, column=0, padx=30, pady=10, sticky="w")

        label_content_bcc = tb.Label(send_bcc_tab, text="CONTENT", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_content_bcc.grid(row=2, column=0, padx=30, pady=10, sticky="w")

        label_file_bcc = tb.Label(send_bcc_tab, text="ATTACHED\n    FILE", bootstyle='light',
                            font=(f'{font_interface}', 10))
        label_file_bcc.grid(row=3, column=0, padx=30, pady=10, sticky="w")

        # BCC ENTRY
        entry_bcc = tb.Entry(send_bcc_tab, font=(f'{font_type}', 10), width=100)
        entry_bcc.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        entry_subject_bcc = tb.Entry(send_bcc_tab, font=(f'{font_type}', 10), width=100)
        entry_subject_bcc.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        entry_content_bcc = ScrolledText(send_bcc_tab, height=20, width=116, autohide=True, bootstyle='info round')
        entry_content_bcc.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        get_file_button_bcc = tb.Button(send_bcc_tab, bootstyle="light, outline, inverse", 
                        text='Select A File', padding=10, command=lambda: open(send_bcc_tab))
        get_file_button_bcc.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        global my_label_bcc
        my_label_bcc = tb.Label(send_bcc_tab, text="", bootstyle='light', font=('Helvetica', 10))
        my_label_bcc.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        submit_mail = tb.Button(send_bcc_tab, bootstyle="info outline", 
                        text='SUBMIT', padding=10)
        submit_mail.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    @staticmethod
    def open_send_email_window(parent):
        send_email_window = Toplevel(parent)
        send_email_window.title("Send Email")
        send_email_window.geometry(window_size)
        
        frame_send = tb.Frame(send_email_window, bootstyle=f'{color}', width=900, height=500)
        frame_send.grid(padx=100)

        label_sent_program = tb.Label(frame_send, text="SEND", bootstyle=f'inverse {color}',
                                    font=(f'{font_interface}', 25, 'bold'))
        label_sent_program.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        my_notebook = tb.Notebook(frame_send, bootstyle='success')
        my_notebook.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", rowspan=3)
        
        global send_to_tab
        global send_cc_tab
        global send_bcc_tab
        send_to_tab = tb.Frame(my_notebook)
        send_cc_tab = tb.Frame(my_notebook)
        send_bcc_tab = tb.Frame(my_notebook)

        my_notebook.add(send_to_tab, text="TO")
        my_notebook.add(send_cc_tab, text="CC")
        my_notebook.add(send_bcc_tab, text="BCC")

        EmailInterface.to_tab(send_to_tab)
        EmailInterface.cc_tab(send_cc_tab)
        EmailInterface.bcc_tab(send_bcc_tab)


        
        # Configure column weights to make them expand evenly
        send_to_tab.columnconfigure(0, weight=1)
        send_to_tab.columnconfigure(1, weight=1)

    @staticmethod
    def them():
        pass
    
    @staticmethod
    def we():
        pass
    
    @staticmethod
    def menu():
        root = tb.Window(themename="darkly")
        root.title("MAIL APPLICATION")
        root.geometry(window_size)

        # Create Frame
        frame_menu = tb.Frame(root, bootstyle=f'{color}', width=900, height=500)
        frame_menu.pack(pady=100, padx=50)

        # Create Label
        label_menu = tb.Label(frame_menu, text="MENU", bootstyle=f'inverse {color}',
                            font=(f'{font_interface}', 25, 'bold'))
        label_menu.grid(row=0, column=1, columnspan=3, pady=10, padx=100)

        # Create Send Email Button
        get_send = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='SEND EMAIL', padding=10, command=lambda: EmailInterface.open_send_email_window(root))
        get_send.grid(row=1, columnspan=4, pady=10, padx=100)

        get_all_download = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='ALL RECEIVED MAIL', padding=10, command=EmailInterface.them)
        get_all_download.grid(row=2, columnspan=4, pady=10, padx=100)

        get_download = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='DOWNLOAD MAIL', padding=10, command=EmailInterface.we)
        get_download.grid(row=3, columnspan=4, pady=10, padx=100)

        get_exit = tb.Button(frame_menu, bootstyle="light, outline, inverse", 
                            text='EXIT', padding=10, command=root.destroy)
        get_exit.grid(row=4, columnspan=4, pady=10, padx=100)

        mainloop()

class EmailClient_Send:
    def __init__(self):
        self.info = EmailSendInfo()
        self.encoder = EmailEncoder()
        self.sender = EmailSender()
    
    def send_email_to(self, from_address, to_addresses, subject, content, attach_files):
        check_attach_file = bool(attach_files)
        to_address = ', '.join(to_addresses)
        user_name_encode = EmailSendInfo.encode_user_name()
        email_data = f"To: {to_address}\r\nFrom: {user_name_encode} <{from_address}>\r\nSubject: {subject}\r\n"

        with socket.create_connection((SERVER, SMTP_PORT)) as server_socket:
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('220'):
                raise Exception(f"Error connecting to server: {response}")

            self.sender.send_header(server_socket, from_address, to_addresses)

            if check_attach_file == True:
                self.sender.send_all_file(server_socket, from_address, attach_files, email_data, content)
            else:
                self.sender.send_header_normal_mail(server_socket, from_address)
                self.sender.send_normal_mail(server_socket, email_data, content)

            server_socket.send("QUIT".encode())

    def send_email_cc(self, from_address, cc_addresses, subject, content, attach_files):
        check_attach_file = bool(attach_files)
        cc_address = ', '.join(cc_addresses)
        email_data = f"Cc: {cc_address}\r\nFrom: {from_address}\r\nSubject: {subject}\r\n"

        with socket.create_connection((SERVER, SMTP_PORT)) as server_socket:
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('220'):
                raise Exception(f"Error connecting To server: {response}")

            self.sender.send_header(server_socket, from_address, cc_addresses)

            if check_attach_file == True:
                self.sender.send_all_file(server_socket, from_address, attach_files, email_data, content)
            else:
                self.sender.send_header_normal_mail(server_socket, from_address)
                self.sender.send_normal_mail(server_socket, email_data, content)

            server_socket.send("QUIT".encode())
    
    def send_email_bcc(self, From, Bcc, subject, content, attach_files):
        check_attach_file = bool(attach_files)

        email_data = f"From: {From}\r\nSubject: {subject}\r\nTo: {BCC_NOTICE}\r\n"

        with socket.create_connection((SERVER, SMTP_PORT)) as server_socket:
            response = server_socket.recv(HEADER).decode()
            if not response.startswith('220'):
                raise Exception(f"Error connecting to server: {response}")
            
            self.sender.send_header(server_socket, From, Bcc)

            if check_attach_file == True:
                self.sender.send_all_file(server_socket, From, attach_files, email_data, content)
            else:
                self.sender.send_header_normal_mail(server_socket, From)
                self.sender.send_normal_mail(server_socket, email_data, content)
            
            server_socket.send("QUIT".encode()) 

    def send_email(self, mails_address_to, mails_address_cc, mails_address_bcc, From, subject, content, attach_files_path):
        if any(email.strip() for email in mails_address_to):
            self.send_email_to(From, mails_address_to, subject, content, attach_files_path)
        if any(email.strip() for email in mails_address_cc):
            self.send_email_cc(From, mails_address_cc, subject, content, attach_files_path)
        if any(email.strip() for email in mails_address_bcc):
            self.send_email_bcc(From, mails_address_bcc, subject, content, attach_files_path)

    def run_send_mail_program(content, content2, content3):
        mails_address_to = []
        mails_address_cc = []
        mails_address_bcc = []
        
        print(content)
        print(content2)
        print(content3)
        #From = input("From: ")
        From = "nguyencongtuan0810@gmail.com"

        
        # self.info.get_email_to(mails_address_to)
        # self.info.get_email_cc(mails_address_cc)
        # self.info.get_email_bcc(mails_address_bcc)
    
        # subject = input("Subject: ")
        # content = input("Content: ")

        # attach_files_path = self.info.get_attached_file()

        # self.send_email(mails_address_to, mails_address_cc, mails_address_bcc, From, subject, content, attach_files_path)

    def run(self):
        EmailInterface.menu()