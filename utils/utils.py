import os
import json
import sys

from enum import Enum


class TypeOfMessages(Enum):
    DisconnectMessage = "!DISCONNECT"
    ServerExit = "!QUIT"
    ServerFull = "!FULL"
    Kick = "!KICk"
    NickAlreadyExist = "!NICKALREADYEXIST"
    Ban = "!BAN"
    CantEntryBanned = "!CANTENTRY"
    QUIT = "!QUIT"


class ConnectionErrors:
    NO_INTERNET = -1
    BAD_INFO = -2
    CONNECTION_REFUSED = -3
    TIME_OUT = -4


class ServerConfig:
    FILE_NAME = 'serverConfig.json'
    MIN_CONNECTIONS = 1
    MAX_CONNECTIONS = 10
    MIN_PORT = 4500
    MAX_PORT = 9999


class ClientConfig:
    FILE_NAME = 'clientConfig.json'
    MIN_PORT = 4500
    MAX_PORT = 9999
    MIN_NICK_LEN = 1
    MAX_NICK_LEN = 10


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
                                     █████╗  ██╗      ██╗ ███████╗ ███╗  ██╗ ████████╗
                                    ██╔══██╗ ██║      ██║ ██╔════╝ ████╗ ██║ ╚══██╔══╝
                                    ██║  ╚═╝ ██║      ██║ █████╗   ██╔██╗██║    ██║
                                    ██║  ██╗ ██║      ██║ ██╔══╝   ██║╚████║    ██║
                                    ╚█████╔╝ ███████╗ ██║ ███████╗ ██║ ╚███║    ██║
                                    ╚════╝  ╚══════╝╚ ═╝  ╚══════╝ ╚═╝ ╚══╝     ╚═╝
    {Colors.RESET}""")


def print_logo_server():
    os.system('cls||clear')
    print(f"""\n{Colors.MAGENTA}{Colors.BOLD}
                                     ██████╗ ███████╗ ██████╗  ██╗   ██╗ ███████╗ ██████╗
                                    ██╔════╝ ██╔════╝ ██╔══██╗ ██║   ██║ ██╔════╝ ██╔══██╗
                                    ╚█████╗  █████╗   ██████╔╝ ╚██╗ ██╔╝ █████╗   ██████╔╝
                                     ╚═══██╗ ██╔══╝   ██╔══██╗  ╚████╔╝  ██╔══╝   ██╔══██╗
                                    ██████╔╝ ███████╗ ██║  ██║   ╚██╔╝   ███████╗ ██║  ██║
                                    ╚═════╝  ╚══════╝ ╚═╝  ╚═╝    ╚═╝    ╚══════╝ ╚═╝  ╚═╝
    {Colors.RESET}""")
    

def print_logo_main():
    os.system('cls||clear')
    print(f"""\n{Colors.GREEN}{Colors.BOLD}
                             ██╗       ██╗ ███████╗ ██╗       █████╗   █████╗  ███╗   ███╗ ███████╗
                             ██║  ██╗  ██║ ██╔════╝ ██║      ██╔══██╗ ██╔══██╗ ████╗ ████║ ██╔════╝
                             ╚██╗████╗██╔╝ █████╗   ██║      ██║  ╚═╝ ██║  ██║ ██╔████╔██║ █████╗ 
                              ████╔═████║  ██╔══╝   ██║      ██║  ██╗ ██║  ██║ ██║╚██╔╝██║ ██╔══╝
                              ╚██╔╝ ╚██╔╝  ███████╗ ███████╗ ╚█████╔╝ ╚█████╔╝ ██║ ╚═╝ ██║ ███████╗
                               ╚═╝   ╚═╝   ╚══════╝ ╚══════╝  ╚════╝   ╚════╝  ╚═╝     ╚═╝ ╚══════╝
    {Colors.RESET}""")
    

def print_start_chat():
    os.system('cls||clear')
    print(f"""\n{Colors.GREEN}{Colors.BOLD}     
                                        ███████╗ ███╗  ██╗     ██╗  █████╗  ██╗   ██╗
                                        ██╔════╝ ████╗ ██║     ██║ ██╔══██╗ ╚██╗ ██╔╝
                                        █████╗   ██╔██╗██║     ██║ ██║  ██║  ╚████╔╝
                                        ██╔══╝   ██║╚████║ ██╗ ██║ ██║  ██║   ╚██╔╝
                                        ███████╗ ██║ ╚███║ ╚█████╔╝╚█████╔╝    ██║
                                        ╚══════╝ ╚═╝  ╚══╝  ╚════╝  ╚════╝     ╚═╝
    {Colors.RESET}""")


def read_settings_server_errors(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)

        if data['MaxConnections'] < ServerConfig.MIN_CONNECTIONS or\
           data['MaxConnections'] > ServerConfig.MAX_CONNECTIONS:

            print(f"\n{Colors.YELLOW}{Colors.BOLD}WARNING: {Colors.RESET}Max Connections must be between"
                  f" {ServerConfig.MIN_CONNECTIONS} and {ServerConfig.MAX_CONNECTIONS}")
            sys.exit(-1)

        if data['Port'] < ServerConfig.MIN_PORT or data['Port'] > ServerConfig.MAX_PORT:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}WARNING: {Colors.RESET}Port must be between "
                  f"{ServerConfig.MIN_PORT} and {ServerConfig.MAX_PORT}")
            sys.exit(-1)

        return data

    except FileNotFoundError:
        print(f"\n\t\t\t\t\t  {Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}No settings file found")
        exit(-1)

    except json.decoder.JSONDecodeError:
        print(f"\n\t\t\t\t\t    {Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Check the json file!!")
        exit(-1)

    except KeyError:
        print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Fill in all the parameters in che {file_name}")
        exit(-1)


def read_settings_client_errors(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)

        if data['Port'] < ClientConfig.MIN_PORT or data['Port'] > ClientConfig.MAX_PORT:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}WARNING: {Colors.RESET}Port must be between "
                  f"{ClientConfig.MIN_PORT} and {ClientConfig.MAX_PORT}")
            sys.exit(-1)

        if len(data['NickName']) < ClientConfig.MIN_NICK_LEN or len(data['NickName']) > ClientConfig.MAX_NICK_LEN:
            print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}NickName length must be >= "
                  f"{ClientConfig.MIN_NICK_LEN} and <= {ClientConfig.MAX_NICK_LEN}")
            sys.exit(-1)

        return data

    except FileNotFoundError:
        print(f"\n\t\t\t\t\t  {Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}No settings file found")
        exit(-1)

    except json.decoder.JSONDecodeError:
        print(f"\n\t\t\t\t\t    {Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Check the json file!!")
        exit(-1)

    except KeyError:
        print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Fill in all the parameters in che {file_name}")
        exit(-1)
