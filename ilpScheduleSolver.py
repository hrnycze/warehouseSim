"""Minimalization makespan of warehouse"""

from ortools.linear_solver import pywraplp
import numpy as np
import matplotlib.pyplot as plt

def solve_schedule(num_machines, num_tasks, all_jobs_process_time, showResult = False):
    solver = pywraplp.Solver("Makespan Minimalizaion", pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)
    all_machines = range(num_machines)
    all_tasks = range(num_tasks)

    #assigned variables
    tasks = {}
    for t in all_tasks:
        for m in all_machines:
            tasks[(t,m)] = solver.IntVar(0,1,f'task_{t}-{m}')

    #each job is assigned to only single machine
    for t in all_tasks:
        solver.Add(sum(tasks[(t,m)] for m in all_machines) == 1)

    makespan = solver.Var(0, solver.infinity(), False, "makespan")

    for m in all_machines:
        solver.Add(sum((all_jobs_process_time[m,t]*tasks[(t,m)]) for t in all_tasks) <= makespan)

    print(f"Number of variables: {solver.NumVariables()}")
    print(f"Number of constrains: {solver.NumConstraints()}")
    #print(solver.ExportModelAsLpFormat(False))

    solver.Minimize(makespan)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        processVal = np.zeros_like(all_jobs_process_time)
        for m in all_machines:
            for j in all_tasks:
                val = tasks[(j,m)].solution_value()
                processVal[m,j] = val
                #print(f"{val}", end=" ")
            #print()
        if showResult:
            print('================= Solution =================')
            print(f'Solved in {solver.wall_time():.2f} milliseconds in {solver.iterations()} iterations')
            print()
            print(f'Optimal makespan = {solver.Objective().Value()} time')
            print("Assign task to machines:")
            print(processVal)
        maxlen = int(max(processVal.sum(axis=1)).item(0))
        #print(maxlen)
        optimSchedule = np.zeros((num_machines, maxlen))
        taskTime = np.zeros((num_machines, maxlen))
        for m in all_machines:
            schedule_m = np.nonzero(processVal[m,:])[0]
            optimSchedule[m,0:schedule_m.size] = schedule_m
            taskTime[m,0:schedule_m.size] = all_jobs_process_time[m,schedule_m]
        #print(all_jobs_process_time)
        optimSchedule = optimSchedule.astype(int)
        #print(optimSchedule)
        #print(jobTime)

        cumsumTime = np.cumsum(taskTime, axis=1)
        starts = (cumsumTime - taskTime)
        batch = create_batch(optimSchedule, starts)


        if showResult:
            print("Batch:")        
            print(batch)
            #plot result into Gant-Chart
            # Gantt-Chart
            plt.rc('font',**{'family':'Cambria'})
            plt.rcParams['font.size'] = 13
            fig, ax = plt.subplots()
            ax.set_title('Optimální rozvrch výroby', fontsize=15)
            ax.set_xlabel("Čas [min]")
            ax.set_ylabel("Číslo stroje")
            #print(cumsumTime)
            #print(starts)
            for i in range(maxlen):
                rect = ax.barh(all_machines,taskTime[:,i],height=0.5,left=starts[:,i], label=i, edgecolor= "black")
                ax.bar_label(rect, optimSchedule[:,i] + 1, label_type="center", color="white")

            # Marking the makespan
            ax.axvline(x=solver.Objective().Value(), color='r', linestyle='dashed')
            ax.text(x=solver.Objective().Value()-2, y=0.5, s='C_max', color='r')

            plt.gca().invert_yaxis()
            ax.set_xlim(0, solver.Objective().Value()+2)
            ax.xaxis.grid(True, alpha=0.25)
            ax.set_yticks(all_machines)
            ax.set_yticklabels(range(1, num_machines+1))
            plt.show()

        return batch
    else:
        print('The solver could not find an optimal solution.')
        return None

def create_batch(optimSchedule, startTime):
    _, col = optimSchedule.shape
    print(optimSchedule)
    bath = []
    subSchedule = optimSchedule[:,0]
    for i in subSchedule:
        bath.append(i+1)
    for c in range(1,col):
        subSchedule = optimSchedule[:,c]
        subTime = startTime[:,c]
        while subSchedule.any(): #is empty
            removeId = np.argmin(subTime)
            if subSchedule[removeId] != 0:
                bath.append(subSchedule[removeId]+1)
            subTime = np.delete(subTime, removeId)
            subSchedule = np.delete(subSchedule, removeId)
    return bath



    

if __name__ == "__main__":
    num_machines = 3
    num_tasks = 10
    #all_jobs_process_time = (np.random.rand(num_jobs,1)*np.ones((1,num_machines))).T
    #all_jobs_process_time = (np.array([[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2]]).T*np.ones((1,num_machines))).T
    all_tasks_process_time = (np.random.randint(3, 15, size=(num_tasks, 1))*np.ones((1,num_machines))).T
    print("Scheduling..")
    solve_schedule(num_machines, num_tasks, all_tasks_process_time,True)
