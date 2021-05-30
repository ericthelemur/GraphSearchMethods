from enumeration import *

var_expr = lambda x: Expr(x, [x], lambda x: x)
or_expr = lambda x, y: Expr(f"{x} or {y}", [x, y], lambda v1, v2: v1 or v2)
and_expr = lambda x, y: Expr(f"{x} and {y}", [x, y], lambda v1, v2: v1 and v2)

vars = list("ABC")

KB = [
    var_expr("A"),
    or_expr("A", "B"),
    or_expr("B", "¬C"),
    or_expr("¬B", "C")
]

result = or_expr("A", "C")

e = Enumerator(vars, KB, result)
e.eval()
