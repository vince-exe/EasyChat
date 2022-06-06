import sys

from server.s_main import server_main
from client.c_main import client_main
from utils.utils import Colors, print_logo_main


if __name__ == '__main__':
    print_logo_main()

    try:
        opt = int(input(f"{Colors.BLU}{Colors.BOLD}1) {Colors.RESET}Create a Chat\n"
                        f"{Colors.BLU}{Colors.BOLD}2) {Colors.RESET}Join a chat\n"
                        f"{Colors.BLU}{Colors.BOLD}3) {Colors.RESET}Exit\n"
                        f"{Colors.RESET}         \n-> {Colors.BLU}{Colors.BOLD}"))

        print(f"{Colors.RESET}")

        if opt == 1: 
            server_main()
        elif opt == 2:
            client_main()

        elif opt == 3:
            print(f"\n{Colors.GREEN}{Colors.BOLD}Bye{Colors.RESET}")
            sys.exit(0)

        else:
            print(f"\n{Colors.RED}ERROR: {Colors.RESET}Invalid option :/\n")

    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}{Colors.BOLD}Bye :)\n{Colors.RESET}")
        sys.exit(0)
    
    except ValueError:
        print(f"\n{Colors.RED}{Colors.BOLD}ERROR: {Colors.RESET}Option must be a number\n")
        sys.exit(0)
    