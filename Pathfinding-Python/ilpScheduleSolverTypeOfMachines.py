"""Minimalization makespan of warehouse"""

from ortools.linear_solver import pywraplp
import numpy as np
import matplotlib.pyplot as plt

def solve_schedule(machinesNums, tasksNums, process_times, showResult = False):
    solver = pywraplp.Solver("Makespan Minimalizaion", pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)


    makespan = solver.Var(0, solver.infinity(), False, "makespan")

    
    tasksOnMachine = [] 
    for num_machines, num_tasks, all_tasks_process_time in zip(machinesNums, tasksNums, process_times):
        all_machines = range(num_machines)
        all_tasks = range(num_tasks)

        #assigned variables
        tasks = {}
        for t in all_tasks:
            for m in all_machines:
                tasks[(t,m)] = solver.IntVar(0,1,f'task_{t}-{m}[typeCount {num_machines}]')

        tasksOnMachine.append(tasks)

        #each job is assigned to only single machine
        for t in all_tasks:
            solver.Add(sum(tasks[(t,m)] for m in all_machines) == 1)


        for m in all_machines:
            solver.Add(sum((all_tasks_process_time[m,t]*tasks[(t,m)]) for t in all_tasks) <= makespan)

    print(f"Number of variables: {solver.NumVariables()}")
    print(f"Number of constrains: {solver.NumConstraints()}")
    #print(solver.ExportModelAsLpFormat(False))

    solver.Minimize(makespan)

    print("Scheduling ILP..")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('================= Solution =================')
        print(f'Solved in {solver.wall_time()/1000:.3f} seconds in {solver.iterations()} iterations')
        print(f'Optimal makespan = {solver.Objective().Value()} time')

        plt.rc('font',**{'family':'Cambria'})
        plt.rcParams['font.size'] = 13
        fig, axs = plt.subplots(len(machinesNums))
        #plt.gca().invert_yaxis()
        axs[0].set_title('Optimální rozvrch výroby', fontsize=15)

        typeMachineID = 0
        for num_machines, num_tasks, all_tasks_process_time in zip(machinesNums, tasksNums, process_times):
            tasks = tasksOnMachine[typeMachineID]
            typeMachineID += 1

            all_machines = range(num_machines)
            all_tasks = range(num_tasks)
            processVal = np.zeros_like(all_tasks_process_time)
            for m in all_machines:
                for t in all_tasks:
                    val = tasks[(t,m)].solution_value()
                    processVal[m,t] = val
                    #print(f"{val}", end=" ")
                #print()
            if showResult:
                print()
                print(f"Assign task to machines {typeMachineID}:")
                print(processVal)
        
            maxlen = int(max(processVal.sum(axis=1)).item(0))
            #print(maxlen)
            optimSchedule = np.zeros((num_machines, maxlen))
            taskTime = np.zeros((num_machines, maxlen))
            for m in all_machines:
                schedule_m = np.nonzero(processVal[m,:])[0]
                optimSchedule[m,0:schedule_m.size] = schedule_m
                taskTime[m,0:schedule_m.size] = all_tasks_process_time[m,schedule_m]
            #print(all_jobs_process_time)
            optimSchedule = optimSchedule.astype(int)
            #print(optimSchedule)
            #print(jobTime)

            cumsumTime = np.cumsum(taskTime, axis=1)
            starts = (cumsumTime - taskTime)


            if showResult:
                #plot result into Gant-Chart
                # Gantt-Chart
                axs[typeMachineID-1].set_xlabel("Čas [min]")
                axs[typeMachineID-1].set_ylabel(f"Stroje typu {typeMachineID}")
                #print(cumsumTime)
                #print(starts)
                for i in range(maxlen):
                    rect = axs[typeMachineID-1].barh(all_machines,taskTime[:,i],height=0.5,left=starts[:,i], label=i, edgecolor= "black")
                    #axs[typeMachineID-1].bar_label(rect, optimSchedule[:,i] + 1, label_type="center", color="white")

                # Marking the makespan
                axs[typeMachineID-1].axvline(x=solver.Objective().Value(), color='r', linestyle='dashed')
                #axs[typeMachineID-1].text(x=solver.Objective().Value()-2, y=0.5, s='C_max', color='r')

                axs[typeMachineID-1].set_xlim(0, solver.Objective().Value()+2)
                axs[typeMachineID-1].xaxis.grid(True, alpha=0.25)
                axs[typeMachineID-1].set_yticks(all_machines)
                axs[typeMachineID-1].set_yticklabels(range(1, num_machines+1))
                axs[typeMachineID-1].invert_yaxis()

       
        if showResult:
            plt.show()

        
    else:
        print('The solver could not find an optimal solution.')
        return None

    

if __name__ == "__main__":
    num_machines = [2, 3]
    num_tasks = [160, 240]
    #all_jobs_process_time = (np.random.rand(num_jobs,1)*np.ones((1,num_machines))).T
    #all_jobs_process_time = (np.array([[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2]]).T*np.ones((1,num_machines))).T
    all_tasks_process_time = []
    for tasks, machines in zip(num_tasks, num_machines):
        all_tasks_process_time.append((np.random.randint(3, 15, size=(tasks, 1))*np.ones((1,machines))).T )
    
    solve_schedule(num_machines, num_tasks, all_tasks_process_time,True)
