from q_learning import *

exp = [
    "s1", "right", 5,
    "s2", "left", 8,
    "s1", "pause", 10,
    "s1", "right", 6,
    "s3"
]

q = QLearner(0.1, 0.95)
q.learn(exp)

# q = QLearner(0.1, 0.95, {"Green": {"Buy": 10, "Sell": 12}, "Blue": {"Buy": 18, "Sell": 3}})
# q.learn(["Green", "Buy", 13, "Green"])
#
# print(q)
# q.softmax_prob("Green", "Sell", 0.9)