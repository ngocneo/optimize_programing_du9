from pyomo.core import *
import pyomo.opt
from cutstock_util import*
import pyomo.environ as pyo

# Reading in Data using the cutstock_util
cutcount = getCutCount()
patcount = getPatCount()
Cuts = getCuts()
Patterns = getPatterns()
PriceSheet = getPriceSheetData()
SheetsAvail = getSheetsAvail()
CutDemand = getCutDemand()
CutsInPattern = getCutsInPattern()
########################################
#CutsInPattern = makeDict([Cuts,Patterns],CutsInPattern)
tmp = {}
for i in range(len(Cuts)):
    tmp[Cuts[i]] = {}
    for j in range(len(CutsInPattern[i])):
        tmp[Cuts[i]][Patterns[j]] = CutsInPattern[i][j]
CutsInPattern = tmp
########################################
#CutDemand = makeDict([Cuts],CutDemand)
tmp = {}
for i in range(len(Cuts)):
    tmp[Cuts[i]] = CutDemand[i]
CutDemand = tmp
print(cutcount)
print(patcount)
print(Patterns)
print(Cuts)
print(SheetsAvail)
for p in Patterns:
    print(p)
print(CutsInPattern)
print(CutDemand)
model = ConcreteModel(name="CutStock Problem")

#Defining Variables
model.SheetsCut = Var()
model.TotalCost = Var()
model.PatternCount = Var(Patterns, bounds=(0,None))
model.ExcessCuts = Var(Cuts, bounds=(0,None))

#objective minimun price 
model.objective = Objective(expr=1.0*model.TotalCost)

#Constraints rang buoc 
model.TotCost = Constraint(expr = model.TotalCost == PriceSheet* model.SheetsCut)

model.RawAvail = Constraint(expr = model.SheetsCut <= SheetsAvail)
model.Sheets = Constraint(expr = summation(model.PatternCount) == model.SheetsCut)
model.CutReq = Constraint(Cuts)
for c in Cuts:
    model.CutReq.add(c, expr=sum(CutsInPattern[c][p]*model.PatternCount[p] for p in Patterns) == CutDemand[c] + model.ExcessCuts[c])

# instance = model.create_instance()
# opt = pyomo.opt.SolverFactory('glpk')
opt = pyo.SolverFactory('glpk')
# results = opt.solve(instance)
results = opt.solve(model)

# instance.load(results)

print( "Status:", results.solver.status)
print("Minimum total cost:", value(model.objective))

for v in model.component_objects(Var,active=True):
    for index in v:
        if (value(v[index]) > 0):
            print(v.name,':',value(v[index]))

# model.display()