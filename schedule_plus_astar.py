import time

import numpy as np
from astar import *
from warehouse import Warehouse, get_random_orders, get_random_state
from ilpScheduleSolver import solve_schedule


if __name__ == "__main__":
	
    N = 15 #number of box in warehouse
    S = 4 #size of warehouse (num_stack)
	
    #order = (2,1) #sequence of box to go out 

    rnd_order = get_random_orders(N,S)
    rnd_state = get_random_state(N,S)

    num_machines = 3
    num_jobs = 8
    all_jobs_process_time = (np.random.rand(num_jobs,1)*np.ones((1,num_machines))).T

    print("Scheduling..")
    batch = solve_schedule(num_machines, num_jobs, all_jobs_process_time,True)
    print(f"Batch: {batch}")

    start = WarehouseHeuristic2(inicial_state=rnd_state, out_order=tuple(reversed(batch)),in_order=[])
	#start = WarehouseWithoutHeuristic(N,S, rnd_order, rnd_state)

    print(f"Searching path: {start} -> for order {start.get_goal_output()}")

    astar = AStar(weigth=1)

    start_t = time.time()
    path = astar.search(start)
    end_t = time.time()
    elapsed_t = end_t - start_t

    if path is not None:
        print(f"Found a path (length={len(path)}): ")
        print(path)
	
        print("How it goes: ")  
        s = start.clone()
        print(s)
        for a in path:
            s.move(a)
            #print(s)
            s.visualization()    
    else:
        print("NO PATH exists.")
	
    print(f"Total expanded nodes: {Warehouse.expanded} Time: {elapsed_t:.2f}")
    if path is not None:
        print(f"Found a path (length={len(path)}): ")