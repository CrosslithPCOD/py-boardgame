def number_guess(player):
    top = []
    record = 10
    num = random.randint(1, 10)
    print("Guess the right number between 1 and 10")
    for i in range(len(player)):
        guess = int(input(f"It's {player[i]} turn: "))
        diff = pow(pow(num - guess, 2), 0.5)
        if diff < record:
            record = diff
            top = [player[i]]
        elif diff == record:
            top.append(player[i])
    if len(top) > 1:
        print(f"It's a tie between {", ".join(top)}. Winner determined by dice.")
    return random.choice(top)