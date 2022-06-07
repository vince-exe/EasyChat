import threading
import socket

from server.server import Server
from utils.utils import *
from user.user import User

DEFAULT_CONNECTIONS = 10


def check_server(info):
    # try to create the server
    try:
        return Server(info['PrivateIp'], info['PublicIp'], info['Port'], info['MaxConnections'], True, True)

    except socket.timeout:
        print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Impossible host the server on the given info\n")
        sys.exit(0)

    except socket.gaierror:
        print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Impossible host the server on the given info\n")
        sys.exit(0)

    except PermissionError:
        print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Permission Denied: Can not host a server on port:"
              f" {info[3]}\n")
        sys.exit(0)

    except OSError:
        print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Impossible host the server on the given info\n")
        sys.exit(0)

    except KeyError:
        print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Check the config file")
        sys.exit(0)


def create_server():
    print_logo_server()

    info = read_settings_server_errors(ServerConfig.FILE_NAME)

    os.system('cls||clear')

    return check_server(info)


def show_active(server):
    print(f"\n{Colors.GREEN}Active Connections: {Colors.RESET}{server.get_active()}\tMax Connections: "
          f"{Colors.RESET}{server.n_listen}")


def ban_user(server):
    try:
        ip = input(f"\n{Colors.RED}{Colors.BOLD}Ip: {Colors.RESET}")
    except ValueError:
        print(f"\n{Colors.RED}{Colors.BOLD}Error: {Colors.RESET}Ip can not be empty!!\n")
        return

    # check if the ip exist
    index = server.check_ip(ip, False)
    # if there is the ip that he wants to kick
    if index != -1:
        server.ban_ip(index, ip)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}Error: Ip {Colors.YELLOW}{Colors.BOLD}{ip}{Colors.RESET} doesn't exist")


def pardon_user(server):
    try:
        ip = input(f"\n{Colors.RED}{Colors.BOLD}Ip: {Colors.RESET}")

    except ValueError:
        print(f"\n{Colors.RED}{Colors.BOLD}[Error] Ip can not be empty!!\n")
        return

    # check if the ip exist
    index = server.check_ip(ip, True)
    if index != -1:
        server.pardon_ip(index)

    else:
        print(f"\n{Colors.RED}{Colors.BOLD}Error: Ip {Colors.YELLOW}{Colors.BOLD}{ip}{Colors.RESET} doesn't exist")


def show(server, banned):
    # if he wants to see the banned users
    if banned:
        for i in range(len(server.black_list)):
            if server.black_list[i]:
                print(f"\n{Colors.GREEN}{Colors.BOLD}Nick: {Colors.YELLOW}{server.black_list[i].get_nick()}"
                      f"\t{Colors.GREEN}Ip: {Colors.YELLOW}{server.black_list[i].get_ip()}")

    # he wants to see the normal users
    else:
        for i in range(len(server.users_list)):
            if server.users_list[i]:
                print(
                    f"\n{Colors.GREEN}{Colors.BOLD}Nick: {Colors.RESET}{server.users_list[i].get_nick()}"
                    f"\t{Colors.GREEN}{Colors.BOLD}Ip: {Colors.RESET}{server.users_list[i].get_ip()}")


def kick_user(server):
    nick_kick = input(f"\n{Colors.RED}{Colors.BOLD}Nick: {Colors.RESET}")

    # check if the nick exist
    index = server.check_user(nick_kick)
    if index != -1:
        print(f"\n{Colors.GREEN}{Colors.BOLD}Successfully kicked the user: {Colors.YELLOW}{Colors.BOLD}{nick_kick}"
              f"\n{Colors.RESET}")
        server.kick_user(index)
        server.kicked_user = nick_kick

    # if there isn't the nick
    else:
        print(f"{Colors.RED}{Colors.BOLD}Error: {Colors.RESET}there isn't any user with the nick: {Colors.YELLOW}"
              f"{Colors.BOLD}{nick_kick}{Colors.RESET}")
        server.kicked_user = nick_kick


def take_option():
    while True:
        try:
            return int(input(f"{Colors.BLU}{Colors.BOLD}1) {Colors.RESET}Show Active Connections"
                             f"{Colors.BLU}{Colors.BOLD}\n2) {Colors.RESET}Close Server"
                             f"{Colors.BLU}{Colors.BOLD}\n3) {Colors.RESET}Clear"
                             f"{Colors.BLU}{Colors.BOLD}\n4) {Colors.RESET}Show Users"
                             f"{Colors.BLU}{Colors.BOLD}\n5) {Colors.RESET}Kick User"
                             f"{Colors.BLU}{Colors.BOLD}\n6) {Colors.RESET}Ban User"
                             f"{Colors.BLU}{Colors.BOLD}\n7) {Colors.RESET}Pardon User"
                             f"{Colors.BLU}{Colors.BOLD}\n8) {Colors.RESET}Show Banned User"
                             f"\n\n{Colors.RED}{Colors.BOLD}>> {Colors.BLU}{Colors.BOLD}"))

        except ValueError:
            print(f"\n{Colors.RED}Option can not be empty/string!!{Colors.RESET}\n")


def close(server):
    try:
        if server.get_active():  # if there are still active connections
            temp = input(f"\n{Colors.RED}{Colors.BOLD}Warning: {Colors.RESET}There are still {server.get_active()}"
                         f" active connections!  Are you sure(y / n): {Colors.BLU}{Colors.BOLD}")

            print(f"{Colors.RESET}")

            if temp == "y" or temp == "yes" or temp == "YES" or temp == "Y":
                # first disconnect all the clients
                server.close_connections(True)
                return True
            else:
                return False

        else:  # else there aren't active connections, close the server
            server.close_connections(False)
            return True

    except KeyboardInterrupt:
        server.close_connections(True)
        return True


def menu(server):
    while True:
        try:
            if server.get_status_listen():
                print(f"{Colors.RESET}\n{Colors.YELLOW}{Colors.BOLD}Status Server: "
                      f"{Colors.GREEN}{Colors.BOLD}Listening{Colors.RESET}\n")
            else:
                print(f"\nStatus Server: {Colors.RED}{Colors.BOLD}Not Listening{Colors.RESET}\n")

            opt = take_option()

            # show the active connections
            if opt == 1:
                show_active(server)

            # close the server
            elif opt == 2:
                if close(server):
                    return False

            # clear the console
            elif opt == 3:
                os.system('cls||clear')

            # show user with ips
            elif opt == 4:
                print(f"\n{Colors.GREEN}{Colors.BOLD}\n[Users of the Chat]")
                show(server, False)

            # kick the user
            elif opt == 5:
                kick_user(server)

            # ban the user
            elif opt == 6:
                ban_user(server)

            # pardon the user
            elif opt == 7:
                pardon_user(server)

            # show banned list    
            elif opt == 8:
                print(f"\n{Colors.RED}{Colors.BOLD}\n[Black List]")
                show(server, True)

            # default
            else:
                print(f"\n{Colors.RED}Enter an existing option :){Colors.RESET}\n")

        except KeyboardInterrupt:
            # if there are active connections
            if server.get_active():
                server.close_connections(True)
            else:
                server.close_connections(False)
            return False


def handle_clients(server, conn, ip, ser_full, nick, nick_free, banned):
    index = None
    # if the server is not full
    if not ser_full:
        # if it's not banned
        if not banned:
            # if the nick_name is free
            if nick_free:
                # if the server is running
                if server.run:
                    # welcome msg
                    server.send_all(welcome_msg(nick))
                    # add the user to the list
                    server.add_conn(User(conn, ip, nick))
                    # calculate the index that will be used for del
                    index = (threading.active_count() - 2) - 1

                while server.run:
                    try:
                        # wait for incoming messages
                        msg = conn.recv(1024).decode('utf-8')

                        # CLIENT DISCONNECTED
                        if msg == get_value(TypeOfMessages.DisconnectMessage):
                            # send the "!DISCONNECT" message to the client to confirm
                            conn.send(get_value(TypeOfMessages.DisconnectMessage).encode('utf-8'))
                            server.conn_count -= 1
                            # send the disconnect message to all the clients
                            server.send_all(disconnect_msg(nick))
                            break

                        # when the client receive the message "!QUIT", he resends to the server to confirm and close
                        # the connection, and after he quits
                        elif msg == get_value(TypeOfMessages.ServerExit):
                            break

                        # CLIENT KICKED
                        elif msg == get_value(TypeOfMessages.Kick):
                            # send the kick message to all the user
                            server.send_all(kick_msg(server.kicked_user))
                            server.conn_count -= 1
                            break

                        # CLIENT BANNED
                        elif msg == get_value(TypeOfMessages.Ban):
                            # send the ban message to all the users
                            server.send_all(ban_msg(server.banned_user))
                            server.conn_count -= 1
                            break

                        # NORMAL MESSAGE
                        else:
                            send_msg = f"[{nick}]: {msg}"
                            server.send_all(send_msg)

                    except ConnectionResetError:
                        # send the "!DISCONNECT" message to the client to confirm
                        server.conn_count -= 1

                        if server.conn_count >= 1:
                            # send the disconnect message to all the clients
                            server.send_all(disconnect_msg(nick))

                        break

                if server.run:
                    # close the connection
                    conn.close()
                    # free the space
                    server.users_list[index] = 0

            # if the nick already exist        
            else:
                conn.send(get_value(TypeOfMessages.NickAlreadyExist).encode('utf-8'))
                conn.close()
                return

        # if it's banned
        else:
            conn.send(get_value(TypeOfMessages.CantEntryBanned).encode('utf-8'))
            conn.close()
            return

    # if the server is full     
    else:
        # send a msg SERVER_FULL to the client that want to connect
        conn.send(get_value(TypeOfMessages.ServerFull).encode('utf-8'))
        # close the communication socket
        conn.close()

    server.set_status()


def test_conn(server):
    try:
        # try to connect to the server with a temp client to see if the connection is possible
        check = server.test_connection()

        if check == ConnectionErrors.BAD_INFO:
            print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Can't host the server on the given info,"
                  f" the program will exit after 2 seconds{Colors.RESET}\n")
            sys.exit(0)

        elif check == ConnectionErrors.NO_INTERNET:
            print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Can't connect to the internet, check the wifi")
            sys.exit(0)

        elif check == ConnectionErrors.TIME_OUT:
            print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Connection timeout")

        elif check == ConnectionErrors.CONNECTION_REFUSED:
            print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Can't connect, permissions denied")

    except KeyboardInterrupt:
        sys.exit(0)


def check_connections(server):
    # start the thread to connect the temp client
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
            # check if it's banned
            if server.check_blacklist(ip[0]):
                threading.Thread(target=handle_clients, args=(server, conn, ip, False, nick, False, True)).start()
            else:
                #  check if the nick already exist
                if server.check_nick(nick):
                    # set the parameter nick_free = False
                    threading.Thread(target=handle_clients, args=(server, conn, ip, False, nick, False, False)).start()

                else:
                    # create a thread to communicate with the single client
                    server.conn_count += 1
                    threading.Thread(target=handle_clients, args=(server, conn, ip, False, nick, True, False)).start()

        # else set the variable serv_full to True
        else:
            threading.Thread(target=handle_clients, args=(server, conn, ip, True, nick, True, False)).start()

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

    print(f"{Colors.RESET}")
    sys.exit(0)
