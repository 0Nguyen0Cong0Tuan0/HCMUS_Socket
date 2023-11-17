import os
import base64
# emails_input = input("Enter emails separated by commas: ")

# # Split the input string into a list of emails
# email_list = emails_input.split(',')

# # Remove any leading or trailing whitespaces from each email
# email_list = [email.strip() for email in email_list]

# # Convert the list to a tuple if needed
# email_tuple = tuple(email_list)

# print("Email Tuple:", email_tuple)

# mails_address = []
# emails = "1@gmail.com"
# mails_address.append(emails)

# email_input = "nguyenvanA@gmail.com, nguyenVanB@gmail.com, 2@gmail.com"
# email_input = email_input.split(',')
# email_input = [email.strip() for email in email_input]
# mails_address.extend(email_input)

# mails_address_cc = ', '.join(mails_address)
# print(mails_address_cc)

# num = 41**2

# print(num)

# Original tuple
# original_tuple = (1, 2, 3, 4, 5)

# # Element to remove
# element_to_remove = 3

# # Create a new tuple excluding the element to remove
# original_tuple = tuple(element for element in original_tuple if element != element_to_remove)

# print(original_tuple)

# def read_file_content(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             content = file.read()
#         return content
#     except FileNotFoundError:
#         print(f"File not found: {file_path}")
#         return None
#     except Exception as e:
#         print(f"Error reading file: {e}")
#         return None
    
# file_path = input("Enter the file path: ")
# content = read_file_content(file_path)

# if content is not None:
#     print(f"File content: {content}")

# def separate_files(file_string):
#     files = [file.strip() for file in file_string.split(',')]
    
#     attach_txt = [file for file in files if file.endswith('.txt')]
#     attach_docx = [file for file in files if file.endswith('.docx')]

#     return attach_txt, attach_docx

# file_string = "hello.txt, chao.docx, tambiet.docx, seeyou.txt"
# attach_txt, attach_docx = separate_files(file_string)

# print("attach_txt =", attach_txt)
# print("attach_docx =", attach_docx)

# def getUserInfo():
#     Username = "Nguyen Cong Tuan <nctuan22@clc.fitus.edu.vn>"
#     Password = "123456"
#     MailServer = "127.0.0.1"
#     SMTP = "2225"
#     POP3 = "3335"
#     AuToload = 10

# def download_content_email_pop3(server_socket, email_id, num_id, save_folder):
#     server_socket.send(f"RETR {num_id}\r\n".encode())
#     response = receive_all(server_socket).decode()
#     response = response.splitlines()

#     email_info = {'Date': '', 'To': '', 'From': '', 'Agent': '', 'Subject': '', 'Content': ''}
#     mail_content = ''
#     for line in response:
#         if line.startswith('Date:'):
#             email_info['Date'] = line[6:-6].strip()
#         elif line.startswith('To:'):
#             start_index = line.find('<')
#             email_info['To'] = line[start_index + 1:-1].strip()
#         elif line.startswith('From:'):
#             start_index = line.find('<')
#             email_info['From'] = line[start_index + 1:-1].strip()
#         elif line.startswith('User-Agent:'):
#             email_info['Agent'] = line[11:].strip()
#         elif line.startswith('Subject:'):
#             email_info['Subject'] = line[8:].strip()
#             continue
        
#         if (email_info['Subject'] != ''):
#             mail_content += line + '\r\n'
    
#     content_start = mail_content.find('\r\n\r\n')
#     email_info['Content'] = mail_content[content_start:].strip()

#     content_end = email_info['Content'].find('\r\n.\r\n')
#     if content_end == -1:
#         content_end = email_info['Content'].find('--------------')
    
#     email_info['Content'] = email_info['Content'][:content_end].strip()

#     email_content = 'DATE: ' + email_info['Date'] + '\n' + 'USER_AGENT: ' + email_info['Agent'] + '\n\n' + 'TO: ' + email_info['To'] + '\n' \
#                   + 'FROM: ' + email_info['From'] + '\n\n' + 'Subject: ' + email_info['Subject'] + '\n\n' + 'Content: \n' + email_info['Content']

#     email_filename = os.path.join(save_folder, f"no_file_{email_id}")
#     with open(email_filename, 'w') as email_file:
#         email_file.write(email_content)
# Cc = "nctuan081004@gmail.com, nguyencongtuan0810@gmail.com".split((',', ' '))
# for cc in Cc:
#     print(cc)

# email_addresses = ['nguyencongtuan0810@gmail.com', 'nctuan081004@gmail.com']

# to_address = ', '.join(email_addresses)

# print(to_address)

# def get_Email_To(mails_address_to):
#     To = input("TO: ").split(',')
#     To = [email.strip() for email in To]
#     mails_address_to.extend(To)

# mails_address_to = []
# get_Email_To(mails_address_to)

# print(mails_address_to)

# if any(email.strip() for email in mails_address_to):
#     print("FULL")
# else:
#     print("EMPTY")




#     def save_status_of_mail(sender, subject, type):
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



# greeting = "Xin chao"
# intro = "Tuan"

# print(f"{greeting}, my name is {intro}")
# email = "nctuan@gmail/com"
# server_socket.send(b"'MAIL FROM: ' + email\r\n")





# def download_content_email_pop3(server_socket, num_id, SAVE_FOLDER):
#     server_socket.send(f"RETR {num_id}\r\n".encode())
#     response = receive_all(server_socket).decode()

#     email_info, sender, subject = extract_email_info(response)
    
#     #save_status_of_mail(sender, subject, 0)

#     email_filename = os.path.join(SAVE_FOLDER, f"no_file_{sender}, {subject}.msg")
#     with open(email_filename, 'w') as email_file:
#         email_file.write(email_info)

# def extract_email_info(response):
#     lines = response.splitlines()[1:]

#     second_boundary = False
#     meet_notice = False
#     email_info = ''
#     subject = ''
#     sender = ''

#     for line in lines:
#         if line.strip().startswith((NOTICE, NOTICE_1)):
#             meet_notice = True
#             continue
#         if line.strip().startswith(BOUNDARY) and not second_boundary:
#             second_boundary = True
#             continue
#         if line.strip().startswith(BOUNDARY) and (second_boundary or line.strip().startswith('.')):
#             break
#         if line.strip().startswith('.'):
#             break
#         if line.strip().startswith('From: '):
#             start_index = line.find('<') + 1
#             end_index = line.find('>', start_index)
#             sender += line[start_index:end_index].strip()
#         if line.strip().startswith('Subject: ') and meet_notice:
#             email_info += line
#             subject = line.strip()[9:]
#         elif line.strip().startswith('Subject: '):
#             email_info += line + '\n'
#             subject = line.strip()[9:]
#         else:
#             email_info += line + '\n'

#     return email_info, sender, subject

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
