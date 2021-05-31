from math import log, ceil, floor


class Node:
    def __init__(self, parent, value=None):
        if parent is not None:
            self.parent = parent
            self.player = not parent.player

            parent.children.append(self)
        else:
            self.parent = None
            self.player = True
        self.children = []
        self.value = value
        self.chosen = None
        self.pruned = True
        self.alpha = None
        self.beta = None

    def __str__(self):
        if self.pruned: return "-Pr-"
        if any(c.pruned for c in self.children):
            if self.player: return str(self.value) + "<="
            else: return "<=" + str(self.value)
        if self.parent and self.parent.chosen == self: return ">" + str(self.value) + "<"
        return str(self.value)

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

    def tree_print(self):
        print("Many be horribly mangled")
        for line in self.get_lines():
            print(line)

    def get_lines(self):
        if self.pruned: return [str(self)]
        if not self.children: return [str(self)]
        child_lines = [c.get_lines() for c in self.children]

        return self.merge(str(self), child_lines)


    def merge(self, parent: str, children: list[list[str]]):
        widths = [len(c[0])+1 for c in children]
        lines = [parent.center(sum(widths)), "|".center(sum(widths))]

        bar = " " * (floor(widths[0]/2)-1) + "┌"
        for i in range(1, len(widths)):
            if i > 1: bar += "┬"
            bar += "─" * (ceil(widths[i-1]/2.0) + floor(widths[i]/2.0)-1)
        bar += "┐" + (" " * (ceil(widths[-1]/2)-1))

        if len(children) != 1: lines.append(bar)
        else: lines.append("|".center(sum(widths)))
        comb_lines = ["" for _ in range(max(map(len, children)))]

        for i, c in enumerate(children):
            for j in range(len(comb_lines)):
                if j < len(c): comb_lines[j] += c[j].center(widths[i]-1) + " "
                else: comb_lines[j] += " "*(widths[i])

        return lines + comb_lines



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

