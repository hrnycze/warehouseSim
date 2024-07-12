import sys
import time
import numpy as np
from warehouse import Warehouse
from astar import WarehouseHeuristicDuplicities3, AStar

def process_input_string(input_string):
    # Split the input string by ', ' followed by '['
    list_strings = input_string.split('], [')
    
    # Clean up the split strings and add brackets
    list_strings = [s if s.startswith('[') else '[' + s for s in list_strings]
    list_strings = [s if s.endswith(']') else s + ']' for s in list_strings]

    out_list = [np.array(eval(l)) for l in list_strings]

    return out_list

def main():
    #print("Pathfinding...")
    argv = sys.argv
    if len(argv) != 4:
        print("Wrong number of arrgs!")
        print("Format: PathfindingCallback.py 'inner_state' 'in_order' 'out_order' ")
        sys.exit(101)

    #print(f"s:{argv[1]} i:{argv[2]} o:{argv[3]}")

    warehouse_inner_state_string = argv[1] # "[6, 5], [2], [7, 3, 5], [5, 8, 1, 9, 3, 3, 1, 5]"
    warehouse_inner_state = process_input_string(warehouse_inner_state_string)
    warehouse_in_order_str = tuple(eval(argv[2])) # "[1,2,3]"
    warehouse_out_order_str = tuple(eval(argv[3])) # "[3,5,6]"

    state = WarehouseHeuristicDuplicities3(warehouse_inner_state,
                                           warehouse_out_order_str, 
                                           warehouse_in_order_str,
                                           isInputProccesed=True,
                                           isOutputProccesed=True,
                                           max_stack_items=150)
    
    #state.visualization()

    astar = AStar(weigth=1.3)

    start_t = time.time()
    path = astar.search(state)
    end_t = time.time()
    elapsed_t = end_t - start_t

    if path is not None:
        # print(f"Found a path (length={len(path)}): ")
        # print(path)
        
        # print("How it goes: ")

        s = state.clone()
        # print(s)
        # s.visualization()
        for a in path:
            s.move(a)
            #print(s)
            # print(f"------------ Action: {a} ----------")
            # s.visualization() 
        # print(s) 
        
        #stdout
        print(path)  
    else:
        print("ERRNO(102): NO PATH exists.")
        exit(102)
    # print(f"Found a path (length={len(path)}): ")
    # print(f"Total expanded nodes: {Warehouse.expanded} Time: {elapsed_t:.2f}")

    


if __name__ == "__main__":
    main()