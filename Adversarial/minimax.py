from tree import *
from math import inf

class Minimax:
    def __init__(self, tree: Node):
        self.tree = tree
        self.prune = False

    def minimax(self):
        self.eval(self.tree)
        print(self.tree.indent_print(prune=self.prune))
        best_index = max(list(range(len(self.tree.children))), key=lambda x: self.tree.children[x].value)
        if len(self.tree.children) == 2: branch_str = "LR"[best_index]
        else: branch_str = str(best_index)
        print(f"Choose branch {branch_str}, utility {self.tree.children[best_index].value}")

    def eval(self, node: Node) -> float:
        if isinstance(node, Chance): raise NotImplementedError
        if isinstance(node, Leaf): return node.value
        for c in node.children:
            self.eval(c)

        if node.player: chosen = max(node.children, key=lambda c: c.value)
        else:           chosen = min(node.children, key=lambda c: c.value)

        node.chosen = chosen
        node.value = chosen.value
        return node.value


class ABMinimax(Minimax):
    def __init__(self, tree: Node):
        super().__init__(tree)
        self.prune = True

    def eval(self, node: Node, alpha=-inf, beta=inf, depth=-1) -> float:
        if isinstance(node, Chance): raise NotImplementedError
        node.pruned = False
        if depth == 0 or isinstance(node, Leaf):
            return node.value

        if node.player:
            best_child = node.children[0]
            self.eval(best_child, alpha, beta, depth - 1)
            alpha = max(alpha, best_child.value)

            for child in node.children[1:]:
                if beta <= alpha: break
                self.eval(child, alpha, beta, depth - 1)
                if child.value > best_child.value:
                    best_child = child
                    alpha = max(alpha, best_child.value)

            node.chosen = best_child
            node.value = best_child.value
            return node.value
        else:
            best_child = node.children[0]
            self.eval(node.children[0], alpha, beta, depth - 1)
            beta = min(beta, best_child.value)

            for child in node.children[1:]:
                if beta <= alpha: break
                self.eval(child, alpha, beta, depth - 1)
                if child.value < best_child.value:
                    best_child = child
                    beta = min(beta, best_child.value)

            node.chosen = best_child
            node.value = best_child.value
            return node.value


class ChanceMinimax(Minimax):
    # Cannot prune chance nodes, unless bounds of probability function is known
    def eval(self, node: Node) -> float:
        if isinstance(node, Chance):
            value = 0
            for i in range(len(node.children)):
                value += node.probabilities[i] * self.eval(node.children[i])

            node.value = value
            return value
        else: return super(ChanceMinimax, self).eval(node)
