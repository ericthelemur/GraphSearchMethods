from typing import Union

from graph import *


class GraphSearcher:
    def __init__(self, g, ss: Union[str, list[str]], gs: Union[str, list[str]]):
        self.verbose = True
        self.graph = g

        if isinstance(ss, str): ss = [ss]
        self.start_nodes = [self.graph.nodes[s] for s in ss]
        self.frontier = [Path([], sn) for sn in self.start_nodes]
        self.closed = []

        # If single goal, wrap in list
        if isinstance(gs, str): gs = [gs]
        self.goals = set([self.graph.nodes[n] for n in gs])

        self.table: list[tuple[Path, list[Node], list[Path], list[Path]]] = []
        self.iter_prune = []


    def search(self, cycle_checking=True, early_exit=True, closed_prune=True):
        if self.verbose: print("Assuming tied costs broken alphabetically.")
        self.iter_print("-")
        while True:
            if not self.frontier:
                self.exhaust_print(early_exit)
                self.final_print(None)
                return None
            choice = self.strategy()

            if closed_prune and choice.end in self.closed:
                self.prune_print(choice)
                self.iter_print("-")
                continue
            if choice.end not in self.closed: self.closed.append(choice.end)

            # If done, output and end
            if choice.end in self.goals:
                if early_exit: self.final_print(choice)
                else: self.iter_print(choice)
                self.route_print(choice)
                if early_exit:
                    return choice

            if len(choice.path) >= 2: prev = choice.path[-2]
            else: prev = None
            for e in choice.end.out_edges:
                # Exclude source node
                if (prev and e.end == prev) or (closed_prune and e.end in self.closed):
                    self.prune_print(Path(choice, e.end))
                    continue
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
        self.table.append((choice, self.closed.copy(), self.iter_prune.copy(), self.frontier.copy()))
        self.iter_prune = []

    def prune_print(self, choice: Path):
        self.iter_prune.append(choice)

    def route_print(self, choice):
        # What is printed when a route is found
        if self.verbose: print("PATH:", choice, choice.cost)

    def final_print(self, choice):
        if not self.verbose: return

        widths = [10, 10, 10, 10]
        for row in self.table:
            for i, v in enumerate(row):
                l = len(str(v))
                if i == 1: l = len(separator.join(map(str, v)))
                if i == 2: l = len(", ".join(str(p) for p in v))
                if l > widths[i]: widths[i] = l

        print("Expanded".ljust(widths[0]), "Closed".ljust(widths[1]), "Pruned".ljust(widths[2]), "Frontier".ljust(widths[3]))

        for choice, closed, pruned, frontier in self.table:
            print(str(choice).ljust(widths[0], "."),
                  separator.join(map(str, closed)).ljust(widths[1], "."),
                  (", ".join(str(p) for p in pruned)).ljust(widths[2], "."),
                  "[", ", ".join(f"{p} {p.weight()}" for p in frontier), "]"
                  )

        print(str(choice).ljust(widths[0], "."), "Goal Reached")
        print("Pruned:", sum(len(pr) for _, _, pr, _ in self.table), "Explored:", sum(1 for ex, _, _, _ in self.table if isinstance(ex, Path)))


    def exhaust_print(self, early_exit):
        if not self.verbose: return
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
    def __init__(self, g, ss: Union[str, list[str]], gs: Union[str, list[str]], heuristic):
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
        c = source.cost + edge.cost
        p = Path(source, edge.end, c, h)

        self.frontier.append(p)
        self.frontier.sort(key=lambda p: (p.heuristic, p.end.name))


    def final_print(self, choice):
        if not self.verbose: return
        widths = [10, 10, 10, 10]

        for row in self.table:
            for i, v in enumerate(row):
                l = len(str(v))
                if i == 1: l = len(separator.join(map(str, v)))
                if i == 2: l = len(", ".join(str(p) for p in v))
                if l > widths[i]: widths[i] = l

        print("Expanded".ljust(widths[0]), "Closed".ljust(widths[1]), "Pruned".ljust(widths[2]),
              "Frontier".ljust(widths[3]))

        prev_frontier = []
        for choice, closed, pruned, frontier in self.table:
            heur_str = {p: "" if p in prev_frontier else f"{p.cost} + {p.heuristic} = " for p in frontier}
            print(str(choice).ljust(widths[0], "."),
                  separator.join(map(str, closed)).ljust(widths[1], "."),
                  (", ".join(str(p) for p in pruned)).ljust(widths[2], "."),
                  "[", ", ".join(f"{p} {heur_str[p]}{p.weight()}" for p in frontier), "]"
                  )
            prev_frontier = frontier

        print(str(choice).ljust(widths[0], "."), "Goal Reached")

        print("Pruned:", sum(len(pr) for _, _, pr, _ in self.table),
              "Explored:", sum(1 for ex, _, _, _ in self.table if isinstance(ex, Path)))


class AStarGraphSearcher(GBFHeuristicGraphSearcher):
    def add_strategy(self, source: Path, edge: Edge):
        h = self.heuristic(edge.end)
        c = source.cost + edge.cost
        p = Path(source, edge.end, c, h)

        self.frontier.append(p)
        self.frontier.sort(key=lambda p: (p.cost + p.heuristic, p.end.name))