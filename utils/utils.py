import os

from enum import Enum


class TypeOfMessages(Enum):
    DisconnectMessage = "!DISCONNECT"
    ServerExit = "!QUIT"
    ServerFull = "!FULL"
    Kick = "!KICk"
    NickAlreadyExist = "!NICKALREADYEXIST"
    Ban = "!BAN"
    CantEntryBanned = "!CANTENTRY"


class ConnectionErrors:
    NO_INTERNET = -1
    BAD_INFO = -2
    CONNECTION_REFUSED = -3
    TIME_OUT = -4


def get_value(type_):
    return type_.value


def disconnect_msg(user):
    return f"{Colors.RED}{Colors.BOLD}[Server]: {Colors.GREEN}User {Colors.YELLOW}{user} {Colors.GREEN}" \
           f"has just left the chat{Colors.RESET}"


def kick_msg(user):
    return f"{Colors.RED}{Colors.BOLD}[Server]: {Colors.YELLOW}{Colors.BOLD}The user {Colors.RED}{Colors.BOLD}{user}" \
           f" {Colors.YELLOW}{Colors.BOLD}has just been kicked{Colors.RESET}"


def ban_msg(user):
    return f"{Colors.RED}{Colors.BOLD}[Server]: {Colors.RED}{Colors.BOLD}The user {Colors.YELLOW}{Colors.BOLD}{user}" \
           f" {Colors.RED}{Colors.BOLD}has just been banned{Colors.RESET}"


def welcome_msg(user):
    return f"{Colors.RED}{Colors.BOLD}[Server]: {Colors.GREEN}{Colors.BOLD}The user " \
           f"{Colors.YELLOW}{Colors.BOLD}{user}"\
           f"{Colors.GREEN}{Colors.BOLD}has joined!!{Colors.RESET}"


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
    print(f"\t\t\t\t   {Colors.GREEN}{Colors.BOLD}Hi! Connect to your friend's server")


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
    print(f"\t\t\t\t   {Colors.GREEN}{Colors.BOLD}Be Respectful!!{Colors.RESET}\n")
