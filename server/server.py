from shutil import ExecError
import socket, sys

from colors.colors import Colors as colors

MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024


class Server:
    def __init__(self, port, n_listen, state):
        # take the ip: IPV4
        self.ip = socket.gethostbyname(socket.gethostname() + '.local')
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
        self.state = state

    def accept(self):
        try:
            self.server_socket.listen(self.n_listen)
            
            self.comunication_socket, self.ip_comunication = self.server_socket.accept()
            self.connections_count += 1
        
        except KeyboardInterrupt:
            self.server_socket.close()
            print(f"\n\n{colors.GREEN}Byee :)\n{colors.RESET}")    
            sys.exit(0)
    
    def get_active(self):
        return self.connections_count

    def close(self):
        try:
            self.server_socket.close()

        except KeyboardInterrupt:
            sys.exit(0)
    
    def get_status(self):
        try:
            return self.state

        except KeyboardInterrupt:
            sys.exit(0)
            
    def set_status(self):
        if self.get_active() < self.n_listen - 1:
            self.state = True
            
        else:
            self.state = False
            