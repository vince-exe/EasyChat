import os

from enum import Enum


class TypeOfMessages(Enum):
    DisconnectMessage = "!DISCONNECT"
    ServerExit = "!QUIT"
    ServerFull = "!FULL"


class TypeOfException(Enum):
    KeyboardInterrumpt = True
    
def get_value(type):
    return type.value


def disconnect_msg(user):
    msg = f"{Colors.RED}{Colors.BOLD}[Server]: {Colors.GREEN}User {Colors.YELLOW}{user} {Colors.GREEN}has just left the chat{Colors.RESET}"
    return msg


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
    print(f"\t\t   {Colors.GREEN}{Colors.BOLD}Hi! Connect to your friend's server")

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
    

def print_start_chat():
    os.system('cls||clear')
    print(f"""\n{Colors.GREEN}{Colors.BOLD}     
                ███████╗███╗  ██╗     ██╗ █████╗ ██╗   ██╗
                ██╔════╝████╗ ██║     ██║██╔══██╗╚██╗ ██╔╝
                █████╗  ██╔██╗██║     ██║██║  ██║ ╚████╔╝
                ██╔══╝  ██║╚████║██╗ ██║ ██║  ██║  ╚██╔╝
                ███████╗██║ ╚███║╚█████╔╝╚█████╔╝   ██║
                ╚══════╝╚═╝  ╚══╝ ╚════╝  ╚════╝    ╚═╝
    {Colors.RESET}""")
    print(f"\t\t\t   {Colors.YELLOW}{Colors.BOLD}Be respectfu!!{Colors.RESET}\n")