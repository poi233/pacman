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
import sys


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
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        return Directions.STOP


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        root = TreeNode(state, None, 0, [])
        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal
                      if state.generatePacmanSuccessor(action) is not None]
        if successors is not None and len(successors) > 0 and not state.isWin():
            for successor in successors:
                if successor[0] is not None:
                    root.children.append(TreeNode(successor[0], successor[1], root.stepCost + 1, []))
            min = sys.maxint
            bestAction = None
            for child in root.children:
                minCost = self.dfs(child, [root.state])
                if minCost < min:
                    min = minCost
                    bestAction = child.action
            return bestAction
        else:
            return Directions.STOP

    def dfs(self, node, visited):
        state = node.state
        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal
                      if state.generatePacmanSuccessor(action) is not None]
        for successor in successors:
            if successor[0] is not None:
                node.children.append(TreeNode(successor[0], successor[1], node.stepCost + 1, []))
        if successors is None or len(successors) == 0 or state.isWin():
            return node.stepCost + admissibleHeuristic(state)
        minCost = sys.maxint
        for child in node.children:
            if child.state not in visited:
                minCost = min(minCost, self.dfs(child, visited + [child.state]))
        return minCost


class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        visitedStates = []
        heap = PQ()
        heap.put((admissibleHeuristic(state), state, [], 0))
        bestScore, curState, actions, totalCost = heap.get()
        visitedStates.append((state, bestScore))
        while not curState.isWin():
            legal = curState.getLegalPacmanActions()
            successors = [(curState.generatePacmanSuccessor(action), action) for action in legal]
            for successorState, action in successors:
                if successorState is None:
                    print actions
                    print bestScore
                    return actions[0]
                visitedExit = False
                totalCost = totalCost + scoreEvaluation(successorState)
                for (vCost, vState) in visitedStates:
                    if successorState == vState and totalCost >= vCost:
                        visitedExit = True
                        break
                if not visitedExit:
                    heap.put((totalCost + admissibleHeuristic(successorState), successorState, actions + [action],
                              totalCost))
                    visitedStates.append((successorState, totalCost))
            bestScore, curState, actions, totalCost = heap.get()

        return actions[0]


class TreeNode:

    def __init__(self, state, action, stepCost, children):
        self.state = state
        self.action = action
        self.stepCost = stepCost
        self.children = children
