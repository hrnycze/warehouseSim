import copy, numpy as np

def get_random_orders(num_obj, num_orders, num_from=1):
     obj = np.arange(num_from, num_obj+1)
     return tuple(np.random.choice(obj,num_orders, replace=False))


def get_random_state(num_obj, num_stack, max_stack_items = 100):
     stacks = []
     obj = np.arange(1, num_obj+1)

     while len(obj) > 0:
          stack_len = np.random.randint(1, np.min([len(obj)+1, max_stack_items]))
          stack = np.random.choice(obj, stack_len, replace=False)

          if len(stacks) < num_stack and stack_len <= max_stack_items:
               stacks.append(stack)
          else:
               for o in stack:
                    rand_stack_id = np.random.randint(0, len(stacks))
                    stacks[rand_stack_id] = np.insert(stacks[rand_stack_id],0,o)

          obj = np.setdiff1d(obj, stack)

     # add empty stack to assure full warehouse
     if len(stacks) < num_stack:
          for _ in range(num_stack - len(stacks)):
               empty = np.empty(0, dtype=np.int32)
               stacks.append(empty)

     return stacks

def _find_empty_stack(stacks):
     for stack_id, stack in enumerate(stacks):
          if stack.size == 0:
               return stack, stack_id

GROUND_ID = -1
OUTPUT_ID = -2
INPUT_ID = -3

class Warehouse():
     expanded = 0

     def __init__(self, inicial_state, out_order=None, in_order=None,
                   isInputProccesed = False, isOutputProccesed = True,
                   max_stack_items = 300):
          self.state = inicial_state

          self.input = in_order
          self.output = np.empty(0, dtype=np.int32)

          self.required_order = out_order
          self.isInputProccesed = isInputProccesed
          self.isOutputProccesed = isOutputProccesed
          self.max_stack_items = max_stack_items

     def move(self, move):
          from_id, to_id = move

          if from_id == to_id:
               print("!ERROR: invalid move (from_id == to_id)!")
               return
          if (from_id == GROUND_ID or from_id == OUTPUT_ID 
               or from_id < INPUT_ID or from_id >= len(self.state)) \
               or (to_id < OUTPUT_ID or to_id >= len(self.state)):
               print("!ERROR: invalid move outside of warehouse!")
               return

          object_to_move = None #object from top of stack

          if from_id == INPUT_ID:
               object_to_move = self.input[0]
               self.input = np.delete(self.input, 0)
          else:
               object_to_move = self.state[from_id][0] 
               self.state[from_id] = np.delete(self.state[from_id], 0)

          if to_id == OUTPUT_ID:
               #insert object on the top of stack
               self.output = np.insert(self.output, 0, object_to_move) 
          elif to_id == GROUND_ID:
               to_stack, to_stack_id = _find_empty_stack(self.state)
               self.state[to_stack_id] = np.insert(to_stack, 0, object_to_move)
          else:
               self.state[to_id] = np.insert(self.state[to_id], 0, object_to_move)


     def get_moves(self):
          Warehouse.expanded += 1

          moves = []

          if self.isInputProccesed and self.input is not None and len(self.input) > 0:
               for to_id, to_stack in enumerate(self.state):
                    if to_stack.size == 0 and ((INPUT_ID, GROUND_ID) not in moves):
                         moves.append((INPUT_ID, GROUND_ID))
                    elif to_stack.size > 0 and to_stack.size < self.max_stack_items:
                         moves.append((INPUT_ID, to_id))

          if self.isOutputProccesed:
               for from_id, from_stack in enumerate(self.state):

                    if from_stack.size == 0:
                         continue

                    object_a = from_stack[0] # object from top of stack 
                    
                    #object_a is in order as next item
                    if self.output.size < len(self.required_order) and object_a == self.required_order[-self.output.size - 1]: 
                         # move object from top of from_stack to output
                         moves.append((from_id, OUTPUT_ID)) 

                    for to_id, to_stack in enumerate(self.state):
                         if from_id == to_id:
                              continue

                         if len(from_stack) > 1 and to_stack.size == 0 and ((from_id, GROUND_ID) not in moves):
                              # move object from top of from_stack to ground
                              moves.append((from_id, GROUND_ID)) 
                              continue
                         
                         if to_stack.size > 0 and to_stack.size < self.max_stack_items:
                              moves.append((from_id, to_id))

          return moves
     
     def get_neighbors(self):
          neighbors = []

          for a in self.get_moves():
               new_state = self.clone()
               new_state.move(a)

               neighbors.append((a,new_state))
               
          return neighbors
     
     def get_state(self):
          return self.state

     def get_curr_output(self):
          return tuple(self.output)
     
     def get_goal_output(self):
          return self.required_order
     
     def isGoalOutput(self):
          """ input position must be empty """
          return self.get_curr_output() == self.get_goal_output()
     
     def isGoalInput(self):
          """ output is equal required order """
          return len(self.input)==0

     def isDone(self):
          if self.isInputProccesed and self.isOutputProccesed:
               return self.isGoalInput() and self.isGoalOutput()
          elif self.isOutputProccesed:
               return self.isGoalOutput()
          elif self.isInputProccesed:
               return self.isGoalInput()
          else:
               return False

     def __str__(self) -> str:
          return str([list(o) for o in self.state]) + " \nInput: " +str(self.input)  + " Output: " +str(self.output) + " Orders: " +str(self.required_order) + " Done: " + str(self.isDone())

     def clone(self):
          warehouse = type(self)(0)
          warehouse.state = copy.deepcopy(self.state)
          warehouse.input = copy.deepcopy(self.input)
          warehouse.output = copy.deepcopy(self.output)
          warehouse.required_order = self.required_order
          warehouse.isInputProccesed = self.isInputProccesed
          warehouse.isOutputProccesed = self.isOutputProccesed
          warehouse.max_stack_items = self.max_stack_items

          return warehouse

     def visualization(self):
          reversed_print = []
          max_len_stack = 0
          for i,stack in enumerate(self.state):
               #print(" _ ", end="..")
               if i == 0:
                    reversed_print.append("****''")
               else:
                    reversed_print.append("^^^^''")
               len_stack = len(stack)
               if len_stack > max_len_stack:
                    max_len_stack = len_stack
          if self.output.size > max_len_stack:
                    max_len_stack = self.output.size
          if len(self.input) > max_len_stack:
                    max_len_stack = len(self.input)
          #print(" _ ") # output
          reversed_print.append("^^^^''")
          reversed_print.append("\n''####''") #input position
          heigth = -1
          while max_len_stack != - heigth - 1:
               if len(self.output) >= - heigth and len(self.output) != 0 :
                    #print(f'|{self.out[heigth]}|', end="\n")
                    reversed_print.append(f'|{self.output[heigth]}|')
               else:
                    #print(" ", end="\n")
                    reversed_print.append("     ")
               for stack in self.state:
                    if len(stack) >= - heigth and len(stack) != 0 :
                         #print(f'|{stack[heigth]}|', end="  ")
                         space = 3
                         if stack[heigth] >= 10:
                              space = 2
                         reversed_print.append(f'|{stack[heigth]}|'+space*" ")
                    else:
                         #print(" ", end="    ")
                         reversed_print.append(6*" ")
               # if len(self.out) >= - heigth and len(self.out) != 0 :
               #      print(f'|{self.out[heigth]}|', end="\n")
               # else:
               #      print(" ", end="\n")
               if len(self.input) >= - heigth and len(self.input) != 0 :
                    space = 3
                    if self.input[heigth] >= 10:
                         space = 2
                    reversed_print.append(f'\n  |{self.input[heigth]}|'+space*" ")
               else:
                    reversed_print.append("\n"+ 8*" ")


               heigth -= 1
          #print(list(reversed(reversed_print)))
          for i in list(reversed(reversed_print)):
               print(i, end="")
          #print(f'\n[input]{(6*(len(self.state))-1)*" "}[output]')
          print(f'\n[input]', end="")
          for idx in range(len(self.state), 0, -1):
               print(f"  #{idx-1}  ", end="")
          print("[output]")


if __name__ == "__main__":

    # rndState = _get_random_state(6,3)
    # print(rndState)
    # print(frozenset(tuple(o) for o in rndState))
    N = 9 #number of box in warehouse
    S = 4 #size of warehouse (num_stack)

    state = get_random_state(N,S)
    out_order = get_random_orders(N,S)
    in_order = get_random_orders(N+3,3,N+1)
    wh = Warehouse(state, out_order, in_order, isInputProccesed=True, isOutputProccesed=True, max_stack_items=10)
    

    while True:
          print(f"State (Legend: GROUND_ID={GROUND_ID}, OUTPUT_ID={OUTPUT_ID}, INTPUT_ID={INPUT_ID}):")
          wh.visualization()
          print("Required output order: "+ str(wh.get_goal_output())+ " Work is Done: " + str(wh.isDone()))
          print("moves = "+str(wh.get_moves()))
          print("<from> <to>: ", end="")
        
          id_from, id_to = [int(x) for x in input().split()]
          wh.move((id_from,id_to)) 