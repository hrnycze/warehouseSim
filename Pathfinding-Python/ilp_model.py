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
    
    makespan = solver.Var(0, horizont, True, "makespan")
    #makespan = solver.Var(0, sum(data['processingTime'])/3, False, "makespan")


    ## defined constrains
    for t in all_tasks:
        onlyOneTaskOnOneMachine_expr = sum([ x[(t,m)] for m in all_machines ])
        solver.Add(onlyOneTaskOnOneMachine_expr == 1)

    for t in all_tasks:
        solver.Add(s[t] + data['processingTime'][t] <= makespan)
        solver.Add(s[t] + data['processingTime'][t] <= data['deadline'][t])

    for m in all_machines:
        solver.Add(sum((data['processingTime'][t]*x[(t,m)]) for t in all_tasks) <= makespan)

    #overlaping
    M = 1000 #some big number
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
        
        taskOnMachineId = -20*np.ones(data['numTasks'])
        for t in all_tasks:
            for m in all_machines:
                if x[(t,m)].solution_value() == 1:
                    taskOnMachineId[t] = m
                    break
        print(f"taskOnMachineID: {taskOnMachineId}")
        print(delta.values())
        print([xx.solution_value() for xx in delta.values()])

        # Gantt-Chart
        plt.rc('font',**{'family':'Cambria'})
        plt.rcParams['font.size'] = 13
        fig, ax = plt.subplots()
        ax.set_title('Optimální rozvrch výroby', fontsize=15)
        ax.set_xlabel("Čas [min]")
        ax.set_ylabel("Číslo stroje")
        id = []
        ss = []
        p = []
        m = []
        for tID,mID in enumerate(taskOnMachineId):
            #ax.broken_barh(xranges=[(s[tID].solution_value(), data['processingTime'][tID])], yrange=(mID, 0.5))
            id.append(tID)
            ss.append(s[tID].solution_value())
            p.append(data['processingTime'][tID])
            m.append(mID)
            if (tID+1) % 3 == 0:
                rect = ax.barh(y=m, width=p, height=0.5, left=ss, edgecolor= "black")
                ax.bar_label(rect, id, label_type="center", color="white")
                id = []
                ss = []
                p = []
                m = []
            # color = 'b'
            # for deadColor in data["color"]:
            #     if str(data["deadline"][tID]) in deadColor:
            #         color = data["color"][deadColor]
            #         break
            # rect = ax.barh(y=mID, width=data['processingTime'][tID], height=0.5, left=s[tID].solution_value(), label = tID, edgecolor= "black", color=color)
            # ax.bar_label(rect, [tID+1], label_type="center", color="white")

        #legend
        patches = []
        for deadline in data["color"]:
            patches.append(matplotlib.patches.Patch(color=data["color"][deadline]))
        ax.legend(handles=patches, labels=data["color"].keys(), fontsize=11)

        plt.gca().invert_yaxis()

        # Marking the makespan
        ax.axvline(x=solver.Objective().Value(), color='r', linestyle='dashed')
        #ax.text(x=solver.Objective().Value()-1, y=0.5, s='C_max', color='r')

        ax.xaxis.grid(True, alpha=0.25)
        ax.set_yticks(all_machines)
        ax.set_yticklabels(range(1, data['numMachines']+1))
        plt.show()

    elif status == pywraplp.Solver.INFEASIBLE:
        print("INFEASIBLE")
    elif status == pywraplp.Solver.FEASIBLE:
        print("FEASIBLE")

    return True

def create_deadline(windowSize, numTasks):
    line = windowSize
    deadlines = []
    for i in range(1, numTasks+1):
        deadlines.append(line)
        if i % 3 == 0:
            line = line + windowSize

    return deadlines

def deadlineFromProccesingTime(ptimes):
    deadlines = []
    prevMax = 0
    max = 0
    for i,t in enumerate(ptimes):
        max = np.max([max,t])
        if (i+1)%3 == 0:
            for ii in range(3):
                deadlines.append(prevMax + max)
            prevMax = prevMax + max
            max = 0
    return deadlines


def create_data():
    numTasks = 10

    # deadlines = create_deadline(3, numTasks)
    # print(deadlines) 
    data = {}
    data['processingTime'] = np.random.randint(10, 15, size=(1, numTasks)).tolist()[0]#[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2] #np.random.randint(2, 10, size=(1, 200)).tolist()[0]#[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2]#[3, 2, 1, 3, 3, 2, 1, 1, 1]
    d = deadlineFromProccesingTime(data['processingTime'])
    print(data['processingTime'])
    print(d)
    data['deadline'] = d #[6, 6, 6,  12, 12, 12, 18,18,18,24,24,24]#[ 9, 9, 9, 6, 6, 6,  12, 12, 12, 3, 3, 3, 15, 15, 15]
    #data['color'] = {"deadline=6":'c',"deadline=12":'g',  "deadline=18":'m', "deadline=24":'y'}

    #data['processingTime'] = [2, 3, 2, 3, 3, 2, 1, 2, 3, 3, 3, 3]#, 5, 4, 3, 4, 1, 2]#np.random.randint(2, 10, size=(1, 200)).tolist()[0]#[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2]#[3, 2, 1, 3, 3, 2, 1, 1, 1]
    #data['deadline'] = [ 9, 9, 9, 6, 6, 6,  12, 12, 12, 3, 3, 3]#, 15, 15, 15]
    data['color'] = {"deadline=3":'c', "deadline=6":'y', "deadline=9":'m', "deadline=12":'g'}
    data['numMachines'] = 3
    data['numTasks'] = len(data['processingTime'])

    return data

if __name__ == "__main__":
    data = create_data()
    #print(list(data['color'].values()))
    solve(data)