import time

import numpy as np
from astar import AStar, WarehouseHeuristic
from warehouse import Warehouse, get_random_orders, get_random_state
from mipScheduleSolver import solve_schedule


if __name__ == "__main__":
	
    N = 100 #number of box in warehouse
    S = 4 #size of warehouse (num_stack)
	
    #order = (2,1) #sequence of box to go out 

    rnd_order = get_random_orders(N,S)
    rnd_state = get_random_state(N,S)

    num_machines = 3
    num_jobs = 5
    all_jobs_process_time = (np.random.rand(num_jobs,1)*np.ones((1,num_machines))).T

    print("Scheduling..")
    batch = solve_schedule(num_machines, num_jobs, all_jobs_process_time,True)
    print(f"Batch: {batch}")

    start = WarehouseHeuristic(N,S, order=tuple(reversed(batch)), start_state=rnd_state)
	#start = WarehouseWithoutHeuristic(N,S, rnd_order, rnd_state)

    print(f"Searching path: {start} -> for order {start.get_goal_out()}")

    astar = AStar(weigth=1.1)

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
            s.apply(a)
            print(s)    
    else:
        print("NO PATH exists.")
	
    print(f"Total expanded nodes: {Warehouse.expanded} Time: {elapsed_t:.2f}")
    if path is not None:
        print(f"Found a path (length={len(path)}): ")