from warehouse import Warehouse, get_random_orders, get_random_state
from queue import PriorityQueue
import time
from pympler import asizeof
import numpy as np

def find_pos_in_stack(num, warehouse):
	"""return (num of box above finded box plus 1, index of stack)"""
	for i,stack in enumerate(warehouse):
		for j,val in enumerate(stack):
			if val == num:
				return (j + 1, i) 
	return (0, -1)

def heuristic_order(order, warehouse):
	q = PriorityQueue()
	for o in order:
		cost = find_pos_in_stack(o, warehouse)
		q.put((cost, o))
	new_order = []
	while not q.empty():
		new_order.append(q.get()[1])

	return tuple(new_order)

class WarehouseWithoutHeuristic(Warehouse):
	def __init__(self, inicial_state, out_order=None, in_order=None,
                   isInputProccesed = False, isOutputProccesed = True,
                   max_stack_items = 300):
		super().__init__(inicial_state, out_order, in_order,
		    isInputProccesed, isOutputProccesed, max_stack_items)
	
	def heuristic(self):
		return 0

class WarehouseHeuristic(Warehouse):
	def __init__(self, inicial_state, out_order=None, in_order=None,
                   isInputProccesed = False, isOutputProccesed = True,
                   max_stack_items = 300):
		super().__init__(inicial_state, out_order, in_order,
		    isInputProccesed, isOutputProccesed, max_stack_items)	

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_output()

		heur = 0
		for goal_val in goal_order:
			heur += find_pos_in_stack(goal_val,curr_state)[0]
			
		return heur
	
class WarehouseHeuristic3(Warehouse):
	def __init__(self, inicial_state, out_order=None, in_order=None,
                   isInputProccesed = False, isOutputProccesed = True,
                   max_stack_items = 300):
		super().__init__(inicial_state, out_order, in_order,
		    isInputProccesed, isOutputProccesed, max_stack_items)	

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_output()

		heur = 0

		heur += find_pos_in_stack(goal_order[0],curr_state)[0]
			
		heur += len(self.get_goal_output()) - len(self.get_curr_output())	
		return heur
	
class WarehouseHeuristic4(Warehouse):
	def __init__(self, inicial_state, out_order=None, in_order=None,
                   isInputProccesed = False, isOutputProccesed = True,
                   max_stack_items = 300):
		super().__init__(inicial_state, out_order, in_order,
		    isInputProccesed, isOutputProccesed, max_stack_items)	

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_output()

		heur = 0
		heur_stacks = np.zeros(len(curr_state), dtype=np.int32)

		for goal_val in goal_order:
			val, idx = find_pos_in_stack(goal_val,curr_state)
			if idx == -1:
				continue
			heur_stacks[idx] = np.max([heur_stacks[idx], val-1])
			
		heur = np.sum(heur_stacks)

		heur += len(self.get_goal_output()) - len(self.get_curr_output())

		return heur
	
class WarehouseHeuristic2(Warehouse):
	def __init__(self, inicial_state, out_order=None, in_order=None,
                   isInputProccesed = False, isOutputProccesed = True,
                   max_stack_items = 300):
		super().__init__(inicial_state, out_order, in_order,
		    isInputProccesed, isOutputProccesed, max_stack_items)

	def heuristic(self):
		heur = len(self.get_goal_output()) - len(self.get_curr_output())
	
		return heur
	
class WarehouseHeuristicInput(Warehouse):
	def __init__(self, inicial_state, out_order=None, in_order=None,
                   isInputProccesed = False, isOutputProccesed = True,
                   max_stack_items = 300):
		super().__init__(inicial_state, out_order, in_order,
		    isInputProccesed, isOutputProccesed, max_stack_items)

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_output()

		heur = 0
		for goal_val in goal_order:
			heur += find_pos_in_stack(goal_val,curr_state)[0]
		
		heur += len(self.input)
	
		return heur


class State():
	def __init__(self, warehouse, cost = 0, priority = 0, history = (None, None)):
		self.warehouse = warehouse # current warehouse state
		self.cost = cost # number of moves
		self.priority = priority # priority queue
		self.history = history 

	# def copy(self):
	# 	return State(self.warehouse.clone(), self.cost, self.priority, self.history)

	def __lt__(self, other): # Overrides "<" operator, needed in PriorityQueue.
		return self.priority < other.priority
	def __str__(self):
		return f"{self.warehouse} action: {self.history[0]} prev: {self.history[1]} cost: {self.cost} priority: {self.priority}"

class AStar():
	def __init__(self, weigth=1):
		self.weigth = weigth

	def search(self, start):
		""" Return a optimal sequence of actions
        that takes from start to goal. """

		opened = PriorityQueue()
		closed = {}
		state = State(start.clone())
		opened.put(state)
	
		while not opened.empty():
			state = opened.get()
			#print(f"size of state: {asizeof.asizeof(state)}")
			#print(state)
			action, prev_state = state.history
			if state.warehouse.isDone():
				#return path
				path = [action]
				while prev_state is not None:
					action, prev_state = closed[prev_state]
					if action is not None:
						path.append(action)
				return list(reversed(path))
			if state.warehouse in closed:
				continue
			else:
				closed[state.warehouse] = (action, prev_state)
			
			#print(state.warehouse.get_neighbors())
			for action, neighbor in state.warehouse.get_neighbors():
				next_state = State(neighbor, state.cost + 1, 0, (action, state.warehouse))
				next_state.priority = next_state.cost + self.weigth * next_state.warehouse.heuristic()
				opened.put(next_state)
				#print(f"{state.warehouse}/{next_state.warehouse}[{action}]")

		return None
	

if __name__ == "__main__":
	import sys

	#N=1000 S=4 Total expanded nodes: 10744 Time: 80.24

	N = 200 #number of box in warehouse
	S = 4 #size of warehouse (num_stack)
	
	order = (2,1) #sequence of box to go out 

	rnd_order = get_random_orders(N,S+2)
	rnd_state = get_random_state(N,S)
	in_order = get_random_orders(N+10,3,N+1)

	heur_order = heuristic_order(rnd_order, rnd_state)

	print(f"rnd {rnd_order} heur {heur_order}")

	#start = WarehouseHeuristic(rnd_state, rnd_order, in_order, isInputProccesed = True, isOutputProccesed = False)
	#start = WarehouseWithoutHeuristic(rnd_state, rnd_order, in_order, isInputProccesed = True, isOutputProccesed = False)

	start = WarehouseHeuristic4(rnd_state, heur_order, in_order, isInputProccesed = False, isOutputProccesed = True, max_stack_items = 400)
	#start = WarehouseHeuristicInput(rnd_state, rnd_order, in_order, isInputProccesed = True, isOutputProccesed = True)

	print(f"Searching path: {start} -> for order {start.get_goal_output()}")

	astar = AStar(1.5)

	print(start)
	start.visualization()

	sim2file = True
	origin_sdtout = sys.stdout
	if sim2file:
		print("Start print to file")
		file = open("doc/simulation.txt", "w")
		sys.stdout = file


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
		s.visualization()
		for a in path:
			s.move(a)
			#print(s)
			print(f"------------ Action: {a} ----------")
			s.visualization() 
		print(s)   
	else:
		print("NO PATH exists.")
	
	print(f"Total expanded nodes: {Warehouse.expanded} Time: {elapsed_t:.2f}")

	# from pympler import asizeof

	#print(f"size of state: {asizeof.asizeof(s)}")

	if sim2file:
		file.close()
		sys.stdout = origin_sdtout
		print("End print to file")