from enum import Enum

import os


class TypeOfMessages(Enum):
    DISCONNECT_MESSAGE = "!DISCONNECT"
    SERVER_EXIT = "!QUIT"


def get_value(type):
    return type.value


class Colors:
    GREEN = "\u001b[32m"
    RESET = "\u001b[0m"
    MAGENTA = "\u001b[35m"
    RED = "\u001b[31m"
    YELLOW = "\u001b[33m"
    BLU = "\033[94m"
    BOLD = "\033[1m"
    

def print_logo_client():
    os.system('cls||clear')
    print(f"""\n{Colors.YELLOW}{Colors.BOLD}
             █████╗ ██╗     ██╗███████╗███╗  ██╗████████╗
            ██╔══██╗██║     ██║██╔════╝████╗ ██║╚══██╔══╝
            ██║  ╚═╝██║     ██║█████╗  ██╔██╗██║   ██║
            ██║  ██╗██║     ██║██╔══╝  ██║╚████║   ██║
            ╚█████╔╝███████╗██║███████╗██║ ╚███║   ██║
             ╚════╝ ╚══════╝╚═╝ ╚══════╝╚═╝ ╚══╝   ╚═╝
    {Colors.RESET}""")


def print_logo_server():
    os.system('cls||clear')
    print(f"""\n{Colors.MAGENTA}{Colors.BOLD}
             ██████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
            ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
            ╚█████╗ █████╗  ██████╔╝╚██╗ ██╔╝█████╗  ██████╔╝
             ╚═══██╗██╔══╝  ██╔══██╗ ╚████╔╝ ██╔══╝  ██╔══██╗
            ██████╔╝███████╗██║  ██║  ╚██╔╝  ███████╗██║  ██║
            ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
    {Colors.RESET}""")
    

def print_logo_main():
    os.system('cls||clear')
    print(f"""\n{Colors.GREEN}{Colors.BOLD}
         ██╗       ██╗███████╗██╗      █████╗  █████╗ ███╗   ███╗███████╗
         ██║  ██╗  ██║██╔════╝██║     ██╔══██╗██╔══██╗████╗ ████║██╔════╝
         ╚██╗████╗██╔╝█████╗  ██║     ██║  ╚═╝██║  ██║██╔████╔██║█████╗ 
          ████╔═████║ ██╔══╝  ██║     ██║  ██╗██║  ██║██║╚██╔╝██║██╔══╝
          ╚██╔╝ ╚██╔╝ ███████╗███████╗╚█████╔╝╚█████╔╝██║ ╚═╝ ██║███████╗
           ╚═╝   ╚═╝  ╚══════╝╚══════╝ ╚════╝  ╚════╝ ╚═╝     ╚═╝╚══════╝
    {Colors.RESET}""")