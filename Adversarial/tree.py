from math import log

class Node:
    def __init__(self, parent):
        if parent is not None:
            self.parent = parent
            self.player = not parent.player

            parent.children.append(self)
        else:
            self.parent = None
            self.player = True
        self.children = []
        self.value = None
        self.chosen = None
        self.pruned = True

    def __repr__(self):
        return f"{self.value}"

    def indent_print(self, depth=0, prefix="", last=False, prune=False):
        # Bit of a mess, prints the tree in a directory list style
        line_start = "" if not depth else (("└" if last else "├") + ("━" if self.parent.chosen == self else "─"))
        new_prefix = "" if not depth else (prefix + (": " if last else "│ "))

        if prune and self.pruned: return prefix + line_start + "Pruned\n"
        s = prefix + line_start + str(self) + "\n"
        if not self.children: return s
        for n in reversed(self.children[1:]):
            s += n.indent_print(depth + 1, new_prefix, prune=prune)
        s += self.children[0].indent_print(depth + 1, new_prefix, True, prune=prune)
        return s



class Leaf(Node):
    def __init__(self, parent, value):
        super().__init__(parent)
        self.value = value

    def __repr__(self):
        return f"{self.value}"


class Chance(Node):
    def __init__(self, parent, probabilities):
        super().__init__(parent)
        self.probabilities = probabilities

    def __repr__(self):
        return f"Chance {self.probabilities} {self.value}"


def construct_balanced_tree(leaves_vals: list[float], bf: int):
    height = log(len(leaves_vals), bf)
    if height != int(height):
        print("Non-balanced tree")
        return

    root = Node(None)
    parents = build_tree([root], height - 1, bf)

    leaves = []
    for i in range(len(leaves_vals)):
        parent = parents[i // bf]
        leaves.append(Leaf(parent, leaves_vals[i]))

    return root


def build_tree(parents: list[Node], height, bf: int):
    if height == 0: return parents

    nodes = []
    for parent in parents:
        nodes += [Node(parent) for _ in range(bf)]

    return build_tree(nodes, height - 1, bf)

