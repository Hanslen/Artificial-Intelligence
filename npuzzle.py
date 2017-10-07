"""
COMS W4701 Artificial Intelligence - Programming Homework 1

In this assignment you will implement and compare different search strategies
for solving the n-Puzzle, which is a generalization of the 8 and 15 puzzle to
squares of arbitrary size (we will only test it with 8-puzzles for now). 
See Courseworks for detailed instructions.

@author: Jiahe Chen (jc4833)
"""

import time

def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped. 
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]
    
    new_state = []
    for row in range(len(state)): 
        new_row = []
        for column in range(len(state[row])): 
            if row == i1 and column == j1: 
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else: 
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)
    

def get_successors(state):
    """
    This function returns a list of possible successor states resulting
    from applicable actions. 
    The result should be a list containing (Action, state) tuples. 
    For example [("Up", ((1, 4, 2),(0, 5, 8),(3, 6, 7))), 
                 ("Left",((4, 0, 2),(1, 5, 8),(3, 6, 7)))] 
    """ 
  
    child_states = []

    # YOUR CODE HERE . Hint: Find the "hole" first, then generate each possible
    # successor state by calling the swap_cells method.
    # Exclude actions that are not applicable. 
    for i in range(0,len(state)):
        for j in range(0,len(state)):
            if state[i][j] == 0:
                row = i
                column = j
                break
    #Left
    if column < len(state)-1:
        child_states.append(tuple(["Left",swap_cells(state, row, column, row, column+1)]))
    #Right
    if column > 0:
        child_states.append(tuple(["Right",swap_cells(state, row, column, row, column-1)]))
    #Up
    if row < len(state)-1:
        child_states.append(tuple(["Up",swap_cells(state, row, column, row+1, column)]))
    #Down
    if row > 0:
        child_states.append(tuple(["Down",swap_cells(state, row, column, row-1, column)]))
    return child_states


            
def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise. 
    """    

    #YOUR CODE HERE
    # return False # Replace this
    goal = (0,)
    for i in range(1, len(state)):
        goal = goal + (i,)
    goal = (goal,)
    for row in range(1, len(state)):
        newRow = (row*len(state),)
        for i in range(1, len(state)):
            newRow = newRow + (row*len(state)+i,)
        goal = goal + (newRow,)
    return goal == state
    # if state ==  ((0,1,2),(3,4,5),(6,7,8)):
    #     return True
    # else:
    #     return False
   
def bfs(state):
    """
    Breadth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """
    parents = {}
    actions = {}

    states_expanded = 0
    max_frontier = 0
            
    #YOUR CODE HERE
    #Hint: You may start with this: 
    frontier = [state]
    explored = set()
    seen = set()    
    seen.add(state)
    while frontier:
        node = frontier.pop(0)
        explored.add(node)
        states_expanded += 1
        if goal_test(node):
            tmp = node
            route = [actions.get(tmp)]
            while tmp != state:
                route.append(actions.get(parents.get(tmp)))
                tmp = parents.get(tmp)
            return route[:-1][::-1], states_expanded, max_frontier
        for successor in get_successors(node):
            if ((successor[1] in explored) == False) and ((successor[1] in seen) == False):
                seen.add(successor[1])
                parents[successor[1]] = node
                actions[successor[1]] = successor[0]
                frontier.append(successor[1])
        max_frontier = max(max_frontier, len(frontier))
    return None, states_expanded, max_frontier # No solution found
                               
def dfs(state):
    """
    Depth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """

    parents = {}
    actions = {}

    #YOUR CODE HERE
    states_expanded = 0
    max_frontier = 0
    frontier = [state]
    seen = set()
    seen.add(state)
    explored = set()
    while frontier:
        node = frontier.pop()
        explored.add(node)
        states_expanded += 1
        if goal_test(node):
            tmp = node
            route = [actions.get(tmp)]
            while tmp != state:
                route.append(actions.get(parents.get(tmp)))
                tmp = parents.get(tmp)
            return route[:-1][::-1], states_expanded, max_frontier
        for successor in get_successors(node):
            if successor[1] not in explored and successor[1] not in seen:
                seen.add(successor[1])
                parents[successor[1]] = node
                actions[successor[1]] = successor[0]
                frontier.append(successor[1])
        max_frontier = max(max_frontier, len(frontier))
    return None, states_expanded, max_frontier # No solution found

def misplaced_heuristic(state):
    """
    Returns the number of misplaced tiles.
    """

    #YOUR CODE HERE
    numberOfMis = 0
    for i in range(0, len(state)):
        for j in range(0,len(state)):
            if state[i][j] != i*len(state)+j and state[i][j] != 0:
                numberOfMis += 1
    return numberOfMis # replace this
    # return 0 # replace this


def manhattan_heuristic(state):
    """
    For each misplaced tile, compute the manhattan distance between the current
    position and the goal position. THen sum all distances. 
    """
    def findCorrect(state, elem):
        for i in range(0,len(state)):
            for j in range(0,len(state)):
                if state[i][j] == elem:
                    return i,j

    manhattanDis = 0
    for i in range(0,len(state)):
        for j in range(0,len(state)):
            if state[i][j] != (i*len(state)+j):
                row, col = findCorrect(state,i*len(state)+j)
                manhattanDis += (abs(row-i)+abs(col-j))
    return manhattanDis # replace this

def best_first(state, heuristic = misplaced_heuristic):
    """
    Breadth first search using the heuristic function passed as a parameter.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """

    # You might want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    parents = {}
    actions = {}
    costs = {}
    costs[state] = 0
    
    states_expanded = 0
    max_frontier = 0

    #YOUR CODE HERE
    frontier = []
    heappush(frontier,(heuristic(state), state))
    explored = set()
    seen = set()
    seen.add(state)
    while frontier:
        nextMove = heappop(frontier)
        states_expanded += 1
        explored.add(nextMove[1])
        if goal_test(nextMove[1]):
            tmp = nextMove[1]
            path = [actions.get(tmp)]
            while tmp != state:
                path.append(actions.get(parents.get(tmp)))
                tmp = parents.get(tmp)
            return path[:-1][::-1], states_expanded, max_frontier
        for successor in get_successors(nextMove[1]):
            if successor[1] not in explored and successor[1] not in seen:
                seen.add(successor[1])
                heappush(frontier,(heuristic(successor[1]), successor[1]))
                parents[successor[1]] = nextMove[1]
                actions[successor[1]] = successor[0]
        max_frontier = max(max_frontier, len(frontier))
    return None, states_expanded, max_frontier


def astar(state, heuristic = misplaced_heuristic):
    """
    A-star search using the heuristic function passed as a parameter. 
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """
    # You might want to use these functions to maintain a priority queue

    from heapq import heappush
    from heapq import heappop

    parents = {}
    actions = {}
    costs = {}
    costs[state] = 0
   
    states_expanded = 0
    max_frontier = 0

    #YOUR CODE HERE
    frontier = []
    explored = set()
    seen = set()
    seen.add(state)
    heappush(frontier, (heuristic(state)+costs[state], state))
    while frontier:
        nextMove = heappop(frontier)
        explored.add(nextMove[1])
        states_expanded += 1
        if goal_test(nextMove[1]):
            tmp = nextMove[1]
            path = [actions.get(tmp)]
            while tmp != state:
                path.append(actions.get(parents.get(tmp)))
                tmp = parents.get(tmp)
            return path[:-1][::-1], states_expanded, max_frontier
        for successor in get_successors(nextMove[1]):
            if successor[1] not in explored and successor[1] not in seen:
                seen.add(successor[1])
                costs[successor[1]] = costs[nextMove[1]] + 1
                parents[successor[1]] = nextMove[1]
                actions[successor[1]] = successor[0]
                heappush(frontier, ((heuristic(successor[1])+costs[successor[1]]), successor[1]))
        max_frontier = max(max_frontier,len(frontier))
    return None, states_expanded, max_frontier # No solution found

def print_result(solution, states_expanded, max_frontier):
    """
    Helper function to format test output. 
    """
    if solution is None: 
        print("No solution found.")
    else: 
        print("Solution has {} actions.".format(len(solution)))
    print("Total states exppanded: {}.".format(states_expanded))
    print("Max frontier size: {}.".format(max_frontier))



if __name__ == "__main__":

    #Easy test case
    test_state = ((1, 4, 2),
                  (0, 5, 8), 
                  (3, 6, 7))  

    #More difficult test case
    # test_state = ((7, 2, 4),
    #              (5, 0, 6), 
    #              (8, 3, 1))  

    # 4puzzle
    # test_state = ((1,5,2,3),
    #               (4,6,10,7),
    #               (8,9,11,15),
    #               (12,13,0,14))

    print(state_to_string(test_state))
    print()

    print("====BFS====")
    start = time.time()
    solution, states_expanded, max_frontier = bfs(test_state) #
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))

    print() 
    print("====DFS====") 
    start = time.time()
    solution, states_expanded, max_frontier = dfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    # if solution is not None:
    #     print(solution)
    print("Total time: {0:.3f}s".format(end-start))

    print() 
    print("====Greedy Best-First (Misplaced Tiles Heuristic)====") 
    start = time.time()
    solution, states_expanded, max_frontier = best_first(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    # if solution is not None:
    #     print(solution)
    print("Total time: {0:.3f}s".format(end-start))
    
    print() 
    print("====A* (Misplaced Tiles Heuristic)====") 
    start = time.time()
    solution, states_expanded, max_frontier = astar(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    # if solution is not None:
    #     print(solution)
    print("Total time: {0:.3f}s".format(end-start))

    print() 
    print("====A* (Total Manhattan Distance Heuristic)====") 
    start = time.time()
    solution, states_expanded, max_frontier = astar(test_state, manhattan_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    # if solution is not None:
    #     print(solution)
    print("Total time: {0:.3f}s".format(end-start))

