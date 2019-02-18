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
        root = StateNode(state, None, 0)
        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal
                      if state.generatePacmanSuccessor(action) is not None]
        if successors is not None and len(successors) > 0 and not state.isWin():
            queue = []
            for successor in successors:
                node = StateNode(successor[0], successor[1], root.stepCost + 1)
                queue.append((node, node.action))
            minCost = MAX_VALUE
            bestAction = None
            visited = [root.state]
            while len(queue) > 0:
                size = len(queue)
                for i in range(0, size):
                    curNode, curAction = queue.pop(0)
                    curState = curNode.state
                    if curState not in visited:
                        legal = curState.getLegalPacmanActions()
                        successors = [(curState.generatePacmanSuccessor(action), action) for action in legal
                                      if curState.generatePacmanSuccessor(action) is not None]
                        if successors is None or len(successors) == 0 or curState.isWin():
                            if minCost > curNode.stepCost + admissibleHeuristic(curState):
                                minCost = curNode.stepCost + admissibleHeuristic(curState)
                                bestAction = curAction
                        else:
                            for successor in successors:
                                if successor[0] is not None and successor[0] not in visited:
                                    queue.append((StateNode(successor[0], successor[1], curNode.stepCost + 1), curAction))
                        visited.append(curState)
            print(minCost)
            return bestAction
        else:
            return Directions.STOP


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        root = StateNode(state, None, 0)
        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal
                      if state.generatePacmanSuccessor(action) is not None]
        if successors is not None and len(successors) > 0 and not state.isWin():
            stack = []
            for successor in successors:
                node = StateNode(successor[0], successor[1], root.stepCost + 1)
                stack.append((node, node.action))
            minCost = MAX_VALUE
            bestAction = None
            visited = [root.state]
            while len(stack) > 0:
                curNode, curAction = stack.pop()
                curState = curNode.state
                if curState not in visited:
                    legal = curState.getLegalPacmanActions()
                    successors = [(curState.generatePacmanSuccessor(action), action) for action in legal
                                  if curState.generatePacmanSuccessor(action) is not None]
                    if successors is None or len(successors) == 0 or curState.isWin():
                        if minCost > curNode.stepCost + admissibleHeuristic(curState):
                            minCost = curNode.stepCost + admissibleHeuristic(curState)
                            bestAction = curAction
                    else:
                        for successor in successors:
                            if successor[0] is not None and successor[0] not in visited:
                                stack.append((StateNode(successor[0], successor[1], curNode.stepCost + 1), curAction))
                    visited.append(curState)
            print(minCost)
            return bestAction
        else:
            return Directions.STOP


class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        root = StateNode(state, None, 0)
        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal
                      if state.generatePacmanSuccessor(action) is not None]
        if successors is not None and len(successors) > 0 and not state.isWin():
            pq = PriorityQueue()
            for successor in successors:
                node = StateNode(successor[0], successor[1], root.stepCost + 1)
                pq.put((node.stepCost + admissibleHeuristic(node.state), node, node.action))
            minCost = MAX_VALUE
            bestAction = None
            visited = [root.state]
            while pq.size() > 0:
                _, curNode, curAction = pq.get()
                curState = curNode.state
                if curState not in visited:
                    legal = curState.getLegalPacmanActions()
                    successors = [(curState.generatePacmanSuccessor(action), action) for action in legal
                                  if curState.generatePacmanSuccessor(action) is not None]
                    if successors is None or len(successors) == 0 or curState.isWin():
                        if minCost > curNode.stepCost + admissibleHeuristic(curState):
                            minCost = curNode.stepCost + admissibleHeuristic(curState)
                            bestAction = curAction
                    else:
                        for successor in successors:
                            if successor[0] is not None and successor[0] not in visited:
                                pq.put((curNode.stepCost + 1 + admissibleHeuristic(successor[0]),
                                        StateNode(successor[0], successor[1], curNode.stepCost + 1),
                                        curAction))
                    visited.append(curState)
            print minCost
            return bestAction
        else:
            return Directions.STOP


class StateNode:
    def __init__(self, state, action, stepCost):
        self.state = state
        self.action = action
        self.stepCost = stepCost


# input (totalCost, node, action)
class PriorityQueue(object):
    def __init__(self):
        self.data_list = []

    def size(self):
        return len(self.data_list) - 1

    def left_child(self, root):
        return (root + 1) * 2 - 1

    def right_child(self, root):
        return (root + 1) * 2 + 1 - 1

    def father(self, node):
        return (node + 1) / 2 - 1

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
        for i in range(self.size()/2, 0, -1):
            self.heapify(i)

    def get(self):
        if self.size() == 0:
            return None
        ret = self.data_list[0]
        self.data_list[0] = self.data_list[-1]
        del self.data_list[-1]
        self.heapify(0)
        return ret

    def put(self, data):
        self.data_list.append(data)
        now_index = self.size()
        pre = self.father(now_index)
        while self.data_list[pre][0] > data[0] and now_index != 1:
            self.data_list[pre], self.data_list[now_index] = self.data_list[now_index], self.data_list[pre]
            now_index = pre
            pre = now_index / 2

