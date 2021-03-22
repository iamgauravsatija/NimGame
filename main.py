import random

def main():
    k = int(input("Define K "))
    piles = []
    piles.append(1)
    piles.append(2)
    piles.append(3)
    piles.append(1)
    piles.append(2)
    piles.append(3)
    # piles.append(1)
    # piles.append(2)
    # piles.append(3)
    piles.append(0)
    piles.append(0)
    #temporary check win for debugging
    #check_win(k,piles)
    #using 3 piles with an arbitrary number of objects for now
    turnOrder = choose_start()
    while True:
        if turnOrder:
            display_pile(piles)
            toRemove = player_turn()
            piles = remove_object(piles,toRemove[0],toRemove[1])
            check_win("P1",k,piles)
            enemy_turn(piles)
            check_win("P2",k,piles)
        else:
            enemy_turn(piles)
            check_win("P2",k,piles)
            display_pile(piles)
            toRemove = player_turn()
            piles = remove_object(piles,toRemove[0],toRemove[1])
            check_win("P1",k,piles)

def display_pile(piles):
    print("Displaying the Pile")
    for i in range(len(piles)):
        print(str(piles[i]) + ", ", end = '' )
    print("")


def remove_object(piles,pileNumber,numItems):
    piles[pileNumber-1] = piles[pileNumber-1]-numItems
    return piles

def choose_start():
    number = random.randint(0,1)
    if number == 1:
        returnBool = True
    else:
        returnBool = False
    return returnBool

def enemy_turn(piles):
    x = 1
    #ai stuff goes here
    #enemy_turn should return the same thing as player_turn

def player_turn():
    pileNumber = int(input("Enter a pile to remove items from "))
    numItems = int(input("Enter number of items to remove "))
    returnList = [pileNumber,numItems]
    return returnList


def check_win(playerName,k,objectPiles):
    #TODO put each section in separate method :)

    allEmpty = True
    #the first section is for the condition "all piles are empty"
    for i in range(len(objectPiles)):
        if objectPiles[i] != 0:
            allEmpty = False
    if(allEmpty):
        print(playerName + " lost the game")
    #the second section is for the condition "3 piles each with 2 objects and all other piles are empty"
    emptyPilesCounter = 0
    emptyPilesLimit = len(objectPiles)-3
    pilesTwoObjCounter = 0
    pilesTwoObjLimit = 3
    for i in range(len(objectPiles)):
        if objectPiles[i] == 0:
            emptyPilesCounter+=1
        if objectPiles[i] == 2:
            pilesTwoObjCounter+=1
    if(emptyPilesCounter == emptyPilesLimit and pilesTwoObjLimit == pilesTwoObjCounter):
        print(playerName + " lost the game")
    #the third section is for the condition "1 pile with 1 object, 1 pile with 2 objects, 1 pile with 3 objects, all other piles are empty"
    oneObjectPileCounter = 0
    twoObjectPileCounter = 0
    threeObjectPileCounter = 0
    zeroObjectPileCounter = 0
    zeroObjectPileLimit = len(objectPiles)-3
    for i in range(len(objectPiles)):
        if objectPiles[i] == 1:
            oneObjectPileCounter += 1
        if objectPiles[i] == 2:
            twoObjectPileCounter += 1
        if objectPiles[i] == 3:
            threeObjectPileCounter +=1
        if objectPiles[i] == 0:
            zeroObjectPileCounter+=1

    if oneObjectPileCounter ==1 and twoObjectPileCounter==1 and threeObjectPileCounter==1 and zeroObjectPileCounter==zeroObjectPileLimit:
        print(playerName + " lost the game")
    #the fourth section os for the condition "2 piles each with 1 object, 2 piles each with 2 objects, the others are empty, this is the general case and has been tested for k=2 and k=3"
    kPilesValue = []
    kPilesCounter = []
    for i in range(int(k)):
        kPilesValue.append(int(i)+1)
        kPilesCounter.append(0)
    objectPileCounter = 0
    zeroObjectPileCounter = 0
    zeroObjectPileLimit = len(objectPiles) - (k*k)
    for i in range(len(objectPiles)):
        for j in range(len(kPilesValue)):
            if objectPiles[i] == kPilesValue[j]:
                kPilesCounter[j] = kPilesCounter[j]+1
                objectPileCounter += 1
        if objectPiles[i] == 0:
            zeroObjectPileCounter += 1
    currentBool = True
    for i in range(len(kPilesValue)):
        if(kPilesCounter[i]!=k):
            currentBool = False

    if(zeroObjectPileLimit == zeroObjectPileCounter and currentBool):
        print(playerName + " lost the game")


main()
