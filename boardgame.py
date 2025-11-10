### when game start no more conn accept
### ending with points instead of who reaches first; loop board until everyone passes through end atleast once
### if not player asked for input, their message will be ignored UNLESS socket disconnect
### improve player appending

with open("words_alpha.txt") as f:
    word_set = set(word.strip().lower() for word in f)
from board import drawBoard
from minigames import speed_typing, number_guess, word_guess, rps_game
import socket
import threading
import random
import time

HOST = '0.0.0.0'
PORT = 50000
turn = 1
end = 0
cBoard = ""
diceTile = []
pointTile = []
gameTile = []
unluckyTile = []
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
                    diceTile = [7, 8, 12, 13, 17, 18, 22, 23, 27, 28, 32, 33, 37, 38, 42]
                    pointTile = [4, 9, 14, 19, 24, 29, 31, 36, 34, 39]
                    gameTile = [6, 11, 16, 21, 26, 41]
                    unluckyTile = [1, 2, 3]
                    end = 43
                    break
                if msg == 'neo':
                    cBoard = "neo"
                    diceTile = [4, 7, 8, 10, 11, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31, 34]
                    pointTile = [5, 9, 12, 13, 17, 20, 21, 25, 29, 33]
                    gameTile = [6, 16, 24, 28, 32]
                    unluckyTile = [1, 2, 3]
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
        broadcast(drawBoard(players, cBoard))
        
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
                # broadcast(drawBoard(players, cBoard))
                
                if q[4] in gameTile:
                    random_game = random.randint(1, 1)
                    
                    minigame(random_game)
                                        
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

def minigame(random_game):
    if random_game == 1:
        broadcast(b'Speed typing minigame starting!\n')

        minigame_scores = []
        threads = []
        score_lock = threading.Lock()

        def play_speed_typing(player):
            try:
                score = speed_typing(player[6])
            except Exception as e:
                score = 0
                try:
                    player[6].sendall(f"Error during minigame: {e}\n".encode())
                except:
                    pass
            with score_lock:
                player[3] += score
                minigame_scores.append((player[1], score, player[3]))

        # one thread per player
        for p in players:
            t = threading.Thread(target=play_speed_typing, args=(p,))
            t.start()
            threads.append(t)

        # wait for all threads to finish
        for t in threads:
            t.join()

        for name, score, total in minigame_scores:
            broadcast(f"{name} scored {score} points in the minigame, now has {total} points.\n")

        broadcast(b'Loading...\n')
        time.sleep(3)

    elif random_game == 2:
        broadcast(b'Word guessing minigame starting!\n')
        word_guess()
        broadcast(b'Loading...\n')
        time.sleep(3)

    elif random_game == 3:
        broadcast(b'Number guessing minigame starting!\n')
        number_guess()
        broadcast(b'Loading...\n')
        time.sleep(3)
        
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            

if __name__ == '__main__':
    main()