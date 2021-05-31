import itertools

from CSP import *


def domain_consistency(csp: BackTrackingCSP):
    print("Domain consistency")
    for var in csp.variables.values():
        print(f"Checking {var.name}:", end=" ")

        print(", ".join(f"{v}✓" if csp.check_assignment((var, v), undo_on_succeed=True)[0] else f"{v}\u0336✗" for v in var.domain))

        var.domain = [v for v in var.domain if csp.check_assignment((var, v), undo_on_succeed=True)[0]]
    print_line(csp)
    print("")


def arc_consistency(csp: BackTrackingCSP):
    print("Arc consistency; Domain consistency first?")
    print("You may want to reorder these")

    print("Const".ljust(9), "Var".ljust(4), "Remove".ljust(15), end=" ")
    for var in csp.variables.values():
        print(str(var.name).ljust(15), end=" ")
    print()
    print("Initial".ljust(30), end=" ")
    print_line(csp)

    for i, c in enumerate(csp.constraints):
        if len(c.variables) <= 1: continue
        for var in c.variables:
            other_vars = [v for v in c.variables if v != var]
            asss = list(itertools.product(*[v.domain for v in other_vars]))

            remove = []
            for v in var.domain:
                if not try_val(c, var, v, other_vars, asss):
                    remove.append(v)

            print((c.constraint_to_str().ljust(10) + var.name).ljust(15), end="")
            print(str(remove).ljust(15), end=" ")

            var.domain = [v for v in var.domain if v not in remove]

            print_line(csp)
    print("May try a second round, if values removed")


def try_val(c, var, val, other, asss):
    for ass in asss:
        ass_dict = dict(zip(other, ass)) | {var: val}
        args = [ass_dict[v] for v in c.variables]
        if c.constraint(*args):
            return True
    return False


def print_line(csp: BackTrackingCSP):
    for var in csp.variables.values():
        if var.value is None:
            print(str(var.domain).ljust(15), end=" ")
        else: print(str(var.value).ljust(15), end=" ")
    print()
