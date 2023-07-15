from warehouse import Warehouse, get_random_orders, get_random_state
from queue import PriorityQueue
import time

class WarehouseWithoutHeuristic(Warehouse):
	def __init__(self, start_state=None, order=None, in_order=None, isInputProccesed = False, isOutputProccesed=True):
		super().__init__(start_state, order, in_order, isInputProccesed, isOutputProccesed)
	
	def heuristic(self):
		return 0

class WarehouseHeuristic(Warehouse):
	def __init__(self, start_state=None, order=None, in_order=None, isInputProccesed = False, isOutputProccesed=True):
		super().__init__(start_state, order, in_order, isInputProccesed, isOutputProccesed)	

	def find_pos_in_stack(self, num, warehouse):
		for i,stack in enumerate(warehouse):
			for j,val in enumerate(stack):
				if val == num:
					return j + 1 # ret num of box above finded box plus 1
		return 0

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_output()

		heur = 0
		for goal_val in goal_order:
			heur += self.find_pos_in_stack(goal_val,curr_state)
			
		return heur
	
class WarehouseHeuristic2(WarehouseHeuristic):
	def __init__(self, start_state=None, order=None, in_order=None, isInputProccesed = False, isOutputProccesed=True):
		super().__init__(start_state, order, in_order, isInputProccesed, isOutputProccesed)	

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_output()

		heur = 0
		for goal_val in goal_order:
			heur += self.find_pos_in_stack(goal_val,curr_state) - 1
			heur += len(self.get_goal_output()) - len(self.get_curr_output())
	
		return heur
	
class WarehouseHeuristicInput(WarehouseHeuristic):
	def __init__(self, start_state=None, order=None, in_order=None, isInputProccesed = False, isOutputProccesed=True):
		super().__init__(start_state, order, in_order, isInputProccesed, isOutputProccesed)	

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_output()

		heur = 0
		for goal_val in goal_order:
			heur += self.find_pos_in_stack(goal_val,curr_state) - 1
			heur += len(self.get_goal_output()) - len(self.get_curr_output())
		
		heur += len(self.input)
	
		return heur


class State():
	def __init__(self, warehouse, cost = 0, priority = 0, history = (None, None)):
		self.warehouse = warehouse # current warehouse state
		self.cost = cost # number of moves
		self.priority = priority # priority queue
		self.history = history 

	def copy(self):
		return State(self.warehouse.clone(), self.cost, self.priority, self.history)

	def __lt__(self, other): # Overrides "<" operator, needed in PriorityQueue.
		return self.priority < other.priority
	def __str__(self):
		return f"{self.warehouse} action: {self.history[0]} prev: {self.history[1]} cost: {self.cost} priority: {self.priority}"

class AStar():
	def __init__(self, weigth=1):
		self.weigth = weigth

	def search(self, start):
		# Return a optimal sequence of actions that takes from start to goal.

		opened = PriorityQueue()
		closed = {}
		state = State(start.clone())
		opened.put(state)
	
		while not opened.empty():
			state = opened.get()
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
			
			for action, neighbor in state.warehouse.get_neighbors():
				print(state.warehouse.get_neighbors())
				next_state = State(neighbor, state.cost + 1, 0, (action, state.warehouse))
				next_state.priority = next_state.cost + self.weigth * next_state.warehouse.heuristic()
				opened.put(next_state)
				#print(f"{state.warehouse}/{next_state.warehouse}[{action}]")

		return None
	

if __name__ == "__main__":
	import sys

	sim2file = True
	origin_sdtout = sys.stdout
	if sim2file:
		print("Start print to file")
		file = open("doc/simulation.txt", "w")
		sys.stdout = file
		
	
	
	#N=1000 S=4 Total expanded nodes: 10744 Time: 80.24

	N = 10#number of box in warehouse
	S = 4 #size of warehouse (num_stack)
	
	order = (2,1) #sequence of box to go out 

	rnd_order = get_random_orders(N,S)
	rnd_state = get_random_state(N,S)
	in_order = get_random_orders(N+10,3,N+1)

	#start = WarehouseHeuristic(rnd_state, rnd_order, in_order, isInputProccesed = True, isOutputProccesed = False)
	start = WarehouseWithoutHeuristic(rnd_state, rnd_order, in_order, isInputProccesed = True, isOutputProccesed = False)

	#start = WarehouseHeuristic(rnd_state, rnd_order, in_order, isInputProccesed = False, isOutputProccesed = True)
	#start = WarehouseHeuristicInput(rnd_state, rnd_order, in_order, isInputProccesed = False, isOutputProccesed = False)

	print(f"Searching path: {start} -> for order {start.get_goal_output()}")

	astar = AStar(1.1)

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
			s.apply(a)
			#print(s)
			print(f"------------ Action: {a} ----------")
			s.visualization() 
		print(s)   
	else:
		print("NO PATH exists.")
	
	print(f"Total expanded nodes: {Warehouse.expanded} Time: {elapsed_t:.2f}")


	if sim2file:
		file.close()
		sys.stdout = origin_sdtout
		print("End print to file")