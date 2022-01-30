import sys, os, threading, socket

from server.server import Server
from utils.utils import Colors as colors, print_logo_server, get_value
from client.c_main import TypeOfMessages
from client.client import Client

DEFAULT_CONNECTIONS = 10
DISCONNECT_MESSAGE = "!DISCONNECT"

def get_info():
    max_connections, max_port = DEFAULT_CONNECTIONS + 1, 0
    
    try:
        private_ip = input(f"{colors.YELLOW}{colors.BOLD}Host Ip: ")

        public_ip = input(f"\nPublic Ip: ") 

        try:
            while max_connections > DEFAULT_CONNECTIONS or max_connections < 1:
                max_connections = int(input(f"\nConnections (max: {DEFAULT_CONNECTIONS}/min: 1): "))
        except ValueError:
            print(f"\n{colors.RESET}{colors.RED}{colors.BOLD}Connections can not be empty/int!!\n{colors.RESET}")
            sys.exit(0)
            
        try:
            while max_port < 4500 or max_port > 9999:
                max_port = int(input("\nPort (max: 9999 / min: 4500): "))
        except ValueError:
            print(f"\n{colors.RESET}{colors.RED}{colors.BOLD}Port can not be empty/string !!{colors.RESET}\n")
            sys.exit(0)
            
    except KeyboardInterrupt:
        sys.exit(0)
    
    return (private_ip, public_ip, max_connections, max_port)


def check_server(info):
    # try to create the server
    try:    
        # create and return the istance of Server()
        return Server(info[0], info[1], info[3], info[2], True, True) 
    
    except socket.gaierror:
        print(f"\n{colors.RESET}{colors.RED}{colors.BOLD}Can not host a server on port: {info[3]}, Host Ip: {info[0]}, Public Ip: {info[1]}{colors.RESET}\n")
        sys.exit(0)
    
    except PermissionError:
        print(f"\n{colors.RESET}{colors.RED}{colors.BOLD}Permission Denied: Can not host a server on port: {info[3]}{colors.RESET}\n")
        sys.exit(0)
        
    except OSError as error:
        print(f"\n{colors.RESET}{colors.RED}{colors.BOLD}Impossibile to host a server on port: {info[3]} {error}{colors.RESET}\n")
        sys.exit(0)   


def create_server():
    print_logo_server()
    
    info = get_info()
    os.system('cls||clear')
    
    return check_server(info)


def show_active(server):
    print(f"\n{colors.GREEN}Active Connections: {server.get_active()}{colors.RESET}")
    
    
def take_option():
    while True:
        try:
            opt = int(input(f"1)Show Active Connections\n2)Close Server\n\n{colors.BLU}{colors.BOLD}>> {colors.RESET}"))
            return opt
        
        except ValueError:
            print(f"\n{colors.RED}Option can not be empty/string!!{colors.RESET}\n")
            

def close(server):
    if server.get_active(): # if there are still active connections
        temp = input(f"\n{colors.RED}Warning: There are still {server.get_active()} active connections!  Are you sure(y / n): {colors.RESET}")

        if(temp == "y" or temp == "yes" or temp == "YES" or temp == "Y"):
            # first disconnect all the clients
            server.close(True)
            return True
        else: 
            return False

    else: # else there aren't active connections, close the server
        server.close(False)
        return True
        
        
def menu(server):
    while True:   
        try:  
            if server.get_status_listen():
                print(f"{colors.RESET}\nStatus Server: {colors.GREEN}{colors.BOLD}Listening{colors.RESET}\n")
            else:
                print(f"\nStatus Server: {colors.RED}{colors.BOLD}Not Listening{colors.RESET}\n")    
                    
            opt = take_option()
                
            # show the active connections
            if(opt == 1):
                show_active(server)
                
            # close the server
            elif(opt == 2):
                if close(server):
                    return False
            
            else:   # default
                print(f"\n{colors.RED}Enter an existing option :){colors.RESET}\n")

        except KeyboardInterrupt:
            # if there are active connections
            if server.get_active():
                server.close(True)
            else:
                server.close(False)
            return False


def handle_clients(server, conn, ip):
    if server.run:
        # add the comunication socket to the list
        server.client_list.append(conn)
        # calculate the index that will be used for del
        index = (threading.activeCount() - 2) - 1

    while server.run:
        # wait for incoming messages
        msg = conn.recv(1024).decode('utf-8')
        # if the the message is "!DISCONNECT": disconnect the client and delete his comunication socket from the list
        if msg == get_value(TypeOfMessages.DISCONNECT_MESSAGE):
            # send the "!DISCONNECT" message to the client to confirm
            conn.send(get_value(TypeOfMessages.DISCONNECT_MESSAGE).encode('utf-8'))
            print(f"\n{colors.GREEN}{colors.BOLD}The client {colors.RESET}{colors.YELLOW}{colors.BOLD}{ip[0]}{colors.RESET}{colors.GREEN}{colors.BOLD} has just left the chat\n{colors.RESET}")
                        
            break
        # when the client receive the message "!QUIT", they resend to the server to confirm and after they quit
        elif msg == get_value(TypeOfMessages.SERVER_EXIT):
            break
    
    conn.close()
    if server.run:
        del server.client_list[index]
    

def accept_connections(server):
    # if the server is listening and is running
    while server.run:
        conn, ip = server.accept()
        # set the status Listening/No Listening
        server.set_status()

        # create a thread to comunicate with the single client    
        threading.Thread(target=handle_clients, args=(server, conn, ip)).start()
    

def server_main():
    server = create_server()
    
    # create a thread for server.accept() because stop the program
    threading.Thread(target=accept_connections, args=(server,)).start()

    while menu(server):
        pass
    
    # close the server with the "close_client"
    server.close(False)
    # close the socket server
    server.shutdown()
    sys.exit(0)
