import random, copy, numpy as np

def get_random_orders(num_obj, num_orders):
     obj = np.arange(1, num_obj+1)
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

    def __init__(self, num_box=5, num_stack=3, order=None, start_state=None) -> None:
         #create random state
          # if start_state is None:
          #      self.state = get_random_state(num_box, num_stack)
          # else:
          self.state = start_state
          self.out = np.empty(0,dtype=np.int32)
          self.order = order
          self.stateFset = None
          #self.stateFset = frozenset(tuple(o) for o in self.state)


    def apply(self, action):
         what, where = action

         if what==where:
              print("!invalid action what==where")
              return
         
         stack_from, stack_from_id = _find_stack(self.state, what)
         if stack_from is None:
              print("!invalid action cannot move what")
              return
         
         if where == 0: # to ground of empty stack
              stack_to, stack_to_id = _find_empty_stack(self.state)
         
         elif where == -1: # to ground of output stack
              stack_to, stack_to_id = self.out, -1
         else:
              stack_to, stack_to_id = _find_stack(self.state, where)     
        
         if stack_to is None:
                print("!invalid action empty stack or where DON'T exists")
                return

         #move object
         self.state[stack_from_id] = np.delete(stack_from,0)
         if stack_to_id != -1:
            self.state[stack_to_id] = np.insert(stack_to,0, what)
         else:
            self.out = np.insert(self.out,0,what)

         self.stateFset = frozenset(tuple(o) for o in self.state)

    def get_action(self):
          Warehouse.expanded += 1

          actions = []
          for s_from in self.state:
                if s_from.size == 0:
                      continue
                object_a = s_from[0]

                if self.out.size < len(self.order) and object_a == self.order[-self.out.size - 1]: #obj_a is next ordered box
                      actions.append((object_a, -1)) # obj a move to output

                for s_to in self.state:
                      if len(s_from) > 1 and s_to.size == 0:
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

    def get_cur_out(self):
         return tuple(self.out)
    
    def get_goal_out(self):
         return self.order
    
    def isDone(self):
         return self.get_cur_out() == self.get_goal_out()

    def __str__(self) -> str:
        return str([list(o) for o in self.state]) + " Output: " +str(self.out) + " Orders: " +str(self.order) + " Done: " + str(self.isDone())
    
    def clone(self):
        warehouse = type(self)(0)
        warehouse.state = copy.deepcopy(self.state)
        warehouse.out = copy.deepcopy(self.out)
        warehouse.order = self.order
        warehouse.stateFset = self.stateFset

        return warehouse
          
    

if __name__ == "__main__":

    # rndState = _get_random_state(6,3)
    # print(rndState)
    # print(frozenset(tuple(o) for o in rndState))
    N = 6 #number of box in warehouse
    S = 3 #size of warehouse (num_stack)

    order = get_random_orders(N,S)
    wh = Warehouse(N,S, order)
    #cwh = wh.clone()
    

    while True:
          #print(cwh)
          print(f"state: {wh}")
          print(f"actions = {wh.get_action()}")
          print("<from> <to>: ", end="")
        
          o_from, o_to = [int(x) for x in input().split()]
          wh.apply((o_from,o_to)) 