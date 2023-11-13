import socket

HEADER = 1024

def send_email(to, cc, bcc, subject, content, attach_files):
    with socket.create_connection(("127.0.0.1", 2225)) as server_socket:
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('220'):
            raise Exception(f"Error connecting to server: {response}")

def getUserInfo():
    Username = "Nguyen Cong Tuan <nctuan22@clc.fitus.edu.vn>"
    Password = "123456"
    MailServer = "127.0.0.1"
    SMTP = "2225"
    POP3 = "3335"
    Autoload = 10

def getReceiverInfo():
    to = input("TO: ")
    cc = input("CC: ")
    bcc = input("BCC: ")
    subject = input("Subject: ")
    content = input("content: ")
    attach_files = input("Attack files (comma-separated): ").split(',')

    send_email(to, cc, bcc, subject, content, attach_files)