# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random

MAX_VALUE = 100000000

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0, len(actions) - 1)]


class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)


class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        root = StateNode(state, 0)
        queue = [(root, None)]
        minCost = MAX_VALUE
        bestAction = Directions.STOP
        visited = []
        while len(queue) > 0:
            size = len(queue)
            for i in range(0, size):
                curNode, curAction = queue.pop(0)
                curState = curNode.state
                if curState not in visited:
                    if curNode != root and minCost > curNode.stepCost + admissibleHeuristic(curState):
                        minCost = curNode.stepCost + admissibleHeuristic(curState)
                        bestAction = curAction
                    if not curState.isWin() and not curState.isLose():
                        legal = curState.getLegalPacmanActions()
                        successors = [(curState.generatePacmanSuccessor(action), action) for action in legal]
                        for successor in successors:
                            if successor[0] is not None and successor[0] not in visited:
                                queue.append((StateNode(successor[0], curNode.stepCost + 1),
                                              curAction if curAction is not None else successor[1]))
                    visited.append(curState)
        return bestAction


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        root = StateNode(state, 0)
        stack = [(root, None)]
        minCost = MAX_VALUE
        bestAction = Directions.STOP
        visited = []
        while len(stack) > 0:
            curNode, curAction = stack.pop()
            curState = curNode.state
            if curState not in visited:
                if curNode != root and minCost > curNode.stepCost + admissibleHeuristic(curState):
                    minCost = curNode.stepCost + admissibleHeuristic(curState)
                    bestAction = curAction
                if not curState.isWin() and not curState.isLose():
                    legal = curState.getLegalPacmanActions()
                    successors = [(curState.generatePacmanSuccessor(action), action) for action in legal]
                    for successor in successors:
                        if successor[0] is not None and successor[0] not in visited:
                            stack.append((StateNode(successor[0], curNode.stepCost + 1),
                                          curAction if curAction is not None else successor[1]))
                visited.append(curState)
        return bestAction


class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        root = StateNode(state, 0)
        pq = PriorityQueue()
        pq.put((admissibleHeuristic(state), root, None))
        minCost = MAX_VALUE
        bestAction = Directions.STOP
        visited = []
        while pq.size() > 0:
            _, curNode, curAction = pq.get()
            curState = curNode.state
            if curState not in visited:
                if curNode != root and minCost > curNode.stepCost + admissibleHeuristic(curState):
                    minCost = curNode.stepCost + admissibleHeuristic(curState)
                    bestAction = curAction
                if not curState.isWin() and not curState.isLose():
                    legal = curState.getLegalPacmanActions()
                    successors = [(curState.generatePacmanSuccessor(action), action) for action in legal]
                    for successor in successors:
                        if successor[0] is not None and successor[0] not in visited:
                            pq.put((curNode.stepCost + 1 + admissibleHeuristic(successor[0]),
                                    StateNode(successor[0], curNode.stepCost + 1),
                                    curAction if curAction is not None else successor[1]))
                visited.append(curState)
        return bestAction

    def allNone(self, successors):
        for successor in successors:
            if successor[0] is not None:
                return False
        return True

class StateNode:
    def __init__(self, state, stepCost):
        self.state = state
        self.stepCost = stepCost


# input (totalCost, node, action)
class PriorityQueue(object):
    def __init__(self):
        self.data_list = [(None, None, None)]

    def size(self):
        return len(self.data_list) - 1

    def left_child(self, root):
        return root * 2

    def right_child(self, root):
        return root * 2 + 1

    def father(self, node):
        return node / 2

    def heapify(self, root):
        if root > self.size():
            return
        left_node = self.left_child(root)
        right_node = self.right_child(root)
        smallest = root
        if left_node <= self.size():
            if self.data_list[left_node][0] < self.data_list[smallest][0]:
                smallest = left_node

        if right_node <= self.size():
            if self.data_list[right_node][0] < self.data_list[smallest][0]:
                smallest = right_node

        if smallest != root:
            self.data_list[root], self.data_list[smallest] = self.data_list[smallest], self.data_list[root]
            self.heapify(smallest)

    def build_heap(self):
        for i in range(self.size() / 2, 0, -1):
            self.heapify(i)

    def get(self):
        if self.size() < 1:
            return None
        ret = self.data_list[1]
        self.data_list[1] = self.data_list[-1]
        del self.data_list[-1]
        self.heapify(1)
        return ret

    def put(self, data):
        self.data_list.append(data)
        now_index = self.size()
        pre = self.father(now_index)
        while now_index > 1 and self.data_list[pre][0] > data[0]:
            self.data_list[pre], self.data_list[now_index] = self.data_list[now_index], self.data_list[pre]
            now_index = pre
            pre = now_index / 2
