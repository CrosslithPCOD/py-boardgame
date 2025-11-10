import socket
import threading
import random
import time


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
            conn.sendall(b"You got everything correct. Your score is: 10 points!\n")
            score = 10
            break
    return score
    

def number_guess(conn):
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