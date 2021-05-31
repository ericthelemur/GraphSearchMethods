from math import floor, ceil
from typing import Iterable

class Node:
    def __init__(self, var, parent, rule=None):
        self.var = var
        self.parent = parent
        if parent is not None:
            parent.children.append(self)

        self.children = []
        self.cost = -1
        self.rule = rule

    def set_parent(self, parent):
        if self.parent is not None:
            self.parent.children.remove(self)
        self.parent = parent
        if self.parent is not None:
            self.parent.children.append(self)


    def __repr__(self):
        return self.var

    def indent_print(self, depth=0, prefix="", last=False, prune=False):
        # Bit of a mess, prints the tree in a directory list style
        line_start = "" if not depth else (("└" if last else "├") + "─")
        new_prefix = "" if not depth else (prefix + (": " if last else "│ "))

        s = prefix + line_start + str(self) + "\n"
        if not self.children: return s

        self.children.sort(key=lambda n: n.var, reverse=True)
        for n in reversed(self.children[1:]):
            s += n.indent_print(depth + 1, new_prefix, prune=prune)
        s += self.children[0].indent_print(depth + 1, new_prefix, True, prune=prune)
        return s

    def tree_print(self):
        print("Many be horribly mangled")
        for line in self.get_lines():
            print(line)

    def get_lines(self):
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


class Impl:
    def __init__(self, pre: list[str], post: str):
        self.pre = pre
        self.post = post

    def __repr__(self):
        return f"Rule {self.pre} -> {self.post}"


class BackwardChain:
    def __init__(self, known: list[str], rules: list[Impl]):
        self.rules = rules
        self.known = set(known)


    def solve(self, need: str, parent: Node = None, verbose=True) -> int:
        if verbose and parent is None: print("Presents answer as tree, should merge duplicate nodes. Does not account for infinite depth, however, this should give the fewest node tree.")
        if need in self.known:
            Node(need, parent, None)
            return 1

        options = []
        for rule in self.rules:
            if rule.post == need:
                n = Node(need, None, rule)
                options.append(n)
                results = {p: self.solve(p, n) for p in rule.pre}

                if all(c > 0 for c in results.values()):
                    n.cost = 1+sum(c for c in results.values())

        if not options: return -1

        best = min(options, key=lambda x: x.cost)
        best.set_parent(parent)

        if parent is None:
            self.construct_rules(best, verbose)
            if verbose:
                print()
                print(best.indent_print())
                best.tree_print()
        return best.cost

    def construct_rules(self, parent: Node, verbose=True):
        fired = []
        layer = [parent]
        new_layer = []
        known = [parent.var]
        if verbose: print(parent.var)

        while layer:
            for node in layer:
                new_layer += node.children

                for c in node.children:
                    if c.var not in known: known.append(c.var)
                known.sort()

                if node.rule is not None and node.rule not in fired:
                    if verbose: print(node.rule)
                    fired.append(node.rule)

            layer = new_layer
            new_layer = []
            if verbose: print(''.join(known))
        print(f"Required {len(fired)} rules.")



class ForwardChain:
    def __init__(self, known: list[str], rules: list[Impl]):
        self.rules = rules
        self.known = known.copy()
        self.known_orig = known.copy()

    def solve(self, need):
        print("\t\t\t\t" + ''.join(self.known))
        iterations = 0
        while rule := self.select_rule():
            self.known.append(rule.post)
            self.known.sort()
            print(f"{rule} \t{''.join(self.known)}")
            iterations += 1

        print(f"{iterations} rules expanded.")
        b = BackwardChain(self.known_orig, self.rules)
        b.solve(need, None, verbose=False)
        return need in self.known

    def select_rule(self):
        for rule in self.rules:
            if rule.post not in self.known and \
                    all(r in self.known for r in rule.pre):
                return rule
        return None



