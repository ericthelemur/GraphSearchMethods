import itertools

class Factor:
    def __init__(self, vars, vals: list):
        self.vars = list(vars)
        self.vals = vals
        print(len(self.vals), (2 ** (len(self.vars)-1)), len(self.vals), len(self.vars))
        if len(self.vals) != (2 ** (len(self.vars)-1)):
            self.vals += [1 - v for v in self.vals]

        if len(self.vals) != 2 ** len(self.vars):
            raise Exception("Mismatching # vals and # vars")
        self.index = len(f)+1
        f.append(self)
        self.merged = False


    def get_val(self, *assignment: bool) -> float:
        if len(assignment) != len(self.vars):
            raise Exception("Mismatching # of vars")

        index = self.get_index(*assignment)
        return self.vals[index]

    @staticmethod
    def get_index(*assignment: bool) -> int:
        index = 0
        for i, val in enumerate(assignment):
            if not val:
                index += 2 ** (len(assignment) - i - 1)
        return index

    def get_index_dict(self, assignment: dict, vars=None) -> int:
        if vars is None: vars = self.vars
        ass = [assignment[v] for v in vars]
        return self.get_index(*ass)

    @staticmethod
    def boolstr(bool):
        return "T" if bool else "F"

    def __repr__(self):
        s = f"f{self.index}\n" + " | ".join(self.vars) + " ||\n"
        for ass in itertools.product([True, False], repeat=len(self.vars)):
            ind = self.get_index(*ass)
            s += " | ".join(self.boolstr(b) for b in ass)
            s += " || %.3f" % self.vals[ind] + "\n"
        return s


    def condition(self, var, val):
        new_vars = [v for v in self.vars if v != var]
        new_vals = [-1 for _ in range(len(self.vals) // 2)]

        for ass in itertools.product([True, False], repeat=(len(self.vars))-1):
            ass_dict = {v: a for v, a in zip(new_vars, ass)}
            ass_dict[var] = val

            old_ind = self.get_index_dict(ass_dict)
            new_ind = self.get_index_dict(ass_dict, new_vars)
            new_vals[new_ind] = self.vals[old_ind]

        self.merged = True
        f = Factor(new_vars, new_vals)
        print(f"f{f.index}({', '.join(f.vars)}) = Conditioning of f{self.index}: {var} = {val}")
        self.print_op([self, f], [f"{var}={val} ->"])
        return f

    def multiply(self, f2):
        all_vars = self.vars + f2.vars
        all_vars = list(dict.fromkeys(all_vars))
        new_vals = [-1 for _ in range(2**(len(all_vars)))]

        for ass in itertools.product([True, False], repeat=len(all_vars)):
            ass_dict = {v: a for v, a in zip(all_vars, ass)}

            ind1 = self.get_index_dict(ass_dict)
            ind2 = f2.get_index_dict(ass_dict)
            new_ind = self.get_index_dict(ass_dict, all_vars)

            new_vals[new_ind] = self.vals[ind1] * f2.vals[ind2]

        self.merged = True
        f2.merged = True

        f = Factor(all_vars, new_vals)
        print(f"f{f.index}({', '.join(f.vars)}) = Multiplication of f{self.index} x f{f2.index}")
        self.print_op([self, f2, f], [f"x", "="])
        return f


    def sum_out(self, var):
        new_vars = [v for v in self.vars if v != var]
        new_vals = [-1 for _ in range(len(self.vals) // 2)]

        for ass in itertools.product([True, False], repeat=(len(self.vars)) - 1):
            ass_dict = {v: a for v, a in zip(new_vars, ass)}

            old_ind1 = self.get_index_dict(ass_dict | {var: True})
            old_ind2 = self.get_index_dict(ass_dict | {var: False})

            new_ind = self.get_index_dict(ass_dict, new_vars)
            new_vals[new_ind] = self.vals[old_ind1] + self.vals[old_ind2]

        self.merged = True
        f = Factor(new_vars, new_vals)
        print(f"f{f.index}({', '.join(f.vars)}) = Summing out {var} on f{self.index}")
        self.print_op([self, f], [f"Σ{var} ->"])
        return f

    def normalize(self):
        total = sum(self.vals)
        f = Factor(self.vars, [v / total for v in self.vals])

        self.merged = True
        print(f"f{f.index}({', '.join(f.vars)}) = Normalising f{self.index}")
        self.print_op([self, f], [f"norm ->"])
        return f


    @staticmethod
    def print_op(factors, combiners):
        lines = [str(f).strip().split("\n") for f in factors]
        widths = [max(map(len, l)) for l in lines]
        height = max(map(len, lines))

        lines = [["" for _ in range((height - len(l)) // 2)] + l + ["" for _ in range((height - len(l)) // 2+1)] for l in lines]

        for i in range(height):
            for j, l in enumerate(lines):
                if j < len(lines)-1:
                    if i == height // 2: end = "  " + combiners[j] + "  "
                    else: end = " " * (4 + len(combiners[j]))
                else: end = "\n"
                print(l[i].ljust(widths[j]), end=end)
        print("\n")

    @staticmethod
    def print_current(merged_only=True):
        if merged_only: facts = [f1 for f1 in f if not f1.merged]
        else: facts = f
        Factor.print_op(facts, ["" for _ in range(len(facts) - 1)])


    @staticmethod
    def eliminate(*vars):
        var = vars[0]
        print("Eliminating", var)
        involved = [fact for fact in f if var in fact.vars and fact.merged == False]
        involved.sort(key=lambda x: len(x.vars))

        new = involved[0]

        for f2 in involved[1:]:
            new = new.multiply(f2)


        new = new.sum_out(var)
        print("Eliminated", var, "\n")
        if len(vars) <= 1: return new
        return Factor.eliminate(*vars[1:])


    @staticmethod
    def var_elim(known: list[tuple[str, bool]], elim: list[str]=None):

        Factor.print_op(f, ["" for _ in range(len(f) - 1)])

        for var, val in known:
            for fact in f:
                if var in fact.vars and not fact.merged:
                    fact.condition(var, val)

        Factor.eliminate(*elim)

        mult = [f1 for f1 in f if not f1.merged]

        f1 = mult[0]
        if len(mult) > 1:
            for f2 in mult[1:]:
                f1 = f1.multiply(f2)
        f1 = f1.normalize()
        Factor.print_current(False)
        return f1


f: list[Factor] = []
