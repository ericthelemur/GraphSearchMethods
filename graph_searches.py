from typing import Union, Callable

from graph import *


class GraphSearcher:
    def __init__(self, g: Graph, ss: Union[str, list[str]], gs: Union[str, list[str]]):
        self.graph = g

        if isinstance(ss, str): ss = [ss]
        self.start_nodes = [self.graph.nodes[s] for s in ss]
        self.frontier = [Path([], sn) for sn in self.start_nodes]
        self.closed = []

        # If single goal, wrap in list
        if isinstance(gs, str): gs = [gs]
        self.goals = set([self.graph.nodes[n] for n in gs])


    def search(self, cycle_checking=True, early_exit=True, closed_prune=True):
        print("Assuming tied costs broken alphabetically.")
        while True:
            if not self.frontier:
                self.exhaust_print(early_exit)
                self.final_print()
                return None
            choice = self.strategy()

            if closed_prune and choice.end in self.closed:
                self.prune_print(choice)
                continue
            if choice.end not in self.closed: self.closed.append(choice.end)

            # If done, output and end
            if choice.end in self.goals:
                if early_exit: self.iter_print(choice)
                self.route_print(choice)
                if early_exit:
                    self.final_print()
                    return

            if len(choice.path) >= 2: prev = choice.path[-2]
            else: prev = None
            for e in choice.end.out_edges:
                # Exclude source node
                if prev and e.end == prev: continue
                # Specific case in seminar question S1Q1, assumed general - omitting ancestors from expansion
                if cycle_checking and e.end in choice.path: continue

                self.add_strategy(choice, e)
            self.iter_print(choice)


    def strategy(self) -> Path:
        # Strategy for selecting a node:
        # Expand alphabetically
        choice = min(self.frontier, key=lambda p: p.end.name)
        self.frontier.remove(choice)
        return choice

    def add_strategy(self, source: Path, edge: Edge):
        # Strategy for adding a node to candidates
        p = Path(source, edge.end)
        self.frontier.append(p)
        self.frontier.sort(key=lambda p: p.end.name)


    def iter_print(self, choice: Path):
        print("Explored", str(choice).ljust(20, "."),
              str(self.closed).ljust(30, "."),
              "[", ", ".join(str(p) for p in self.frontier), "]")

    def prune_print(self, choice: Path):
        print("Pruned  ", str(choice).ljust(20, "."),
              str(self.closed).ljust(30, "."),
              "[", ", ".join(str(p) for p in self.frontier), "]")

    def route_print(self, choice):
        # What is printed when a route is found
        print("PATH:", choice)

    def final_print(self):
        pass

    def exhaust_print(self, early_exit):
        if not early_exit: print("Any paths printed previously")
        else: print("No Path")



class DFSGraphSearcher(GraphSearcher):
    def strategy(self) -> Path:
        return self.frontier.pop(0)

    def add_strategy(self, source: Path, edge: Edge):
        p = Path(source, edge.end, source.cost+1)
        self.frontier.insert(0, p)
        self.frontier.sort(key=lambda p: p.end.name)
        self.frontier.sort(key=lambda p: p.cost, reverse=True)


class BFSGraphSearcher(GraphSearcher):
    def strategy(self) -> Path:
        return self.frontier.pop(0)

    def add_strategy(self, source: Path, edge: Edge):
        p = Path(source, edge.end, source.cost+1)
        self.frontier.append(p)
        self.frontier.sort(key=lambda p: (p.cost, p.end.name))


class LCFGraphSearcher(GraphSearcher):
    def strategy(self) -> Path:
        # Expand lowest-cost first
        choice = self.frontier.pop(0)
        return choice

    def add_strategy(self, source: Path, edge: Edge):
        # Calc cost
        c = source.cost + edge.cost
        p = Path(source, edge.end, c)

        self.frontier.append(p)
        # Sort candidates (lazy PQ)
        # TODO sort past end node name
        self.frontier.sort(key=lambda p: (p.cost, p.end.name))



class GBFHeuristicGraphSearcher(GraphSearcher):
    def __init__(self, g: Graph, ss: Union[str, list[str]], gs: Union[str, list[str]], heuristic):
        super().__init__(g, ss, gs)

        if heuristic is None: self.heuristic = lambda x: 0
        elif isinstance(heuristic, dict): self.heuristic = lambda x: heuristic[x.name]
        else: self.heuristic = heuristic

        self.frontier = [Path([], sn, 0, self.heuristic(sn)) for sn in self.start_nodes]

    def strategy(self) -> Path:
        choice = self.frontier.pop(0)
        return choice

    def add_strategy(self, source: Path, edge: Edge):
        h = self.heuristic(edge.end)
        p = Path(source, edge.end, 0, h)

        self.frontier.append(p)
        self.frontier.sort(key=lambda p: (p.heuristic, p.end.name))


class AStarGraphSearcher(GBFHeuristicGraphSearcher):
    def add_strategy(self, source: Path, edge: Edge):
        h = self.heuristic(edge.end)
        c = source.cost + edge.cost
        p = Path(source, edge.end, c, h)

        self.frontier.append(p)
        self.frontier.sort(key=lambda p: (p.cost + p.heuristic, p.end.name))