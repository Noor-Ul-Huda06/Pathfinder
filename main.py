import matplotlib.pyplot as plt
import numpy as np
import time
import heapq
from collections import deque

ROWS = 10
COLS = 10

EMPTY = 0
WALL = -1
START = 1
TARGET = 2
FRONTIER = 3
EXPLORED = 4
PATH = 5

DELAY = 0.15
MOVES = [
    (-1,0),   
    (0,1),    
    (1,0),    
    (1,1),    
    (0,-1),   
    (-1,-1)   
]


def create_grid():

    grid = np.zeros((ROWS,COLS))

    for i in range(1,7):
        grid[i][5] = WALL

    start = (4,7)
    target = (6,1)

    grid[start] = START
    grid[target] = TARGET

    return grid,start,target


def draw(grid,title="Search"):

    plt.clf()

    colors={
        EMPTY:'white',
        WALL:'red',
        START:'green',
        TARGET:'blue',
        FRONTIER:'cyan',
        EXPLORED:'yellow',
        PATH:'purple'
    }

    for i in range(ROWS):
        for j in range(COLS):

            val = grid[i][j]

            plt.gca().add_patch(
                plt.Rectangle((j,i),1,1,
                color=colors[val],
                ec='black')
            )

            if val == WALL:
                plt.text(j+.3,i+.6,"-1")

            elif val == START:
                plt.text(j+.3,i+.6,"S")

            elif val == TARGET:
                plt.text(j+.3,i+.6,"T")

            else:
                plt.text(j+.3,i+.6,"0")

    plt.xlim(0,COLS)
    plt.ylim(ROWS,0)
    plt.title(title)
    plt.pause(DELAY)


def get_neighbors(grid,node):

    result=[]

    for move in MOVES:

        r=node[0]+move[0]
        c=node[1]+move[1]

        if 0<=r<ROWS and 0<=c<COLS:
            if grid[r][c]!=WALL:
                result.append((r,c))

    return result


def reconstruct_path(grid,parent,start,target):

    node = target

    while node in parent:

        node = parent[node]

        if node != start:
            grid[node] = PATH

        draw(grid,"Final Path")


def bfs(grid,start,target):

    queue = deque([start])
    visited = set([start])
    parent = {}

    while queue:

        current = queue.popleft()

        if current == target:
            reconstruct_path(grid,parent,start,target)
            return

        if current != start:
            grid[current] = EXPLORED

        for neighbor in get_neighbors(grid,current):

            if neighbor not in visited:

                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

                if grid[neighbor] == EMPTY:
                    grid[neighbor] = FRONTIER

        draw(grid,"BFS")



def dfs(grid,start,target):

    stack = [start]
    visited = set()
    parent = {}

    while stack:

        current = stack.pop()

        if current == target:
            reconstruct_path(grid,parent,start,target)
            return

        if current not in visited:

            visited.add(current)

            if current != start:
                grid[current] = EXPLORED

            for neighbor in reversed(get_neighbors(grid,current)):

                if neighbor not in visited:

                    parent[neighbor] = current
                    stack.append(neighbor)

                    if grid[neighbor] == EMPTY:
                        grid[neighbor] = FRONTIER

        draw(grid,"DFS")


def ucs(grid,start,target):

    pq = [(0,start)]
    parent = {}
    cost = {start:0}

    while pq:

        current_cost,current = heapq.heappop(pq)

        if current == target:
            reconstruct_path(grid,parent,start,target)
            return

        if current != start:
            grid[current] = EXPLORED

        for neighbor in get_neighbors(grid,current):

            new_cost = current_cost + 1

            if neighbor not in cost or new_cost < cost[neighbor]:

                cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq,(new_cost,neighbor))

                if grid[neighbor] == EMPTY:
                    grid[neighbor] = FRONTIER

        draw(grid,"UCS")


def dls(grid, start, target, limit):

    stack = [(start, 0)]
    parent = {}
    visited = set()

    while stack:

        current, depth = stack.pop()

        if current == target:
            reconstruct_path(grid, parent, start, target)
            print("Target Found!")
            return True

        if depth <= limit and current not in visited:

            visited.add(current)

            if current != start:
                grid[current] = EXPLORED

            for neighbor in reversed(get_neighbors(grid, current)):

                if neighbor not in visited:

                    parent[neighbor] = current
                    stack.append((neighbor, depth + 1))

                    if grid[neighbor] == EMPTY:
                        grid[neighbor] = FRONTIER

        draw(grid, f"DLS Limit={limit}")

    print("Target NOT found within depth limit")
    return False



def iddfs(grid, start, target):

    max_depth = ROWS * COLS

    for limit in range(max_depth):

        temp_grid, start, target = create_grid()

        draw(temp_grid, f"IDDFS depth={limit}")

        found = dls(temp_grid, start, target, limit)

        if found:
            return

def bidirectional(grid, start, target):

    q_start = deque([start])
    q_target = deque([target])

    parent_start = {}
    parent_target = {}

    visited_start = {start}
    visited_target = {target}

    meet = None

    while q_start and q_target:

        current_start = q_start.popleft()

        if current_start != start:
            grid[current_start] = EXPLORED

        for neighbor in get_neighbors(grid, current_start):

            if neighbor not in visited_start:

                visited_start.add(neighbor)
                parent_start[neighbor] = current_start
                q_start.append(neighbor)

                if grid[neighbor] == EMPTY:
                    grid[neighbor] = FRONTIER

                if neighbor in visited_target:
                    meet = neighbor
                    break

        if meet:
            break

        current_target = q_target.popleft()

        for neighbor in get_neighbors(grid, current_target):

            if neighbor not in visited_target:

                visited_target.add(neighbor)
                parent_target[neighbor] = current_target
                q_target.append(neighbor)

                if neighbor in visited_start:
                    meet = neighbor
                    break

        draw(grid, "Bidirectional")

        if meet:
            break

    if meet:

        node = meet

        while node in parent_start:
            node = parent_start[node]
            if node != start:
                grid[node] = PATH
            draw(grid, "Bidirectional Path")

        node = meet

        while node in parent_target:
            node = parent_target[node]
            if node != target:
                grid[node] = PATH
            draw(grid, "Bidirectional Path")

while True:

    print("\nChoose Algorithm:")
    print("1 → BFS")
    print("2 → DFS")
    print("3 → UCS")
    print("4 → DLS")
    print("5 → IDDFS")
    print("6 → Bidirectional")
    print("0 → Exit")

    choice = input("Enter choice: ")

    if choice == "0":
        break

    plt.figure(figsize=(6,6))

    grid,start,target = create_grid()

    draw(grid,"Original Grid")

    time.sleep(1)

    if choice == "1":
        bfs(grid,start,target)

    elif choice == "2":
        dfs(grid,start,target)

    elif choice == "3":
        ucs(grid,start,target)

    elif choice == "4":
        limit = int(input("Enter depth limit: "))
        found = dls(grid,start,target,limit)

        if not found:
            print("Try higher depth")

    elif choice == "5":
        iddfs(grid,start,target)

    elif choice == "6":
        bidirectional(grid,start,target)

    plt.show()
