import socket, sys, os
import threading

GREEN = "\u001b[32m"
RESET = "\u001b[0m"
MAGENTA = "\u001b[35m"
RED = "\u001b[31m"
YELLOW = "\u001b[33m"
BLU = "\033[94m"

BOLD = "\033[1m"

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

    def accept_connections(self):
        self.server_socket.listen(self.n_listen)
        
        self.comunication_socket, self.ip_comunication = self.server_socket.accept()
        self.connections_count += 1
            
    def get_active(self):
        return self.connections_count

    def close(self):
        self.server_socket.close()

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
            
def print_logo():
    os.system('cls||clear')
    print(f"""\n{MAGENTA}{BOLD}
         ██████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
        ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
        ╚█████╗ █████╗  ██████╔╝╚██╗ ██╔╝█████╗  ██████╔╝
         ╚═══██╗██╔══╝  ██╔══██╗ ╚████╔╝ ██╔══╝  ██╔══██╗
        ██████╔╝███████╗██║  ██║  ╚██╔╝  ███████╗██║  ██║
        ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝\n\n{RESET}""")

def create_server():
    print_logo()
    port = 0
    try:
        port = int(input(f"\n{YELLOW}{BOLD}Port: "))
        
        n_connection = 11
  
        while n_connection > 10 or n_connection < 1:
            n_connection = int(input(f"\n{YELLOW}{BOLD}Connections Number(max: 10 / min: 1): "))
    
    except KeyboardInterrupt:
        print(f"\n\n{RESET}{GREEN}Byeeee :){RESET}\n")
        sys.exit(0)

    except ValueError:
        print(f"\n{RESET}{RED}Port/Number Connections can not be empty/string !!{RESET}\n")
        sys.exit(0)
    
    # try to create the server
    try:    
        os.system('cls||clear')
        # create and return the istance of Server()
        return Server(port, n_connection, True) 
    
    except PermissionError:
        print(f"\n\n{RESET}{RED}Permission Denied: Can not host a server on port: {port}{RESET}\n")
        sys.exit(0)
        

def show_active(server):
    print(f"\n{GREEN}Active Connections: {server.get_active()}{RESET}")
    

def menu(server):
    while True:
        
        try:
            if server.get_status():
                print(f"{RESET}\nStatus Server: {GREEN}{BOLD}Listening{RESET}\n")
            else:
                print(f"\nStatus Server: {RED}{BOLD}Not Listening{RESET}\n")
                
            opt = int(input(f"1)Show Active Connections\n2)Close Server\n\n{BLU}{BOLD}>> {RESET}"))
            
            # show the active connections
            if(opt == 1):
                show_active(server)
            
            # close the server
            elif(opt == 2):
                if server.get_active(): # if there are still active connections
                    temp = input(f"\n{RED}Warning: There are still {server.get_active()} active connections!  Are you sure(y / n): {RESET}")

                    if(temp == "y" or temp == "yes" or temp == "YES" or temp == "Y"):
                        print(f"\n{GREEN}Closing the server, press {RESET}{YELLOW}{BOLD}Ctrl + C{RESET} {GREEN}to stop the server{RESET}\n")
                        server.close()
                        return
                        
                    else:
                        print(f"\n{GREEN}Great Answer :){RESET}\n")
                
                else:
                    print(f"\n{GREEN}Closing the server, press {RESET}{YELLOW}Ctrl + C {RESET}{GREEN}to stop the server{RESET}\n")
                    
                    server.close()
                    return
            else:
                print(f"\n{RED}Enter an existing option :){RESET}\n")

        except KeyboardInterrupt:
            server.close()
            sys.exit(0)

        except ValueError:
            server.close()
            sys.exit(0)
            
        
def server_main():
    server = create_server()
    
    #start the menu thread
    threading.Thread(target=menu, args=(server,)).start()
    while True:
        if server.get_status():
            # wait for incoming connections
            server.accept_connections()
            server.set_status()
        
            
server_main()