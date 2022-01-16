import socket

from client.client import Client

MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024


class Server:
    def __init__(self, public_ip, port, n_listen, state, run_):
        # take the ip: IPV4
        self.ip = socket.gethostbyname(socket.gethostname() + '.local')
        #used for connect a "close_server" client
        self.public_ip = public_ip
        self.port = port
        # create the socket server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bound the ip and the port to the socket server
        self.server_socket.bind((self.ip, self.port))
        # declarate the comunication socket that is returned by socket.accept()
        self.comunication_socket = None
        self.ip_comunication = None
        
        self.buffer_size = BUFFER_SIZE
        # create a list for the active connections
        self.active_connections = []
        # contain the max number of connection
        self.n_listen = n_listen
        # counter for connections
        self.connections_count = 0
        # take care of the server status TRUE: LISTEN FALSE: NOT LISTEN
        self.state_listening = state
        self.run = run_
    
    def accept(self):
        self.server_socket.listen(self.n_listen)
        
        self.comunication_socket, self.ip_comunication = self.server_socket.accept()
        self.connections_count += 1
        
    def get_active(self):
        return self.connections_count

    def close(self):
        self.run = False
        # create a temp_client that connect to the server and stop it
        Client(self.public_ip, self.port, self.buffer_size).connect()

    def get_status_listen(self):
        return self.state_listening

    def set_status(self):
        if self.connections_count < self.n_listen:
            self.state_listening = True
        else:
            self.state_listening = False

    def set_run(self, bool_):
        self.run = bool_
        
    def get_run(self):
        return self.run

            