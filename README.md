# Japanese Volleyball League Schedule Analysis

As the title suggests, this is a analysis for the upcoming schedule of the Japanese V League, to figure out which matches I should go watch. I live in Tokyo, and the matches take place all over the country, and I want to figure which matches I should watch to receive the most enjoyment per yen spent. This analysis has two parts:
1. Evaluating how *exciting* or *enjoyable* a match will be.
2. How much *time* and *money* it takes for me to travel to the location.

If you're interested in volleyball, feel free to consider my results. I can't assure they're the most accurate (especially because I think my metric #1 for *satisfaction* is flawed), and this project is more of a proof-of-concept.

## Enjoyment Evaluation

As you might expect, the amount of enjoyment I'm going to receive from a match between teams that haven't played yet is pretty hard to accurately predict. I've decided to keep things simple and derive this from how **evenly-matched** I think two teams are going to be. 

The principle I used is as follows: if team A played team B and they're evenly matched, and if team B played team C and they're evenly matched, then in theory, when team A plays team C, they will also be evenly matched. In practice, however, this might not be the case. If the star players of one of the teams become injured, or if the playstyles of one of the teams make them advantageous over the other, the results could vary.

Nonetheless, for simplicity's sake, I've decided to go with this method. Instead of using three teams, I expanded to a graph of teams, where the paths between two nodes on the graph represent the same logical as before.

Let ![S(A, B)](https://latex.codecogs.com/svg.image?\inline&space;\bg{white}&space;S(A,B)) represent the score difference between two teams, A and B. 
