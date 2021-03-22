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
            check_win(k,piles)
            enemy_turn(piles)
            check_win(k,piles)
        else:
            enemy_turn(piles)
            check_win(k,piles)
            display_pile(piles)
            piles = toRemove = player_turn()
            piles = remove_object(piles,toRemove[0],toRemove[1])
            check_win(k,piles)

def display_pile(piles):
    print("Displaying the Pile")
    for i in range(len(piles)):
        print(str(piles[i]) + ", ", end = '' )
    print("")


def remove_object(piles,pileNumber,numItems):
    piles[pileNumber-1] = piles[pileNumber-1]-1
    return piles


def choose_start():
    number = random.randint(0,1)
    if number == 1:
        returnBool = True
    else:
        returnBool = False
    return returnBool

def enemy_turn(piles):
    #ai stuff goes here
    print("ai stuff")
    #enemy_turn should return the same thing as player_turn

def player_turn():
    print("player does something")
    pileNumber = int(input("Enter a pile to remove items from "))
    numItems = int(input("Enter number of items to remove "))
    returnList = [pileNumber,numItems]
    return returnList


def check_win(k,objectPiles):
    #TODO put each section in separate method :)
    
    allEmpty = True
    #the first section is for the condition "all piles are empty"
    for i in range(len(objectPiles)):
        if objectPiles[i] != 0:
            allEmpty = False
    if(allEmpty):
        print("someone won from this condition")
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
        print("someone won from this condition")
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
        print("someoen won from this condition ")
    #the fourth section os for the condition "2 piles each with 1 object, 2 piles each with 2 objects, the others are empty"
    kPilesValue = []
    kPilesCounter = []
    for i in range(int(k)):
        kPilesValue.append(int(i)+1)
        kPilesCounter.append(0)
    objectPileCounter = 0
    objectPileBool = False
    rememberedIndex = 0
    print(kPilesValue)
    zeroObjectPileCounter = 0
    zeroObjectPileLimit = len(objectPiles) - (k*k)
    print("certainly attempted this doubtless")
    for i in range(len(objectPiles)):
        for j in range(len(kPilesValue)):
            if objectPiles[i] == kPilesValue[j]:
                print("its true)")
                kPilesCounter[j] = kPilesCounter[j]+1
                objectPileCounter += 1
                objectPileBool = True
                rememberedIndex = j
        if objectPiles[i] == 0:
            zeroObjectPileCounter += 1
        # if(objectPileBool):
        #     kPilesValue.remove(rememberedIndex)
    currentBool = True
    for i in range(len(kPilesValue)):
        if(kPilesCounter[i]==k):
            print("did nothing")
        else:
            currentBool = False
    print("current bool is "+str(currentBool))
    print("zero ojbect pile counter is "+str(zeroObjectPileCounter))
    print("zero object pile limit is "+str(zeroObjectPileLimit))
    if(zeroObjectPileLimit == zeroObjectPileCounter and currentBool):
        print("the final condition was also met")


    # if objectPileCounter == k and zeroObjectPileCounter == zeroObjectPileLimit:
    #     print("this condition was met")



    # if oneObjectPileCounter ==2 and twoObjectPileCounter==2 and zeroObjectPileCounter==zeroObjectPileLimit:
    #     print("someoen won from the final condition ")









main()
