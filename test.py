with open("words_alpha.txt") as f:
    word_set = set(word.strip().lower()for word in f)

def speed_typing():
    import time
    import random
    base = 3
    size = 1
    turn = 0
    score = 0
    ready = ""
    print("Type the given letters withing the time limit\n"
          "Type 'start' when you're ready")
    while ready != "start":
        ready = input()
    time.sleep(0.5)
    print("")
    while True:
        word = ""
        if turn == 3:
            size = size + 1
            turn = 0
        while len(word) != size:
            word = random.choice(word_set)
        timer = (base + (len(word) - 3 * 0.5)) - turn
        print(word)
        s = time.perf_counter()
        x = input()
        e = time.perf_counter()
        print(f"Elapsed: {round((e - s), 3)} s")
        if x != word:
            print("You typed wrong\n"
                  f"Your score is: {score} points!")
            return score
        if (e - s) > timer:
            print("You typed to slow\n"
                  f"Your score is: {score} points!")
            return score
        turn = turn + 1
        score = score + 1
        if score >= 9:
            print("You got everything correct.\n"
                  "Your score is: 9 points!")
            score = 9
            return score

speed_typing