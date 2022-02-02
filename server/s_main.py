from sqlite3 import Time
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
        return Server(info[0], info[1], info[3], info[2], True, True)

    except socket.timeout:
        print(f"\n{colors.RED}{colors.BOLD}Impossible host the server on the given info{colors.RESET}\n")
        sys.exit(0)

    except socket.gaierror:
        print(f"\n{colors.RED}{colors.BOLD}Impossible host the server on the given info{colors.RESET}\n")
        sys.exit(0)
    
    except PermissionError:
        print(f"\n{colors.RED}{colors.BOLD}Permission Denied: Can not host a server on port: {info[3]}{colors.RESET}\n")
        sys.exit(0)
        
    except OSError:
        print(f"\n{colors.RED}{colors.BOLD}Impossible host the server on the given info{colors.RESET}\n")
        sys.exit(0)   


def create_server():
    print_logo_server()
    
    info = get_info()
    os.system('cls||clear')
    
    return check_server(info)


def show_active(server):
    print(f"\n{colors.GREEN}Active Connections: {server.get_active()}\tMax Connections: {server.n_listen}{colors.RESET}")
    
    
def take_option():
    while True:
        try:
            opt = int(input(f"1)Show Active Connections\n2)Close Server\n3)Clear\n\n{colors.BLU}{colors.BOLD}>> {colors.RESET}"))
            return opt
        
        except ValueError:
            print(f"\n{colors.RED}Option can not be empty/string!!{colors.RESET}\n")
            

def close(server):
    try:
        if server.get_active(): # if there are still active connections
            temp = input(f"\n{colors.RED}Warning: There are still {server.get_active()} active connections!  Are you sure(y / n): {colors.RESET}")

            if(temp == "y" or temp == "yes" or temp == "YES" or temp == "Y"):
                # first disconnect all the clients
                server.close_connections(True)
                return True
            else: 
                return False

        else: # else there aren't active connections, close the server
            server.close_connections(False)
            return True
    
    except KeyboardInterrupt:
        server.close_connections(True)
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
            
            elif(opt == 3):
                os.system('cls||clear')

            else:   # default
                print(f"\n{colors.RED}Enter an existing option :){colors.RESET}\n")

        except KeyboardInterrupt:
            # if there are active connections
            if server.get_active():
                server.close_connections(True)
            else:
                server.close_connections(False)
            return False


def handle_clients(server, conn, ip, ser_full):
    # if the server is not full
    if not ser_full:
        if server.run:
            # add the comunication socket to the list
            server.add_conn(conn)
            # calculate the index that will be used for del
            index = (threading.activeCount() - 2) - 1

        while server.run:
            # wait for incoming messages
            msg = conn.recv(1024).decode('utf-8')
            # if the the message is "!DISCONNECT": disconnect the client and delete his comunication socket from the list
            if msg == get_value(TypeOfMessages.DISCONNECT_MESSAGE):
                # send the "!DISCONNECT" message to the client to confirm
                conn.send(get_value(TypeOfMessages.DISCONNECT_MESSAGE).encode('utf-8'))
                server.conn_count -= 1
                break
            
            # when the client receive the message "!QUIT", they resend to the server to confirm and after they quit
            elif msg == get_value(TypeOfMessages.SERVER_EXIT):
                break
            
            # send the message to all the clients
            else:
                server.send_all(msg)
    
        conn.close()
        if server.run:
            server.client_list[index] = 0
            
    else:
        # senf a msg SERVER_FULL to the client that want to connect
        conn.send(get_value(TypeOfMessages.SERVER_FULL).encode('utf-8'))
        # close the comunication socket
        conn.close()
        
    server.set_status()
    

def test_conn(server):
    try:
        # try to connect to the server with a temp client to see if the connection is possible
        server.test_connection()
    
    except socket.timeout:
        sys.exit(0)
    
    except socket.gaierror:
        print(f"\n{colors.RED}{colors.BOLD}Impossible host the server on the given info, the program will exit after 2 seconds{colors.RESET}\n")
        sys.exit(0)

    except ConnectionRefusedError:
        print(f"\n{colors.RED}{colors.BOLD}Impossible host the server on the given info, the program will exit after 2 seconds{colors.RESET}\n")
        sys.exit(0)
        
    except KeyboardInterrupt:
        sys.exit(0)
        
    
def check_connections(server):
    # start the thred to connect the temp client
    threading.Thread(target=test_conn, args=(server,)).start()
    try:
        server.test_accept()
       
    except socket.timeout:
        sys.exit(0)
        
    except KeyboardInterrupt:
        sys.exit(0)


def accept_connections(server):
    # if the server is listening and is running
    while server.run:
        conn, ip = server.accept()
        # set the status Listening/No Listening
        server.set_status()
        
        if server.get_status_listen():    
            # create a thread to comunicate with the single client 
            server.conn_count += 1  
            threading.Thread(target=handle_clients, args=(server, conn, ip, False)).start()
    
        else:
            threading.Thread(target=handle_clients, args=(server, conn, ip, True)).start()
            
        server.set_status()


def server_main():
    # create the server
    server = create_server()
    # check if the connections with the clients is possible
    check_connections(server)

    # create a thread for server.accept() because stop the program
    threading.Thread(target=accept_connections, args=(server,)).start()
    
    while menu(server):
        pass
    
    # close the server with the "close_client"
    server.close_connections(False)
    # close the socket server
    server.close()
    sys.exit(0)
