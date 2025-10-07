### when game start no more conn accept
### ending with points instead of who reaches first; loop board until everyone passes through end atleast once
### if not player asked for input, their message will be ignored UNLESS socket disconnect
### improve player appending

with open("words_alpha.txt") as f:
    word_set = set(word.strip().lower() for word in f)
import socket
import threading
import random
import time

HOST = '0.0.0.0'
PORT = 12345
turn = 1
end = 0
cBoard = ""
diceTile = []
pointTile = []
gameTile = []
players = [
    # [0id, 1naam, 2piece, 3points, 4positions, 5address, 6conn, 7smalldice, 8bigdice, 9superdice],
]
lock = threading.Lock()
game_started = threading.Event()
LIGHT_GREEN = "\033[92m"
GREEN = "\033[32m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# talk to all players
def broadcast(message):
    with lock:
        for p in players:
            try:
                if isinstance(message, str):
                    p[6].sendall(message.encode())
                else:
                    p[6].sendall(message)
            except Exception as e:
                print(f"Broadcast error to {p[1]}: {e}")

# all main functionality
def handle_client(conn, addr):
    global players, turn, cBoard, diceTile, pointTile, gameTile, end
    try:
        conn.sendall(b'Enter your name: ')
        name = conn.recv(1024).decode().strip()
        # welcome and register new players
        with lock:
            player_id = len(players) + 1
            piece = chr(64 + player_id)
            players.append([player_id, name, piece, 0, 0, addr[1], conn, 0, 0, 0])
            is_host = (player_id == 1)
            print(f'Player {player_id}: ({name}) connected from {addr}. Assigned piece: {piece}: ', players)
            message = (
                f"To play the game, you will need to roll dice and move your piece on the board.\n"
                f"You can choose between {YELLOW}small dice{RESET} (1-3), {YELLOW}normal dice{RESET} (1-6), {YELLOW}big dice{RESET} (1-9) and {YELLOW}super dice{RESET} (4-9).\n"
                "During play, you may encounter special events which can give you dice, points or minigames to participate in.\n"
                "The goal is to reach the end of the board with as much points as possible! Points can be gained through tiles, minigames and reaching the end.\n"
                "Good luck and have fun!\n"
            )
            conn.sendall(message.encode())
        # if player == 0, become host
        if is_host:
            conn.sendall(f'You are the host!\n'.encode())
            conn.sendall(b'Type out which map you want to play on:\n')
            conn.sendall(b'1. Snake (43 tiles)\n')
            conn.sendall(b'2. Neo (45 tiles)\n')
            while True:
                msg = conn.recv(1024).decode().strip().lower()
                if msg == 'snake':
                    cBoard = "snake"
                    diceTile = [2, 3, 7, 8, 12, 13, 17, 18, 22, 23, 27, 28, 32, 33, 37, 38, 42]
                    pointTile = [4, 9, 14, 19, 24, 29, 31, 36, 34, 39]
                    gameTile = [6, 11, 16, 21, 26, 41]
                    end = 43
                    break
                if msg == 'neo':
                    cBoard = "neo"
                    diceTile = [3, 4, 7, 8, 10, 11, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31, 34]
                    pointTile = [5, 9, 12, 13, 17, 20, 21, 25, 29, 33]
                    gameTile = [6, 16, 24, 28, 32]
                    end = 45
                    break
                else:
                    conn.sendall(b'Invalid map.\n')
                    continue
            print(f"Map selected: {cBoard} with {end} tiles.")
            conn.sendall(b'Type "start" to begin the game when ready.')
            while True:
                msg = conn.recv(1024).decode().strip().lower()
                if msg == 'start':
                    print("Start received from host.")
                    broadcast(f'Host {name} started the game!\n')
                    game_started.set()
                    break
                else:
                    conn.sendall(b'Type "start" to begin the game.\n')
        else:
            conn.sendall(f'Welcome, {name}! Waiting for the host to start the game...\n'.encode())
        
        # wait until host unlocks 
        game_started.wait()
        print("Game started, notifying players.\n")
        broadcast(b'Game started!\n')
        
        broadcast(f'Selected map: {cBoard} with {end} tiles.\n')
        for p in players:
            broadcast(f'Player {p[0]}: {p[1]} with piece {p[2]}\n')
        broadcast(b'Board generating in 5 seconds...\n')
        time.sleep(5)
        broadcast(drawBoard())
        
        ### MAIN GAME LOOP ###
        while True:
            finish = False
            
            # find which player turn
            for q in players:
                small_dice = random.randint(1, 3)
                normal_dice = random.randint(1, 6)
                big_dice = random.randint(1, 9)
                super_dice = random.randint(4, 9)
                move = ""
                chosen_dice = ""
                msg_turn = ""
                
                broadcast(f"\nIt's {q[1]}'s turn.\n\n")
                if turn == q[0]:
                    if q[7] >= 1:
                        q[6].sendall(f"You have {str(q[7])} {YELLOW}small dice{RESET} (1-3 eyes). Type \"small\" to throw a {YELLOW}small dice{RESET}.\n".encode())
                    q[6].sendall(f"You have unlimited {YELLOW}normal dice{RESET} (1-6 eyes). Type \"normal\" to throw a {YELLOW}normal dice{RESET}.\n".encode())
                    if q[8] >= 1:
                        q[6].sendall(f"You have {str(q[8])} {YELLOW}big dice{RESET} (1-9 eyes). Type \"big\" to throw a {YELLOW}big dice{RESET}.\n".encode())
                    if q[9] >= 1:
                        q[6].sendall(f"You have {str(q[9])} {YELLOW}super dice{RESET} (4-9 eyes). Type \"super\" to throw a {YELLOW}super dice{RESET}.\n".encode())
                    
                    while True:
                        msg_turn = q[6].recv(1024).decode().strip().lower()
                        if msg_turn == 'small' and q[7] >= 1:
                            move = small_dice
                            q[4] += move
                            q[7] -= 1
                            chosen_dice = "small dice"
                        elif msg_turn == 'normal':
                            move = normal_dice
                            q[4] += move
                            chosen_dice = "normal dice"
                        elif msg_turn == 'big' and q[8] >= 1:
                            move = big_dice
                            q[4] += move
                            q[8] -= 1
                            chosen_dice = "big dice"
                        elif msg_turn == 'super' and q[9] >= 1:
                            move = super_dice
                            q[4] += move
                            q[9] -= 1
                            chosen_dice = "super dice"
                        else:
                            q[6].sendall(b'Invalid choice or no dice left. Try again.\n')
                            continue
                        
                        broadcast(f"{q[1]} threw the {chosen_dice}, rolling a {move}, moving to position {q[4]}.\n")
                        turn += 1
                        break
                
                if q[4] in diceTile:
                    random_bonus = random.randint(1, 11)
                    random_amount = random.randint(1, 2)
                    
                    if random_bonus in range(1, 6):
                        q[7] += random_amount
                        broadcast(f"{q[1]} found a {YELLOW}small dice{RESET} bonus! Now has {q[7]} small dice.\n")
                    elif random_bonus in range(6, 11):
                        q[8] += random_amount
                        broadcast(f"{q[1]} found a {YELLOW}big dice{RESET} bonus! Now has {q[8]} big dice.\n")
                    elif random_bonus == 11:
                        q[9] += 1
                        broadcast(f"{q[1]} found a {YELLOW}super dice{RESET} bonus! Now has {q[9]} super dice.\n")
                
                if q[4] in pointTile:
                    random_points = random.randint(-5, 5)
                    q[3] += random_points
                    if random_points >= 0:
                        broadcast(f"{q[1]} found a {YELLOW}point bonus{RESET}! Gained {random_points} points, now has {q[3]} points.\n")
                    else:
                        broadcast(f"{q[1]} hit a {RED}point penalty{RESET}! Lost {-random_points} points, now has {q[3]} points.\n")
                
                time.sleep(2)
                broadcast(drawBoard())
                
                if q[4] in gameTile:
                    random_game = random.randint(1, 1)
                    
                    if random_game == 1:
                        broadcast(b'Speed typing minigame starting!\n')
                        
                        minigame_scores = []
                        for p in players:
                            try:
                                score = speed_typing(p[6])
                            except Exception as e:
                                score = 0
                                p[6].sendall(b"Error during minigame. Score: 0\n")
                            p[3] += score
                            minigame_scores.append((p[1], score, p[3]))
                            
                        for name, score, total in minigame_scores:
                            broadcast(f"{name} scored {score} points in the minigame, now has {total} points.\n")
                        broadcast(b'Loading...\n')
                        time.sleep(3)
                        
                    elif random_game == 2:
                        broadcast(b'Numer guessing minigame starting!\n')
                        
                        number_guess()
                        
                        broadcast(b'Loading...\n')
                        time.sleep(3)
                        
                    elif random_game == 3:
                        broadcast(b'Word guessing minigame starting!\n')
                        
                        word_guess()
                        
                        broadcast(b'Loading...\n')
                        time.sleep(3)
                                        
                if q[4] >= end:
                    q[4] == end
                    broadcast(f"\n{q[1]} has reached the end and wins the game! Congratulations!\n")
                    finish = True
                if turn == len(players) + 1:
                    turn = 1
                    for p in players:
                        broadcast(f"{p[1]} has {p[3]} points\n")
            if finish:
                break
        broadcast("Game over! Final scores:\n")
        for p in players:
            broadcast(f"{p[1]}: {p[3]} points\n")
            broadcast(b'Thank you for playing!\n')
            broadcast(b'The server will shut down in 10 seconds.\n')
            time.sleep(10)
            broadcast(b'Server shutting down.\n')
            conn.close()
            
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected.")
                break
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    with lock:
        players = [p for p in players if p[5] != addr[1]]
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

    if cBoard == "snake":
        board = [
            [( "                                                                                                    @@", LIGHT_GREEN)],
            [( "                                                                                                    @@", LIGHT_GREEN)],
            [( "                                                                                                    @@", LIGHT_GREEN)],
            [( "                                                                                                    @@@@@@@", LIGHT_GREEN)],
            [( "                                                                                                   @@", LIGHT_GREEN)],
            [( "                                                                                        @@@@@@@@@@@@", LIGHT_GREEN)],
            [( "                                                                                 @@@@@@@@@     -@@@", LIGHT_GREEN)],
            [( "                                                                               @@@                @", LIGHT_GREEN)],
            [( "                         @@@@@@@@@@@@@@@+                                    :@@                  @@", LIGHT_GREEN)],
            [( "                    @@@@@@  @        @ @@@@@@                                @@      @@@          @@", LIGHT_GREEN)],
            [( "                 @@@@        @  ", LIGHT_GREEN), (a(34), RED), ("  @      @ @@@@%                           @@     @@            @@", LIGHT_GREEN)],
            [( "              =@@@   @@   ", LIGHT_GREEN), (a(33), RED), ("  @    @  ", LIGHT_GREEN), (a(35), RED), ("   @     @@@@@                       @@             @     @@", LIGHT_GREEN)],
            [( "             @@        @@@    @    @      @@      @  @@@@@                   @@            @@     @", LIGHT_GREEN)],
            [( "           @@@ @@   ", LIGHT_GREEN), (a(32), RED), ("    @    @  @       @  ", LIGHT_GREEN), (a(36), RED), ("   @      @@@@@               @     ", LIGHT_GREEN), (a(43), RED), ("     @@     @@", LIGHT_GREEN)],
            [( "          @@     @@@       @@@@@@@@@@@-  @       @  ", LIGHT_GREEN), (a(37), RED), ("  @    @@@@@@@@     @@@                   @@", LIGHT_GREEN)],
            [( "         @@    ", LIGHT_GREEN), (a(31), RED), ("   @  @@@@            @@@@@   @@      @     @     @ @@@@@   @@               @@@", LIGHT_GREEN)],
            [( "         @@@@@@      @@@                   @@@@       @ ", LIGHT_GREEN), (a(38), RED), ("  @     @   @   @    @      @@@@@@@@@", LIGHT_GREEN)],
            [( "        @@     @@@@ @@                         @@@+  @     @  ", LIGHT_GREEN), (a(39), RED), (" @    @   @     @    @@", LIGHT_GREEN)],
            [( "        @.  ", LIGHT_GREEN), (a(30), RED), ("     @@:                            @@@@    @     @ ", LIGHT_GREEN), (a(40), RED), ("  @    @ ", LIGHT_GREEN), (a(42), RED), ("  @  @@", LIGHT_GREEN)],
            [( "        @       @@@ @@                               @@@@@     @     @  ", LIGHT_GREEN), (a(41), RED), ("  @     @@@", LIGHT_GREEN)],
            [( "        @@   @@@     #@@                                 @@@@ @      @      @   @@@", LIGHT_GREEN)],
            [( "         @@@@       @  @@@@                                  @@@@@@  @       @@@@", LIGHT_GREEN)],
            [( "         @@    ", LIGHT_GREEN), (a(29), RED), ("  @      @@@@@                                   @@@@@@@@@@@", LIGHT_GREEN)],
            [( "          @@      @       @   @@@@@", LIGHT_GREEN)],
            [( "           @@=   @   ", LIGHT_GREEN), (a(28), RED), ("   @      @@@@@@@@", LIGHT_GREEN)],
            [( "            @@@  @       @      @      @@@@@@@@", LIGHT_GREEN)],
            [( "              @@@        @  ", LIGHT_GREEN), (a(27), RED), ("  @      @    @@@@@@@@@@@", LIGHT_GREEN)],
            [( "                @@@@    @      @@  ", LIGHT_GREEN), (a(26), RED), ("  @      @     @@@@@@@@@@@@", LIGHT_GREEN)],
            [( "                   @@@@ @      @      @@      @       @     @@@@@@@@@@@@@", LIGHT_GREEN)],
            [( "                      @@@@@    @      @   ", LIGHT_GREEN), (a(25), RED), (" @@       @      @        @@@@@@@@", LIGHT_GREEN)],
            [( "                          @@@@@       @      @   ", LIGHT_GREEN), (a(24), RED), ("  @       @       @       @@@@@", LIGHT_GREEN)],
            [( "                              @@@@@@  @      @       @  ", LIGHT_GREEN), (a(23), RED), ("  @   ", LIGHT_GREEN), (a(22), RED), ("  @       @     @@@", LIGHT_GREEN)],
            [( "                                    @@@@@@@  @       @      @       @  ", LIGHT_GREEN), (a(21), RED), ("  @         @@@", LIGHT_GREEN)],
            [( "                                           @@@@@@@@@@@@     @      @      @   ", LIGHT_GREEN), (a(20), RED), ("   @@  @@@", LIGHT_GREEN)],
            [( "                                                       @@@@@@@@@@@@@     @       @@      @@", LIGHT_GREEN)],
            [( "                  @@@@@@@@@@@@@@@                                   @@@@@@     @@   ", LIGHT_GREEN), (a(19), RED), ("    @@", LIGHT_GREEN)],
            [( "               @@@        @      @@@@@                                   @@@@ @          @ @@", LIGHT_GREEN)],
            [( "              @@@     ", LIGHT_GREEN), (a(6), RED), ("   @     @     @@@@                                  @@@      @@@@   @@", LIGHT_GREEN)],
            [( "             @@  @@@     @  ", LIGHT_GREEN), (a(7), RED), ("  @      @  .@@@:                                @@ @@@@        @", LIGHT_GREEN)],
            [( "             @@     @@@  @     @  ", LIGHT_GREEN), (a(8), RED), ("  @     @ @@@@                              @@            @", LIGHT_GREEN)],
            [( "            .@   ", LIGHT_GREEN), (a(5), RED), ("     @ @    @     @  ", LIGHT_GREEN), (a(9), RED), ("  @     @@@@                           @@     ", LIGHT_GREEN), (a(18), RED), ("     @", LIGHT_GREEN)],
            [( "            %@      @@@ @@@@@@@@   @     @ ", LIGHT_GREEN), (a(10), RED), ("  @    @@@@                       @@@           @", LIGHT_GREEN)],
            [( "            +@  @@@@   @@@      @@@@.   @     @      @  @@@@@                @@@  @@        @@", LIGHT_GREEN)],
            [( "             @@@       #@           @@@@    @@  ", LIGHT_GREEN), (a(11), RED), ("  @     @ .@@@@@@@@@@@@@@@@@@     @@@    @@", LIGHT_GREEN)],
            [( "             @@    ", LIGHT_GREEN), (a(4), RED), ("   @@@              @@@@       @ ", LIGHT_GREEN), (a(12), RED), ("  @      @    @    @    @       @@ @@", LIGHT_GREEN)],
            [( "              @@     @@  @@                @@@@   @     @  ", LIGHT_GREEN), (a(13), RED), ("  @     @     @    @  ", LIGHT_GREEN), (a(17), RED), ("    @@", LIGHT_GREEN)],
            [( "               @@ @@@@    @@@@                @@@@@    @      @  ", LIGHT_GREEN), (a(14), RED), ("  @ ", LIGHT_GREEN), (a(15), RED), ("  @ ", LIGHT_GREEN), (a(16), RED), ("  @     @@@", LIGHT_GREEN)],
            [( "                @@@    ", LIGHT_GREEN), (a(3), RED), ("     @@@@                 @@@@@@     @      @      @      @  @@@@", LIGHT_GREEN)],
            [( "                  @@       @@   @@@@                 %@@@@@  @      @       @      @@@@", LIGHT_GREEN)],
            [( "                    @@@  @@   ", LIGHT_GREEN), (a(2), RED), ("   @@@@@@                  @@@@@@@%   @        @@@@@@", LIGHT_GREEN)],
            [( "                      @@@@       @@@   @@                       @@@@@@@@@@@@@@@", LIGHT_GREEN)],
            [( "                         @@@@  @@@   ", LIGHT_GREEN), (a(1), RED), ("  @@@", LIGHT_GREEN)],
            [( "                            @@@@@         @@", LIGHT_GREEN)],
            [( "                                 @@@@@    @@", LIGHT_GREEN)],
            [( "                                      @@@@@", LIGHT_GREEN)],
        ]
    elif cBoard == "neo":
        board = [
            [("                                                    @                                                     ", YELLOW)],
            [("                                                   @ @                                                    ", YELLOW)],
            [("                                                  @   @                                                   ", YELLOW)],
            [("                                                 @     @                                                  ", YELLOW)],
            [("                                           @@@@@@  " + CYAN + str(a(45)) + YELLOW + "   @@@@@@                                            ", YELLOW)],
            [("                                             @@@@       @@@@                                              ", YELLOW)],
            [("                                                 @  @  @                                                  ", YELLOW)],
            [("                                                @  @ @  @                                                 ", YELLOW)],
            [("                                               @  @   @  @                                                ", YELLOW)],
            [("                                              @   @   @   @                                               ", YELLOW)],
            [("                                   @@@       @   @     @   @        @@@                                   ", YELLOW)],
            [("                              @@@@@   @@@@   @  @   " + CYAN + str(a(44)) + YELLOW + "  @  @   @@@@@  @@@@@@                              ", YELLOW)],
            [("                           @@@            @@@@ @    @    @ @@@@             @@                            ", YELLOW)],
            [("                         @@     " + CYAN + str(a(32)) + YELLOW + "  @@@@@@@@@  @   @ @   @  @@@@@@@@@  " + CYAN + str(a(43)) + YELLOW + "     @@                          ", YELLOW)],
            [("                        @    " + CYAN + str(a(31)) + YELLOW + "   @@         @@   @   @   @@         @@   " + CYAN + str(a(42)) + YELLOW + "    @                         ", YELLOW)],
            [("                       @         @   @@@@@@@      @   @     @@@@@@@   @         @                        ", YELLOW)],
            [("                       @       @@  @@       @@@  @     @  @@@       @@  @@       @                        ", YELLOW)],
            [("                       @  " + CYAN + str(a(30)) + YELLOW + "  @   @    " + CYAN + str(a(33)) + YELLOW + "      @@       @@      " + CYAN + str(a(39)) + YELLOW + "    @   @  " + CYAN + str(a(41)) + YELLOW + "  @                        ", YELLOW)],
            [("                       @      @   @                                   @   @      @                        ", YELLOW)],
            [("                       @      @   @    " + CYAN + str(a(34)) + YELLOW + "                       " + CYAN + str(a(38)) + YELLOW + "    @   @      @                        ", YELLOW)],
            [("                       @  " + CYAN + str(a(29)) + YELLOW + "  @   @        " + CYAN + str(a(35)) + YELLOW + "      " + CYAN + str(a(36)) + YELLOW + "       " + CYAN + str(a(37)) + YELLOW + "        @   @  " + CYAN + str(a(40)) + YELLOW + "  @                        ", YELLOW)],
            [("                        @     @    @                                  @   @     @                         ", YELLOW)],
            [("                         @@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@                          ", YELLOW)],
            [("               @@@                                                                                        ", YELLOW)],
            [("               @  @@     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      @@@@@                ", YELLOW)],
            [("                @   @@   @                          " + CYAN + str(a(28)) + YELLOW + "                        @    @@    @                ", YELLOW)],
            [("                @    @   @     " + CYAN + str(a(10)) + YELLOW + "    " + CYAN + str(a(11)) + YELLOW + "    " + CYAN + str(a(12)) + YELLOW + "   " + CYAN + str(a(13)) + YELLOW + "      " + CYAN + str(a(14)) + YELLOW + "   " + CYAN + str(a(15)) + YELLOW + "   " + CYAN + str(a(16)) + YELLOW + "   " + CYAN + str(a(17)) + YELLOW + "     @    @    @                 ", YELLOW)],
            [("                @    @   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @    @                 ", YELLOW)],
            [("                 @@  @                                                             @  @@                  ", YELLOW)],
            [("                   @@ @ " + RED + "  @@@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@ " + YELLOW + "  @@@                    ", YELLOW)],
            [("                     @@ " + RED + "  @     " + CYAN + str(a(9)) + RED + "     @   @         " + CYAN + str(a(27)) + RED + "         @   @    " + CYAN + str(a(18)) + RED + "    @ " + YELLOW + "  @@                      ", YELLOW)],
            [("           @@@@@@@   @@  " + RED + " @           @   @                   @   @           @ " + YELLOW + "  @@   @@@@@@@            ", YELLOW)],
            [("             @@   @@ @ @ " + RED + " @     " + CYAN + str(a(8)) + RED + "      @   @@       " + CYAN + str(a(26)) + RED + "       @   @     " + CYAN + str(a(19)) + RED + "     @ " + YELLOW + " @ @ @@   @@              ", YELLOW)],
            [("               @@@@@@@ @  " + RED + " @            @    @@@          @@@    @           @  " + YELLOW + " @ @@@@@@@                ", YELLOW)],
            [("                      @ @ " + RED + " @      " + CYAN + str(a(7)) + RED + "      @      @@@@@@@@@@     @@     " + CYAN + str(a(20)) + RED + "     @ " + YELLOW + " @ @                       ", YELLOW)],
            [("                       @ @ " + RED + " @@            @@@               @@@             @ " + YELLOW + "  @ @                       ", YELLOW)],
            [("                       @ @  " + RED + "  @     " + CYAN + str(a(6)) + RED + "        @@@         @@@       " + CYAN + str(a(21)) + RED + "      @ " + YELLOW + "  @ @                        ", YELLOW)],
            [("                        @ @@ " + RED + " @@                @@@@@@@@@                @@ " + YELLOW + "  @ @                         ", YELLOW)],
            [("                         @  @  " + RED + " @      " + CYAN + str(a(5)) + RED + "                        " + CYAN + str(a(22)) + RED + "      @  " + YELLOW + " @@ @                          ", YELLOW)],
            [("               @@@@@@@@@@    @@ " + RED + " @@@       " + CYAN + str(a(4)) + RED + "       " + CYAN + str(a(25)) + RED + "      " + CYAN + str(a(23)) + RED + "        @@@  " + YELLOW + " @    @@@@@@@@@@                ", YELLOW)],
            [("                 @@@@@@@@@@@@  @  " + RED + "  @@          " + CYAN + str(a(3)) + RED + "      " + CYAN + str(a(24)) + RED + "          @@  " + YELLOW + "  @@ @@@@@@@@@@@@                  ", YELLOW)],
            [("                             @@ @@@  " + RED + " @@@@          " + CYAN + str(a(2)) + RED + "          @@@@  " + YELLOW + "  @@  @                              ", YELLOW)],
            [("                               @@  @@   " + RED + "  @@@@@@@@     @@@@@@@@   " + YELLOW + "  @@@  @@                               ", YELLOW)],
            [("                                 @@  @@@    " + RED + "      @@@@@     " + YELLOW + "     @@@  @@@                                 ", YELLOW)],
            [("                                   @    @@@@@               @@@@@    @                                    ", YELLOW)],
            [("                              @@@@@  @@@@@   @@@@@@@@@@@@@@@   @@@@@  @@@@@                               ", YELLOW)],
            [("                            @@@@@ @@@     @@@@@@         @@@@@@     @@@ @@@@@                             ", YELLOW)],
            [("                                 @              @   " + CYAN + str(a(1)) + YELLOW + "   @              @                                  ", YELLOW)],
            [("                                                 @     @                                                  ", YELLOW)],
            [("                                                  @   @                                                   ", YELLOW)],
            [("                                                  @   @                                                   ", YELLOW)],
            [("                                                  @   @                                                   ", YELLOW)],
            [("                                                   @ @                                                    ", YELLOW)],
            [("                                                    @                                                     ", YELLOW)],
            [("                                                    @                                                     ", YELLOW)],
        ]

    colored_board = ""
    for line in board:
        for segment, color in line:
            colored_board += color + segment
        colored_board += RESET + "\n"
    board = colored_board
    
    return board

def speed_typing(conn):
    base = 3
    size = 3
    turn = 0
    score = 0
    conn.sendall(b"Type the given letters as fast as possible; there is a time limit!\n")
    conn.sendall(b"Words will be sent right after each other, so get ready!\n")
    conn.sendall(b"Starting in 5...")
    time.sleep(3)
    conn.sendall(b"2...")
    time.sleep(1)
    conn.sendall(b"1...")
    time.sleep(1)
    while True:
        letters = ""
        if turn == 3:
            size += 1
            turn = 0
        for j in range(size):
            letters += chr(random.randint(ord("a"), ord("z")))
        timer = (base + (len(letters) - 3 * 0.5)) - turn
        conn.sendall(f"Type this: {letters}\n".encode())
        try:
            conn.settimeout(timer + 1)
            s = time.perf_counter()
            x = conn.recv(1024).decode().strip()
            e = time.perf_counter()
        except socket.timeout:
            conn.sendall(b"You typed too slow.\n")
            break
        finally:
            conn.settimeout(None)
        if x != letters:
            conn.sendall(b"You typed wrong.\n")
            break
        if (e - s) > timer:
            conn.sendall(b"You typed too slow.\n")
            break
        turn += 1
        score += 1
        if score >= 9:
            conn.sendall(b"You got everything correct. Your score is: 9 points!\n")
            score = 9
            break
    return score

def number_guess(conn):
    import random
    turn = 3
    score = 5
    top = 10
    ready = ""
    print("Guess the right number between 1 and 10\n"
          "Type 'start' when you're ready")
    while ready != "start":
        ready = input()
    print("")

    num = random.randint(1, 10)
    while turn > 0:
        print(num)
        print(f"You still have {turn} guesses left")
        guess = int(input("The number is? "))
        diff = num - guess
        if diff > 0:
            print("Your number is too small")
        if diff < 0:
            print("Your number is too big")
        if diff == 0:
            turn = 0
        diff = pow(pow(diff, 2), 0.5)
        if diff <= top:
            top = diff
        turn = turn - 1
    high = score - top
    print(f"The correct number is {num}\n"
          f"You score {high} points!")
    return high

def word_guess():
    import time
    word = random.choice(list(word_set))
    broadcast(b"Each player in order of turns, will be given 2 letters with which to form a word.\n")
    broadcast(b"The word has to be a real word, and the letters can be anywhere in the word.\n")
    conn.sendall(b"Starting in 5...")
    time.sleep(3)
    conn.sendall(b"2...")
    time.sleep(1)
    conn.sendall(b"1...")
    time.sleep(1)
    while True:
        for p in players:
            if turn == p[0]:
                print("Player choosing: ", p)
                msg_turn = q[6].recv(1024).decode().strip().lower()
            

if __name__ == '__main__':
    main()