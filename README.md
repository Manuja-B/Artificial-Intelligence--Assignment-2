# **Elements of Artificial Intelligence Assignment 2**

## **Part 1: IJK**

**{We have made an assumption that, &#39;+&#39; player will play using MiniMax, and &#39;-&#39; player will play randomly. Because, to find the best possible strength of the algorithm we have to make other player weak. If we would have given both the AI same power, there is a great chance that game might end up in a draw.}**

The question is to make a game - IJK which is a sliding tile game played on a 6x6 board by two players. So, it is basically a two-person 2048 with 6x6 grid.

In the given skeleton code, the AI played randomly. So, our AI was not intelligent at all.  Our goal for this assignment was to make the AI play the game optimally by writing code for two of its variants – Deterministic and Non-deterministic.

Deterministic is that the position for the next character is fixed, it finds the position linearly starting from [0][0] and subsequently moving on till it finds one. Whereas non-deterministic approach doesn&#39;t care about any particular place, it just places randomly on the empty positions on the board.

To implement this, we have used &#39;Minimax&#39; algorithm using &#39;Alpha-Beta Pruning&#39;. By using minimax algorithm we choose an optimal move for a player assuming that the other player is also playing optimally.

### **Initial State:**

Initial state is a board given with one move placed on the board according to the game variant{deterministic or non-deterministic}. This is specified by how the game is set up at the start and who plays the first move. The combination could be as follows:

1. AI vs AI
2. Human vs Human
3. Human vs AI
4. AI vs Human

### Terminal State:

When either one of the players wins i.e.the player who has maximum value (&#39;K&#39; for + Player, &#39;k&#39; for - Player) is the winner. If none of the player reaches the maximum state then whoever has the max. wins. Or, if some player has forfeited the match, the other player is the winner. Or else there is a tie, and nobody is a winner.

### Actions:

It will return the set of legal moves in a state space. For this problem actions could be Up(U), Left(L), Down(D) and Right(R).

### State Space: 
Is a collection of all possible states, that can be visited by taking the legal Actions.

### Successor function:
It provides all the next possible states, from the current position on the board.

### General flow of algorithm

**Step 1:** Generate game tree: As the number of possible states is very high, if we search till the end it will generate memory error. For this we define an arbitrary depth at which the algorithm will stop.

**Step 2:** Apply utility function to get utility values of states. We do this by defining heuristics. The details of heuristic functions are discussed in more detail below.

 We have used a weighted structure where have have experimented on various heuristic&#39;s combination. The combination was solely based on the experimental results.

**Step 3** : Calculate the utility values with the help of leaves considering one layer at a time until the root of the tree.

**Step 4** : Back-up the values from leaves to root

**Step 5** : Select move toward min node that has largest utility value

## Algorithm:

•        MINIMAX-Decision(S)

         Return action leading to state S&#39;SUCC(S) that maximizes MIN-Value(S&#39;)

•        MAX-Value(S)

        If Terminal?(S) return Result(S)

        Else return maxS&#39;SUCC(S) MIN-Value(S&#39;)

•        MIN-Value(S)

        If Terminal?(S) return Result(S)

        Else return minS&#39;SUCC(S) MAX-Value(S&#39;)

## Alpha-Beta Pruning: 

We use this to reduce time, by finding the optimal minimax solution while avoiding searching subtrees of moves which won't be selected. In an average case time complexity is reduced from O(b<sup>d</sup>) to O(b<sup>3d/4</sup>).

**Alpha:** It is the best choice so far for the player MAX. So, a MAX player can only alter with the alpha value. We want to get the highest possible value here. So, basically alpha is the lower bound on the values read by the node, it always picks the highest possible value.

**Beta:** It is the best choice so far for MIN, and it has to be the lowest possible value. And as the opposite, MIN Player can always alter the beta value. And beta is an upper bound on the values read by a MIN node, so it always picks the least values from the MAX nodes below it.

1. Initialize alpha to -infinity and beta to infinity.
2. Assign initial values of alpha and beta to roots
3. Prune the nodes for following conditions:

Beta &le; alpha of max ancestors

Alpha &ge; beta of min ancestors

## Heuristic function:
Heuristic function plays the most important thing in the search algorithms. They are the deciding factor for the direction of the move. We have used various different heuristic functions and are used with different weights. The details are-

1. **Empty tile heuristic-** This function provides the number of empty tiles on the board. So, the idea is if there are more empty positions on the board the chances of winning increase in the future, as more and more space to play will be available.
2. **Gradient Heuristic:** While playing the game, we analyzed that it would be better if the higher letters are acquired in the corner and the following letters should subsequently decrease. So, we created a gradient structure that is multiplied by our board, to get a score. Each board is tested for 4 gradients(priority to each different corner) and the max one is selected.
3. **Monotonic Heuristic:** This heuristic was created to maintain the similar alphabets(both uppercase and lowercase) together. So, the idea was that if we are getting similar characters adjacent, then they are more likely to combine together on the next step and move towards the goal state.
4. **Adjacent Heuristic:** This heuristic maintains the smoothness in the board. So, in any game we would more likely to have minimum difference between the adjacent tiles, so in the future moves it is more probable to combine them together.
5. **Max at Corner Heuristic:** So, this is just kind of an update to Gradient Heuristic, where we were more concerned about the orientation in a particular order. Here, we are giving priority, if the highest value comes onto any of the corners. So, the thought is that the new element is always either &#39;a&#39; or &#39;A&#39;, and we want them to stay away from the larger values, because then these will get stuck and won&#39;t be able to combine. So, we try to place the highest ones on the corner.
6. **Weighted Score** : This heuristic relies on the fact that, if in two consecutive moves the sum of all my weighted characters subtracted from the same of other player&#39;s characters increases, then there is an intuition that I am moving in the right direction.
7. **Max\_tile\_score** : This heuristic states that if in certain move I am able to increase my highest character, then I am moving in the right direction towards the goal.(though not that much impactful)

## Problems we faced:

- So, the biggest problem was to find the best combination of the heuristic measures, to generate a combined value. We tried several combinations, at some point we felt that a particular heuristic has less value, but other point you feel that, no it is actually very important. So, we comment that every heuristic is important, even if there is never an end to the heuristic functions. It&#39;s always a problem to find an improving combination.
- Whine implementing the gradient heuristic, we were assigning weights in linear fashion to the increasing values of the alphabet, but this seems to not work properly, as 2 &#39;s will be weighted the same as 1 b in that. So, we introduced an exponential weight base, so as to remove the conflict.
- We weren&#39;t able to find a more accurate algorithm to solve the non-deterministic approach. As both deterministic and non-deterministic, were able to play the same algorithm. We thought of implementing &quot;Expectiminimax&quot;, due to the factor of chance in the non-deterministic approach. But, due to the time constraints and the complexity of the algorithms we refrained from doing it.

## Few Suggestionsto create more fun in the game:

- What if the move is placed at the worst possible position. In this case the AI will have a hard time winning and it&#39;s utility is tested best.
- It can be a little fun if the user is allowed to place the tile, at desired position, this can be viewed as the opposite of the previous point.

# Assignment 2 - Games and Bayes


## Part 2

A)  Simple Approach

This problem was relatively easy. We are able to use the Bayes Net provided in the
assignment. The Bayes Net shows a direct relationship between the hidden variables, s,
and the observed variables, v. We are not considering any relationships between the
hidden variables. As such, we can solve this problem by simply finding the strongest
edge point on each column of pixels.

Writing the code for this solution is very straightforward - we transpose the "edge
strength" matrix and then find the maximum edge points. We position these points on
the input image using a blue mark.

The simplicity of this approach is also its downfall - by not factoring in the relationships
between hidden variables, we expose the possibility of finding a non-contiguous border. In fact,
this is what happened with our sample image. The border line found by our program "jumps
around" at one point. Of course, this should not happen. We can handle for this problem
by using the Viterbi Algorithm, as we will see in part B.

B) Viterbi Algorithm

This problem seeks to improve on what we built in part A. In part A, we arrived at a
set of points which could be the border of the mountain. These points are our "observed
variables". Unfortunately, we know that our solutions from part A are not always correct.
We can improve on part A by considering the relationship between hidden variables, using the Viterbi
Algorithm. In this implementation, we consider the transition probabilities to be the likelyhood that
a border's pixel location follows the previous columns pixel location. We consider the emission
probabilities to be the likelihood that a suggested pixel is actually a border edge. We calculate
this probability by using same edge weights used in part A.

The code for this problem is somewhat involved. We start by determining all of the
possible states. This is simply a list of all of the pixels available on the y axis.
Next, we get the set of transition probabilities. We have to use some logic here to
decide the appropriate probabilities. We determined that it is strongly likely for
a pixel to be within 1 y-coordinate of the preceding pixel. Next, we get the set
of emission probabilities. Again, this requires some custom logic. We determined that
emission probabilities should increase linearly with the strength of an edge point. To
do this in code, we created an evenly spaced array of 1000 points, where the sum of the
values in the array is equal to 1. Finally, we are able to use the Viterbi Algorithm.
We calculate v(0) using the emission probabilities and the initial probabilities. Next,
we calculate v(1) to v(max). At each step, we identify the route that maximizes our
probability, using both the emission and transition probabilities. When we are finished,
we backtrack from the final maximum value back to the initial value. Along the way, we
ensure that we maximize our probability.

We did have some issues with this implementation. 

Our first issue was that, given how large our decision tree was, our probabilities became incalculably 
small. At some point, these numbers simply rounded down to 0. As a result, our final probability
was 0. Of course, this is not what we want. We attempted to factor our emission and transition
probabilites up by 100. This solved the "0 probability problem", but led to other issues. 
We found that our transition probability would always dominate the emission probability. 
This appeared on the image as a line that began on the mountain's border, but then increased
linearly until it was at the very top of the image. Our next attempt to fix this problem was to use
logarithms. However, we were unable to get this to work properly. Ultimately, we were able to confirm
that our transition and emission probabilities were working, but we were unable to finetune them to 
get the desired result.

C) Human input

This problem is built on top of part B, and therefore suffers from some of the same problems that we faced 
in part B. However, were were able to successfully implement a feature that considers human input when 
determining where to draw a border line. 

To accomplish this, we tweaked the creation of our transition probability matrix. The adjustment that we made
gives preferential treatment to the point that the user said is on the borderline. In this way, the algorithm
properly draws a line over the indicated spot.

This implementation can be problematic in the sense that it produces strange outputs when the user chooses a point
that is completely off the mark. In these cases, the line can "jump" to that spot. The reason for this seems to be
that the strength of the transition probability overwhelms that of the emission probability. So, we will properly choose
to create a line along the border until, all of a sudden, we overwhelmingly need to go to one specific point.
