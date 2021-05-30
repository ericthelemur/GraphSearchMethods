from var_elim import *

"""
Vals order:
1 var: T F
2 var: TT TF FT FF
3 var: TTT TTF TFT TFF FTT FTF FFT FFF 
...
If first listed var is the result, the second half is 1- corresponding val in first half
Be careful with order of vars and vals
"""

# Factor("S", [0.4, 0.6])
# Factor("B", [0.8, 0.2])
# Factor("OSB", [0.6, 0.1, 0.4, 0.9,
#                     0.4, 0.9, 0.6, 0.1])
# Factor("OI", [0.2, 0.8, 0.7, 0.3])

Factor(["Bl"], [0.3])
Factor(["Ra"], [0.4])
Factor(["Ru", "Ra"], [0.2, 0.7])
Factor(["Fl", "Bl", "Ra"], [0.8, 0.5, 0.6, 0.2])
Factor(["Br", "Fl"], [0.8, 0.1])


# I highly recommend using the console, if you don't know what you are doing
# var_elim(known, elim):
#   conditions on each known, eliminates each elim and normalizes to find target
#   If not all eliminated, will include more in normalized

# Factor.var_elim([("I", True)], list("OS"))
Factor.var_elim([("Br", True), ("Ru", True)], ["Fl", "Ra"])


