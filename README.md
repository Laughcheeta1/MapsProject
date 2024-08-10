<img alt="Simple visualization of A*" width="400" src="./AStar_Algorithm.gif">

# Best Route Searching

This is a small project designed to search the best route to take on a city, for getting from one point to another.
(Something like Google Maps).

## The algorithm
The algorithm used is the `A* algorithm`. This is a search algorithm designed to try and search for the best path of solving a search problem,
in this case the problem would be driving from one point to another in the most efficient way possible.

### Uses of this algorithm
This algorithm can be used for example for route planning, this is what companies like Amazon and Mercado Libre uses for 
planning they're last mile deliveries, this because this algorithm can help us find a route not only most efficient in a
distance or time planning way, but also helps in for example finding optimal routes that minimises the amount of left
turns (In places like England it would be right turns), because accidents are more prone to happen while turning left,
also things like finding routes that for example, passes through the most amount of charging stations, etc.

This algorithm is not only relegated for maps tho, this algorithm is meant to be used in al kinds of problems that can be
thought as graphs, or more generally problems were we seek to get to a state via actions.

## The implementation
We implemented a simple version of its heuristics and cost function, this because not only due to technical limitations 
(our computers), but also because of the cost implicated of using external sources to gather the relevant information.

### The cost function
We measured cost as a combination of the following:
<li>Time it will take to get from one point to another</li>
<li>Amount of turns (like turning to another street) we have to make</li>
<br>

#### Time:
This time is calculated via a simple division of `distance / real_time_average_speed`, therefore getting the average 
time it takes to get to a node.
We choose this because in the average speed all sort of things are intrinsically encoded, for example, if in the route
there was an accident, is safe to say that the average speed in that route will reflect that reality. In that way we can
avoid having to take a lot of data into account, that even tho may not be that accurate, it is accurate enough for the
scope of the project.

<br>

#### Amount of turns:
The more turns you have to make from a road to another, the worse, because changing roads is more time-consuming and
dangerous than just staying on the same road.

<br>

### The Heuristic
We went for a simple heuristic, because the heuristic is meant to be an educated guess of a future state, without
actually visiting it, and with the limitations we had, we did not find a way of calculating a metric like that without 
actually visiting the node.  
So for example, for getting the average speed of a route to another node, we have to give the API the coordinates of the
current node and the next node, that means visiting the node, so now that we are here, we might as well get the distance,
etc.

`Note`: now thinking about it, a mitigation of this could have been checking the speed (that is on the graph) of the edges
connecting two nodes, but oh well, lil too late.

All this explanation is to say that our heuristic is just the great_circle distance between a node, to the objective's
coordinates.

## Additions we made
We made the possibility of making a gif file showing the nodes that are being visited on a graph.


# How to run it
We sadly only had time to make the actual implementation in code, and not a pretty UI that is more user-friendly.
What can be done therefore is explicitly code it.