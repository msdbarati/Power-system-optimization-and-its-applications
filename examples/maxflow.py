"""Maximum Netwrok flow

This script uses pyomo package to model a simple maximum network flow problem.
fill the GLPK_EXE_PATH based on your local GLPK solver path.
dual values and reduced costs are extracted from solver.
"""
GLPK_EXE_PATH = "<glpk-path>"

import pyomo.environ as pyo

## fix it according to your GLKP solver local path
solvername = 'glpk'
solverpath_exe = GLPK_EXE_PATH

## Connecting to Solver and solving the instance
solver= pyo.SolverFactory(solvername, executable=solverpath_exe)

N = [1,2,3,4,5,6]
A = [(1,2),(1,4),(2,3),(4,5),(3,6),(5,6),(2,5),(4,3),(6,1)]
c ={
    (1,2):8,
    (1,4):9,
    (2,3):7,
    (4,5):2,
    (3,6):6,
    (5,6):5,
    (2,5):4,
    (4,3):3,
    (6,1):100, # don't use inf
}


model = pyo.ConcreteModel()

## Variables
model.x = pyo.Var(A,within=pyo.NonNegativeReals)

## Constraints
def capacity_rule(model,i,j):
    return model.x[i,j] <= c[i,j]
model.capacity = pyo.Constraint(A, rule=capacity_rule)

def equliburium_rule(model,i):
    expr = 0
    for j in N:
        if (i,j) in A:
            expr += model.x[(i,j)]
    for k in N:
        if (k,i) in A:
            expr -= model.x[(k,i)]
    return expr == 0
model.equil = pyo.Constraint(N,rule=equliburium_rule)

## Objective
model.obj = pyo.Objective(expr=model.x[6,1], sense=pyo.maximize)

## Dual values
## dual values are not captured by default, it should be signaled before optimization
## this variables should be named exactly "dual" and "rc" 
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)


results = solver.solve(model)
# print(pyo.value(model.obj))

print ("Duals")
print ("  Capacity Constraint")
for index in model.capacity:
    print ("      ", index, model.dual[model.capacity[index]])
print ("  Equiliburium Constraint")
for index in model.equil:
    print ("      ", index, model.dual[model.equil[index]])

print ("Reduced Costs")
print ("  X variables")
for index in model.x:
    print ("      ", index, model.rc[model.x[index]])

# for (i,j) in A:
#     if pyo.value(model.x[(i,j)]) == c[i,j]:
#         print(i,j)

