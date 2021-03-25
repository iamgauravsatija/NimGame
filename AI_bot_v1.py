# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Pseudocode or steps:                                                                        
#     - Bot reads the situation
#     - Choose a pile: index_pile
#     - while loop:
#         - take 1 object from index_pile
#         - call check function
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    

def getNextMove(given_list):
    # create a local copy of list
    local_list = given_list.copy()

    # choose pile with maximum object
    max_pile_count = max(local_list)
    max_pile_index = local_list.index(max_pile_count)

    item_taken = 0

    while item_taken >= max_pile_count:
        item_taken += 1
        is_valid = check_move(max_pile_index, max_pile_count - item_taken, local_list)


def check_move(pile_index, pile_objects_left, local_list):
    
    total_piles = len(local_list)

    # condition 1
    # 1 pile with 1 object, 1 pile with 2 objects, 1 pile with 3 objects, all other piles are empty.
    if ( local_list.count(1) == 1 and local_list.count(2) == 1 and local_list.count(3) == 1 ):
        if (total_piles - 3 == local_list.count(0) ):
            print("Loose condition")
    
    # condition 2
    # 3 piles each with 2 objects, and all other piles are empty.
    if ( local_list.count(3) == 2 ):
        if (total_piles - 2 == local_list.count(0) ):
            print("Loose condition")
    
    
    # condition 3
    # All piles empty
    if ( local_list.count(0) == total_piles ):
        print("Loose condition")

    
    # condition 4
    # for this I need an array or a data structure which will tell n_i and m_j value:

        