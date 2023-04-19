from warehouse import Warehouse, get_random_orders, get_random_state
from queue import PriorityQueue
import time

class WarehouseWithoutHeuristic(Warehouse):
	def __init__(self, num_box=5, num_stack=3, order=None, start_state=None):
		super().__init__(num_box, num_stack, order, start_state)
	
	def heuristic(self):
		return 0

class WarehouseHeuristic(Warehouse):
	def __init__(self, num_box=5, num_stack=3, order=None, start_state=None):
		super().__init__(num_box, num_stack, order, start_state)
		

	def find_pos_in_stack(self, num, warehouse):
		for i,stack in enumerate(warehouse):
			for j,val in enumerate(stack):
				if val == num:
					return j + 1 # ret num of box above finded box
		return 0

	def heuristic(self):
		curr_state = self.get_state()
		goal_order = self.get_goal_out()

		heur = 0
		for goal_val in goal_order:
			heur += self.find_pos_in_stack(goal_val,curr_state)
			
		return heur


class State():
	def __init__(self, warehouse, cost = 0, priority = 0, history = (None, None)):
		self.warehouse = warehouse
		self.cost = cost # number of moves
		self.priority = priority
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
		# Return a list of optimal actions that takes start to goal.

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
				next_state = State(neighbor, state.cost+1, 0, (action, state.warehouse))
				next_state.priority = next_state.cost + self.weigth * next_state.warehouse.heuristic()
				opened.put(next_state)

		return None
	

if __name__ == "__main__":
	
	#N=1000 S=4 Total expanded nodes: 10744 Time: 80.24

	N = 10 #number of box in warehouse
	S = 4 #size of warehouse (num_stack)
	
	order = (2,1) #sequence of box to go out 

	rnd_order = get_random_orders(N,S)
	rnd_state = get_random_state(N,S)

	#start = WarehouseHeuristic(N,S, rnd_order, rnd_state)
	start = WarehouseWithoutHeuristic(N,S, rnd_order, rnd_state)

	print(f"Searching path: {start} -> for order {start.get_goal_out()}")

	astar = AStar()

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

