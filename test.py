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

def get_Attached_File():
    attach_files_path = []
    files_input = input("Attach files: ").split(',')
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

def attach_file_in_email(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as at:
            file_content = at.read()

            file_content_encode = base64.b64encode(file_content).decode()

            attachment_header = "\r\nContent-Type: application/octet-stream" \
                               f"\r\nContent-Disposition: attachment; filename=\"{os.path.basename(file_path)}\"" \
                               "\r\nContent-Transfer-Encoding: base64\r\n\r\n"
            return attachment_header + file_content_encode + "\r\n"
    else:
        print("The file does not exist")
        return ""

def run_send_mail_program():
    attach_files_path = get_Attached_File()

    for path in attach_files_path:
        hello = attach_file_in_email(path)
        print(hello)

    


run_send_mail_program()

