
from pyscipopt import Model
from pyscipopt import multidict
from pyscipopt import quicksum
# from pyscipopt import GRB




def mctransp(I, J, K, c, d, M):
    model = Model("multi-commodity transportation")
    x = {}
    for i,j,k in c:
        x[i,j,k] = model.addVar(vtype="C", name="x[%s,%s,%s]" % (i, j, k))
    # model.update()
    for i in I:
        for k in K:
            model.addCons(quicksum(x[i,j,k] for j in J if (i,j,k) in x) == d[i,k], "Demand[%s,%s]" % (i,k))
    for j in J:
        model.addCons(quicksum(x[i,j,k] for (i,j2,k) in x if j2 == j) <= M[j], "Capacity[%s]" % j)
    model.setObjective(quicksum(c[i,j,k]*x[i,j,k]  for i,j,k in x), "minimize")
    # model.update()
    # model.__data = x
    return model, x




J,M = multidict({1:3000, 2:3000, 3:3000})
produce = {1:[2,4], 2:[1,2,3], 3:[2,3,4]}

d = {(1,1):80,   (1,2):85,   (1,3):300,  (1,4):6,
     (2,1):270,  (2,2):160,  (2,3):400,  (2,4):7,
     (3,1):250,  (3,2):130,  (3,3):350,  (3,4):4,
     (4,1):160,  (4,2):60,   (4,3):200,  (4,4):3,
     (5,1):180,  (5,2):40,   (5,3):150,  (5,4):5
     }
I = set([i for (i,k) in d])
K = set([k for (i,k) in d])

weight = {1:5, 2:2, 3:3, 4:4}
cost = {(1,1):4,  (1,2):6, (1,3):9,
        (2,1):5,  (2,2):4, (2,3):7,
        (3,1):6,  (3,2):3, (3,3):4,
        (4,1):8,  (4,2):5, (4,3):3,
        (5,1):10, (5,2):8, (5,3):4
        }
c = {}
for i in I:
    for j in J:
        for k in produce[j]:
            c[i, j, k] = cost[i,j] * weight[k]

model,x = mctransp(I, J, K,c,d,M)
model.optimize()
print ("Optimal value:", model.getObjVal)
EPS = 1.e-6
# x = model.
for i,j,k in x:
    if model.getVal(x[i,j,k])> EPS:
        print ("sending %10g units of %3d from plant %3d to customer %3d" % (model.getVal(x[i,j,k]), k, j, i))