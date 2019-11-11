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