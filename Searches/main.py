from graph import *
from graph_searches import *
from tree_searches import *

g = Graph([
    # ("A", "B", 5),
    # ("A", "C", 2),
    # ("A", "E", 3),
    # ("B", "E", 3),
    # ("B", "G", 5),
    # ("C", "D", 2),
    # ("D", "H", 4),
    # ("D", "I", 4),
    # ("E", "F", 2),
    # ("H", "I", 4),
    # ("H", "J", 4),
    (*"AB", 11),
    (*"AC", 7),
    (*"AD", 13),
    (*"BE", 7),
    (*"CD", 9),
    (*"CE", 14),
    (*"DF", 10),
    (*"DG", 5),
    (*"EH", 10),
    (*"FH", 10),
    (*"HI", 6),
], directed=False)
print(g)
print("\n\n")

h1 = {
    # "A": 10,
    # "B": 6,
    # "C": 8,
    # "D": 5,
    # "E": 5,
    # "F": 3,
    # "G": 1,
    # "H": 3,
    # "I": 4,
    # "J": 0,
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

h2 = {
    "A": 24,
    "B": 28,
    "C": 24,
    "D": 38,
    "E": 17,
    "F": 16,
    "G": 85,
    "H": 7,
    "I": 0,
}

# Available options are DFS, BFS and LCF for both Tree and Graph
# GBFHeuristic and AStar for Graph only, heuristic param can be either function on Node or dict
s = AStarGraphSearcher(g, "A", "I", h1)
# Options:
#   cycle_checking - cycle checking + pruning, not guaranteed, esp on tree search, is in seminars however
#   early_exit - exit on finding route, not optimal for DFS
#   closed_prune - closed list pruning (graph only) - multi-path prune
s.search()

# A admissible heuristic function is also provided, which calculates the distance from all nodes to the goal, and compares that to the given heuristic
g.admissible_heuristic("I", h2)

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
