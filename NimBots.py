import random

from PlayerController import playerController

# Simple bot that randomly picks a pile and amount
#to take from said pile.
class randomBot(playerController):

    @staticmethod
    def getDescription():
        return "a random selection bot"

    def playTurn(self, nim_instance):
        pile_list = nim_instance.peek_list()
        index = random.randrange(0, len(pile_list))
        amount = random.randint(1, pile_list[index])

        self.callback(self.name, nim_instance, (index, amount))

# Bot designed to always win a 1v1 in a game with only the
# first win condition whenever possible.    
class standard1v1Bot(playerController):

    @staticmethod
    def getDescription():
        return "a standard 1v1 bot"

    def playTurn(self, nim_instance):
        if(nim_instance.isMisere()):
            choice = self.getMisereChoice(nim_instance.peek_list())
        else:
            choice = self.getStandardChoice(nim_instance.peek_list())

        self.callback(self.name, nim_instance, choice)

    # If playing a standard game, bot will use this method to find its next move.
    def getStandardChoice(self, pile_list):
        nim_sum = 0

        for pile in pile_list:
            nim_sum = nim_sum ^ pile

        largest_pile = 0
        saved_index = 0

        for i, pile in enumerate(pile_list):
            if nim_sum ^ pile < pile:
                return (i, pile-(nim_sum^pile))
            else:
                if pile > largest_pile:
                    largest_pile = pile
                    saved_index = i
        
        return (saved_index, 1)

    # If playing a misere game, bot will use this method to find its next choice.
    def getMisereChoice(self, pile_list):
        large_piles = 0
        small_piles = 0

        for i, pile in enumerate(pile_list):
            if pile > 1:
                large_piles += 1
                saved_index = i
            else:
                small_piles += 1

        if large_piles == 1:
            if small_piles%2 == 1:
                return (saved_index, pile_list[saved_index])
            else:
                return (saved_index, pile_list[saved_index]-1)

        else:
            return self.getStandardChoice(pile_list)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Pseudocode or steps:                                                                        
#     - Bot reads the situation
#     - Choose a pile: index_pile
#     - while loop:
#         - take 1 object from index_pile
#         - call check function
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
class gauravTestBot(playerController):
    
    @staticmethod
    def getDescription():
        return "Gaurav's Testing Bot"

    def choosePile(self, pile_list):
        nim_sum = 0

        for pile in pile_list:             # complexitiy - n
            nim_sum = nim_sum ^ pile

        for pile in pile_list:              # complexitiy - n
            if pile < nim_sum ^ pile:
                return pile

        return max(pile_list) # I don't know if this is optimal, but it seems intuitive.
                              # Either way, you're losing at this point.

    def checkMove(self, pile_index, pile_objects_left, local_list, condition_list):
        
        total_piles = len(local_list)
        new_list = local_list.copy()

        new_list[pile_index] = pile_objects_left

        # condition 1
        # 1 pile with 1 object, 1 pile with 2 objects, 1 pile with 3 objects, all other piles are empty.
        if ( local_list.count(1) == 1 and local_list.count(2) == 1 and local_list.count(3) == 1 ):
            if (total_piles - 3 == local_list.count(0) ):
                print("Loose condition")
                return False
        
        # condition 2
        # 3 piles each with 2 objects, and all other piles are empty.
        if ( local_list.count(3) == 2 ):
            if (total_piles - 2 == local_list.count(0) ):
                print("Loose condition")
                return False
        
        
        # condition 3
        # All piles empty
        if ( local_list.count(0) == total_piles ):
            print("Loose condition")
            return False

        
        # condition 4
        flag = True
        cond_set = set(condition_list)  
        
        for elements in cond_set:               # complexitiy - n, if all the values are different then size of set = size of list
            if new_list.count(elements) != condition_list.count(elements):
                flag = False
                break

        if flag == True:
            print("Loose conditon")
            return False
        
        return True

    def getNextMove(self, given_list, condition_list):
        # create a local copy of list
        local_list = given_list.copy()

        # choose pile with maximum object
        target_pile_count = self.choosePile(local_list)
        target_pile_index = local_list.index(target_pile_count)

        item_taken = 0
        is_valid = True

        while item_taken >= target_pile_count and  is_valid == True:       
            item_taken += 1
            is_valid = self.checkMove(target_pile_index, target_pile_count - item_taken, local_list, condition_list)
        
        item_taken = item_taken - 1

        if item_taken < 1:
            item_taken = 1

        # if item_taken > max_pile_count or item_taken == 0:
        #     print("Choose new PILE!!!")
        #     # choose new pile and call get next move

        new_list = local_list.copy()
        new_list[target_pile_index] = target_pile_count - item_taken    

        return  target_pile_index, item_taken

    def playTurn(self, nim_instance):
        self.callback(self.name, nim_instance, self.getNextMove(nim_instance.peek_list(), nim_instance.wincon_list)

                      
class bruteForceBot(playerController):

    @staticmethod
    def getDescription():
        return "a bot using brute force"

    def playTurn(self, nim_instance):
        self.callback(self.name, nim_instance, self.calculateMove(nim_instance))

    # Checks all possible moves to determine whether the bot is 
    # in a winning positions. If it is, it transitions
    # to a new winning position. Otherwise, makes
    # the first move it finds.
    def calculateMove(self, nim_instance):
        pile_list = nim_instance.peek_list()

        for element in set(pile_list):
            i = pile_list.index(element)
            for k in range(element, 0, -1):
                if self.isWinning(nim_instance.peekAfterTurn(i, k), False):
                    return (i, k)

        for element in set(pile_list):
            i = pile_list.index(element)
            for k in range(element, 0, -1):
                if not nim_instance.peekAfterTurn(i, k).checkForWin():
                    return (i, k)

        return (0, 1)

    # Uses recursion to determine if it is winning or not.
    # if a chain of its own moves always wins against any set of moves
    # the opponent can make, it is winning. Otherwise, it's losing.
    def isWinning(self, nim_instance, my_turn):
        if nim_instance.checkForWin():
            return my_turn

        for element in set(nim_instance.pile_list):
            i = nim_instance.pile_list.index(element)
            for k in range(element, 0, -1):
                if self.isWinning(nim_instance.peekAfterTurn(i, k), not my_turn) == my_turn:
                    return my_turn

        return not my_turn

class shortPredictionBot(playerController):

    @staticmethod
    def getDescription():
        return "a bot that tries to predict the opponent"

    def playTurn(self, nim_instance):
        self.callback(self.name, nim_instance, self.makeChoice(nim_instance))

    # Returns the nim sum of any number of piles
    def getNimSum(self, *args):
        nim_sum = 0

        for pile in args:
            nim_sum = nim_sum ^ pile

        return nim_sum

    # Returns a list of moves that result in a nim_sum of zero
    def getZeroSumMoves(self, game_state):
        result = list()

        nim_sum = self.getNimSum(*game_state)

        for index, pile in enumerate(game_state):
            if nim_sum^pile < pile:
                temp = (index, pile-(nim_sum^pile))
                if temp not in result:
                    result.append((index, pile-(nim_sum^pile)))

        return result

    # If this turn results in a losing state, this is
    # considered a trap. Optimal play from a winning position
    # will always be considered a trap.
    def isTrap(self, nim_instance):
        if nim_instance.checkForWin():
            return False

        large_piles = 0
        small_piles = 0

        for i, pile in enumerate(nim_instance.pile_list):
            if pile > 1:
                large_piles += 1
                saved_index = i
                if large_piles > 1:
                    break
            else:
                small_piles += 1

        if large_piles == 1:
            if small_piles%2 == 1:
                choice = (saved_index, nim_instance.pile_list[saved_index])
            else:
                choice = (saved_index, nim_instance.pile_list[saved_index]-1)

            if nim_instance.peekAfterTurn(*choice).checkForWin():
                return True
            else:
                return False
        
        for move in self.getZeroSumMoves(nim_instance.pile_list):
            if not nim_instance.peekAfterTurn(*move).checkForWin():
                return False

        return True

        
    # Tries to determine optimal play and looks out for traps
    # set by the enemy by looking one turn ahead.
    def makeChoice(self, nim_instance):

        large_piles = 0
        small_piles = 0

        # Check for the number of piles with more than one object
        # Remember the number of piles with only one object
        # in case we are in a late-game state.
        for i, pile in enumerate(nim_instance.pile_list):
            if pile > 1:
                large_piles += 1
                saved_index = i
                if large_piles > 1:
                    break
            else:
                small_piles += 1

        # If there's only one pile with more than one object,
        # the game is in late game, and the strategy changes.
        if large_piles == 1:
            if small_piles%2 == 1:
                choice = (saved_index, nim_instance.pile_list[saved_index])
            else:
                choice = (saved_index, nim_instance.pile_list[saved_index]-1)

            if not nim_instance.peekAfterTurn(*choice).checkForWin():
                return choice

        else:

            # Look for zero sum moves to make, but watch out for potential enemy traps
            for move in self.getZeroSumMoves(nim_instance.pile_list):
                prediction = nim_instance.peekAfterTurn(*move)
                
                if prediction.checkForWin():
                    continue
                
                is_viable = True

                # Test all potential enemy moves on the next turn to see if
                # they are a trap
                for element in set(prediction.pile_list):
                    index = prediction.pile_list.index(element)
                    for k in range(element, 0 , -1):
                        next_move = (index, k)
                        enemy_state = prediction.peekAfterTurn(*next_move)

                        if self.isTrap(enemy_state):
                            is_viable = False
                            break

                # No traps were found, we can safely make a zero-sum move. 
                if is_viable:
                    return move

            viable_moves = list()

            # No moves that allow a zero sum exist, look to set a trap yourself.
            for element in set(nim_instance.pile_list):
                index = nim_instance.pile_list.index(element)
                for k in range(element, 0, -1):
                    next_move = (index, k)

                    prediction = nim_instance.peekAfterTurn(*next_move)

                    if prediction.checkForWin():
                        continue
                    
                    if next_move not in viable_moves:
                        viable_moves.append(next_move)

                    if self.isTrap(prediction):
                        return next_move             
            
            # No good moves to play; Play the viable move with the smallest difference
            # In order to increase chances of winning.
            if viable_moves:
                greatest_difference = 0
                saved_move = viable_moves[1]
                
                for move in viable_moves:

                    current_difference = nim_instance.pile_list[move[0]]-move[1]

                    if current_difference > greatest_difference:
                        saved_move = move
                        greatest_difference = current_difference

                return saved_move


            # You lost; pick up the last object.
            return (0, 1)

