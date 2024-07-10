import matplotlib.pyplot as plt
import numpy as np
import time
from astar import WarehouseHeuristic, AStar, WarehouseWithoutHeuristic
from warehouse import Warehouse, get_random_orders, get_random_state 

x = [1, 2, 3]
y = [1, 2, 3]

def timeToSolve(start_state):
    aStar = AStar()

    t_s = time.time()
    aStar.search(start_state)
    t_e = time.time()

    return t_e - t_s 

if __name__ == "__main__":

    numOfStacks = 2
    numOfBoxes = 12
    problemSize = []
    problemTime = []
    problemTimeNoHeur = []

    for num in range(numOfStacks,numOfBoxes+1,1):
        t = 0
        tNoHeur = 0
        n = 4
        for i in range(n):
            rnd_order = get_random_orders(num, numOfStacks)
            rnd_start_state = get_random_state(num, numOfStacks)
            start = WarehouseHeuristic(num, numOfStacks, rnd_order, rnd_start_state)
            startNoHeur = WarehouseWithoutHeuristic(num, numOfStacks, rnd_order, rnd_start_state)
            t += timeToSolve(start)
            tNoHeur += timeToSolve(startNoHeur)
        problemTime.append(t/n) #average time
        problemTimeNoHeur.append(tNoHeur/n)
        problemSize.append(num)
        # if (num % 100) == numOfStacks:
        print(f"Done: {num}/{numOfBoxes} time: {t} | {tNoHeur}")

    fig, ax = plt.subplots()
    ax.plot(problemSize,problemTime, color='r', label='A* heuristic')
    ax.plot(problemSize,problemTimeNoHeur, color='g', label='A* without heuristic')
    ax.set_xlabel("Number of boxes")
    ax.set_ylabel("Solved time")
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    ax.set_title(f"Complexity of A* (warehouse stack= {numOfStacks})")
    ax.legend()
    plt.show()
