from ortools.sat.python import cp_model
import numpy as np

def solve(data):
    model = cp_model.CpModel()

    all_machines = range(data['numMachines'])
    all_tasks = range(data['numTasks'])

    horizont = sum(data['processingTime'])

    makespan = model.NewIntVar(0, horizont, "makespan")
    x = {}
    intervals = []
    starts = []
    ends = []
    for t in all_tasks:
        for m in all_machines:
            x[(t,m)] = model.NewBoolVar(f"x_{t}-{m}")
        start_var = model.NewIntVar(0,horizont, f"start_{t}")
        end_var = model.NewIntVar(0,horizont, f"end_{t}")
        interval_var = model.NewIntervalVar(start_var, data['processingTime'][t], end_var, f"interval_{t}")
        intervals.append(interval_var)
        ends.append(end_var)
        starts.append(start_var)
    
    #precence variable: delta_i_j is 1 if task i before j, otherwise 0
    delta = {}
    for i in all_tasks:
        for j in all_tasks:
            if i == j:
                continue
            delta[(i, j)] = model.NewBoolVar(f"delta_{i}-{j}")
    for i in all_tasks:
        for j in all_tasks:
            if i == j:
                continue
            #model.Add(delta[(i,j)] == delta[(j,i)].Not())
            model.AddAllDifferent(delta[(i,j)], delta[(j,i)])

    ## defined constrains
    for t in all_tasks:
        model.AddExactlyOne([ x[(t,m)] for m in all_machines ])
    
    for m in all_machines:
        for t1 in all_tasks:
            for t2 in all_tasks:
                if t1 == t2:
                    continue
                model.Add(starts[t1] + data['processingTime'][t1] <= starts[t2]).OnlyEnforceIf([x[(t1,m)],x[(t2,m)], delta[(t1,t2)]])

    # for t in all_tasks:
    #     #model.Add(starts[t] + data['processingTime'][t] <= ends[t] )
    #     model.Add(ends[t] <= data['deadline'][t])            
    
    model.AddMaxEquality(makespan, [starts[t] + data['processingTime'][t] for t in all_tasks])

    model.Minimize(makespan)

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4  # use 8 cores
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution found:")
        print(f'Optimal Schedule Makespan: {solver.ObjectiveValue()}')
        print([xx for xx in x])
        print([solver.Value(x[xx]) for xx in x])
        print("start time:")
        print([solver.Value(s) for s in starts])
        print("end time:")
        print([solver.Value(s) for s in ends])

    else:
        print("There is nothing :[")

    # Statistics.
    print('\nStatistics')
    print('  - conflicts: %i' % solver.NumConflicts())
    print('  - branches : %i' % solver.NumBranches())
    print('  - wall time: %f s' % solver.WallTime())
    print(solver.SolutionInfo())

def generuj_posloupnost(velikost):
    posloupnost = []
    for i in range(1, velikost+1):
        hodnota = (i // 3) * 3 + 3
        for j in range(3):
            posloupnost.append(hodnota)
    return posloupnost[:velikost]


def create_data():
    velikost_posloupnosti = 20
    vysledek = generuj_posloupnost(velikost_posloupnosti)
    print(str(vysledek) + str(len(vysledek)))
    data = {}
    data['processingTime'] = np.random.randint(1, 2, size=(1, 10)).tolist()[0]#[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2] #np.random.randint(2, 10, size=(1, 200)).tolist()[0]#[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2]#[3, 2, 1, 3, 3, 2, 1, 1, 1]
    data['deadline'] = vysledek  #[ 3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 15, 15, 15]
    data['color'] = {"deadline=3":'c', "deadline=6":'y', "deadline=9":'m'}
    data['numMachines'] = 3
    data['numTasks'] = len(data['processingTime'])

    return data

if __name__ == "__main__":
    data = create_data()
    #print(list(data['color'].values()))
    solve(data)