from collections import defaultdict
from math import exp, e
from typing import Union


class QLearner:
    def __init__(self, alpha, gamma, initial: dict[str, dict[str, float]] = None, default=0.0):
        self.alpha = alpha
        self.gamma = gamma
        self.q = defaultdict(lambda: defaultdict(lambda: default))
        if initial is not None:
            for k, d in initial.items():
                self.q[k] = defaultdict(lambda: default, d)
        self.default = default

    def learn(self, experience: list[Union[str, float]]):
        print("Q[s, a] = (1-α)Q[s, a] + α(r + γ max a'(Q[s', a']))\n")
        s = experience.pop(0)
        while experience:
            a = experience.pop(0)
            r = float(experience.pop(0))
            s2 = experience.pop(0)

            best_next = max([self.default] + list(self.q[s2].values()))
            print(s, a, r, s2, f"\n\tbest = max_a'(Q[{s2}, a'] = {best_next}\n\tQ[{s}, {a}] = (1-{self.alpha})x{self.q[s][a]} + {self.alpha}({r} + {self.gamma} x {best_next})", end=" = ")
            self.q[s][a] = (1-self.alpha)*self.q[s][a] + self.alpha * (r + self.gamma * best_next)
            print(self.q[s][a], "\n")
            s = s2

    def __repr__(self):
        res = ""
        for s, acts in self.q.items():
            res += f"{s}:\n"

            for a, v in acts.items():
                res += f"\t{a}: {v}\n"
        return res

    def softmax_prob(self, s, a, t):
        num = exp(self.q[s][a] / t)
        print(f"exp({self.q[s][a]} / {t}) /")
        vals = [v for v in self.q[s].values()]
        print("\t(", " + ".join(f"exp({v} / {t})" for v in vals), ")")
        den = sum(exp(float(v)/t) for v in vals)

        print("= %.3f" % (num/den))
        return num / den
