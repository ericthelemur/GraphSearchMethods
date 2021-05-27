from typing import Callable, Any, Iterable, Union


class Variable:
    def __init__(self, name: str, domain: list):
        self.name = name
        self.domain = domain
        self.constraints = []
        self.value = None

    def degree(self):
        return len(self.constraints)

    def __repr__(self):
        return f"{self.name} = {self.value}"


class Constraint:
    def __init__(self, variables: list[Variable], constraint: Callable):
        self.variables = variables
        for v in self.variables:
            v.constraints.append(self)
        self.constraint = constraint



class BackTrackingCSP:
    def __init__(self, vars: list[tuple[str, list]], constraints: list[tuple[list[str], Callable]]):
        self.variables = {n: Variable(n, d) for n, d in vars}
        self.constraints = [Constraint([self.variables[v] for v in vs], f) for vs, f in constraints]


    def solve(self) -> bool:
        print(" "*15, end="  ")
        for var in self.variables.values():
            print(str(var.name).ljust(15), end=" ")
        print()
        self.iter_print(None, None, True)

        return self.recursive_solve()

    def recursive_solve(self) -> bool:
        if all(v.value is not None for v in self.variables.values()): return True

        var = self.select_unassigned_variable()
        print()

        for val in self.order_domain_values(var):
            r, old_val = self.check_assignment((var, val))
            if r:
                var.value = val
                self.iter_print(var, val, True)
                result = self.recursive_solve()

                if result:
                    return True
                var.value = old_val[0]
            else:
                self.iter_print(var, val, False)

        self.backtrack_print(var)
        return False


    def iter_print(self, ass_var, ass_val, succeed: bool):
        if ass_var: print(f"{ass_var.name} = {ass_val} {'✅' if succeed else '❎'}".ljust(15), end="  ")
        else: print(" "*15, end="  ")

        for var in self.variables.values():
            if var.value is None:
                print(str([v for v in var.domain if self.check_assignment((var, v), undo_on_succeed=True)[0]]).ljust(15), end=" ")
            else: print(str(var.value).ljust(15), end=" ")
        print()

    def backtrack_print(self, ass_var):
        print("Stop here? <- kinda sketchy to, but did in ex")
        print("No valid assignment to", ass_var.name)
        print(f"Backtracking, assignment to {ass_var.name} failed, backtracking to:")
        print("\t", ", ".join(f"{var.name} = {var.value}" for var in self.variables.values() if var.value is not None))
        print("\t Unassigned: ", ", ".join(var.name for var in self.variables.values() if var.value is None))

    def select_unassigned_variable(self) -> Variable:
        for var in self.variables.values():
            if var.value is None:
                return var

    def order_domain_values(self, var) -> Iterable[Any]:
        return var.domain


    def check_consistent(self) -> bool:
        for cons in self.constraints:
            vals = (v.value for v in cons.variables)
            if any(v is None for v in vals): continue

            if not cons.constraint(*(v.value for v in cons.variables)):
                return False
        return True

    def check_assignment(self, *assignments: tuple[Variable, Any], undo_on_succeed: bool = False) -> tuple[bool, Any]:
        old_vals = [var.value for var, _ in assignments]

        for var, val in assignments:
            var.value = val

        r = self.check_consistent()
        if r and not undo_on_succeed: return r, old_vals

        for (var, val), old_val in zip(assignments, old_vals):
            var.value = old_val     # unassign for purity
        return r, old_vals


class HeuristicCSP(BackTrackingCSP):
    def select_unassigned_variable(self) -> Variable:
        # Significantly more complex to  display ties in MRV (no deg) separately
        unassigned_vars = [v for v in self.variables.values() if v.value is None]
        mrv_ties = HeuristicCSP.get_top_ties(unassigned_vars, self.MRV)
        print("MRV =", "/".join(v.name for v in mrv_ties), end="  ")
        if len(mrv_ties) == 1: return mrv_ties[0]

        deg_ties = HeuristicCSP.get_top_ties(mrv_ties, self.deg_heur)
        print("Deg =", "/".join(v.name for v in deg_ties), end="  ")
        if len(deg_ties) == 1: return deg_ties[0]

        print("Alphabetical =", deg_ties[0].name, end="  ")
        return deg_ties[0]

    def MRV(self, var: Variable) -> int:
        return sum(1 for val in var.domain if self.check_assignment((var, val), undo_on_succeed=True)[0])

    def deg_heur(self, var: Variable) -> int:
        return -len(var.constraints)


    def order_domain_values(self, var) -> Iterable[Any]:
        actual_domain = [v for v in var.domain if self.check_assignment((var, v), undo_on_succeed=True)[0]]
        return sorted(actual_domain, key=(lambda x: self.LCV(var, x)))

    def LCV(self, var: Variable, val):
        count = 0
        for count_var in self.variables.values():
            if count_var.value is None:
                count += self.count_valid(count_var, (var, val))
        return count


    def count_valid(self, check_var: Variable, *assignments: tuple[Variable, Any]):
        return sum(1 for val in check_var.domain if self.check_assignment(*assignments, (check_var, val), undo_on_succeed=True))

    @staticmethod
    def get_top_ties(options: list[Variable], key: Callable[[Variable], Any]) -> list[Variable]:
        sort_vals = {v: key(v) for v in options}
        result = sorted(options, key=(lambda v: (sort_vals[v], v.name)))
        best_val = sort_vals[result[0]]
        ties = [v for v in result if sort_vals[v] == best_val]
        return ties

    def solve(self) -> bool:
        print("   ", end=" ")
        return super(HeuristicCSP, self).solve()

    def iter_print(self, ass_var, ass_val, succeed: bool):
        print("LCV" if ass_var else "   ", end=" ")
        super(HeuristicCSP, self).iter_print(ass_var, ass_val, succeed)
