import socket, sys

from colors.colors import Colors as colors



class Client:
    def __init__(self, ip, port, buffer_size):
        self.ip = ip
        self.port = port
        # create the client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.buffer_size = buffer_size
    
    def connect(self):
        # try to connect...
        try:
            self.client_socket.connect((self.ip, self.port))
        
        except KeyboardInterrupt:
            print(f"\n\n{colors.GREEEN}Byee :){colors.RESET}\n")
            sys.exit(0)   
        
        except ConnectionRefusedError:
            print(f"\n{colors.RED}Connections refused from the server!!{colors.RESET}\n")
            sys.exit(0)
        
    def recv(self):
            return self.client_socket.recv(self.buffer_size).decode('utf-8')
    
    def send(self, msg):
        self.client_socket.send(msg.encode('utf-8'))

    def close(self):
        self.client_socket.close()

