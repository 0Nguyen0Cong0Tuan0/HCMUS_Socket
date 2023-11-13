import socket

HEADER = 1024

def getEmailTo(mails_address_to):
    To = input("To: ")
    mails_address_to.append(To)

def getEmailCc(mails_address_cc):
    Cc = input("CC: ")
    Cc = Cc.split(',')
    Cc = [email.strip() for email in Cc]
    mails_address_cc.extend(Cc)
    
def getEmailBcc(mails_address_bcc):
    Bcc = input("BCC: ")
    Bcc = Bcc.split(',')
    Bcc = [email.strip() for email in Bcc]
    mails_address_bcc.extend(Bcc)

def send_email_to(From, To, subject, content):
    with socket.create_connection(("127.0.0.1", 2225)) as server_socket:
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('220'):
            raise Exception(f"Error connecting To server: {response}")
        
        server_socket.send("EHLO [127.0.0.1]\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending EHLO: {response}")
        
        server_socket.send(f"MAIL FROM:<{From}>\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")
        
        server_socket.send(f"RCPT TO:<{To}>\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")
        
        server_socket.send("DATA\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('354'):
            raise Exception(f"Error sending data: {response}")
        
        email_data = f"To: {To}\r\nFrom: {From}\r\nSubject: {subject}\r\n\r\n{content}\r\n"
        server_socket.sendall(f"{email_data}\r\n.\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending email: {response}")

def send_email_cc(From, Cc, mails_address_cc, subject, content):
    with socket.create_connection(("127.0.0.1", 2225)) as server_socket:
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('220'):
            raise Exception(f"Error connecting To server: {response}")
        
        server_socket.send("EHLO [127.0.0.1]\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending EHLO: {response}")
        
        server_socket.send(f"MAIL FROM:<{From}>\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")
        
        server_socket.send(f"RCPT TO:<{Cc}>\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")
        
        server_socket.send("DATA\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('354'):
            raise Exception(f"Error sending data: {response}")
        
        email_data = f"CC: {mails_address_cc}\r\nFrom: {From}\r\nSubject: {subject}\r\n\r\n{content}\r\n"
        server_socket.sendall(f"{email_data}\r\n.\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending email: {response}")

def send_email_bcc(From, Bcc, subject, content):
    with socket.create_connection(("127.0.0.1", 2225)) as server_socket:
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('220'):
            raise Exception(f"Error connecting To server: {response}")
        
        server_socket.send("EHLO [127.0.0.1]\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending EHLO: {response}")
        
        server_socket.send(f"MAIL FROM:<{From}>\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")
        
        server_socket.send(f"RCPT TO:<{Bcc}>\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")
        
        server_socket.send("DATA\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('354'):
            raise Exception(f"Error sending data: {response}")
        
        email_data = f"BCC: {Bcc}\r\nFrom: {From}\r\nSubject: {subject}\r\n\r\n{content}\r\n"
        server_socket.sendall(f"{email_data}\r\n.\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending email: {response}")

def run_send_mail_program():
    mails_address_to = []
    mails_address_cc = []
    mails_address_bcc = []

    From = input("From: ")

    getEmailTo(mails_address_to)
    getEmailCc(mails_address_cc)
    getEmailBcc(mails_address_bcc)
   
    subject = input("Subject: ")
    content = input("Content: ")
    #attach_files = input("Attack files (comma-separated): ").split(',')

    for To in mails_address_to:
        send_email_to(From, To, subject, content)

    for Cc in mails_address_cc:
        send_email_cc(From, Cc, subject, content)

    for Bcc in mails_address_bcc:
        send_email_bcc(From, Bcc, subject, content)


# def getUserInfo():
#     Username = "Nguyen Cong Tuan <nctuan22@clc.fitus.edu.vn>"
#     Password = "123456"
#     MailServer = "127.0.0.1"
#     SMTP = "2225"
#     POP3 = "3335"
#     AuToload = 10

def main():
    run_send_mail_program()
    

if __name__ == "__main__":
    main()
