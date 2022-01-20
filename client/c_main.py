import sys, os, socket

from colors.colors import Colors as colors, print_logo_client
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
        
            
def client_main():
    client = create_client()
    connect_client(client)
    
    os.system('cls||clear')

    while True:
        pass