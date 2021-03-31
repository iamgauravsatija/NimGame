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
    
class bot_v2 (playerController):
    
    @staticmethod
    def getDescription():
        return "bot_v2"

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
        self.callback(self.name, nim_instance, self.getNextMove(nim_instance.peek_list(), nim_instance.wincon_list))
