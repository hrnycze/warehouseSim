from astar import *
from warehouse import *
import sys

if __name__ == "__main__":

    for desk_types in range(1, 21):
        for i in range(1,31):
            print(f"{desk_types}/10 {i}/10")

            sim2file = True
            if sim2file:
                f = open("deskTypeStats2.txt", "a")
                print("Start print to file")
            else:
                f = sys.stdout


            N = 400 #number of box in warehouse
            S = 4 #size of warehouse (num_stack)
            order_size = 6

            rnd_state = get_random_state(N,S, max_stack_items=100, num_type=desk_types)
            rnd_order = tuple(np.random.choice([id for stack in rnd_state for id in stack], order_size, replace=False))

            heur_order = heuristic_duplicities_order(rnd_order, rnd_state)

            #h1 = WarehouseHeuristicDuplicities(rnd_state, rnd_order, [],False,True,200)
            #h2 = WarehouseHeuristicDuplicities2(rnd_state, rnd_order, [],False,True,200)
            h3 = WarehouseHeuristicDuplicities3(rnd_state, rnd_order, [],False,True,200)

            
            astar = AStar(1)
            timeout = 120

            heuristics = [h3]
            stats = []
            for h in heuristics:
                Warehouse.expanded = 0 # dont forgot reset stats

                start_t = time.time()
                path = astar.search(h, start_t, timeout)
                end_t = time.time()
                elapsed_t = end_t - start_t

                if path is not None:
                    stats.append([len(path), Warehouse.expanded, elapsed_t, path])
                else:
                    stats.append(None)
            
                # print(f"{order_size} : {rnd_order}", end="", file=f)
                # if path is not None:
                #     print(f" & {len(path)} & {Warehouse.expanded} ({elapsed_t:.3f}s) & {path} & {[a.tolist() for a in h.state]}", file=f)
                # else:
                #     print(f" & Timeout ({elapsed_t:.3f} > {timeout:.3f})",file=f)

            #print(f"{order_size} : {rnd_order} & {stats[0][0]} | {stats[1][0]} | {stats[2][0]} & {stats[0][1]} | {stats[1][1]} | {stats[2][1]} \
            #     & {stats[0][2]:.3f} | {stats[1][2]:.3f} | {stats[2][2]:.3f}", file=f)
            
            print(f"{desk_types} & {rnd_order}", end="", file=f)
            for sid in range(4):
                for hid in range(len(heuristics)):
                    if stats[hid] == None: 
                        print(f" & Timeout {timeout}s", end="", file=f)
                    else:
                        if sid == 2:
                            print(f" & {stats[hid][sid]:.3f}", end="", file=f)
                        else:
                            print(f" & {stats[hid][sid]}", end="", file=f)
            print(f" & {[a.tolist() for a in rnd_state]}",file=f)

            if sim2file:
                print("End print to file")
                f.close()