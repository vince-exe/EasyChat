import sys, os, socket
import threading

from utils.utils import Colors as colors, print_logo_client, TypeOfMessages, get_value, print_start_chat
from client.client import Client

BUFFER_SIZE = 1024


def takeNickname(min, max):
    nick = input(f"\n{colors.GREEN}{colors.BOLD}Nick: ")
    
    while len(nick) <= min or len(nick) > max:
        nick = input(f"\n{colors.GREEN}{colors.BOLD}Nick has to be > 0 and < 6 characters: ")
        
    return nick


def create_client():
    print_logo_client()

    try:
        ip = input(f"\n{colors.GREEN}{colors.BOLD}Ip: ")
        port = int(input(f"{colors.GREEN}{colors.BOLD}\nPort: "))
        nick = takeNickname(0, 7)

    except KeyboardInterrupt:
        print(f"\n{colors.RESET}{colors.GREEN}Byeeee :){colors.RESET}\n")
        sys.exit(0)
        
    except ValueError:
        print(f"\n{colors.RESET}{colors.RED}Port/Ip can not be empty/string !!{colors.RESET}\n")
        sys.exit(0)

    os.system('cls||clear')
    return Client(ip, port, BUFFER_SIZE, nick)


def connect_client(client):
    try:
        print(f"{colors.YELLOW}{colors.BOLD}Attempt to connect to the server with ip: {colors.GREEN}{colors.BOLD}{client.ip}{colors.RESET}")
        client.connect()
        client.set_connected(True)

    except ConnectionRefusedError:
        print(f"\n{colors.RED}{colors.BOLD}Connections refused by the sever {client.ip}{colors.RESET}\n")
        sys.exit(0)
    
    except socket.timeout:
        print(f"\n{colors.RED}{colors.BOLD}The server did not accept the request within the time limit{colors.RESET}\n")
        sys.exit(0)

    except socket.gaierror:
        print(f"\n{colors.RED}{colors.BOLD}Connection Error, are u sure that the ip: {colors.YELLOW}{client.ip}{colors.RED} is correct?{colors.RESET}\n")
        sys.exit(0)
          
    except KeyboardInterrupt:
        print(f"\n{colors.GREEN}{colors.BOLD}Byee :){colors.RESET}\n")
        sys.exit(0)
        

def receive_message(client):
    while client.connected:
        # waiting for an incoming message
        msg = client.recv()
        
        # SERVER QUIT
        if msg == get_value(TypeOfMessages.ServerExit):
            client.send(get_value(TypeOfMessages.ServerExit))
            print(f"{colors.RED}{colors.BOLD}\nThe server has interrumpted the connection: Press {colors.GREEN}Enter{colors.RED} to exit{colors.RESET}\n")
            client.connected = False
            break
        
        # CLIENT DISCONNECT
        elif msg == get_value(TypeOfMessages.DisconnectMessage):
            print(f"{colors.RED}{colors.BOLD}\nYou have just been disconnected: Press {colors.GREEN}Enter{colors.RED} to exit{colors.RESET}\n")
            client.connected = False
            break
            
        # SERVER IS FULL
        elif msg == get_value(TypeOfMessages.ServerFull):
            print(f"{colors.RED}{colors.BOLD}\nThe server is full: Press {colors.GREEN}Enter{colors.RED} to exit{colors.RESET}\n")
            client.connected = False
            break
        
        # CLIENT KICKED
        elif msg == get_value(TypeOfMessages.Kick):
            print(f"\n{colors.RED}{colors.BOLD}The server kicked you >:(\n")
            client.send(get_value(TypeOfMessages.Kick))
            client.connected = False
            break
        
        # NICK ALREADY EXIST
        elif msg == get_value(TypeOfMessages.NickalreadyExist):
            print(f"\n{colors.RED}{colors.BOLD}The nickname: {colors.GREEN}{colors.BOLD}{client.nick} {colors.RED}Already exist!!\n")
            client.connected = False
            break
        
        # CLIENT BANNED
        elif msg == get_value(TypeOfMessages.Ban):
            print(f"\n{colors.RED}{colors.BOLD}The server banned you!!\n")
            client.send(get_value(TypeOfMessages.Ban))
            client.connected = False
            break
        
        # CLIENT BANNED THAT TRYIED TO ENTRY
        elif msg == get_value(TypeOfMessages.CantEntryBanned):
            print(f"\n{colors.RED}{colors.BOLD}You can't entry the server banned you!!\n")
            client.connected = False
            break
        
        # NORMAL MESSAGE
        else:
            # if the message received != my message, color it in yellow
            if not msg == client.msg:
                print(f"{colors.YELLOW}{colors.BOLD}{msg}{colors.RESET}\n")
  
        client.msg = None


def send(client):
    try:
        while client.connected:
            msg = input("\n")
            
            if msg == get_value(TypeOfMessages.DisconnectMessage):
                client.send(get_value(TypeOfMessages.DisconnectMessage))
                print(f"\n{colors.GREEN}{colors.BOLD}Disconnected from the server\n{colors.RESET}")
                break
            
            # if the message is good to send
            elif len(msg):
                # save our message to check it later
                client.msg = f"[{client.nick}]: {msg}"
                client.send(msg)
                
            # if the len of the message is 0 (empty) and the client is connected
            elif not len(msg) and client.connected:
                print(f"{colors.RED}{colors.BOLD}Can not send empty message :({colors.RESET}")

    except KeyboardInterrupt:
        client.send(get_value(TypeOfMessages.DisconnectMessage))
        client.close()
        sys.exit(0)


def client_main():
    # create and connect the client to the server
    client = create_client()
    connect_client(client)
    
    # send the nickname to the server
    client.send(client.nick)
    print_start_chat()
    
    # create a thread for listeing
    threading.Thread(target=receive_message, args=(client,)).start()    
    
    send(client)

    # close the client socket
    client.close()
    sys.exit(0)
