import random, copy, numpy as np

def get_random_orders(num_obj, num_orders, num_from=1):
     obj = np.arange(num_from, num_obj+1)
     return tuple(np.random.choice(obj,num_orders, replace=False))


def get_random_state(num_obj, num_stack):
    stacks = []
    obj = np.arange(1, num_obj+1)

    while len(obj) > 0:
        stack_len = np.random.randint(1, len(obj)+1)
        stack = np.random.choice(obj, stack_len, replace=False)

        if len(stacks) < num_stack:
            stacks.append(stack)
        else:
            for o in stack:
                rand_stack_id = np.random.randint(0,num_stack)
                stacks[rand_stack_id] = np.insert(stacks[rand_stack_id],0,o)

        obj = np.setdiff1d(obj, stack)

    # add empty stack to assure full warehouse
    if len(stacks) < num_stack: 
         for _ in range(num_stack - len(stacks)):
              empty = np.empty(0, dtype=np.int32)
              stacks.append(empty)

    return stacks

def _find_stack(stacks, item):
	for stack_id, stack in enumerate(stacks):
		if stack.size != 0 and stack[0] == item:
			return stack, stack_id

	return None, None

def _find_empty_stack(stacks):
	for stack_id, stack in enumerate(stacks):
		if stack.size == 0:
			return stack, stack_id

	return None, None

class Warehouse():
    expanded = 0

    def __init__(self, start_state=None, out_order=None, in_order=None, isInputProccesed = False) -> None:
          self.state = start_state

          self.input = in_order
          self.output = np.empty(0,dtype=np.int32)

          self.out_order = out_order

          self.stateFset = None
          self.isInputProccesed = isInputProccesed

    def apply_from_input():
         return None

    def apply(self, action):
         what, where = action

         if what==where:
              print("!invalid action what==where")
              return
         
         stack_from, stack_from_id = None, None
         if self.isInputProccesed and what == self.input[0]:
              stack_from_id = -1
         else:
              stack_from, stack_from_id = _find_stack(self.state, what)

         if stack_from is None and stack_from_id is None:
              print("!invalid action cannot move 'what'")
              return
         
         if where == 0: # to ground of empty stack
              stack_to, stack_to_id = _find_empty_stack(self.state)
         
         elif where == -1: # to output stack
              stack_to, stack_to_id = self.output, -1
         else:
              stack_to, stack_to_id = _find_stack(self.state, where)     
        
         if stack_to is None:
                print("!invalid action empty stack or 'where' DON'T exists")
                return

         #move object
         if stack_from_id != -1:
            self.state[stack_from_id] = np.delete(stack_from,0)
         else:
            self.input = np.delete(self.input, 0)
         
         if stack_to_id != -1:
            self.state[stack_to_id] = np.insert(stack_to,0, what)
         else:
            self.output = np.insert(self.output,0,what)

         self.stateFset = frozenset(tuple(o) for o in self.state)

    def get_action(self):
          Warehouse.expanded += 1

          actions = []
          
          if self.isInputProccesed and self.input is not None and len(self.input) > 0:
               obj_a_from_in = self.input[0]
               for s_to in self.state:
                      if s_to.size == 0 and ((obj_a_from_in,0) not in actions):
                            actions.append((obj_a_from_in, 0))
                            continue

                      object_b = s_to[0]

                      actions.append((obj_a_from_in, object_b))

          for s_from in self.state:
                if s_from.size == 0:
                      continue
                object_a = s_from[0]

                if self.output.size < len(self.out_order) and object_a == self.out_order[-self.output.size - 1]: #obj_a is next ordered box
                      actions.append((object_a, -1)) # obj a move to output

                for s_to in self.state:
                      if len(s_from) > 1 and s_to.size == 0 and ((object_a,0) not in actions):
                            actions.append((object_a,0)) # obj a move to ground
                            continue
                      elif s_to.size == 0:
                            continue

                      object_b = s_to[0]

                      if object_a != object_b:
                            actions.append((object_a, object_b))

          return actions
    
    def get_neighbors(self):
          neighbors = []

          for a in self.get_action():
                new_state = self.clone()
                new_state.apply(a)

                neighbors.append((a,new_state))
          
          return neighbors
    
    def get_state(self):
         return self.stateFset

    def get_curr_output(self):
         return tuple(self.output)
    
    def get_goal_output(self):
         return self.out_order
    
    def isDone(self):
         return self.get_curr_output() == self.get_goal_output()

    def __str__(self) -> str:
        return str([list(o) for o in self.state]) + " Input: " +str(self.input)  + " Output: " +str(self.output) + " Orders: " +str(self.out_order) + " Done: " + str(self.isDone())
    
    def clone(self):
        warehouse = type(self)(0)
        warehouse.state = copy.deepcopy(self.state)
        warehouse.output = copy.deepcopy(self.output)
        warehouse.out_order = self.out_order
        warehouse.stateFset = self.stateFset

        return warehouse
    
    def visualization(self):
        reversed_print = []
        max_len_stack = 0
        for i,stack in enumerate(self.state):
             #print(" _ ", end="..")
             if i == 0:
                  reversed_print.append("***''")
             else:
                  reversed_print.append("^^^''")
             len_stack = len(stack)
             if len_stack > max_len_stack:
                  max_len_stack = len_stack
        if self.output.size > max_len_stack:
                  max_len_stack = self.output.size
        
        #print(" _ ") # output
        reversed_print.append("\n^^^''")
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
                    reversed_print.append(f'|{stack[heigth]}|  ')
               else: 
                    #print(" ", end="    ")
                    reversed_print.append("     ")
          # if len(self.out) >= - heigth and len(self.out) != 0 :
          #      print(f'|{self.out[heigth]}|', end="\n")
          # else: 
          #      print(" ", end="\n")
          reversed_print.append("\n")         
          
          heigth -= 1
        #print(list(reversed(reversed_print)))
        for i in list(reversed(reversed_print)):
             print(i, end="")
        print(f'\n{(5*len(self.state)-2)*" "}[output]')



if __name__ == "__main__":

    # rndState = _get_random_state(6,3)
    # print(rndState)
    # print(frozenset(tuple(o) for o in rndState))
    N = 9 #number of box in warehouse
    S = 3 #size of warehouse (num_stack)

    state = get_random_state(N,S)
    out_order = get_random_orders(N,S)
    in_order = get_random_orders(N+10,3,N+1)
    wh = Warehouse(state, out_order, in_order, isInputProccesed=True)
    

    while True:
          print(f"state: {wh}")
          wh.visualization()
          print(f"actions = {wh.get_action()}")
          print("<from> <to>: ", end="")
        
          o_from, o_to = [int(x) for x in input().split()]
          wh.apply((o_from,o_to)) 