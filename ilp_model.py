"""ILP model for scheduling parallel machine"""

from ortools.linear_solver import pywraplp
import numpy as np
import matplotlib.pyplot as plt


def solve(data):
    solver = pywraplp.Solver("Min. makespan", pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)
    
    if not solver:
        print("ERROR: creation solver")
        return
    
    all_machines = range(data['numMachines'])
    all_tasks = range(data['numTasks'])
    all_intervals = range(data['numTasks'])


    ## declared variables

    x = {}
    for t in all_tasks:
        for m in all_machines:
            for i in all_intervals:
                x[(t,m,i)] = solver.IntVar(0,1,f"x_{t}-{m}-{i}")
    
    s = {}
    for t in all_tasks:
        s[t] = solver.Var(0,solver.infinity(),False, f"s_{t}")

    delta = {}
    for i in all_tasks:
        for j in all_tasks:
            delta[(i,j)] = solver.IntVar(0,1, f"delta_{i}_{j}")
    
    makespan = solver.Var(0, solver.infinity(), False, "makespan")
    print(f"Number of variables: {solver.NumVariables()}")


    ## defined constrains
    for t in all_tasks:
        onlyOneExecutionOfTask_expr = sum([ sum([ x[(t,m,i)] for i in all_intervals]) for m in all_machines ])
        solver.Add(onlyOneExecutionOfTask_expr == 1)

    for m in all_machines:
        for i in all_intervals:
            onlyOneTaskInIntervalOnOneMachine_expr = sum([ x[(t,m,i)] for t in all_tasks ])
            solver.Add(onlyOneTaskInIntervalOnOneMachine_expr <= 1)

    for t in all_tasks:
        solver.Add(s[t] + data['processingTime'][t] <= makespan)
        solver.Add(s[t] + data['processingTime'][t] <= data['deadline'][t])

    #overlaping
    M = 100 #some big number
    for m in all_machines:
        for t1 in all_tasks:
            for t2 in all_tasks:
                if t1 == t2:
                    continue
                t1OnM_expr = sum([x[(t1,m,i)] for i in all_intervals])
                t2OnM_expr = sum([x[(t2,m,i)] for i in all_intervals])
                solver.Add(s[t1] + data['processingTime'][t1] <= s[t2] + M * (3 - t1OnM_expr - t2OnM_expr - delta[(t1,t2)]))

    #precence constrain: delta_i_j is 1 if task i before j, otherwise 0
    for i in all_tasks:
        for j in all_tasks:
            if i == j:
                continue
            solver.Add(delta[(i,j)] + delta[(j,i)] == 1)


    ## cost function
    solver.Minimize(makespan)

    print(f"Number of constrains: {solver.NumConstraints()}")
    print(solver.ExportModelAsLpFormat(False))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('================= Solution =================')
        print(f'Solved in {(solver.wall_time()/1000):.2f} seconds in {solver.iterations()} iterations')
        print(f"Makespan = {solver.Objective().Value()}")
        for t in all_tasks:
            print(f"{s[t].solution_value()}+{data['processingTime'][t]} = {s[t].solution_value()+data['processingTime'][t]}")
        print(x.values())
        print([xx.solution_value() for xx in x.values()])
        print(delta.values())
        print([xx.solution_value() for xx in delta.values()])
    elif status == pywraplp.Solver.INFEASIBLE:
        print("INFEASIBLE")
    elif status == pywraplp.Solver.FEASIBLE:
        print("FEASIBLE")

    return True

def create_data():
    data = {}
    data['processingTime'] = [2, 2, 3, 5, 6]
    data['deadline'] = [3, 3, 3, 8, 8]
    data['numMachines'] = 3
    data['numTasks'] = len(data['processingTime'])

    return data

if __name__ == "__main__":
    a = [1,2,3]
    b = [4,5,6]

    for i in a:
        for j in b:
            print(f"{i}_{j}")


    solve(create_data())