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
