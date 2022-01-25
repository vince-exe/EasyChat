import sys

from server.s_main import server_main
from client.c_main import client_main
from colors.colors import print_logo_main, Colors


if __name__ == '__main__':
    print_logo_main()
    print(f"\t\t\t{Colors.GREEN}{Colors.BOLD}Create/Join a chat!!{Colors.RESET}\n")
    
    try:
        opt = int(input(f"{Colors.YELLOW}{Colors.BOLD}1)Create a Chat\n2)Join a chat\n\n--> "))
        
        if opt == 1: 
            server_main()
        elif opt == 2:
            client_main()
        else:
            print(f"\n{Colors.RED}Invalid option :/\n{Colors.RESET}\n")
    
    except KeyboardInterrupt:
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}Byee :)\n{Colors.RESET}")
        sys.exit(0)
    
    except ValueError:
        print(f"\n{Colors.RED}{Colors.BOLD}Option can not be a string/empty\n{Colors.RESET}\n")
        sys.exit(0)
    