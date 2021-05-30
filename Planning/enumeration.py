from typing import Callable
import itertools


class Expr:
    def __init__(self, name: str, args: list[str], func: Callable):
        self.name = name
        self.args = args
        self.func = func

    def eval(self, vals: dict[str, bool]):
        args = [vals[var] for var in self.args]
        return self.func(*args)

    def __repr__(self):
        return self.name + str(self.args)


class Enumerator:
    def __init__(self, vars: list[str], KB: list[Expr], result: Expr):
        self.vars = vars
        self.literals = vars + ["¬" + v for v in vars]
        self.KB = KB
        self.result = result

    def eval(self):
        table = []
        table.append([v for v in self.vars] + [e.name for e in self.KB] + ["All KB"] + [self.result.name] + ["KB valid"])

        for ass in itertools.product([True, False], repeat=len(self.vars)):
            vals = {v: a for v, a in zip(self.vars, ass)} | {("¬"+v): not a for v, a in zip(self.vars, ass)}
            row = [boolstr(v) for v in ass]

            result = self.result.eval(vals)

            KB = [e.eval(vals) for e in self.KB]
            row += [boolstr(v) for v in KB]

            row += [boolstr(all(KB))]

            row += [boolstr(result)]

            row.append(boolstr(result) if all(KB) else "")
            table.append(row)

        print_table(table)


def boolstr(bool):
    return "T" if bool else "F"


def print_table(rows: list[list[str]]):
    lengths = [3 for _ in range(len(rows[0]))]
    for row in rows:
        for i in range(len(row)):
            if len(row[i]) > lengths[i]:
                lengths[i] = len(row[i])

    for row in rows:
        for c, l in zip(row, lengths):
            print(c.center(l), end="|")
        print()