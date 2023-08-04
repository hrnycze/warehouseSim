"""ILP model for scheduling parallel machine"""

import matplotlib
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

    horizont = sum(data['processingTime'])
    ## declared variables

    x = {}
    for t in all_tasks:
        for m in all_machines:
            x[(t,m)] = solver.IntVar(0,1,f"x_{t}-{m}")
    
    s = {}
    for t in all_tasks:
        s[t] = solver.Var(0,horizont,True, f"s_{t}")

    delta = {}
    for i in all_tasks:
        for j in all_tasks:
            if i == j:
                continue
            delta[(i,j)] = solver.IntVar(0,1, f"delta_{i}_{j}")
    
    makespan = solver.Var(0, horizont, False, "makespan")
    #makespan = solver.Var(0, sum(data['processingTime'])/3, False, "makespan")


    ## defined constrains
    for t in all_tasks:
        onlyOneTaskOnOneMachine_expr = sum([ x[(t,m)] for m in all_machines ])
        solver.Add(onlyOneTaskOnOneMachine_expr == 1)

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
                t1OnM_expr = x[(t1,m)]
                t2OnM_expr = x[(t2,m)]
                solver.Add(s[t1] + data['processingTime'][t1] <= s[t2] + M * (3 - t1OnM_expr - t2OnM_expr - delta[(t1,t2)]))
                

    #precence constrain: delta_i_j is 1 if task i before j, otherwise 0
    for i in all_tasks:
        for j in all_tasks:
            if i == j:
                continue
            solver.Add(delta[(i,j)] + delta[(j,i)] == 1)


    ## cost function
    solver.Minimize(makespan)

    print(f"Number of variables: {solver.NumVariables()}")
    print(f"Number of constrains: {solver.NumConstraints()}")
    #print(solver.ExportModelAsLpFormat(False))

    #solver.SetNumThreads(4)
    status = solver.Solve()

    print('================= Solution =================')
    if status == pywraplp.Solver.OPTIMAL:
        print(f'Solved in {(solver.wall_time()/1000):.2f} seconds in {solver.iterations()} iterations')
        print(f"Makespan = {solver.Objective().Value()}")
        for t in all_tasks:
            print(f"{s[t].solution_value()}+{data['processingTime'][t]} = {s[t].solution_value()+data['processingTime'][t]}")
        print(x.values())
        print([xx.solution_value() for xx in x.values()])
        count = 0
        for xx in x.values():
            print(xx.solution_value(), end=", ")
            count+=1
            if count % (data['numMachines']) == 0:
                print()
        
        # taskOnMachineId = -20*np.ones(data['numTasks'])
        # nextTask = False
        # for t in all_tasks:
        #     for i in all_intervals:
        #         if nextTask:
        #             nextTask = False
        #             break
        #         for m in all_machines:
        #             if x[(t,m,i)].solution_value() == 1:
        #                 taskOnMachineId[t] = m
        #                 if i != all_intervals[-1]:
        #                     nextTask = True
        #                 break
        # print(f"taskOnMachineID: {taskOnMachineId}")
        # print(delta.values())
        # print([xx.solution_value() for xx in delta.values()])

        # # Gantt-Chart
        # plt.rc('font',**{'family':'Cambria'})
        # plt.rcParams['font.size'] = 13
        # fig, ax = plt.subplots()
        # ax.set_title('Optimální rozvrch výroby', fontsize=15)
        # ax.set_xlabel("Čas")
        # ax.set_ylabel("Číslo stroje")
        # for tID,mID in enumerate(taskOnMachineId):
        #     #ax.broken_barh(xranges=[(s[tID].solution_value(), data['processingTime'][tID])], yrange=(mID, 0.5))
        #     color = 'b'
        #     for deadColor in data["color"]:
        #         if str(data["deadline"][tID]) in deadColor:
        #             color = data["color"][deadColor]
        #             break
        #     rect = ax.barh(y=mID, width=data['processingTime'][tID], height=0.5, left=s[tID].solution_value(), label = tID, edgecolor= "black", color=color)
        #     ax.bar_label(rect, [tID+1], label_type="center", color="white")

        # #legend
        # patches = []
        # for deadline in data["color"]:
        #     patches.append(matplotlib.patches.Patch(color=data["color"][deadline]))
        # ax.legend(handles=patches, labels=data["color"].keys(), fontsize=11)

        # plt.gca().invert_yaxis()

        # # Marking the makespan
        # ax.axvline(x=solver.Objective().Value(), color='r', linestyle='dashed')
        # ax.text(x=solver.Objective().Value()-1, y=0.5, s='C_max', color='r')

        # ax.xaxis.grid(True, alpha=0.25)
        # ax.set_yticks(all_machines)
        # ax.set_yticklabels(range(1, data['numMachines']+1))
        # plt.show()

    elif status == pywraplp.Solver.INFEASIBLE:
        print("INFEASIBLE")
    elif status == pywraplp.Solver.FEASIBLE:
        print("FEASIBLE")

    return True

def create_data():
    data = {}
    data['processingTime'] = [2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3]#, 5, 4, 3, 4, 1, 2]#np.random.randint(2, 10, size=(1, 200)).tolist()[0]#[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2]#[3, 2, 1, 3, 3, 2, 1, 1, 1]
    data['deadline'] = [ 3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12]#, 15, 15, 15]
    data['color'] = {"deadline=3":'c', "deadline=6":'y', "deadline=9":'m'}
    data['numMachines'] = 3
    data['numTasks'] = len(data['processingTime'])

    return data

if __name__ == "__main__":
    data = create_data()
    print(list(data['color'].values()))
    solve(create_data())