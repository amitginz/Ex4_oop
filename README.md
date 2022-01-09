#  our ex4_oop


![duFNXTrRmmyhqHPC88gS2V](https://user-images.githubusercontent.com/93703549/148675134-ea5492d1-4c25-44ea-9e1c-bdb17cbc93af.jpg)



# Overview - Task information:
In this assignment, we were expected to design a “Pokemon game” .
Given a weighted and directed graph - we need to place agents who will catch as many Pokemon as possible efficiently and quickly.
The goal: to maximize the amount of weights of the Pokemon collected, without exceeding the amount of calls per server allowed per second. To implement this, we used algorithms from the previous task(dealing with graphs).

# the class
1) agent
2) pokemon
3) DiGraph
4) client
5) my_code
6) GraphAlgo
7) test for game

# the UML:


**first algorithm:**
*there is pokimons on edges in directed wieghted graph.\
*there is agent in some point on the graph.\
*the agent will pick the closet pokimon to him and the most value pokemon by dijkstra algorithm and we do the same with the next pokimon(greedy algorithm).\
*we will call move after eact planning of the travel and when he near picking the pokimon by the agent.
