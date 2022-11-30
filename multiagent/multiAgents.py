# multgameState=None-------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        foodList = newFood.asList()

        nearestFood = len(foodList)
        if len(foodList) != 0:
            nearestFood = util.manhattanDistance(newPos, foodList[0])
        nearestGhost = util.manhattanDistance(newPos, newGhostStates[0].getPosition())

        for food in foodList:
            foodDistance = util.manhattanDistance(newPos, food)
            if foodDistance < nearestFood:
                nearestFood = foodDistance

        for ghost in newGhostStates:
            ghostDistance = util.manhattanDistance(newPos, ghost.getPosition())
            if ghostDistance < nearestGhost:
                nearestGhost = ghostDistance





        # print(action)
        # print(successorGameState.getScore())
        # print(successorGameState.getScore())


        "*** YOUR CODE HERE ***"
        return successorGameState.getScore() - nearestFood + nearestGhost


def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        "*** YOUR CODE HERE ***"
        #print(gameState.getNumAgents())
        # paccy = gameState.getLegalActions(0)
        # g = gameState.getLegalActions(1)
        # print(gameState.getLegalActions(0), "For paccy")
        # print(gameState.getLegalActions(1), "for g-dawg")
        # print(gameState.generateSuccessor(0), paccy[0])
        # print(gameState.generateSuccessor(0), paccy[1])
        # print(gameState.generateSuccessor(1), g[0])
        # print(gameState.generateSuccessor(1), g[1])
        # depth = 0
        # bestAction = None
        #
        # while depth != self.depth:
        #
        #     bestAction = self.value(gameState, self.index, self.depth)
        #     depth += 1
        #
        # return bestAction
        bestAction = self.maxValue(gameState, 0, 0)
        return bestAction[1]
       # return self.maxValue(gameState, 0, 0)[1]



    def maxValue(self, gameState, index, depth):

        v = (-(100 ** 100), "")
        legalAction = gameState.getLegalActions(index)
        numOfAgents = gameState.getNumAgents()
        for action in legalAction:
            newGameState = gameState.generateSuccessor(index, action)
            newDepth = depth + 1
            newIndex = (index + 1) % numOfAgents
            dispatch = self.value(newGameState, newIndex, newDepth, action)
            if dispatch[0] > v[0]:
                v = (dispatch[0], action)

        return v

    def minValue(self, gameState, index, depth):

        v = (100 ** 100, "")
        legalAction = gameState.getLegalActions(index)
        numOfAgents = gameState.getNumAgents()
        for action in legalAction:
            newGameState = gameState.generateSuccessor(index, action)
            newDepth = depth + 1
            newIndex = (index + 1) % numOfAgents
            dispatch = self.value(newGameState, newIndex, newDepth, action)
            if dispatch[0] < v[0]:
                v = (dispatch[0], action)

        return v

    def value(self, gameState, index, depth, action):

        if depth >= self.depth * gameState.getNumAgents():
            return (self.evaluationFunction(gameState), action)
        elif gameState.isWin():
            return (self.evaluationFunction(gameState), action)
        elif gameState.isLose():
            return (self.evaluationFunction(gameState), action)
        elif index == 0:
            return self.maxValue(gameState, index, depth)
        else:
            return self.minValue(gameState, index, depth)




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
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
        "*** YOUR CODE HERE ***"
        # print(gameState.getNumAgents())
        # paccy = gameState.getLegalActions(0)
        # g = gameState.getLegalActions(1)
        # print(gameState.getLegalActions(0), "For paccy")
        # print(gameState.getLegalActions(1), "for g-dawg")
        # print(gameState.generateSuccessor(0), paccy[0])
        # print(gameState.generateSuccessor(0), paccy[1])
        # print(gameState.generateSuccessor(1), g[0])
        # print(gameState.generateSuccessor(1), g[1])
        # depth = 0
        # bestAction = None
        #
        # while depth != self.depth:
        #
        #     bestAction = self.value(gameState, self.index, self.depth)
        #     depth += 1
        #
        # return bestAction
        bestAction = self.maxValue(gameState, 0, 0, -(100 ** 100), 100 ** 100)
        return bestAction[1]
        # return self.maxValue(gameState, 0, 0)[1]

    def maxValue(self, gameState, index, depth, alpha, beta):

        v = (-(100 ** 100), "")
        legalAction = gameState.getLegalActions(index)
        numOfAgents = gameState.getNumAgents()
        for action in legalAction:
            newGameState = gameState.generateSuccessor(index, action)
            newDepth = depth + 1
            newIndex = (index + 1) % numOfAgents
            dispatch = self.value(newGameState, newIndex, newDepth, action, alpha, beta)
            if dispatch[0] > v[0]:
                v = (dispatch[0], action)
            if v[0] > beta:
                return v
            alpha = max(alpha, v[0])

        return v

    def minValue(self, gameState, index, depth, alpha, beta):

        v = (100 ** 100, "")
        legalAction = gameState.getLegalActions(index)
        numOfAgents = gameState.getNumAgents()
        for action in legalAction:
            newGameState = gameState.generateSuccessor(index, action)
            newDepth = depth + 1
            newIndex = (index + 1) % numOfAgents
            dispatch = self.value(newGameState, newIndex, newDepth, action, alpha, beta)
            if dispatch[0] < v[0]:
                v = (dispatch[0], action)
            if v[0] < alpha:
                return v
            beta = min(beta, v[0])


        return v

    def value(self, gameState, index, depth, action, alpha, beta):

        if depth >= self.depth * gameState.getNumAgents():
            return (self.evaluationFunction(gameState), action, alpha, beta)
        elif gameState.isWin():
            return (self.evaluationFunction(gameState), action, alpha, beta)
        elif gameState.isLose():
            return (self.evaluationFunction(gameState), action, alpha, beta)
        elif index == 0:
            return self.maxValue(gameState, index, depth, alpha, beta)
        else:
            return self.minValue(gameState, index, depth, alpha, beta)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
