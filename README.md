We're going to work with patterns where a pattern is cross shape showing how the empty and blocked squares might be laid out relative to one number. The end of each arm has a blocked square and the rest of the arms are empty.
First we will generate all the possible patterns for each number, then we will successively eliminate possible patterns via constraint propagation until we are left with only the actual patterns.
Isn't this inefficient? I hear you ask. Just how many patterns are there for each number? you ask.
If you take the 4 arms of the patterns cross, chop of the blocked squares and lay the empty squares end to end you get a strip of N-1 length (where N is the patterns number) with 3 cut points. So the question of how many patterns can be reduced to how many cut points which can trivially be shown to be N^3/6, the largest number is 15 which has 562 patterns, no biggie.

0: Load and print state.
We'll have the usual clear text input and output format.
.. for unknown
01 for a small number
12 for a bigger number
OO for definitely empty
XX for definitely blocked

1: Generate patterns.
We could chop the arms to the size of the grid as we generate them, but that's a hassle, so instead we will make the arms complete and then inject blocked squares around the perimeter eliminating any arms that cross the edge.
With that in mind generating the patterns is trivial. We will store them as little objects that have the number they belong to, which squares they require to be blocked, which squares empty and an eliminated flag.
For each square we will also keep lists of the patterns that require that square to be blocked and the patterns that require it to be empty.

2: Inject known data.
As mentioned above we need the whole border to be outlined with blocked. We also need the numbers to be marked empty.
Whenever we inject data we eliminate all the patterns that conflict with the new data and queue their numbers to be updated.

3: Eliminate patterns via propagation.
For each queued number we will look through all the squares in all the numbers uneliminated patterns. Any square that is in all the patterns and has the same value in them all can be treated as known data and injected as above.
While doing this we'll apply an additional rule that if we inject a blocked square we will also inject empty ones around it, this needs to be clipped to the grid of course.
Proceed until the queue is empty.

4: Search
The above covers all the game rules except the reach-ability one.
That's not easy to constraint propagate, so instead we will use a recursive search.
Each time we exhaust the queue we copy the state, pick a random unknown cell and mark it either blocked or empty and recurse.
If we run out of unknown squares then we have a possible solution and we apply a spanning tree test to see if it meets the final rule.
If it passes we win if not we keep searching.
Additionally if during constraint propagation we end up with a number whose patterns have all been eliminated then we made a bad move and need to keep searching.
To help this along we will keep blocked, empty and unknown lists in the state.
