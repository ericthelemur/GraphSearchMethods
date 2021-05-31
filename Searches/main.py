from graph import *
from graph_searches import *
from tree_searches import *

# g = Graph([
#     (*"AB", 10),
#     (*"AC", 8),
#     (*"AD", 12),
#     (*"BE", 8),
#     (*"CD", 10),
#     (*"CE", 16),
#     (*"DF", 12),
#     (*"DG", 14),
#     (*"EH", 11),
#     (*"FH", 11),
#     (*"HI", 2),
# ], directed=False)
#
# h1 = {
#     "A": 34,
#     "B": 23,
#     "C": 30,
#     "D": 39,
#     "E": 15,
#     "F": 16,
#     "G": 44,
#     "H": 6,
#     "I": 0,
# }

# 2020 4a
# g = Graph([
#     (*"AB", 1),
#     (*"BC", 2),
#     (*"CD", 2),
#     (*"DB", 2),
#     (*"DE", 4),
#     (*"DF", 3),
#     (*"DG", 2),
#     (*"EF", 2),
#     (*"EH", 6),
#     (*"FD", 3),
#     (*"FH", 3),
#     (*"GH", 9)
# ], directed=True)

# h1 = {
#     "A": 10,
#     "B": 9,
#     "C": 8,
#     "D": 6,
#     "E": 6,
#     "F": 2,
#     "G": 1,
#     "H": 0,
#     # "I": 0,
# }

# 2019 2a
g = Graph([
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

h1 = {
    "A": 34,
    "B": 28,
    "C": 34,
    "D": 38,
    "E": 17,
    "F": 16,
    "G": 85,
    "H": 7,
    "I": 0,
}
s = GBFHeuristicGraphSearcher(g, "A", "I", h1)
s.search()

# Available options are DFS, BFS and LCF for both Tree and Graph
# GBFHeuristic and AStar for Graph only, heuristic param can be either function on Node or dict
# s = GBFHeuristicGraphSearcher(g, "A", "I", h1)
# Options:
#   cycle_checking - cycle checking + pruning, not guaranteed, esp on tree search, is in seminars however
#   early_exit - exit on finding route, not optimal for DFS
#   closed_prune - closed list pruning (graph only) - multi-path prune
# s.search()

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
