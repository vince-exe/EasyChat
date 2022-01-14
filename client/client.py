import socket, sys

GREEEN = "\u001b[32m"
RESET = "\u001b[0m"

class Client:
    def __init__(self, ip, port, buffer_size):
        self.ip = ip
        self.port = port
        # create the client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.buffer_size = buffer_size
    
    def connect(self):
        try:
            # try to connect...
            self.client_socket.connect((self.ip, self.port))
        
        except KeyboardInterrupt:
            print(f"\n\n{GREEEN}Byee :){RESET}\n")
            sys.exit(0)
    
    def recv(self):
            return self.client_socket.recv(self.buffer_size).decode('utf-8')
    
    def send(self, msg):
        self.client_socket.send(msg.encode('utf-8'))

    def close(self):
        self.client_socket.close()


def client_main():
    client = Client("213.45.54.55", 7000, 1024)
    
    client.connect()
    print(f"\n{GREEEN}Connection established with the server{RESET}")
    
    while True:
        pass

client_main()