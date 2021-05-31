from typing import Union
from graph import *


class TreeSearcher:
    def __init__(self, g: Graph, s: str, gs: Union[str, list[str]]):
        self.graph = g

        self.start = self.graph.nodes[s]
        self.search_tree = TreeNode(self.start, None)
        self.candidates = [self.start.search_node]

        # If single goal, wrap in list
        if isinstance(gs, str): gs = [gs]
        self.goals = set([self.graph.nodes[n] for n in gs])
        self.iterations = 0


    def search(self, cycle_checking=True, early_exit=True):
        if cycle_checking: print("Assuming can omit child nodes of choice that are ancestors of choice in the search tree (cycle pruning).")
        print("Assuming tied costs broken alphabetically.")
        self.iterations = 0

        while True:
            self.iterations += 1
            if not self.candidates:
                self.exhaust_print(early_exit)
                self.final_print()
                return None
            choice = self.strategy()
            choice.position = self.iterations

            # If done, output and end
            if choice.node in self.goals:
                if not early_exit: self.iter_print(choice)
                else: print(str(self.iterations).ljust(3), choice.node.name.ljust(3), "Goal Reached")
                self.route_print(choice)
                if early_exit:
                    self.final_print()
                    return

            prev = choice.parent
            for e in choice.node.out_edges:
                # Exclude source node
                if prev and e.end == prev.node: continue
                # Specific case in seminar question S1Q1, assumed general - omitting ancestors from expansion
                if cycle_checking and e.end in choice.ancestors(): continue

                self.add_strategy(choice, e)
            self.iter_print(choice)


    def strategy(self) -> TreeNode:
        # Strategy for selecting a node:
        # Expand alphabetically
        choice = min(self.candidates, key=lambda n: n.node.name)
        self.candidates.remove(choice)
        return choice

    def add_strategy(self, source: TreeNode, edge: Edge):
        # Strategy for adding a node to candidates
        t = TreeNode(edge.end, source)
        self.candidates.append(t)
        self.candidates.sort(key=lambda t: t.node.name)


    def iter_print(self, choice: TreeNode):
        print(str(self.iterations).ljust(3), choice.node.name.ljust(3), "[", ", ".join(f"{c.node.name}: {c.cost}" for c in self.candidates), "]")

    def route_print(self, choice):
        # What is printed when a route is found
        print("PATH:", choice.ancestors() + [choice.node], choice.cost)

    def final_print(self):
        print("Nodes expanded:", self.iterations)
        print("\nSearch Tree:")
        print("Numbered nodes show order of expansion. Non-numbered nodes were added to the queue, but never expanded.")
        print(self.search_tree)

    def exhaust_print(self, early_exit):
        if not early_exit: print("Any paths printed previously")
        else: print("No Path")


class DFSTreeSearcher(TreeSearcher):
    def strategy(self) -> TreeNode:
        return self.candidates.pop(0)

    def add_strategy(self, source: TreeNode, edge: Edge):
        t = TreeNode(edge.end, source, source.cost+1)
        self.candidates.insert(0, t)
        self.candidates.sort(key=lambda t: t.node.name)
        self.candidates.sort(key=lambda t: t.cost, reverse=True)


class BFSTreeSearcher(TreeSearcher):
    def strategy(self) -> TreeNode:
        return self.candidates.pop(0)

    def add_strategy(self, source: TreeNode, edge: Edge):
        t = TreeNode(edge.end, source, source.cost+1)
        self.candidates.append(t)
        self.candidates.sort(key=lambda t: (t.cost, t.node.name))


class LCFTreeSearcher(TreeSearcher):

    def strategy(self) -> TreeNode:
        # Expand lowest-cost first
        choice = self.candidates.pop(0)
        return choice

    def add_strategy(self, source: TreeNode, edge: Edge):
        # Calc cost
        c = source.cost + edge.cost

        t: TreeNode = TreeNode(edge.end, source, c)

        self.candidates.append(t)
        # Sort candidates (lazy PQ)
        self.candidates.sort(key=lambda n: (n.cost, n.node.name))