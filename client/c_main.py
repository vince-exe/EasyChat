import sys

from colors.colors import Colors as colors
from client.client import Client


def client_main():
    client = Client("213.45.54.55", 7000, 1024)
    client.connect()
    
    print(f"\n{colors.GREEN}Connection established with the server{colors.RESET}")
    
    while True:
        pass