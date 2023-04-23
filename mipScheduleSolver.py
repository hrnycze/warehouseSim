"""Minimalization makespan of warehouse"""
#from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp
import numpy as np
import matplotlib.pyplot as plt

def solve_schedule(num_machines, num_jobs, all_jobs_process_time, showResult = False):
    solver = pywraplp.Solver("Min. makespan", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    all_machines = range(num_machines)
    all_jobs = range(num_jobs)
    #assigned variable
    jobs = {}
    for j in all_jobs:
        for m in all_machines:
            jobs[(j,m)] = solver.IntVar(0,1,f'job_{j}-{m}')

    #each job is assigned to only single machine
    for j in all_jobs:
        solver.Add(sum(jobs[(j,m)] for m in all_machines) == 1)

    makespan = solver.Var(0, solver.infinity(), False, "makespan")

    for m in all_machines:
        solver.Add(sum((all_jobs_process_time[m,j]*jobs[(j,m)]) for j in all_jobs) <= makespan)

    solver.Minimize(makespan)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        processVal = np.zeros_like(all_jobs_process_time)
        for m in all_machines:
            for j in all_jobs:
                val = jobs[(j,m)].solution_value()
                processVal[m,j] = val
                #print(f"{val}", end=" ")
            #print()
        if showResult:
            print('================= Solution =================')
            print(f'Solved in {solver.wall_time():.2f} milliseconds in {solver.iterations()} iterations')
            print()
            print(f'Optimal makespan = {solver.Objective().Value()} time')
            print("Assign job to machines:")
            print(processVal)
        maxlen = int(max(processVal.sum(axis=1)).item(0))
        #print(maxlen)
        optimSchedule = np.zeros((num_machines, maxlen))
        jobTime = np.zeros((num_machines, maxlen))
        for m in all_machines:
            schedule_m = np.nonzero(processVal[m,:])[0]
            optimSchedule[m,0:schedule_m.size] = schedule_m
            jobTime[m,0:schedule_m.size] = all_jobs_process_time[m,schedule_m]
        #print(all_jobs_process_time)
        optimSchedule = optimSchedule.astype(int)
        #print(optimSchedule)
        #print(jobTime)

        cumsumTime = np.cumsum(jobTime, axis=1)
        starts = (cumsumTime - jobTime)
        batch = create_batch(optimSchedule, starts)

        if showResult:
            print("Batch:")        
            print(batch)
            #plot result into Gant-Chart
            fig, ax = plt.subplots()
            ax.set_title("Optimal schedule")
            ax.set_xlabel("Time")
            ax.set_ylabel("Machine's number")
            ax.yaxis.set_ticks(all_machines)
            #print(cumsumTime)
            #print(starts)
            for i in range(maxlen):
                rect = ax.barh(all_machines,jobTime[:,i],height=0.5,left=starts[:,i], label=i)
                ax.bar_label(rect, optimSchedule[:,i], label_type="center", color="white")
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
    num_jobs = 11
    all_jobs_process_time = (np.random.rand(num_jobs,1)*np.ones((1,num_machines))).T
    
    print("Scheduling..")
    solve_schedule(num_machines, num_jobs, all_jobs_process_time,True)
