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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState


BIGNUM = 1000000000
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

        "*** YOUR CODE HERE ***"
        # List of food and manhattan distance to food
        foodScore, ghostScore, totalFood = 100, 100, 0
        foodList = newFood.asList()
        for food in foodList:
            foodScore = min(foodScore, manhattanDistance(newPos, food)) # Manhattan distance to closest food
            totalFood += manhattanDistance(newPos, food) # Total manhattan distance to all food to encourage PacMan to move towards food

        # List of all ghost positions
        for ghost in newGhostStates:
            ghostScore = min(ghostScore, manhattanDistance(newPos, ghost.getPosition()))
        if ghostScore <  3: return 100 * ghostScore - 10000 # If ghost is too close then run away
        elif len(foodList) == 0: return 1000000 # If there is no food then the game is won
        else: 
            return - totalFood - foodScore*50 + manhattanDistance(newPos,currentGameState.getPacmanPosition()) * 1000 - len(foodList) *50 + 1000 * (len(currentGameState.getFood().asList()) - len(foodList)) # Else return score + foodScore - total
        #  -50 * foodScore - 100 * len(foodList) \
        #       + 1000 * manhattanDistance(newPos, currentGameState.getPacmanPosition()) \
        #        - totalFood + 1000 * (len(currentGameState.getFood().asList()) - len(foodList))# Else return score + foodScore - total
        
        
        # return successorGameState.getScore()

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

    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
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
        def value(state,  agentIndex, depth):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            if depth == self.depth:
                return self.evaluationFunction(state)
            elif agentIndex == 0:
                return max_value(state, agentIndex, depth)
            else:
                return min_value(state, agentIndex, depth)


        def max_value(state, agentIndex, depth):
            best_action = None
            v = float('-inf')
            for action in state.getLegalActions(agentIndex):
                successor_state = state.generateSuccessor(agentIndex, action)
                successor_value = value(successor_state, agentIndex + 1, depth)
                if successor_value > v:
                    v = successor_value
                    best_action = action
            if depth == 0:
                return best_action
            else:
                return v
            

        def min_value(state, agentIndex, depth):
            best_action = None
            v = float('inf')
            nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
            for action in state.getLegalActions(agentIndex):
                successor_state = state.generateSuccessor(agentIndex, action)
                if nextAgentIndex == 0:
                    successor_value = value(successor_state, nextAgentIndex, depth + 1)
                else:
                    successor_value = value(successor_state, nextAgentIndex, depth)
                if successor_value < v:
                    v = successor_value
                    best_action = action
            return v
        
        return value(gameState, 0, 0)
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
    
        def value(state,  agentIndex, depth, alpha, beta):
                if state.isWin() or state.isLose():
                    return self.evaluationFunction(state)
                if depth == self.depth:
                    return self.evaluationFunction(state)
                elif agentIndex == 0:
                    return max_value(state, agentIndex, depth, alpha, beta)
                else:
                    return min_value(state, agentIndex, depth, alpha, beta)


        def max_value(state, agentIndex, depth, alpha, beta):
            best_action = None
            v = float('-inf')
            for action in state.getLegalActions(agentIndex):
                successor_state = state.generateSuccessor(agentIndex, action)
                successor_value = value(successor_state, agentIndex + 1, depth, alpha, beta)
                if successor_value > v:
                    v = successor_value
                    best_action = action
                if v > beta:
                    return v
                alpha = max(alpha, v)
            if depth == 0:
                return best_action
            else:
                return v
            

        def min_value(state, agentIndex, depth, alpha, beta):
            best_action = None
            v = float('inf')
            nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
            for action in state.getLegalActions(agentIndex):
                successor_state = state.generateSuccessor(agentIndex, action)
                if nextAgentIndex == 0:
                    successor_value = value(successor_state, nextAgentIndex, depth + 1, alpha, beta)
                else:
                    successor_value = value(successor_state, nextAgentIndex, depth, alpha, beta)
                if successor_value < v:
                    v = successor_value
                    best_action = action
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

                    
        return value(gameState, 0, 0, float('-inf'), float('inf'))
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (refactored from minimax agent)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing expectimax.

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
        def value(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            elif agentIndex == 0:
                return max_value(state, agentIndex, depth)
            else:
                return exp_value(state, agentIndex, depth)

        def max_value(state, agentIndex, depth):
            best_action = None
            v = float('-inf')
            for action in state.getLegalActions(agentIndex):
                successor_state = state.generateSuccessor(agentIndex, action)
                successor_value = value(successor_state, agentIndex + 1, depth)
                if successor_value > v:
                    v = successor_value
                    best_action = action
            if depth == 0:
                return best_action
            else:
                return v

        def exp_value(state, agentIndex, depth):
            actions = state.getLegalActions(agentIndex)
            num_actions = len(actions)
            v = 0
            for action in actions:
                successor_state = state.generateSuccessor(agentIndex, action)
                if agentIndex == state.getNumAgents() - 1:
                    v += value(successor_state, 0, depth + 1)
                else:
                    v += value(successor_state, agentIndex + 1, depth)
            return v / num_actions

        return value(gameState, 0, 0)
    
    
def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Incorporates factors such as distance to nearest ghost,
    distance to nearest scared ghost, number of remaining food pellets,
    and the current score to calculate the evaluation score.
    """
    if currentGameState.isWin():
        return BIGNUM
    elif currentGameState.isLose():
        return -BIGNUM
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    walls = currentGameState.getWalls()
    dmap = walls.copy()
    stk = util.Queue()
    stk.push(pos)
    dmap[pos[0]][pos[1]] = 0
    dis = 0
    while not stk.isEmpty():  # use BFS to aim at the closest food if not disturbed
        x , y = stk.pop()
        dis = dmap[x][y] + 1
        if food[x][y]:
            break
        for v in [(0, 1) , (1, 0) , (0 , -1) , (-1 , 0)]:
            xn = x + v[0]
            yn = y + v[1]
            if dmap[xn][yn] == False:
                dmap[xn][yn] = dis
                stk.push((xn, yn))
    ret = 1 - dis
    ghosts = currentGameState.getGhostStates()
    for ghost in ghosts:
        if ghost.scaredTimer == 0:  # active ghost poses danger to the pacman
            ret -= 100 ** (1.6 - manhattanDistance(ghost.getPosition(), pos))
        else:  # bonus points for having a scared ghost 
            ret += 25
    ret -= 30 * food.count()  # bonus points for eating a food 
    return ret
        


# Abbreviation
better = betterEvaluationFunction
