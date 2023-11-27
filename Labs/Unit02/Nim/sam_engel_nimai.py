"""
File to be modified by the students
The student should rename the file to 
be yourname_nimai.py.
"""
from functools import reduce

def ai_take_turn(piles):
    # TODO: Complete function
    a = 0
    b = 0
    for pile_num in range(len(piles)):
        for n in range(1,piles[pile_num]+1):
            a = pile_num
            b = n
            new_piles = [p for p in piles]
            new_piles[pile_num] = piles[pile_num]-n
            if reduce(lambda x,y:x^y, new_piles) == 0:
                #print("Winning: return ", (a,b))
                return (a,b)
    max_index = 0
    for pile_num in range(len(piles)):
        if piles[pile_num] >= piles[max_index]:
            max_index = pile_num
    a = max_index
    b = 1
    #print("Losing: return ", (a,b))
    return (a,b)