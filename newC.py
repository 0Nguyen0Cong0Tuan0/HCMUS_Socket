import socket

HEADER = 1024
SENDER = "<nctuan22@clc.fitus.edu.vn>"

def send_email(to, cc, bcc, subject, content):
    with socket.create_connection(("127.0.0.1", 2225)) as server_socket:
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('220'):
            raise Exception(f"Error connecting to server: {response}")
        
        server_socket.send("EHLO [127.0.0.1]\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending EHLO: {response}")
        
        server_socket.send(f"MAIL FROM: {SENDER}".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")
        
        server_socket.send(f"RCPT TO: {SENDER}".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending mail address: {response}")
        
        server_socket.send("DATA".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('354'):
            raise Exception(f"Error sending data: {response}")
        
        email_data = f"From: {SENDER}\r\nTo: {to}\r\nCc: {cc}\r\nBcc: {bcc}\r\nSubject: {subject}\r\n\r\n{content}\r\n"
        #for file_path in attach_files:
            #with open(file_path, 'rb') as attachment:
                #email_data += f"Content-Type: application/octet-stream\r\nContent-Disposition: attachment; filename=\"{os.path.basename(file_path)}\"\r\n\r\n"
                #email_data += attachment.read() + b'\r\n'
        server_socket.sendall(f"MAIL FROM: {SENDER}\r\nRCPT TO: {to}\r\nDATA\r\n{email_data}\r\n.\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending email: {response}")

def getUserInfo():
    Username = "Nguyen Cong Tuan <nctuan22@clc.fitus.edu.vn>"
    Password = "123456"
    MailServer = "127.0.0.1"
    SMTP = "2225"
    POP3 = "3335"
    Autoload = 10

def main():
    to = input("TO: ")
    cc = input("CC: ")
    bcc = input("BCC: ")
    subject = input("Subject: ")
    content = input("content: ")
    #attach_files = input("Attack files (comma-separated): ").split(',')

    send_email(to, cc, bcc, subject, content)

if __name__ == "__main__":
    main()
