import server.s_main as server
import client.c_main as client

if __name__ == '__main__':
    a = int(input("-> "))
    
    if a == 1: 
        server.server_main()
    else:
        client.client_main()