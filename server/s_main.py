import sys, os, threading

from server.server import Server
from colors.colors import Colors as colors, print_logo_server

def create_server():
    print_logo_server()
    port = 0
    public_ip = None
    try:
        port = int(input(f"\n{colors.YELLOW}{colors.BOLD}Port: "))
        public_ip = input("\nPublic ip: ")
        n_connection = 11
  
        while n_connection > 10 or n_connection < 1:
            n_connection = int(input(f"\n{colors.YELLOW}{colors.BOLD}Connections Number(max: 10 / min: 1): "))
    
    except KeyboardInterrupt:
        print(f"\n\n{colors.RESET}{colors.GREEN}Byeeee :){colors.RESET}\n")
        sys.exit(0)

    except ValueError:
        print(f"\n{colors.RESET}{colors.RED}Port/Number Connections can not be empty/string !!{colors.RESET}\n")
        sys.exit(0)
    
    # try to create the server
    try:    
        os.system('cls||clear')
        # create and return the istance of Server()
        return Server(public_ip, port, n_connection, True, True) 
    
    except PermissionError:
        print(f"\n\n{colors.RESET}{colors.RED}Permission Denied: Can not host a server on port: {port}{colors.RESET}\n")
        sys.exit(0)
        
    except OSError as error:
        print(f"\n\n{colors.RESET}{colors.RED}Impossibile to host a server on port: {port} {error}{colors.RESET}\n")
        sys.exit(0)


def show_active(server):
    print(f"\n{colors.GREEN}Active Connections: {server.get_active()}{colors.RESET}")
    
    
def take_option():
    while True:
        try:
            opt = int(input(f"1)Show Active Connections\n2)Close Server\n\n{colors.BLU}{colors.BOLD}>> {colors.RESET}"))
            return opt
        
        except ValueError:
            print(f"\n{colors.RED}Option can not be empty/string!!{colors.RESET}\n")
            
     
def menu(server):
    while True:   
        try:  
            if server.get_status_listen():
                print(f"{colors.RESET}\nStatus Server: {colors.GREEN}{colors.BOLD}Listening{colors.RESET}\n")
            else:
                print(f"\nStatus Server: {colors.RED}{colors.BOLD}Not Listening{colors.RESET}\n")    
                    
            opt = take_option()
                
            # show the active connections
            if(opt == 1):
                show_active(server)
                
            # close the server
            elif(opt == 2):
                if server.get_active(): # if there are still active connections
                    temp = input(f"\n{colors.RED}Warning: There are still {server.get_active()} active connections!  Are you sure(y / n): {colors.RESET}")

                    if(temp == "y" or temp == "yes" or temp == "YES" or temp == "Y"):
                        server.close()
                        return False
                        
                else: # else there aren't active connections, close the server
                    server.close()
                    return False
                    
            else:   # default
                print(f"\n{colors.RED}Enter an existing option :){colors.RESET}\n")

        except KeyboardInterrupt:
            server.close()
            return False


def accept_connections(server):
    #if the server is listening and is running
    while server.run:
        server.accept()
        server.set_status()

    # exit from the function so exit from the thread
    return


def server_main():
    server = create_server()
    
    #create a thread for server.accept() because stop the program
    threading.Thread(target=accept_connections, args=(server,)).start()

    while menu(server):
        pass
    
    # close the server, and exit from the program
    server.close()
    sys.exit(0)
