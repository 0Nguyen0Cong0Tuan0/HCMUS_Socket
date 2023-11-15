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

def separate_files(file_string):
    files = [file.strip() for file in file_string.split(',')]
    
    attach_txt = [file for file in files if file.endswith('.txt')]
    attach_docx = [file for file in files if file.endswith('.docx')]

    return attach_txt, attach_docx

file_string = "hello.txt, chao.docx, tambiet.docx, seeyou.txt"
attach_txt, attach_docx = separate_files(file_string)

print("attach_txt =", attach_txt)
print("attach_docx =", attach_docx)

# def getUserInfo():
#     Username = "Nguyen Cong Tuan <nctuan22@clc.fitus.edu.vn>"
#     Password = "123456"
#     MailServer = "127.0.0.1"
#     SMTP = "2225"
#     POP3 = "3335"
#     AuToload = 10
