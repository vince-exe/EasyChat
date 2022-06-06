import sys

from server.s_main import server_main
from client.c_main import client_main
from utils.utils import Colors as colors, print_logo_main


if __name__ == '__main__':
    print_logo_main()
    print(f"\t\t\t\t    {colors.GREEN}{colors.BOLD}Create/Join a chat!!{colors.RESET}\n")
    
    try:
        opt = int(input(f"{colors.YELLOW}{colors.BOLD}1)Create a Chat"
                        f"                          \n2)Join a chat"
                        f"                          \n3)Exit"
                        f"{colors.RESET}            \n\n-> {colors.BLU}{colors.BOLD}"))

        print(f"{colors.RESET}")

        if opt == 1: 
            server_main()
        elif opt == 2:
            client_main()

        elif opt == 3:
            print(f"\n{colors.GREEN}{colors.BOLD}Bye{colors.RESET}")
            sys.exit(0)

        else:
            print(f"\n{colors.RED}ERROR: {colors.RESET}Invalid option :/\n")

    except KeyboardInterrupt:
        print(f"\n{colors.MAGENTA}{colors.BOLD}Bye :)\n{colors.RESET}")
        sys.exit(0)
    
    except ValueError:
        print(f"\n{colors.RED}{colors.BOLD}ERROR: {colors.RESET}Option must be a number\n")
        sys.exit(0)
    