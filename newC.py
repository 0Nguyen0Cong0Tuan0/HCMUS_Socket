import socket

HEADER = 1024

def send_email(From, To, Cc, Bcc, subject, content):
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
        
        email_data = f"To: {To}\r\nFrom: {From}\r\nCC: {Cc}\r\nBCC: {Bcc}\r\nSubject: {subject}\r\n\r\n{content}\r\n"
        server_socket.sendall(f"{email_data}\r\n.\r\n".encode())
        response = server_socket.recv(HEADER).decode()
        if not response.startswith('250'):
            raise Exception(f"Error sending email: {response}")

def getUserInfo():
    Username = "Nguyen Cong Tuan <nctuan22@clc.fitus.edu.vn>"
    Password = "123456"
    MailServer = "127.0.0.1"
    SMTP = "2225"
    POP3 = "3335"
    AuToload = 10

def main():
    From = input("From: ")
    To = input("To: ")
    Cc = input("CC: ")
    Bcc = input("BCC: ")
    subject = input("Subject: ")
    content = input("content: ")
    #attach_files = input("Attack files (comma-separated): ").split(',')

    send_email(From, To, Cc, Bcc, subject, content)

if __name__ == "__main__":
    main()
