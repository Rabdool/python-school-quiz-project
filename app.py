import socket

class App:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run_server(self):
        self.sock.bind((self.host, self.port))
        print("socket has been bind")
        self.sock.listen()
        print(f"listening on port: {self.port}")
        client, addr = self.sock.accept()
        print(f"Accepted connection from {addr}")

        while True:
            recieved_message = client.recv(1024).decode()
            print(recieved_message)
            break
    def run_client(self):
        self.sock.connect((self.host, self.port))
        message = input("Enter message: ").strip()
        self.sock.send(message.encode("utf-8"))
    