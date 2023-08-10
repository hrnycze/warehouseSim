from ortools.sat.python import cp_model
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

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
    
    ## overlaping
    for m in all_machines:
        for t1 in all_tasks:
            for t2 in all_tasks:
                if t1 == t2:
                    continue
                model.Add(starts[t1] + data['processingTime'][t1] <= starts[t2]).OnlyEnforceIf([x[(t1,m)],x[(t2,m)], delta[(t1,t2)]])

    for t in all_tasks:
        model.Add(starts[t] + data['processingTime'][t] <= data['deadline'][t] )          

    for m in all_machines:
        model.Add(sum((data['processingTime'][t]*x[(t,m)]) for t in all_tasks) <= makespan)
    
    model.AddMaxEquality(makespan, [starts[t] + data['processingTime'][t] for t in all_tasks])

    model.Minimize(makespan)

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4  # use 8 cores
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print("Solution found:")
        print(f'Optimal Schedule Makespan: {solver.ObjectiveValue()}')
        print([xx for xx in x])
        print([solver.Value(x[xx]) for xx in x])
        print("start time:")
        print([solver.Value(s) for s in starts])
        print("end time:")
        print([solver.Value(s) for s in ends])

        taskOnMachineId = -20*np.ones(data['numTasks'])
        for t in all_tasks:
            for m in all_machines:
                if solver.Value(x[(t,m)]) == 1:
                    taskOnMachineId[t] = m
                    break
        print(f"taskOnMachineID: {taskOnMachineId}")

        # Gantt-Chart
        plt.rc('font',**{'family':'Cambria'})
        plt.rcParams['font.size'] = 13
        fig, ax = plt.subplots()
        ax.set_title('Optimální rozvrch výroby', fontsize=15)
        ax.set_xlabel("Čas [min]")
        ax.set_ylabel("Číslo stroje")

        id = []
        s = []
        p = []
        m = []
        for tID,mID in enumerate(taskOnMachineId):
            #ax.broken_barh(xranges=[(s[tID].solution_value(), data['processingTime'][tID])], yrange=(mID, 0.5))
            id.append(tID)
            s.append(solver.Value(starts[tID]))
            p.append(data['processingTime'][tID])
            m.append(mID)
            if (tID+1) % 3 == 0:
                rect = ax.barh(y=m, width=p, height=0.5, left=s, edgecolor= "black")
                ax.bar_label(rect, id, label_type="center", color="white")
                id = []
                s = []
                p = []
                m = []
            # color = 'b'
            # for deadColor in data["color"]:
            #     if str(data["deadline"][tID]) in deadColor:
            #         color = data["color"][deadColor]
            #         break
            # rect = ax.barh(y=mID, width=data['processingTime'][tID], height=0.5, left=solver.Value(starts[tID]), label = tID, edgecolor= "black")#, color=color)
            # ax.bar_label(rect, [tID+1], label_type="center", color="white")

        #legend
        patches = []
        for deadline in data["color"]:
            patches.append(matplotlib.patches.Patch(color=data["color"][deadline]))
        ax.legend(handles=patches, labels=data["color"].keys(), fontsize=11)

        plt.gca().invert_yaxis()

        # Marking the makespan
        ax.axvline(x=solver.ObjectiveValue(), color='r', linestyle='dashed')
        #ax.text(x=solver.Objective().Value()-1, y=0.5, s='C_max', color='r')

        ax.xaxis.grid(True, alpha=0.25)
        ax.set_yticks(all_machines)
        ax.set_yticklabels(range(1, data['numMachines']+1))
        plt.show()
    else:
        print("There is nothing :[")

    # Statistics.
    print('\nStatistics')
    print('  - conflicts: %i' % solver.NumConflicts())
    print('  - branches : %i' % solver.NumBranches())
    print('  - wall time: %f s' % solver.WallTime())
    print(solver.SolutionInfo())



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
    numTasks = 240

    # deadlines = create_deadline(15, numTasks)
    # print(deadlines) 
    data = {}
    data['processingTime'] = np.random.randint(3, 15, size=(1, numTasks)).tolist()[0]#[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2] #np.random.randint(2, 10, size=(1, 200)).tolist()[0]#[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2]#[3, 2, 1, 3, 3, 2, 1, 1, 1]
    d = deadlineFromProccesingTime(data['processingTime'])
    print(data['processingTime'])
    print(d)
    data['deadline'] = d #[6, 6, 6,  12, 12, 12, 18,18,18,24,24,24]#[ 9, 9, 9, 6, 6, 6,  12, 12, 12, 3, 3, 3, 15, 15, 15]
    data['color'] = {"deadline=3":'c', "deadline=6":'y', "deadline=9":'m', "deadline=12":'g'}#{"deadline=6":'c',"deadline=12":'g',  "deadline=18":'m', "deadline=24":'y'}#{"deadline=3":'c', "deadline=6":'y', "deadline=9":'m', "deadline=12":'g'}
    data['numMachines'] = 3
    data['numTasks'] = len(data['processingTime'])

    return data

if __name__ == "__main__":
    data = create_data()
    #print(list(data['color'].values()))
    solve(data)