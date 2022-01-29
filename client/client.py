import socket


class Client:
    def __init__(self, ip, port, buffer_size):
        self.ip = ip
        self.port = port
        # create the client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.buffer_size = buffer_size
        self.wait_time = 10
        
        self.connected = None

    def connect(self):
        # set timeout for connection
        self.client_socket.settimeout(self.wait_time)
        # try to connect to the server
        self.client_socket.connect((self.ip, self.port))
        # if connect stop the timeout
        self.client_socket.settimeout(None)

    def recv(self):
        return self.client_socket.recv(self.buffer_size).decode('utf-8')
    
    def send(self, msg):
        self.client_socket.send(msg.encode('utf-8'))
        
    def close(self):
        self.client_socket.close()

    def set_connected(self, state):
        self.connected = state
        
