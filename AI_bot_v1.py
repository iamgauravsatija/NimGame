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
    def getDescription(self):
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

    def check_move(self, pile_index, pile_objects_left, local_list, condition_list):
        
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
        target_pile_count = choosePile(local_list)
        target_pile_index = local_list.index(target_pile_count)

        item_taken = 0
        is_valid = True

        while item_taken >= target_pile_count and  is_valid == True:       
            item_taken += 1
            is_valid = check_move(target_pile_index, target_pile_count - item_taken, local_list, condition_list)
        
        item_taken = item_taken - 1

        # if item_taken > max_pile_count or item_taken == 0:
        #     print("Choose new PILE!!!")
        #     # choose new pile and call get next move

        new_list = local_list.copy()
        new_list[target_pile_index] = target_pile_count - item_taken    

        return  target_pile_index, item_taken