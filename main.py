from graph import *
from graph_searches import *
from tree_searches import *

g = Graph([
    ("A", "B", 5),
    ("A", "C", 2),
    ("A", "E", 3),
    ("B", "E", 3),
    ("B", "G", 5),
    ("C", "D", 2),
    ("D", "H", 4),
    ("D", "I", 4),
    ("E", "F", 2),
    ("H", "I", 4),
    ("H", "J", 4),
], directed=False)
print(g)
print("\n\n")

h1 = {
    "A": 10,
    "B": 6,
    "C": 8,
    "D": 5,
    "E": 5,
    "F": 3,
    "G": 1,
    "H": 3,
    "I": 4,
    "J": 0,
}

# Available options are DFS, BFS and LCF for both Tree and Graph
# GBFHeuristic and AStar for Graph only, heuristic param can be either function on Node or dict
s = AStarGraphSearcher(g, "A", "J", h1)
# Options:
#   cycle_checking - cycle checking + pruning, not guaranteed, esp on tree search, is in seminars however
#   early_exit - exit on finding route, not optimal for DFS
#   closed_prune - closed list pruning (graph only) - multi-path prune
s.search(cycle_checking=True, early_exit=True, closed_prune=True)

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
