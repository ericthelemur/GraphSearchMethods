from Adversarial.minimax import *
from tree import *

t = construct_balanced_tree([8, 4, 2, 7, 6, 10, 3, 5, 5, 9, 1, 8, 7, 3, 9, 2], 2)
# t = construct_balanced_tree([-1, 3, 5, 1, -6, -4, 0, 9], 2)

# Chance replace test
# old = t.children[0].children[0]
# old.parent.children.remove(old)
#
# chance = Chance(old.parent, [0.6, 0.4])
# chance.children = old.children
# for child in old.children: child.parent = chance

m = ABMinimax(t)
m.minimax()

m.tree.tree_print()
