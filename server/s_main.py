import sys, os, threading

from server.server import Server
from colors.colors import Colors as colors, print_logo_server

def create_server():
    print_logo_server()
    port = 0
    try:
        port = int(input(f"\n{colors.YELLOW}{colors.BOLD}Port: "))
        
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
        return Server(port, n_connection, True) 
    
    except PermissionError:
        print(f"\n\n{colors.RESET}{colors.RED}Permission Denied: Can not host a server on port: {port}{colors.RESET}\n")
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
        if server.get_status():
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
                    print(f"\n{colors.GREEN}Closing the server, press {colors.RESET}{colors.YELLOW}{colors.BOLD}Ctrl + C{colors.RESET} {colors.GREEN}to stop the server{colors.RESET}\n")
                    server.close()
                    return
                    
            else: # else there aren't active connections, close the server
                print(f"\n{colors.GREEN}Closing the server, press {colors.RESET}{colors.YELLOW}Ctrl + C {colors.RESET}{colors.GREEN}to stop the server{colors.RESET}\n")
                server.close()
                return
                
        else:   # default
            print(f"\n{colors.RED}Enter an existing option :){colors.RESET}\n")

            
def server_main():
    server = create_server()
    
    #start the menu thread
    threading.Thread(target=menu, args=(server,)).start()
    while True:
        if server.get_status():
            # wait for incoming connections
            server.accept()
            server.set_status()
        