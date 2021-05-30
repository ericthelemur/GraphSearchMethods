from CSP import *
from consistency import *

eq = lambda x, y: x == y
neq = lambda x, y: x != y
gr = lambda x, y: x > y
le = lambda x, y: x < y
geq = lambda x, y: x >= y
leq = lambda x, y: x <= y

# Seminar
# vars = [
#     ("A", [1, 2, 3]),
#     ("B", [1, 2, 3, 4]),
#     ("C", [1, 2]),
#     ("D", [2, 3, 4, 5]),
# ]
#
# cons = [
#     ("AB", lambda a, b: a < b),
#     ("AD", lambda a, d: a != d),
#     ("AD", lambda a, d: a != d+1),
#     ("BC", lambda b, c: b != c),
#     ("CD", lambda c, d: c+1 <= d)
# ]

# Revision Lecture
# vars = [
#     ("A", [1, 2, 3]),
#     ("B", [1, 2, 3]),
#     ("C", [1, 2, 3]),
#     ("D", [1, 2, 3]),
#     ("E", [1, 2, 3]),
#     ("F", [1, 2, 3]),
# ]
#
# cons = [
#     ("AB", neq), ("AC", neq), ("AD", neq),
#     ("BC", neq), ("BD", neq), ("BE", neq), ("BF", neq),
#     ("CF", neq),
#     ("DE", neq),
#     ("EF", neq)
# ]

# 2020 5e
vars = [
    ("A", [1, 2, 3, 4]),
    ("B", [1, 2, 3, 4]),
    ("C", [1, 2, 3, 4]),
    ("D", [1, 2, 3, 4]),
]

cons = [
    ("AB", neq), ("AC", eq), ("B", lambda b: b != 3),
    ("BC", neq), ("C", lambda c: c < 3), ("CD", le)
]


s = HeuristicCSP(vars, cons)
domain_consistency(s)
arc_consistency(s)

# s.solve()
# print(", ".join(map(str, s.variables.values())))
