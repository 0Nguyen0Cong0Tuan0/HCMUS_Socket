import socket
import threading

HEADER = 10000
PORT = 1234
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'BYE'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION]: {addr} CONNECTED.")
    conn.send(f"[Server]: {response()}".encode(FORMAT))

    while True:
        msg = conn.recv(HEADER).decode(FORMAT)

        if msg == DISCONNECT_MESSAGE:
            print(f"[CLIENT]: {addr} has disconnected.")
            break
        else:
            print(f"[CLIENT]: {msg}")

        conn.send(f"[Server]: {response()}".encode(FORMAT))

    conn.close()

def response():
    return input("[Server]: ")

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    print("Waiting for connection.....")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def main():
    start()

if __name__ == "__main__":
    main()
