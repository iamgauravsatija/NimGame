# NimGame
Project for CPSC-482

## PseudoCode:
	1. Bot reads the input to analyze the current situation
	2. Then chooses a pile 
	(not sure what should be the criteria to choose one {first pile, second pile…} {pile with most obj} etc.)
	
	For a standard game with only the first win condition:
		X = 0
		for each pile in list:
			X = X xor pile
			
		for each pile in list:
			if pile < X xor pile:
				Choose this pile
				break
		
		If it didn't find a pile, then it's losing.
	
	
	3. After the pile n is chosen, take one object from it;   object count = 1 
	4. Call check_function()        {returns TRUE or FALSE}
		○ 4th condition
		○ 3 piles each with 2 objects, and all other piles are empty.
		○ 1 pile with 1 object, 1 pile with 2 objects, 1 pile with 3 objects, all other piles are empty.
		○ all piles are empty. We need this check because there may be condition n=3 
		
	5. If check() == TRUE:
		○ Increase the object count by 1 
		○ Call check function (step 4)
		○ Recursion this check function == false at object count = i
		○ Return count = i-1
	6. If check() == False:
		○ Choose next pile based on criteria
		○ Repeat from step 3
		
	7. Check if new situation == old situation:
		○ True: You lost
		○ False: send to next bot.
   
   Link to image of [pseudocode](https://user-images.githubusercontent.com/32801600/112295613-4dc61980-8c51-11eb-8720-5645388e8539.png)
