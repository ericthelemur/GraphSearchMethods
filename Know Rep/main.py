from chaining import *

known = ["A", "F"]

rules = [
    Impl("A", "B"),
    Impl("A", "C"),
    Impl("B", "E"),
    Impl("BC", "H"),
    Impl("BH", "L"),
    Impl("CF", "D"),
    Impl("CK", "G"),
    Impl("DF", "E"),
    Impl("DF", "H"),
    Impl("FG", "I"),
    Impl("FG", "L"),
    Impl("H", "K"),
]

b = BackwardChain(known, rules)
b.solve("I")

# f = ForwardChain(known, rules)
# f.solve("L")


# 2020
# known = ["A"]
#
# rules = [
#     Impl("A", "E"),
#     Impl("B", "C"),
#     Impl("B", "D"),
#     Impl("CE", "Z"),
#     Impl("E", "F"),
#     Impl("E", "B"),
#     Impl("F", "G"),
# ]
#
# b = ForwardChain(known, rules)
# b.solve("Z")