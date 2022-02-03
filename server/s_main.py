import sys, os, threading, socket

from server.server import Server
from utils.utils import *
from user.user import User

DEFAULT_CONNECTIONS = 10
DISCONNECT_MESSAGE = "!DISCONNECT"


def get_info():
    max_connections, max_port = DEFAULT_CONNECTIONS + 1, 0
    
    try:
        private_ip = input(f"{Colors.YELLOW}{Colors.BOLD}Host Ip: ")

        public_ip = input(f"\nPublic Ip: ") 

        try:
            while max_connections > DEFAULT_CONNECTIONS or max_connections < 1:
                max_connections = int(input(f"\nConnections (max: {DEFAULT_CONNECTIONS}/min: 1): "))
        except ValueError:
            print(f"\n{Colors.RESET}{Colors.RED}{Colors.BOLD}Connections can not be empty/int!!\n{Colors.RESET}")
            sys.exit(0)
            
        try:
            while max_port < 4500 or max_port > 9999:
                max_port = int(input("\nPort (max: 9999 / min: 4500): "))
        except ValueError:
            print(f"\n{Colors.RESET}{Colors.RED}{Colors.BOLD}Port can not be empty/string !!{Colors.RESET}\n")
            sys.exit(0)
            
    except KeyboardInterrupt:
        sys.exit(0)

    return (private_ip, public_ip, max_connections, max_port)



def check_server(info):
    # try to create the server
    try:
        return Server(info[0], info[1], info[3], info[2], True, True)

    except socket.timeout:
        print(f"\n{Colors.RED}{Colors.BOLD}Impossible host the server on the given info{Colors.RESET}\n")
        sys.exit(0)

    except socket.gaierror:
        print(f"\n{Colors.RED}{Colors.BOLD}Impossible host the server on the given info{Colors.RESET}\n")
        sys.exit(0)
    
    except PermissionError:
        print(f"\n{Colors.RED}{Colors.BOLD}Permission Denied: Can not host a server on port: {info[3]}{Colors.RESET}\n")
        sys.exit(0)
        
    except OSError:
        print(f"\n{Colors.RED}{Colors.BOLD}Impossible host the server on the given info{Colors.RESET}\n")
        sys.exit(0)   


def create_server():
    print_logo_server()
    
    info = get_info()
    os.system('cls||clear')
    
    return check_server(info)


def show_active(server):
    print(f"\n{Colors.GREEN}Active Connections: {server.get_active()}\tMax Connections: {server.n_listen}{Colors.RESET}")
    

def show_users(server):
    print(f"\n{Colors.GREEN}{Colors.BOLD}\n[Users of the Chat]")
    
    for i in range(len(server.users_list)):
        if server.user_list[i]:
            print(f"\n{Colors.GREEN}{Colors.BOLD}Nick: {Colors.YELLOW}{server.users_list[i].get_nick()}\t{Colors.GREEN}Ip: {Colors.YELLOW}{server.users_list[i].get_ip()}")    

    
def kick_user(server):
    nick_kick = input(f"\n{Colors.RED}{Colors.BOLD}Nick: ")        
    if not server.kick_user(nick_kick):
        print(f"\n{Colors.RED}{Colors.BOLD}[Error] there is no user with the name: {nick_kick}\n")

    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}Succesfully kicked the user: {nick_kick}\n")
        
        
def take_option():
    while True:
        try:
            return int(input(f"1)Show Active Connections\n2)Close Server\n3)Clear\n4)Show Users\n5)Kick User\n6)Ban User\n7)Pardon User\n\n{Colors.RED}{Colors.BOLD}>> {Colors.RESET}"))
        
        except ValueError:
            print(f"\n{Colors.RED}Option can not be empty/string!!{Colors.RESET}\n")
            

def close(server):
    try:
        if server.get_active(): # if there are still active connections
            temp = input(f"\n{Colors.RED}Warning: There are still {server.get_active()} active connections!  Are you sure(y / n): {Colors.RESET}")

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
                print(f"{Colors.RESET}\n{Colors.YELLOW}{Colors.BOLD}Status Server: {Colors.GREEN}{Colors.BOLD}Listening{Colors.RESET}\n")
            else:
                print(f"\nStatus Server: {Colors.RED}{Colors.BOLD}Not Listening{Colors.RESET}\n")    
                    
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

            elif(opt == 4):
                show_users(server)

            elif(opt == 5):
                kick_user(server)

            else:   # default
                print(f"\n{Colors.RED}Enter an existing option :){Colors.RESET}\n")

        except KeyboardInterrupt:
            # if there are active connections
            if server.get_active():
                server.close_connections(True)
            else:
                server.close_connections(False)
            return False


def handle_clients(server, conn, ip, ser_full, nick, nick_free):
    # if the server is not full
    if not ser_full:
        # if the nick_name is free
        if nick_free:
            # if the server is running
            if server.run:
                # add the user to the list
                server.add_conn(User(conn, ip, nick))
                # calculate the index that will be used for del
                index = (threading.activeCount() - 2) - 1

            while server.run:
                # wait for incoming messages
                msg = conn.recv(1024).decode('utf-8')
                
                # if the the message is "!DISCONNECT": disconnect the client and delete his comunication socket from the list
                if msg == get_value(TypeOfMessages.DisconnectMessage):
                    # send the "!DISCONNECT" message to the client to confirm
                    conn.send(get_value(TypeOfMessages.DisconnectMessage).encode('utf-8'))
                    server.conn_count -= 1
                    # send the disconnect message to all the clients
                    server.send_all(disconnect_msg(nick))
                    break
                
                # when the client receive the message "!QUIT", he resends to the server to confirm and close the connecton and after he quits
                elif msg == get_value(TypeOfMessages.ServerExit):
                    break
                
                # when the client receive the message "!KICK", he resends to the server to confirm and close the connections and after he quits
                elif msg == get_value(TypeOfMessages.Kick):
                    break
                
                # send the message to all the clients
                else:
                    send_msg = f"[{nick}]: {msg}"
                    server.send_all(send_msg)
            
        # if the nick already exist        
        else:
            conn.send(get_value(TypeOfMessages.NickalreadyExist).encode('utf-8'))
            conn.close()
            return

        if server.run:
            # close the connection
            conn.close()
            # free the space
            server.users_list[index] = 0
    
    # if the server is full     
    else:
        # send a msg SERVER_FULL to the client that want to connect
        conn.send(get_value(TypeOfMessages.ServerFull).encode('utf-8'))
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
        print(f"\n{Colors.RED}{Colors.BOLD}Impossible host the server on the given info, the program will exit after 2 seconds{Colors.RESET}\n")
        sys.exit(0)

    except ConnectionRefusedError:
        print(f"\n{Colors.RED}{Colors.BOLD}Impossible host the server on the given info, the program will exit after 2 seconds{Colors.RESET}\n")
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
        # take the nickname
        nick = conn.recv(1024).decode('utf-8')
        
        # set the status Listening/No Listening
        server.set_status()
        
        # if the server is listening
        if server.get_status_listen(): 
            # check if the nick already exist
            if server.check_nick(nick):
                # set the paramater nick_free = False
                threading.Thread(target=handle_clients, args=(server, conn, ip, False, nick, False)).start()
            
            else:
                # create a thread to comunicate with the single client 
                server.conn_count += 1  
                threading.Thread(target=handle_clients, args=(server, conn, ip, False, nick, True)).start()

        # else set the variable 
        else:
            threading.Thread(target=handle_clients, args=(server, conn, ip, True, nick, True)).start()
            
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
