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

def find_best_pos_in_stack(num, warehouse):
	"""return best (num of box above finded box, index of stack)"""
	best_pos = None, None
	min_val = np.infty
	for i,stack in enumerate(warehouse):
		for j,val in enumerate(stack):
			if val == num and j < min_val:
				min_val = j	
				best_pos = (j, i) 
	return best_pos

def find_all_best_pos_in_stack(num, warehouse):
	"""return sorted list of position of id 'num' """
	all_best_pos = PriorityQueue()
	for i,stack in enumerate(warehouse):
		for j,val in enumerate(stack):
			if val == num:	
				all_best_pos.put(j)
	pos = []
	while not all_best_pos.empty():
		pos.append(all_best_pos.get())

	return pos

def find_first_n_best_pos_in_stack(num, warehouse, n):
	"""return sorted list of first 'n' (position, stack index) of id 'num' """
	all_best_pos = PriorityQueue()
	for i,stack in enumerate(warehouse):
		for j,val in enumerate(stack):
			if val == num:	
				all_best_pos.put((j, [j, i]))
	pos = []
	while n > 0:
		a = all_best_pos.get()[1]
		pos.append(a)
		#print(a)
		n -= 1

	return pos

def heuristic_order(order, warehouse):
	q = PriorityQueue()
	for o in order:
		cost = find_pos_in_stack(o, warehouse)[0]
		q.put((cost, o))
	new_order = []
	while not q.empty():
		new_order.append(q.get()[1])

	return tuple(reversed(new_order))

def heuristic_duplicities_order(order, warehouse):
	q = PriorityQueue()

	values, counts = np.unique(order, return_counts=True)
	for v,c in zip(values,counts):
		all_pos = find_first_n_best_pos_in_stack(v,warehouse, c)
		for cost in all_pos:
			q.put((cost[0], v))
	new_order = []
	while not q.empty():
		new_order.append(q.get()[1])

	return tuple(reversed(new_order))

class WarehouseHeuristicDuplicities(Warehouse):
	def __init__(self, inicial_state, out_order=None, in_order=None,
                   isInputProccesed = False, isOutputProccesed = True,
                   max_stack_items = 300):
		super().__init__(inicial_state, out_order, in_order,
		    isInputProccesed, isOutputProccesed, max_stack_items)	

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_output()

		out_diff = len(self.get_goal_output()) - len(self.get_curr_output())
		goal_diff = goal_order[:out_diff]
		heur = 0
		for goal_val in goal_diff:
			heur += find_best_pos_in_stack(goal_val,curr_state)[0]
			
		heur += out_diff
		return heur
	
class WarehouseHeuristicDuplicities2(Warehouse):
	def __init__(self, inicial_state, out_order=None, in_order=None,
                   isInputProccesed = False, isOutputProccesed = True,
                   max_stack_items = 300):
		super().__init__(inicial_state, out_order, in_order,
		    isInputProccesed, isOutputProccesed, max_stack_items)	

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_output()

		out_diff = len(self.get_goal_output()) - len(self.get_curr_output())
		heur = 0
		goal_diff = goal_order[:out_diff]
		values, counts = np.unique(goal_diff, return_counts=True)
		for v,c in zip(values,counts):
			all_pos = find_all_best_pos_in_stack(v,curr_state)
			heur += np.sum(all_pos[:c])
			#print(f"v:{v} c:{c} pos: {all_pos} heur:{np.sum(all_pos[:c])}")
			
		heur += out_diff
		return heur
	
class WarehouseHeuristicDuplicities3(Warehouse):
	def __init__(self, inicial_state, out_order=None, in_order=None,
                   isInputProccesed = False, isOutputProccesed = True,
                   max_stack_items = 300):
		super().__init__(inicial_state, out_order, in_order,
		    isInputProccesed, isOutputProccesed, max_stack_items)	

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_output()

		out_diff = len(self.get_goal_output()) - len(self.get_curr_output())
		heur = 0
		heur_stacks = np.zeros(len(curr_state), dtype=np.int32)
		goal_diff = goal_order[:out_diff]
		values, counts = np.unique(goal_diff, return_counts=True)
		for v,c in zip(values,counts):
			all_pos = find_first_n_best_pos_in_stack(v,curr_state, c)
			#print(f"v:{v} c:{c} pos: {all_pos} heur:{np.sum(all_pos, axis=0)[0]}")
			for pos, idx in all_pos:
				heur_stacks[idx] = np.max([pos, heur_stacks[idx]])
		#print(f"heur_stack:{heur_stacks}")
		heur += np.sum(heur_stacks)	
		heur += out_diff
		if self.isInputProccesed:
			heur += len(self.input)
		return heur

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
	
class WarehouseHeuristic2(Warehouse):
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
		self.cost = cost # accumulated cost g(n)
		self.priority = priority # evaluation functione f(n) = g(n) + h(n)
		self.history = history # tuples (action, previous state)

	def __lt__(self, other): # Overrides "<" operator, needed in PriorityQueue.
		return self.priority < other.priority
	def __str__(self):
		return f"{self.warehouse} action: {self.history[0]} prev: {self.history[1]} cost: {self.cost} priority: {self.priority}"

class AStar():
	def __init__(self, weigth=1, w_cost = 1):
		self.weigth = weigth
		self.w_cost = w_cost

	def search(self, start, s_time = 0, timeout = np.inf):
		""" Return a optimal sequence of actions
        that takes from start to goal. """

		opened = PriorityQueue()
		closed = {}
		state = State(start.clone())
		opened.put(state)
	
		while not opened.empty() and time.time()-s_time < timeout:
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
				next_state.priority = self.w_cost*next_state.cost + self.weigth * next_state.warehouse.heuristic()
				opened.put(next_state)
				#print(f"{state.warehouse}/{next_state.warehouse}[{action}]")
				#print(next_state)

		return None
	

if __name__ == "__main__":
	import sys

	N = 20 #number of box in warehouse
	S = 4 #size of warehouse (num_stack)

	rnd_state = get_random_state(N,S, max_stack_items=100, num_type=10)
	rnd_order = tuple(np.random.choice([id for stack in rnd_state for id in stack], 6, replace=False))
	#rnd_order = get_random_orders(N,S, num_from=1, num_type=5)
	in_order = get_random_orders(N+10,6,N+1)

	#heur_order = heuristic_order(rnd_order, rnd_state)
	heur_order = heuristic_duplicities_order(rnd_order, rnd_state)

	print(f"rnd {rnd_order} heur {heur_order}")

	#start = WarehouseHeuristic(rnd_state, rnd_order, in_order, isInputProccesed = False, isOutputProccesed = True)
	#start = WarehouseWithoutHeuristic(rnd_state, rnd_order, in_order, isInputProccesed = True, isOutputProccesed = False)

	#start = WarehouseHeuristic4(rnd_state, rnd_order, in_order, isInputProccesed = False, isOutputProccesed = True, max_stack_items = 300)
	#start = WarehouseHeuristicInput(rnd_state, rnd_order, in_order, isInputProccesed = True, isOutputProccesed = True)


	start = WarehouseHeuristicDuplicities3(rnd_state, heur_order, in_order, isInputProccesed = True, isOutputProccesed = True, max_stack_items=150)

	print(f"Searching path: {start} -> for order {start.get_goal_output()}")

	astar = AStar(1.3)

	print(start)
	start.visualization()

	sim2file = False
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
	print(f"Found a path (length={len(path)}): ")
	print(f"Total expanded nodes: {Warehouse.expanded} Time: {elapsed_t:.2f}")

	# from pympler import asizeof

	#print(f"size of state: {asizeof.asizeof(s)}")

	if sim2file:
		file.close()
		sys.stdout = origin_sdtout
		print("End print to file")