import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('ascii')
                if not message:
                    break

                print(f"Client: {message}")

                if message.lower() == 'hello':
                    response = "Hi there! How can I help you?"
                elif message.lower() == 'how are you?':
                    response = "I'm good, thanks."
                elif message.lower() == 'what is your name?':
                    response = "I'm Group Prime"
                else:
                    response = input("Group Prime: ")

                client_socket.send(response.encode('ascii'))

            except Exception as e:
                print(f"Error: {e}")
                break

        client_socket.close()

    def start(self):
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connected to {address}")

            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket,)
            )
            client_thread.start()

# Entry point
if __name__ == "__main__":
    server = Server("127.0.0.1", 5555)
    server.start()
