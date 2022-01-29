import sys

from server.s_main import server_main
from client.c_main import client_main
from utils.utils import Colors as colors, print_logo_main


if __name__ == '__main__':
    print_logo_main()
    print(f"\t\t\t{colors.GREEN}{colors.BOLD}Create/Join a chat!!{colors.RESET}\n")
    
    try:
        opt = int(input(f"{colors.YELLOW}{colors.BOLD}1)Create a Chat\n2)Join a chat\n\n--> "))
        
        if opt == 1: 
            server_main()
        elif opt == 2:
            client_main()
        else:
            print(f"\n{colors.RED}Invalid option :/\n{colors.RESET}\n")
    
    except KeyboardInterrupt:
        print(f"\n{colors.MAGENTA}{colors.BOLD}Byee :)\n{colors.RESET}")
        sys.exit(0)
    
    except ValueError:
        print(f"\n{colors.RED}{colors.BOLD}Option can not be a string/empty\n{colors.RESET}\n")
        sys.exit(0)
    