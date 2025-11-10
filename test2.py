def number_guess():
    import random
    turn = 3
    score = 5
    top = 10
    ready = ""
    print("Guess the right number between 1 and 20\n"
          "Type 'start' when you're ready")
    while ready != "start":
        ready = input()
    print("")

    num = random.randint(1, 20)
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
 
number_guess()