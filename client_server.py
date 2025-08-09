import socket

def start_client():
    host = '127.0.0.1'  # Server's IP address (localhost)
    port = 5555         # Server's port

    # Create a socket connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Connected to the server. Type your messages below.")
    print("Type 'exit' to close the connection.\n")

    while True:
        message = input("You: ")

        if message.lower() == 'exit':
            print("Disconnected from server.")
            break

        client_socket.send(message.encode('ascii'))
        response = client_socket.recv(1024).decode('ascii')
        print(f"Server: {response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
