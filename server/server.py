import socket, threading

from client.client import Client
from utils.utils import TypeOfMessages, get_value

MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024


class Server:
    def __init__(self, private_ip, public_ip, port, n_listen, state, run_):
        # take the ip: IPV4
        self.ip = private_ip
        #used for connect a "close_server" client
        self.public_ip = public_ip
        self.port = port
        # create the socket server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bound the ip and the port to the socket server
        self.server_socket.bind((self.ip, self.port))  
        self.buffer_size = BUFFER_SIZE
        # create a list for the active connections
        self.active_connections = []
        # contain the max number of connection
        self.n_listen = n_listen
        # counter for connections
        self.connections_count = 0
        # take care of the server status TRUE: LISTEN / FALSE: NOT LISTEN
        self.state_listening = state
        # True: The server is running / False: the server is not running
        self.run = run_
        # a list that contain all the comunications sockets with the clients
        self.client_list = []

    def accept(self):
        self.server_socket.listen(self.n_listen)
        return self.server_socket.accept()
        
    def get_active(self):
        # -2 because we exclude the "main" thread and the "connectios_thread"
        return threading.activeCount() - 2

    def shutdown(self):
        # close the server socket
        self.server_socket.close()

    def conn_close_client(self):
        # create a temp_client that connect to the server and stop it
        t_client = Client(self.public_ip, self.port, self.buffer_size)
        t_client.connect()
        t_client.send(get_value(TypeOfMessages.DISCONNECT_MESSAGE))

    def close(self, active):
        # if there are still active connections
        if active:
            # disconnect all the clients
            self.disconecct_all()
        else:
            self.run = False
            self.conn_close_client()
        
    def disconecct_all(self):
        for s_client in self.client_list:
            # we have to encode this because we are not using our Clients class but socket class
            s_client.send(get_value(TypeOfMessages.SERVER_EXIT).encode('utf-8'))
            s_client.close()

    def get_status_listen(self):
        return self.state_listening

    def set_status(self):
        if (threading.activeCount() - 2) < self.n_listen:
            self.state_listening = True
        else:
            self.state_listening = False
            