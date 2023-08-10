from matplotlib import pyplot as plt
from ortools.sat.python import cp_model
import numpy as np

def solve_schedule(machinesNums, tasksNums, process_times, showResult = False):
    model = cp_model.CpModel()

    horizont = np.max([np.sum(times[0,:]) for times in process_times])

    makespan = model.NewIntVar(0, int(horizont), "makespan")

    tasksOnMachine = []
    for num_machines, num_tasks, all_tasks_process_time in zip(machinesNums, tasksNums, process_times):
        all_machines = range(num_machines)
        all_tasks = range(num_tasks)

        tasks = {}
        for t in all_tasks:
            for m in all_machines:
                tasks[(t,m)] = model.NewBoolVar(f'task_{t}-{m}[typeCount {num_machines}]')
        tasksOnMachine.append(tasks)

        for t in all_tasks:
            model.AddExactlyOne([tasks[(t,m)] for m in all_machines])

        for m in all_machines:
            model.Add(sum((all_tasks_process_time[m,t]*tasks[(t,m)]) for t in all_tasks) <= makespan)

    model.Minimize(makespan)
    solver = cp_model.CpSolver()
    #solver.parameters.num_search_workers = 4
    

    print("Scheduling CP..")
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print("Solution found:")
        print(f"Solved in {solver.WallTime():.3f} seconds. Branches: {solver.NumBranches()}. Conflicts: {solver.NumConflicts()}")
        print(f'Optimal Schedule Makespan: {solver.ObjectiveValue()}')
        
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
                    val = solver.Value(tasks[(t,m)])
                    processVal[m,t] = val
            if showResult:
                print()
                print(f"Assign task to machines {typeMachineID}:")
                print(processVal)

        # for tasks in tasksOnMachine:
        #     print([xx for xx in tasks])
        #     print([solver.Value(tasks[xx]) for xx in tasks])
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
            # batch = create_batch(optimSchedule, starts)


            if showResult:
                # print("Batch:")        
                # print(batch)
                #plot result into Gant-Chart
                # Gantt-Chart
                axs[typeMachineID-1].set_xlabel("Čas [min]")
                axs[typeMachineID-1].set_ylabel(f"Stroje typu {typeMachineID}")
                #print(cumsumTime)
                #print(starts)
                for i in range(maxlen):
                    rect = axs[typeMachineID-1].barh(all_machines,taskTime[:,i],height=0.5,left=starts[:,i], label=i, edgecolor= "black")
                    axs[typeMachineID-1].bar_label(rect, optimSchedule[:,i] + 1, label_type="center", color="white")

                # Marking the makespan
                axs[typeMachineID-1].axvline(x=solver.ObjectiveValue(), color='r', linestyle='dashed')
                #axs[typeMachineID-1].text(x=solver.Objective().Value()-2, y=0.5, s='C_max', color='r')

                axs[typeMachineID-1].set_xlim(0, solver.ObjectiveValue()+2)
                axs[typeMachineID-1].xaxis.grid(True, alpha=0.25)
                axs[typeMachineID-1].set_yticks(all_machines)
                axs[typeMachineID-1].set_yticklabels(range(1, num_machines+1))
                axs[typeMachineID-1].invert_yaxis()

        if showResult:
            plt.show()

        # return batch


    else:
        print("There is nothing :[")

if __name__ == "__main__":
    num_machines = [4, 4]
    num_tasks = [820, 880, 540, 500]
    #all_jobs_process_time = (np.random.rand(num_jobs,1)*np.ones((1,num_machines))).T
    #all_jobs_process_time = (np.array([[2, 3, 2, 2, 3, 2, 1, 2, 3, 5, 4, 3, 4, 1, 2]]).T*np.ones((1,num_machines))).T
    all_tasks_process_time = []
    for tasks, machines in zip(num_tasks, num_machines):
        process_times = (np.random.randint(3, 15, size=(tasks, 1))*np.ones((1,machines), dtype=np.int32)).T
        all_tasks_process_time.append(process_times)
        #print(process_times)

    
    solve_schedule(num_machines, num_tasks, all_tasks_process_time,True)