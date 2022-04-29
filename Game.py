import copy
import math
import random

from GameError import *

class Game:


    def __init__(self,n,k):

        # check whether arguments are valid
        if n<5 or k<=2 or 2*k-1>=n:
            raise ValueError('Invalid arguments.')
        self.n = n
        self.k = k

        self.tab = [i+1 for i in range(n)]
        self.properties = [0 for i in range(n)]
        self.players = [[],[]]

        self.subsequences = []

        #we start from any number
        for i in range(n-k+1):
            #we get any possible difference between elements in a subsequence
            for r in range(int((n-1)/(k-1))):
                this_subsequence = []
                #we build a subsequence of given length k
                for l in range(k):
                    if i+(r+1)*l<n:
                        this_subsequence.append(self.tab[i+(r+1)*l])
                if len(this_subsequence)==k:
                    self.subsequences.append(this_subsequence)

        # tab contain all players subsequences possible in future,
        self.possible_players_subsequences = [copy.deepcopy(self.subsequences),copy.deepcopy(self.subsequences)]
        number_all_subsequences = len(self.subsequences)

        # tab contains how many numbers of each subsequences payer have chose
        self.score_players_subsequences=[[0 for i in range(number_all_subsequences)],[0 for i in range(number_all_subsequences)]]

    def choose_number(self,player,i):
        if self.properties[i-1]!=0:
            print(f"Number {i} is already occupied. Choose another number.")
            return self
        else:
            print(f"Player {player} chooses number {i}.")
            self.properties[i-1]=player
            self.players[player-1].append(i)
            print(self.tab)
            print(self.properties)

            #print(self.players)

            self.update_possible_subsequences_and_scores(player,i)

    def update_possible_subsequences_and_scores(self,player,i):
        second_player=self.other_player(player)

        # delate possible subsequences in other player wich contain chooses number
        for j in reversed(range(len(self.possible_players_subsequences[second_player-1]))):
            if i in self.possible_players_subsequences[second_player-1][j]:
               self.possible_players_subsequences[second_player-1].pop(j)
               self.score_players_subsequences[second_player-1].pop(j)


        # update score of possible subsequences, plus one in which contains choose number
        for j in range(len(self.possible_players_subsequences[player-1])):
            if i in self.possible_players_subsequences[player-1][j]:
                self.score_players_subsequences[player-1][j] += 1

        #print("possible_players_subsequences:")
        #print(self.possible_players_subsequences[0])
        #print(self.possible_players_subsequences[1])

        #print("score_players_subsequences:")
        #print(self.score_players_subsequences[0])
        #print(self.score_players_subsequences[1])

    def losing_condition(self,last_player):
        end = False
        for subsequence in self.subsequences:
            if end == True:
                print(f"Player number {last_player} has lost.")
                raise PlayerLost()
                return
            this_end = True
            for i in range(len(subsequence)):
                if subsequence[i] not in self.players[last_player-1]:
                    this_end = False
            end = end + this_end
        print("Game has not ended yet.")

    def draw_condition(self): #check after losing conditions
        # if no empty field
        if not 0 in self.properties:
            print("Game end, draw")
            raise Draw

    def computer_movement(self,player,strategy="defensive"):
        second_player=self.other_player(player)

        if (strategy=="defensive"):
            occurrences = [0]*self.n
            for i, j in enumerate(self.properties):
                # fied empty
                if (j==0):
                    # count how many possibles subsequences contains field "j"
                    for subsequences_i, subsequences in enumerate(self.possible_players_subsequences[player-1]):
                        if i+1 in subsequences:
                            occurrences[i] +=1

                            # if payer have chosen all fields from subsequences apart from
                            #field "j", choose it is loose
                            if  (self.score_players_subsequences[player-1][subsequences_i] == (self.k - 1)):
                                occurrences[i] = math.inf
                # field not empty
                else:
                    occurrences[i] = math.inf
            #print("occurrences")
            #print(occurrences)

            if (min(occurrences) == math.inf):
                # player loose in any case, so we take firts available field
                prefer_field = self.available_fields()[0]

            else :
                # take field which appear at least times possible sequences
                prefer_field= occurrences.index(min(occurrences))

            #print ("prefer_field:", prefer_field)

            self.choose_number(player,prefer_field +1 )


        elif (strategy=="offensive"):
            occurrences = [0]*self.n
            for i, j in enumerate(self.properties):
                # fied empty
                if (j==0):
                    # count in how many possibles subsequences in second player contains field "j"
                    for subsequences_i, subsequences in enumerate(self.possible_players_subsequences[second_player-1]):
                        if i+1 in subsequences:
                            occurrences[i] +=1

                        #if payer have chosen all fields from subsequences apart from
                        #field "j", choose it is loose
                    for subsequences_i, subsequences in enumerate(self.possible_players_subsequences[player-1]):
                        if i+1 in subsequences:
                            if  (self.score_players_subsequences[player-1][subsequences_i] == (self.k - 1)):
                               occurrences[i] = math.inf
                # field not empty
                else:
                    occurrences[i] = math.inf
            #print("occurrences")
            #print(occurrences)

            if (min(occurrences) == math.inf):
                # player loose in any case, so we take firts available field
                prefer_field = self.available_fields()[0]

            else :
                # take field which appear at least times  in second player possible sequences
                prefer_field= occurrences.index(min(occurrences))

            #print ("prefer_field:", prefer_field)

            self.choose_number(player,prefer_field +1 )


        elif (strategy=="combined"): # merge offensive and defensive strategy
            occurrences = [0]*self.n
            for i, j in enumerate(self.properties):
                # fied empty
                if (j==0):
                    # count in how many possibles subsequences in second player contains field "j"
                    for subsequences_i, subsequences in enumerate(self.possible_players_subsequences[second_player-1]):
                        if i+1 in subsequences:
                            occurrences[i] +=1

                    # count how many possibles subsequences contains field "j"
                    for subsequences_i, subsequences in enumerate(self.possible_players_subsequences[player-1]):
                        if i+1 in subsequences:
                            occurrences[i] +=1

                        # if payer have chosen all fields from subsequences apart from
                        #field "j", choose it is loose
                            if  (self.score_players_subsequences[player-1][subsequences_i] == (self.k - 1)):
                                occurrences[i] = math.inf
                                print("inf loss i: ", i)
                                print("self.score_players_subsequences[player-1][subsequences_i] ",
                                      self.score_players_subsequences[player-1][subsequences_i])
                                print("subsequences_i ",subsequences_i)
                # field not empty
                else:
                    occurrences[i] = math.inf

                    print("inf, j!=0 : ", i)

            #print("occurrences")
            #print(occurrences)

            if (min(occurrences) == math.inf):
                # player loose in any case, so we take firts available field
                prefer_field = self.available_fields()[0]

            else :
                # take field which appear at least times possible sequences
                prefer_field= occurrences.index(min(occurrences))

            #print ("prefer_field:", prefer_field)

            self.choose_number(player,prefer_field +1 )



        elif (strategy=="random"):
            available = self.available_fields()
            n = len(available)
            prefer_field =available[random.randint(0, n-1)]
            self.choose_number(player,prefer_field +1 )

        else: print ("wrong strategy")

    def available_fields(self):
        print("properties")
        print(self.properties)
        field=[]
        for i, j in enumerate(self.properties):
            if (j==0):
                field.append(i)
        return field

    @staticmethod
    def other_player(player):
        second_player=2
        if player == 2:
            second_player=1
        return second_player

    strategy = ["defensive","offensive","combined","random"]