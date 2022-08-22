from pyomo.core import *
import pyomo.opt
from cutstock_util import*
import pyomo.environ as pyo
import random 

# Reading data 
def DiscreteUniform(n=10,LB=1,UB=99,B=100):
    """DiscreteUniform: create random, uniform instance for the bin packing problem."""
    B = 100
    s = [0]*n
    for i in range(n):
        s[i] = random.randint(LB,UB)
    return s,B


s,B = DiscreteUniform()
print(s,B)



# len phuong an 

def FFD(s,B):
    """First Fit Decreasing heuristics for the Bin Packing Problem.
    Parameters:
        - s: list with item widths
        - B: bin capacity
    Returns a list of lists with bin compositions.
    """
    remain = [B]        # keep list of empty space per bin
    sol = [[]]          # a list ot items (i.e., sizes) on each used bin
    for item in sorted(s,reverse=True):
        for (j,free) in enumerate(remain):
            if free >= item:
                remain[j] -= item
                sol[j].append(item)
                break
        else: #does not fit in any bin
            sol.append([item])
            remain.append(B-item)
    return sol

ffd = FFD(s,B)
print("\n\n\n FFD heuristic:")
print("Solution:")
print(ffd)
print(len(ffd), "bins")







