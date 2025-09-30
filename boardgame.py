if __name__ == "__main__":
    import socket
    import threading
    
    def handle_client(client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received: {message}")
                client_socket.send(f"Echo: {message}".encode('utf-8'))
            except:
                break
        client_socket.close()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen()
    print("Server listening on port 5555")
    
    while True:
        client, addr = server.accept()
        print(f"Connected by {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()

    turn = 1
    plyrs = 0
    players = [
        # [id,'naam','piece','points', positions],
        [0, 'Kemal', 'K', 0, 4],
        [0, 'Alice', 'A', 0, 10],
    ]
    
    def drawBoard():
        def a(pos):
            for p in players:
                if pos == p[4]:
                    if len(str(pos)) > 1:
                        return " " + str(p[2])
                    return str(p[2])
            return str(pos)
        
        board = (
            "                                                                                                    @@             \n"
            "                                                                                                    @@             \n"
            "                                                                                                    @@             \n"
            "                                                                                                    @@@@@@@        \n"
            "                                                                                                   @@              \n"
            "                                                                                        @@@@@@@@@@@@               \n"
            "                                                                                 @@@@@@@@@     -@@@                \n"
            "                                                                               @@@                @                \n"
            "                         @@@@@@@@@@@@@@@+                                    :@@                  @@               \n"
            "                    @@@@@@  @        @ @@@@@@                                @@      @@@          @@               \n"
            "                 @@@@        @  "+ str(a(34)) +"  @      @ @@@@%                           @@     @@            @@               \n"
            "              =@@@   @@   "+ str(a(33)) +"  @    @  "+ str(a(35)) +"   @     @@@@@                       @@             @     @@               \n"
            "             @@        @@@    @    @      @@      @  @@@@@                   @@            @@     @                \n"
            "           @@@ @@   "+ str(a(32)) +"    @    @  @       @  "+ str(a(36)) +"   @      @@@@@               @     "+ str(a(43)) +"     @@     @@                \n"
            "          @@     @@@       @@@@@@@@@@@-  @       @  "+ str(a(37)) +"  @    @@@@@@@@     @@@                   @@                 \n"
            "         @@    "+ str(a(31)) +"   @  @@@@            @@@@@   @@      @     @     @ @@@@@   @@               @@@                  \n"
            "         @@@@@@      @@@                   @@@@       @ "+ str(a(38)) +"  @     @   @   @    @      @@@@@@@@@                    \n"
            "        @@     @@@@ @@                         @@@+  @     @  "+ str(a(39)) +" @    @   @     @    @@                            \n"
            "        @.  "+ str(a(30)) +"     @@:                            @@@@    @     @ "+ str(a(40)) +"  @    @ "+ str(a(42)) +"  @  @@                             \n"
            "        @       @@@ @@                               @@@@@     @     @  "+ str(a(41)) +"  @     @@@                              \n"
            "        @@   @@@     #@@                                 @@@@ @      @      @   @@@                                \n"
            "         @@@@       @  @@@@                                  @@@@@@  @       @@@@                                  \n"
            "         @@    "+ str(a(29)) +"  @      @@@@@                                   @@@@@@@@@@@                                      \n"
            "          @@      @       @   @@@@@                                                                                \n"
            "           @@=   @   "+ str(a(28)) +"   @      @@@@@@@@                                                                          \n"
            "            @@@  @       @      @      @@@@@@@@                                                                    \n"
            "              @@@        @  "+ str(a(27)) +"  @      @    @@@@@@@@@@@                                                            \n"
            "                @@@@    @      @@  "+ str(a(26)) +"  @      @     @@@@@@@@@@@@                                                   \n"
            "                   @@@@ @      @      @@      @       @     @@@@@@@@@@@@@                                          \n"
            "                      @@@@@    @      @   "+ str(a(25)) +" @@       @      @        @@@@@@@@                                     \n"
            "                          @@@@@       @      @   "+ str(a(24)) +"  @       @       @       @@@@@                                 \n"
            "                              @@@@@@  @      @       @  "+ str(a(23)) +"  @   "+ str(a(22)) +"  @       @     @@@                              \n"
            "                                    @@@@@@@  @       @      @       @  "+ str(a(21)) +"  @         @@@                           \n"
            "                                           @@@@@@@@@@@@     @      @      @   "+ str(a(20)) +"   @@  @@@                         \n"
            "                                                       @@@@@@@@@@@@@     @       @@      @@                        \n"
            "                  @@@@@@@@@@@@@@@                                   @@@@@@     @@   "+ str(a(19)) +"    @@                       \n"
            "               @@@        @      @@@@@                                   @@@@ @          @ @@                      \n"
            "              @@@     "+ str(a(6)) +"   @     @     @@@@                                  @@@      @@@@   @@                     \n"
            "             @@  @@@     @  "+ str(a(7)) +"  @      @  .@@@:                                @@ @@@@        @                     \n"
            "             @@     @@@  @     @  "+ str(a(8)) +"  @     @ @@@@                              @@            @                     \n"
            "            .@   "+ str(a(5)) +"     @ @    @     @  "+ str(a(9)) +"  @     @@@@                           @@     "+ str(a(18)) +"     @                     \n"
            "            %@      @@@ @@@@@@@@   @     @ "+ str(a(10)) +"  @    @@@@                       @@@           @                     \n"
            "            +@  @@@@   @@@      @@@@.   @     @      @  @@@@@                @@@  @@        @@                     \n"
            "             @@@       #@           @@@@    @@  "+ str(a(11)) +"  @     @ .@@@@@@@@@@@@@@@@@@     @@@    @@                      \n"
            "             @@    "+ str(a(4)) +"   @@@              @@@@       @ "+ str(a(12)) +"  @      @    @    @    @       @@ @@                       \n"
            "              @@     @@  @@                @@@@   @     @  "+ str(a(13)) +"  @     @     @    @  "+ str(a(17)) +"    @@                        \n"
            "               @@ @@@@    @@@@                @@@@@    @      @  "+ str(a(14)) +"  @ "+ str(a(15)) +"  @ "+ str(a(16)) +"  @     @@@                         \n"
            "                @@@    "+ str(a(3)) +"     @@@@                 @@@@@@     @      @      @      @  @@@@                          \n"
            "                  @@       @@   @@@@                 %@@@@@  @      @       @      @@@@                            \n"
            "                    @@@  @@   "+ str(a(2)) +"   @@@@@@                  @@@@@@@%   @        @@@@@@                               \n"
            "                      @@@@       @@@   @@                       @@@@@@@@@@@@@@@                                    \n"
            "                         @@@@  @@@   "+ str(a(1)) +"  @@@                                                                        \n"
            "                            @@@@@         @@                                                                       \n"
            "                                 @@@@@    @@                                                                       \n"
            "                                      @@@@@                                                                        \n"
        )

        print(board)

    # drawBoard()

    def player_name():
        new = "y"
        name_list = []
        while new == "y":
            name = input("Name: ")
            if name.isalpha() is False:
                print("Input error")
                continue
            name_list.append(name)
            new = input("New participant? (Y or N): ").lower()
            while new != "y" and new != "n":
                print("Input error")
                new = input("New participant? (Y or N): ")
        return name_list
    
    for name in player_name():
        plyrs += 1
        players.append([plyrs, name, chr(64 + plyrs), 0, 0])
    
    print(players)
    
    drawBoard()
    