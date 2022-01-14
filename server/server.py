import socket, sys

GREEN = "\u001b[32m"
RESET = "\u001b[0m"
MAGENTA = "\u001b[35m"
RED = "\u001b[31m"

MAX_CONNECTIONS = 10
BUFFER_SIZE = 1024

class Server:
    def __init__(self, port, n_listen):
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

    def connect(self):
        self.server_socket.listen(self.n_listen)

        # wait for incoming connection
        self.comunication_socket, self.ip_comunication = self.server_socket.accept()
        self.connections_count += 1

    def get_active(self):
        return self.connections_count

    def close(self):
        self.server_socket.close()


def create_server():
    try:
        port = int(input("\nPort: "))
        
        n_connection = 11
        while n_connection > 10 or n_connection < 1:
            n_connection = int(input("\nNumber of max connections (max: 10 / min: 1): "))
        
        # create and return the istance of Server()
        return Server(port, n_connection)

    except KeyboardInterrupt:
        print(f"\n\n{GREEN}Byeeee :){RESET}\n")
        sys.exit()


def show_active(server):
    print(f"\n{GREEN}Active Connections: {server.get_active()}{RESET}")


def menu(server):
    while True:
        opt = int(input(f"\n1)Show Active Connections\n2)Close Server\n\n{MAGENTA}>>{RESET}"))
        
        # show the active connections
        if(opt == 1):
            show_active(server)
            
        elif(opt == 2):
            if server.get_active(): # if there are still active connections
                temp = input(f"\n{RED}Warning: There are still {server.get_active()} active connections!  Are you sure(y / n): {RESET}")

                if(temp == "y" or temp == "yes" or temp == "YES" or temp == "Y"):
                    print(f"\n{GREEN}Closing the server{RESET}\n")
                    return 0
                    
                else:
                    print(f"\n{GREEN}Great Answer :){RESET}\n")
            
            else:
                print(f"\n{GREEN}Closing the server{RESET}\n")
                return 0
            
        else:
            print(f"\n{RED}Enter an existing option :){RESET}\n")


def server_main():
    try:
        server = create_server()
        print(f"\n{GREEN}Server is listening for new connections!{RESET}\n") 
  
        while True:
            # wait for incoming connections
            server.connect()
            
            if not menu(server):
                server.close()
                break
        
        sys.exit(0)
    except KeyboardInterrupt:
            print(f"\n\n{GREEN}Byeee :){RESET}\n")
            sys.exit()

server_main()