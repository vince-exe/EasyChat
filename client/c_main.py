import socket
import threading

from utils.utils import *
from client.client import Client

BUFFER_SIZE = 1024


def create_client():
    print_logo_client()

    try:
        data = read_settings_client_errors(ClientConfig.FILE_NAME)

        os.system('cls||clear')

        return Client(data['PublicIp'], data['Port'], BUFFER_SIZE, data['NickName'])

    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}{Colors.BOLD}Bye :){Colors.RESET}")
        sys.exit(-1)

    except KeyError:
        print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Check the json file")
        sys.exit(-1)


def connect_client(client):
    try:
        print(f"{Colors.YELLOW}{Colors.BOLD}Attempt to connect to the server with ip: {Colors.GREEN}{Colors.BOLD}"
              f"{client.ip}{Colors.RESET}")

        client.connect()
        client.set_connected(True)

    except ConnectionRefusedError:
        print(f"\n{Colors.RED}{Colors.BOLD}Connections refused by the sever {client.ip}{Colors.RESET}\n")
        sys.exit(0)
    
    except socket.timeout:
        print(f"\n{Colors.RED}{Colors.BOLD}The server did not accept the request within the time limit{Colors.RESET}\n")
        sys.exit(0)

    except socket.gaierror:
        print(f"\n{Colors.RED}{Colors.BOLD}Connection Error, are u sure that the ip: "
              f"{Colors.YELLOW}{client.ip}{Colors.RED} is correct?{Colors.RESET}\n")
        sys.exit(0)
          
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}{Colors.BOLD}Bye :){Colors.RESET}\n")
        sys.exit(0)


def receive_message(client):
    while client.connected:
        # waiting for an incoming message
        msg = client.recv()

        # CLIENT QUIT
        if msg == get_value(TypeOfMessages.QUIT):
            print(f"{Colors.GREEN}{Colors.BOLD}Bye :){Colors.RESET}")
            client.connected = False
            break

        # SERVER QUIT
        elif msg == get_value(TypeOfMessages.ServerExit):
            client.send(get_value(TypeOfMessages.ServerExit))
            print(f"{Colors.RED}{Colors.BOLD}\nThe server has interrupted the connection: Press "
                  f"{Colors.GREEN}any key{Colors.RED} to exit{Colors.RESET}\n")
            client.connected = False
            break

        # CLIENT DISCONNECT
        elif msg == get_value(TypeOfMessages.DisconnectMessage):
            print(f"{Colors.RED}{Colors.BOLD}\nYou have just been disconnected: Press {Colors.GREEN}any key"
                  f"{Colors.RED} to exit{Colors.RESET}\n")
            client.connected = False
            break
            
        # SERVER IS FULL
        elif msg == get_value(TypeOfMessages.ServerFull):
            print(f"{Colors.RED}{Colors.BOLD}\nThe server is full: Press {Colors.GREEN}any key"
                  f"{Colors.RED} to exit{Colors.RESET}\n")
            client.connected = False
            break
        
        # CLIENT KICKED
        elif msg == get_value(TypeOfMessages.Kick):
            print(f"\n{Colors.RED}{Colors.BOLD}The server kicked you >:(\n")
            client.send(get_value(TypeOfMessages.Kick))
            client.connected = False
            break
        
        # NICK ALREADY EXIST
        elif msg == get_value(TypeOfMessages.NickAlreadyExist):
            print(f"\n{Colors.RESET}The nickname: {Colors.GREEN}{Colors.BOLD}{client.nick}{Colors.RESET}"
                  f" Already exist!!\n")
            client.connected = False
            break
        
        # CLIENT BANNED
        elif msg == get_value(TypeOfMessages.Ban):
            print(f"\n{Colors.RED}{Colors.BOLD}The server banned you!!\n")
            client.send(get_value(TypeOfMessages.Ban))
            client.connected = False
            break
        
        # CLIENT BANNED THAT TRIED TO ENTRY
        elif msg == get_value(TypeOfMessages.CantEntryBanned):
            print(f"\n{Colors.RED}{Colors.BOLD}You can't entry the server banned you!!\n")
            client.connected = False
            break
        
        # NORMAL MESSAGE
        else:
            # if the message received != my message, color it in yellow
            if not msg == client.msg:
                print(f"{Colors.YELLOW}{Colors.BOLD}{msg}{Colors.RESET}\n")
  
        client.msg = None


def send(client):
    try:
        while client.connected:
            msg = input("\n")
            
            if msg == get_value(TypeOfMessages.DisconnectMessage):
                client.send(get_value(TypeOfMessages.DisconnectMessage))
                client.connected = False
                break
            
            # if the message is good to send
            elif len(msg):
                # save our message to check it later
                client.msg = f"[{client.nick}]: {msg}"
                client.send(msg)
                
            # if the len of the message is 0 (empty) and the client is connected
            elif not len(msg) and client.connected:
                print(f"{Colors.RED}{Colors.BOLD}WARNING: {Colors.RESET}Can not send empty message")

    except KeyboardInterrupt:
        client.send(get_value(TypeOfMessages.DisconnectMessage))
        client.connected = False
        return


def client_main():
    # create and connect the client to the server
    client = create_client()
    connect_client(client)
    
    # send the nickname to the server
    client.send(client.nick)
    print_start_chat()
    
    # create a thread for listing
    threading.Thread(target=receive_message, args=(client,)).start()    

    send(client)

    # close the client socket
    client.close()
    sys.exit(0)
