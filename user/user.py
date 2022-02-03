class User:
    def __init__(self, conn_socket, ip, nick):
        self.conn_socket = conn_socket
        self.ip = ip
        self.nick_name = nick
    
    def get_nick(self):
        return self.nick_name
    
    def get_ip(self):
        return self.ip[0]
    