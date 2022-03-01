"""Warehouse location problem

This script uses pyomo package to model a warehouse location problem.
fill the GLPK_EXE_PATH based on your local GLPK solver path.
"""
GLPK_EXE_PATH = "<glpk-path>"

import pyomo.environ as pyo

## fix it according to your GLKP solver local path
solvername = 'glpk'
solverpath_exe = GLPK_EXE_PATH

## Connecting to Solver and solving the instance
solver= pyo.SolverFactory(solvername, executable=solverpath_exe)

N = ["Harlingen", "Memphis", "Ashland"]
M = ["NYC", "LA", "CHI", "HTX"]
P = 2
d = {
    'Harlingen': {
        'NYC': 1956,
        'LA' : 1606,
        'CHI': 1410,
        'HTX': 330,
    },
    'Memphis': {
        'NYC': 1096,
        'LA' : 1792,
        'CHI': 531,
        'HTX': 567,
    },
    'Ashland': {
        'NYC': 485,
        'LA': 2322,
        'CHI': 324,
        'HTX': 1236,
    },
}

    
model = pyo.ConcreteModel()

## Variables
model.x = pyo.Var(N, M, bounds=(0,1), within=pyo.Reals, initialize = 1)
# alternative method for defining the x variables
# model.x = pyo.Var(N, M, within=pyo.PercentFraction)


initialize_dict = {
    "Harlingen": 0,
    "Memphis": 0,
    "Ashland": 1,
}
model.y = pyo.Var(N, within=pyo.Binary, initialize = initialize_dict)
# model.y = pyo.Var(N, within=[0,1])

# print('x["Harlingen", "NYC"]: ', pyo.value(model.x["Harlingen", "NYC"]))
# print('y["Harlingen"]: ', pyo.value(model.y["Harlingen"]))

## Constraints
model.num_warehouses = pyo.Constraint(expr=sum(model.y[n] for n in N) <= P)

def demand_rule(model, m):
    return sum(model.x[n,m] for n in N) == 1
model.demand = pyo.Constraint(M, rule=demand_rule)

def warehouse_active_rule(mdl, n, m):
    return mdl.x[n,m] <= mdl.y[n]
model.warehouse_active = pyo.Constraint(N, M, rule=warehouse_active_rule)

# model.demand["NYC"].pprint()

# Objective
def obj_rule(model):
    return sum(d[n][m]*model.x[n,m] for n in N for m in M)
model.obj = pyo.Objective(rule=obj_rule)

results = solver.solve(model)
# model.x.pprint()