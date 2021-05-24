separator = ""

class Node:
    def __init__(self, n: str):
        self.name = n
        self.out_edges = []
        self.in_edges = []
        self.search_node: TreeNode = None

    def __repr__(self):
        return f"{self.name}"


class Edge:
    def __init__(self, f: Node, t: Node, cost: int = 1):
        self.start = f
        self.end = t
        f.out_edges.append(self)
        t.in_edges.append(self)

        self.cost = cost

    def __repr__(self):
        return f"Edge {self.start} -> {self.end} c: {self.cost}"


class TreeNode:
    def __init__(self, n, parent, cost=0):
        self.node = n
        self.node.search_node = self
        self.parent: TreeNode = parent
        if self.parent: self.parent.children.append(self)
        self.children = []
        self.cost = cost

    def __repr__(self):
        return self.indent_print()

    def indent_print(self, depth=0, prefix="", last=False, costs=True):
        # Bit of a mess, prints the tree in a directory list style
        line_start = "" if not depth else ("└─" if last else "├─")
        new_prefix = "" if not depth else (prefix + (": " if last else "│ "))

        s = prefix + line_start + str(self.node) + (" " + str(self.cost) if costs else "") + "\n"
        if not self.children: return s
        for n in self.children[:-1]:
            s += n.indent_print(depth + 1, new_prefix)
        s += self.children[-1].indent_print(depth + 1, new_prefix, True)
        return s

    def find(self, name: str):
        if self.node.name == name: return self
        for c in self.children:
            r = c.find(name)
            if r: return r
        return None

    def ancestors(self) -> list[Node]:
        if self.parent:
            return self.parent.ancestors() + [self.parent.node]
        else: return []


class Path:
    def __init__(self, prev, new: Node, cost=0, h=0):
        if isinstance(prev, Path): prev = prev.path
        self.path = prev + [new]
        self.cost = cost
        self.heuristic = h
        self.end = new

    def __repr__(self):
        return "<" + separator.join(f"{n.name}" for n in self.path) + ">"

    def weight(self):
        return self.cost + self.heuristic


from graph_searches import LCFGraphSearcher


class Graph:
    def __init__(self, eds: list[tuple[str, str, int]], directed=True):
        self.nodes = {}
        self.edges = set()
        for f, t, c in eds:
            if f not in self.nodes: self.nodes[f] = Node(f)
            if t not in self.nodes: self.nodes[t] = Node(t)
            self.edges.add(Edge(self.nodes[f], self.nodes[t], c))
            if not directed: self.edges.add(Edge(self.nodes[t], self.nodes[f], c))

    def get_cost(self, start: Node, end: Node):
        for edge in self.edges:
            if edge.start == start and edge.end == end:
                return edge.cost

    def __repr__(self):
        return f"Graph Edges: {self.edges}"

    def admissible_heuristic(self, es: str, h):
        # Very lazy approach
        if h is None: heuristic = lambda x: 0
        elif isinstance(h, dict): heuristic = lambda x: h[x.name]
        else: heuristic = h

        print("\nNode    h   Cost  h <= cost")
        for name, node in self.nodes.items():
            s = LCFGraphSearcher(self, name, es)
            s.verbose = False
            p = s.search()
            print(name.ljust(7), str(heuristic(node)).ljust(4), str(p.cost).ljust(4), heuristic(node) <= p.cost)
