from Game import Game
from GameError import *
import time
import math

endgame = False
while not endgame:
    print("Welcome to Van Der Waerden Coloring Game!")
    time.sleep(1)
    print("")
    print("There are two players: you and computer.")
    time.sleep(1)
    print("Both of you are coloring a board that consists of numbers from 1 to n.")
    time.sleep(1)
    print("There is also another number, k, which stands for length of arithmetic progression.")
    time.sleep(1)
    print("In each round a player can color (assign to himself) one number of 1 to n that hasn't been occupied yet.")
    time.sleep(1)
    print("You have to choose your numbers carefully!")
    time.sleep(1)
    print("The game ends when some player chooses a number that completes a k-length arithmetic progression.")
    time.sleep(1)
    passed = False
    while not passed:
        print("")
        print("Please choose a length of a board:")
        n = (input("n = "))
        try:
            n = int(n)
        except:
            print("This is not an integer")
            continue
        if n<5:
            print("n must be bigger or equal to 5!")
            continue
        passed = True
    maximum_k = math.floor((n+1)/2)
    passed = False
    while not passed:
        print("")
        print("Please choose a length of a arithmetic progression:")
        k = (input("k = "))
        try:
            k = int(k)
        except:
            print("This is not an integer")
            continue
        if k<=2:
            print("k must be bigger than 2!")
            continue
        if k>maximum_k:
            print("k must be smaller or equal to "+str(maximum_k)+"!")
            continue
        passed = True
    passed = False
    while not passed:
        print("")
        print("Please choose a strategy for computer")
        print("1 - defensive, 2 - offensive, 3 - combined, 4 - random")
        strategy_input = input("Strategy: ")
        try:
            strategy_input = int(strategy_input)
        except:
            print("This is not an integer")
            continue
        if strategy_input not in [1,2,3,4]:
            print("Invalid number!")
            continue
        passed = True
    passed = False
    while not passed:
        print("")
        print("Please choose who's going to start")
        print("1 - you, 2 - computer")
        who_start = input("Starting player: ")
        try:
            who_start = int(who_start)
        except:
            print("This is not an integer")
            continue
        if who_start not in [1,2]:
            print("Invalid number!")
            continue
        passed = True

    game = Game(n,k)

    last_player = 1
    if who_start == 1:
        last_player = 2

    while True:
        player = Game.other_player(last_player)
        last_player = player

        # user
        if player==1:
            i = int(input("Choose number: "))
            game.choose_number(player,i)

        # computer
        elif player==2:
            st = game.strategy[strategy_input-1]
            game.computer_movement(player,st)
        else:
            print("Wrong player")
        try:
            game.losing_condition(player)
            game.draw_condition()
        except PlayerLost: break
        except Draw: break

    passed = False
    while not passed:
        new_game = input("Do you want to start new game [y/n]? ")
        if new_game == "n":
            endgame = True
            passed = True
        elif new_game == "y":
            passed = True
        else:
            print("Incorrect input.")
