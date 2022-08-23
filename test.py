from pyomo.core import *
import pyomo.opt
from cutstock_util import*
import pyomo.environ as pyo
import random 

# Reading data 
def BinPackingExample():
    B = 9
    w = [2,3,4,5,6,7,8]
    q = [4,2,6,6,2,2,2]
    s=[]
    for j in range(len(w)):
        for i in range(q[j]):
            s.append(w[j])
    return s,B

s,B = BinPackingExample()
print("items:", s)
print("bin size:", B)


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

n = len(s)
U = len(FFD(s,B)) 
print(n,U)

model = ConcreteModel(name="CutStock Problem")
SheetsAvail = 1000
PriceSheet = 10 
#Defining Variables

model.SheetsCut = Var()
model.TotalCost = Var()
Patterns = []
k = 0
for i in range(n):
    k += 1
    Patterns.append(k)
model.PatternCount = Var(Patterns, bounds=(0,None))
Cuts = []
k = 0
for i in range(U):
    k += 1
    Cuts.append(k)
model.ExcessCuts = Var(Cuts, bounds=(0,None))


model.objective = Objective(expr=1.0*model.TotalCost)


model.TotCost = Constraint(expr = model.TotalCost == PriceSheet* model.SheetsCut)
model.RawAvail = Constraint(expr = model.SheetsCut <= SheetsAvail)
model.Sheets = Constraint(expr = summation(model.PatternCount) == model.SheetsCut)
# model.CutReq = Constraint(Cuts)
# for c in Cuts:
#     model.CutReq.add(c, expr=sum(CutsInPattern[c][p]*model.PatternCount[p] for p in Patterns) == CutDemand[c] + model.ExcessCuts[c])
opt = pyo.SolverFactory('glpk')
# results = opt.solve(instance)
results = opt.solve(model)


print( "Status:", results.solver.status)
print("Minimum total cost:", value(model.objective))

for v in model.component_objects(Var,active=True):
    for index in v:
        if (value(v[index]) > 0):
            print(v.name,':',value(v[index]))




