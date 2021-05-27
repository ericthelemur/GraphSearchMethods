from graph import *
from graph_searches import *
from tree_searches import *

g = Graph([
    (*"AB", 10),
    (*"AC", 8),
    (*"AD", 12),
    (*"BE", 8),
    (*"CD", 10),
    (*"CE", 16),
    (*"DF", 12),
    (*"DG", 14),
    (*"EH", 11),
    (*"FH", 11),
    (*"HI", 2),
], directed=False)
print(g)
print("\n\n")

h1 = {
    "A": 34,
    "B": 23,
    "C": 30,
    "D": 39,
    "E": 15,
    "F": 16,
    "G": 44,
    "H": 6,
    "I": 0,
}


# Available options are DFS, BFS and LCF for both Tree and Graph
# GBFHeuristic and AStar for Graph only, heuristic param can be either function on Node or dict
s = LCFGraphSearcher(g, "A", "I")
# Options:
#   cycle_checking - cycle checking + pruning, not guaranteed, esp on tree search, is in seminars however
#   early_exit - exit on finding route, not optimal for DFS
#   closed_prune - closed list pruning (graph only) - multi-path prune
s.search()

# A admissible heuristic function is also provided, which calculates the distance from all nodes to the goal, and compares that to the given heuristic
# g.admissible_heuristic("I", h2)

# S1Q1
# s = LCFTreeSearcher(g, "A", "J")
# s.search()
# S1Q2
# s = LCFGraphSearcher(g, "A", "J")
# s.search()
# S2Q1a
# s = GBFHeuristicGraphSearcher(g, "A", "J", h1)
# s.search()
# S2Q1b
# s = AStarGraphSearcher(g, "A", "J", h1)
# s.search()
