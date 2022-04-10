from Game import Game
from GameError import *



while True:
    #TODO imput validation
    n = int(input("n"))
    k = int(input("k"))

    strategy_input = int(input("defensive-1,offensive-2,combined-3,random-4"))
    who_start = int(input("player-1, computer-2"))

    game = Game(n,k)

    last_player = 1
    if who_start == 1:
        last_player = 0

    while True:
        player = Game.other_player(last_player)
        last_player = player

        # user
        if player==1:
            i = int(input("choose number"))

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


    new_game = input("Start new Game [y/n]?")
    if new_game.upper() == "N":
        break

