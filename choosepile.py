def choosePile(pile_list):
    nim_sum = 0

    for pile in pile_list:
        nim_sum = nim_sum ^ pile

    for pile in pile_list:
        if pile < nim_sum ^ pile:
            return pile

    return max(pile_list) # I don't know it this is optimal, 
                          # but it seems intuitive.
                          # Either way, you're losing at this point.