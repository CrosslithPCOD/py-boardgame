### when game start no more conn accept
### fix the board drawing function

import socket
import threading
import random
import time

HOST = '0.0.0.0'
PORT = 12345
turn = 1
players = [
    # [0id,'1naam','2piece','3points', 4positions, 5smalldice, 6bigdice, 7address, 8 conn],
]
lock = threading.Lock()
game_started = threading.Event()

def broadcast(message):
    with lock:
        for p in players:
            try:
                if isinstance(message, str):
                    p[8].sendall(message.encode())
                else:
                    p[8].sendall(message)
            except Exception as e:
                print(f"Broadcast error to {p[1]}: {e}")

def handle_client(conn, addr):
    global players, turn
    try:
        conn.sendall(b'Enter your name: ')
        name = conn.recv(1024).decode().strip()
        with lock:
            player_id = len(players) + 1
            piece = chr(64 + player_id)
            players.append([player_id, name, piece, 0, 0, 0, 0, addr[1], conn])
            is_host = (player_id == 1)
            print(f'Player {player_id}: ({name}) connected from {addr}. Assigned piece: {piece}: ', players)
        if is_host:
            conn.sendall(b'You are the host! Type "start" to begin the game when ready.\n')
            while True:
                msg = conn.recv(1024).decode().strip().lower()
                if msg == 'start':
                    print("Start received from host.")
                    broadcast(f'Host {name} started the game!\n')
                    game_started.set()
                    print("Game started.")
                    break
                else:
                    conn.sendall(b'Type "start" to begin the game.\n')
        else:
            conn.sendall(f'Welcome, {name}! Waiting for the host to start the game...\n'.encode())
        game_started.wait()
        print("Game started, notifying players.")
        broadcast(b'Game started!\n')
        
        for p in players:
            broadcast(f'Player {p[0]}: {p[1]} with piece {p[2]}\n')
        broadcast(b'Board generating in 5 seconds...\n')
        time.sleep(5)
        
        ### MAIN GAME LOOP ###
        while True:
            broadcast(drawBoard())
            finish = False
            
            # find which player turn
            for q in players:
                small_die = random.randint(1, 3)
                normal_die = random.randint(1, 6)
                big_die = random.randint(1, 12)
                move = ""
                chosen_die = ""
                
                broadcast(f"\nIt's {q[1]}'s turn (Piece: {q[2]}).\n")
                if turn == q[0]:
                    if q[5] >= 1:
                        q[8].sendall(f"You have {str(q[5])} small dice (1-3 eyes). Type \"small\" to throw a small dice.\n".encode())
                    q[8].sendall(f"You have unlimited normal dice (1-6 eyes). Type \"normal\" to throw a normal dice.\n".encode())
                    if q[6] >= 1:
                        q[8].sendall(f"You have {str(q[6])} big dice (1-12 eyes). Type \"big\" to throw a small dice.\n".encode())
                    
                    while True:
                        msg = q[8].recv(1024).decode().strip().lower()
                        if msg == 'small' and q[5] >= 1:
                            move = small_die
                            q[4] += move
                            q[5] -= 1
                            chosen_die = "small die"
                        elif msg == 'normal':
                            move = normal_die
                            q[4] += move
                            chosen_die = "normal die"
                        elif msg == 'big' and q[6] >= 1:
                            move = big_die
                            q[4] += move
                            q[6] -= 1
                            chosen_die = "big die"
                        else:
                            q[8].sendall(b'Invalid choice or no dice left. Try again.\n')
                        if not chosen_die == "":
                            turn += 1
                            a = f"{q[1]} threw the {chosen_die}, rolling a {move}, moving to position {q[4]}.\n"
                            broadcast(a)
                            break
                
                #if q[5] in (2, 3, 7, 8, 12, 13, 17, 18, 22, 23, 27, 28, 32, 33, 37, 38, 42):
                    
                if q[4] == 43:
                    broadcast(f"\n{q[1]} has reached the end and wins the game! Congratulations!\n")
                    finish = True
                if turn == len(players) + 1:
                    turn = 1
            if finish:
                break
            
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected.")
                break
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        with lock:
            players = [p for p in players if p[7] != addr[1]]
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

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
        "             @@@       #@           @@@@    @@  11  @     @ .@@@@@@@@@@@@@@@@@@     @@@    @@                      \n"
        "             @@    K   @@@              @@@@       @ "+ str(a(12)) +"  @      @    @    @    @       @@ @@                       \n"
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
    
    return board

if __name__ == '__main__':
    main()