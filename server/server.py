import socket

from client.client import Client
from utils.utils import TypeOfMessages, get_value
from user.user import BannedUser


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
        self.buusertive_connections = []
        # contain the max number of connection
        self.n_listen = n_listen
        # counter for connections
        self.conn_count = 0
        # take care of the server status TRUE: LISTEN / FALSE: NOT LISTEN
        self.state_listening = state
        # True: The server is running / False: the server is not running
        self.run = run_
        # a list that contain all the comunications sockets with the clients
        self.users_list = []
        # wait tiem before closing the connection (2.30 minutes)
        self.wait_time = 150
        # buffer size
        self.buffer_size = 1024
        # list of the banned clients
        self.black_list = []
        # temp kicked user used for the print
        self.kicked_user = None
        # temp banned user used for the print
        self.banned_user = None
    
    def accept(self):
        self.server_socket.settimeout(None)
        self.server_socket.listen(self.n_listen)
        return self.server_socket.accept()
    
    def get_active(self):
        return self.conn_count

    def close(self):
        # close the server socket
        self.server_socket.close()

    def conn_close_client(self):
        # create a temp_server_socketlient that connect to the server and stop it
        t_client = Client(self.public_ip, self.port, self.buffer_size, None)
        t_client.connect()
        # send a disconnect message to the server
        t_client.send(get_value(TypeOfMessages.DisconnectMessage))
    
    def test_accept(self):
        self.server_socket.settimeout(2)
        self.server_socket.listen(self.n_listen)
        self.server_socket.accept()
        # reset
        self.server_socket.settimeout(None)

    def test_connection(self):
        # create a temp client to check it the connection is possible
        t_client = Client(self.public_ip, self.port, self.buffer_size, None)
        t_client.client_socket.settimeout(3)
        t_client.connect()
    
        t_client.client_socket.settimeout(None)
        t_client.close()
        
    def close_connections(self, active):
        # if there are still active connections
        if active:
            # disconnect all the clients
            self.disconecct_all()
        else:
            self.run = False
            self.conn_close_client()

    def disconecct_all(self):
        for i in range(len(self.users_list)):
            if self.users_list[i]:
                # we have to encode this because we are not using our Clients class but socket class
                self.users_list[i].conn_socket.send(get_value(TypeOfMessages.ServerExit).encode('utf-8'))
                self.users_list[i].conn_socket.close()
        
        self.conn_count = 0
    
    def add_conn(self, user):
        add = False
        for i in range(len(self.users_list)):
            if not self.users_list[i]:
                self.users_list[i] = user
                add = True
                break
    
        if not add:
            self.users_list.append(user)

    # check if there is an ip in the blacklist
    def check_blacklist(self, ip):
        for i in range(len(self.black_list)):
            if self.black_list[i]:
                if self.black_list[i].ip == ip:
                    return True
        return False
    
    # send a msg to all the clients
    def send_all(self, msg):
        for i in range(len(self.users_list)):
            if self.users_list[i]:
                if len(self.users_list) > 1:
                    # send the message to all the clients
                    self.users_list[i].conn_socket.send(msg.encode('utf-8'))
            
    def get_status_listen(self):
        return self.state_listening

    def set_status(self):
        if self.conn_count < self.n_listen:
            self.state_listening = True
        else:
            self.state_listening = False
            
    # check if the user exist
    def check_user(self, nick):
        for i in range(len(self.users_list)):
            if self.users_list[i]:
                if self.users_list[i].get_nick() == nick:
                    return i
                
        return -1
    
    # kick the user
    def kick_user(self, index):
        # send a message to him "!KICK"
        self.users_list[index].conn_socket.send(get_value(TypeOfMessages.Kick).encode('utf-8'))
        # free the space for another client
        self.users_list[index] = 0
                
    def check_nick(self, nick):
        # check if there is another user with the same nickname
        for i in range(len(self.users_list)):
            if self.users_list[i]:
                if self.users_list[i].get_nick() == nick:
                    # return True (the user exist)
                    return True
                
        # else the user doesn't exist so it's ok
        return False

    # check if there is the ip that he want to ban / pardon
    def check_ip(self, ip, ban_mode):
        # if he want to search in the blacklist
        if ban_mode:
            for i in range(len(self.black_list)):
                if self.black_list[i]:
                    if self.black_list[i].get_ip() == ip:
                        return i
            return -1
        # if he want to search in the userslist
        else:
            for i in range(len(self.users_list)):
                if self.users_list[i]:
                    if self.users_list[i].get_ip() == ip:
                        return i
            return -1
        
    # ban the ip at the given index
    def ban_ip(self, index, ip):
        # check for free position
        for i in range(len(self.black_list)):
            # if there is a free position
            if not self.black_list[i]:  
                self.addBanned(BannedUser(ip, self.users_list[index].get_nick()), i, index)
                break
        
        # else there aren't free places
        self.addBanned(BannedUser(ip, self.users_list[index].get_nick()), -1, index)
    
    def addBanned(self, banned, indexBanned, indexUser):
        # if there are free places 
        if indexBanned != -1:
            self.black_list[indexBanned] = banned

        # else there aren't free places append
        else:
            self.black_list.append(banned)

        # send the BAN message
        self.users_list[indexUser].conn_socket.send(get_value(TypeOfMessages.Ban).encode('utf-8'))   
        # save the temp banned user nickname     
        self.banned_user = self.users_list[indexUser].get_nick()
        # free a space in the users_list
        self.users_list[indexUser] = 0   
                 
    # pardon the banned ip
    def pardon_ip(self, index):
        self.black_list[index] = 0
