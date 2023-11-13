import socket

HEADER = 10000
PORT = 1234
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'BYE'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_and_receive(message):
    client.send(message.encode(FORMAT))
    print(client.recv(HEADER).decode(FORMAT))


def main():
    initial_message = client.recv(HEADER).decode(FORMAT)
    print(initial_message)

    while True:
        message_client = input("[Client]: ")
        if message_client == DISCONNECT_MESSAGE:
            print("Disconnected to server!")
            send_and_receive(message_client)
            break        
        else:
            send_and_receive(message_client)


    client.close()

if __name__ == "__main__":
    main()