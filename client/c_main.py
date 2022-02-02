import sys, os, socket
import threading

from utils.utils import Colors as colors, print_logo_client, TypeOfMessages, get_value, print_start_chat
from client.client import Client


BUFFER_SIZE = 1024


def create_client():
    print_logo_client()
    print(f"\t\t   {colors.GREEN}{colors.BOLD}Hi! Connect to your friend's server")
    
    try:
        ip = input(f"\n{colors.GREEN}{colors.BOLD}Ip: ")
        port = int(input(f"{colors.GREEN}{colors.BOLD}\nPort: "))
        print(f"{colors.RESET}")

    except KeyboardInterrupt:
        print(f"\n{colors.RESET}{colors.GREEN}Byeeee :){colors.RESET}\n")
        sys.exit(0)
        
    except ValueError:
        print(f"\n{colors.RESET}{colors.RED}Port/Ip can not be empty/string !!{colors.RESET}\n")
        sys.exit(0)

    os.system('cls||clear')
    return Client(ip, port, BUFFER_SIZE)


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
        # when the server quits, sends a message to all the client = "!QUIT" and the client resend the message to confirm
        if msg == get_value(TypeOfMessages.SERVER_EXIT):
            client.send(get_value(TypeOfMessages.SERVER_EXIT))
            print(f"{colors.RED}{colors.BOLD}\nThe server has interrumpted the connection: Press {colors.GREEN}Enter{colors.RED} to exit{colors.RESET}\n")
            client.connected = False
            break
        
        # when the clients want to disconnect, the server to confirm the disconnection resend the DISCONNECT_MESSAGE.
        elif msg == get_value(TypeOfMessages.DISCONNECT_MESSAGE):
            print(f"{colors.RED}{colors.BOLD}\nYou have just been disconnected: Press {colors.GREEN}Enter{colors.RED} to exit{colors.RESET}\n")
            client.connected = False
            break
        
        # when the server is full send a SERVER_FULL message
        elif msg == get_value(TypeOfMessages.SERVER_FULL):
            print(f"{colors.RED}{colors.BOLD}\nThe server is full: Press {colors.GREEN}Enter{colors.RED} to exit{colors.RESET}\n")
            client.connected = False
            break
        
        # message of another client
        else:
            # if it's my message color it in green
            if msg == client.msg:
                print(f"{colors.YELLOW}{colors.BOLD}[Chat]: {colors.GREEN}{msg}{colors.RESET}\n")
            else:
                print(f"{colors.YELLOW}{colors.BOLD}[Chat]: {msg}{colors.RESET}\n")
            
            client.msg = None

 
def send(client):
    try:
        while client.connected:
            msg = input(f"{colors.GREEN}{colors.BOLD}\n")
            client.msg = msg
            
            if msg == get_value(TypeOfMessages.DISCONNECT_MESSAGE):
                client.send(get_value(TypeOfMessages.DISCONNECT_MESSAGE))
                print(f"\n{colors.GREEN}{colors.BOLD}Disconnected from the server\n{colors.RESET}")
                break
            
            # check if the lenght of the message is greater then 0 = empty
            elif len(msg):
                client.send(msg)
            # if the len of the message is 0 (empty) and the client is connected
            elif not len(msg) and client.connected:
                print(f"{colors.RED}{colors.BOLD}Can not send empty message :(")

    except KeyboardInterrupt:
        client.send(get_value(TypeOfMessages.DISCONNECT_MESSAGE))
        client.close()
        sys.exit(0)


def client_main():
    client = create_client()
    connect_client(client)
    print_start_chat()
    print(f"\t\t\t   {colors.YELLOW}{colors.BOLD}Be respectfu!!{colors.RESET}\n")

    # create a thread for listeing
    threading.Thread(target=receive_message, args=(client,)).start()    
    
    send(client)

    # close the client socket
    client.close()
    sys.exit(0)
