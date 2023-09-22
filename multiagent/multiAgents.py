# multiAgents.py
# --------------
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



import enum
from hashlib import new
import numbers
from operator import truediv
from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        
        "*** YOUR CODE HERE ***"

        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        ## pacman maximizing - true - looking at next states picks the one with the maximum score
        ## ghosts minimizing - false - looking at next states picks the one with the minimum score 

        ## starts of with pacman, looking at each of his moves and running minimax on each possible state 
        bestScore = -10000000
        bestMove = None
        numberGhosts = gameState.getNumAgents()

        actions = gameState.getLegalActions(0) ## all pacman actions

        for action in actions : 

            successorState = gameState.generateSuccessor(0, action)
            score = self.miniMax(successorState, self.depth, False)

            if score > bestScore : 
                bestScore = score
                bestMove = action
        
        return bestMove

            
    def miniMax(self, state, depth, maximizing): ## return the score of the move 

        ## check if input state is winning state 
        if state.isWin(): 
            return self.evaluationFunction(state)
        elif state.isLose(): 
            return self.evaluationFunction(state)
        elif depth == 0: 
            return self.evaluationFunction(state)
        
        if maximizing : ## pacman who looks at ghosts moves and picks his best scenario
            bestScore = -10000000000
            numberGhosts = state.getNumAgents()
      

            for n in range(1, numberGhosts): 
                legalGhostActions = state.getLegalActions(n)
                for action in legalGhostActions: 
                    successorState = state.generateSuccessor(n, action)
                    if self.miniMax(successorState, depth, False) > bestScore: 
                        bestScore = self.miniMax(successorState, depth, False)
                      
            
            return bestScore

            
        elif not maximizing: ## ghosts looking at pacmans best moves and picks their best scenario 
            numberGhosts = state.getNumAgents()  
            bestScore = 100000000000
            legalPacActions = state.getLegalActions(0)
            
            for action in legalPacActions: 
                successorState = state.generateSuccessor(0, action)
                bestScore = min(bestScore, self.miniMax(successorState, depth-1, True))

            return bestScore


            



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"


        bestScore = -10000000
        alpha = -100000000
        betha = 100000000
        bestMove = None

        actions = gameState.getLegalActions(0) ## all pacman actions

        for action in actions : 

            successorState = gameState.generateSuccessor(0, action)
            score = self.minValue(successorState, self.depth, alpha, betha)

            if score > bestScore : 
                bestScore = score
                bestMove = action
        
        return bestMove

    def minValue(self, state, depth, alpha, betha): 
        if state.isWin() or state.isLose() : 
            return self.evaluationFunction(state)
        elif depth == 0: 
            return self.evaluationFunction(state)

        value = 1000000000

        pacActions = state.getLegalActions(0)
        pacStates = []

        for action in pacActions:
            successorState = state.generateSuccessor(0, action)
            pacStates.append(successorState)
        
        for pacState in pacStates: 
            newVal = self.maxValue(pacState, depth-1, alpha, betha, 1)
            if newVal < value: 
                value = newVal
            if newVal <= alpha: 
                return value
            if newVal < betha: 
                betha = newVal

        return value


    def maxValue(self, state, depth, alpha, betha, agentIndex): 
        if state.isWin() or state.isLose() : 
            return self.evaluationFunction(state)
        elif depth == 0: 
            return self.evaluationFunction(state)

        value = -1000000000
        newVal = value
        bestState = state

        ghostStates = []

        numGhosts = state.getNumAgents() - 1

        if agentIndex <= numGhosts: 

            ghostActions = state.getLegalActions(agentIndex)
           
            for action in ghostActions:
                successorState = state.generateSuccessor(agentIndex, action)
                ghostStates.append(successorState)

            for ghostState in ghostStates:
                newVal = self.maxValue(bestState, depth, alpha, betha, agentIndex+1)
                if newVal > value:
                    value = newVal
                    bestState = ghostState
            
                    

        if agentIndex == numGhosts: 
            newVal = self.minValue(ghostState, depth-1, alpha, betha)
            if newVal > value: 
                value = newVal
            if newVal >= betha: 
                return value
            if newVal > alpha: 
                alpha = newVal

        return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

