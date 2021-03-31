# Bot Complexity Analysis Document

## Content:
 * [standard1v1Bot Analysis](#standard1v1bot-analysis)
 * [bot_v2 Analysis](#bot_v2-analysis)

<br>

## <b>Standard1v1Bot Analysis:</b>
n represents the number of piles
m represents number of objects the pile with most objects has. <br>


<Strong>Methods:</strong>
<br>
1. getMisereChoice: O(n)
2. getStandardChoice: O(n) + O(n) => O(n)
3. choosePile: O(n) + O(n) => O(n)

Total Complexity is the sum of above three complexity.

<b>Total Complexity: </b> O(n) + O(n) + O(n) = <b>O(n) </b>
<br>

## <b>Bot_v2 Analysis:</b>
n represents the number of piles
m represents number of objects the pile with most objects has. <br>

<Strong>Methods:</strong>
1. checkMove: O(n) 
2. getNextMove: O(m)
3. choosePile: O(n) + O(n) => O(n)

Total Complexity is the sum of above three complexity.

<b>Total Complexity: </b> O(n) + O(m) + O(n) = <b>O(m + n) </b>
