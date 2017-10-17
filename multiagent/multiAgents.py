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
from util import PriorityQueue
from game import Directions
import random, util

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

        "*** YOUR CODE HERE ***"
        def helper(current, act, dep = 3, visited=[]):
          successorGameState = current.generatePacmanSuccessor(act)
          newPos = successorGameState.getPacmanPosition()
          newFood = successorGameState.getFood()
          newGhostStates = successorGameState.getGhostStates()
          newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
          legalMoves = successorGameState.getLegalActions()
          Food = current.getFood()
          Pos = current.getPacmanPosition()
          if newPos not in visited:
            visited.append(newPos)
          else:
            return 0
          s = 0
          n = 0
          flag = 0
          a = []
          fc = Food.count()
          nfc = newFood.count()
          if Food.asList():
            tmp = Food.asList()[0]

          for i in range(len(newGhostStates)):
            gp = newGhostStates[i].getPosition()
            a.append(manhattanDistance(gp,newPos))
            if a[i] == 0:
              s -= 10
              flag = 1
            elif a[i] < 4:
              s -= 10.0/a[i]
              flag = 1
          if flag:
            return s
          
          if fc > nfc:
            s += 30
            
          if dep == 1 or abs(s) > 0.001 or act == "Stop":
            return s
          for x in legalMoves:
            n += helper(successorGameState, x, dep-1,visited)
          return s+n/(len(legalMoves)+1)*0.8

        score = helper(currentGameState, action)
        return score

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
        """
        "*** YOUR CODE HERE ***"
        def helper(gameState, depth, index):
          # Collect legal moves and successor states
          legalMoves = gameState.getLegalActions(index)
          # print depth, index, legalMoves
          if len(legalMoves) == 0:
            return ()
          flag = 0
          scores = []

          if index == gameState.getNumAgents()-1:
            if depth == 1:
              flag = 1
              scores = [self.evaluationFunction(gameState.generateSuccessor(index, action)) for action in legalMoves]
            else:
              nextIndex = 0
              depth -= 1
          else:
            nextIndex = index+1

          if flag == 0:
            for action in legalMoves:
              tmp = helper(gameState.generateSuccessor(index, action), depth, nextIndex)
              if tmp == ():
                scores.append(self.evaluationFunction(gameState.generateSuccessor(index, action)))
              else:
                scores.append(tmp[0])

          # print depth, index, len(legalMoves)
          # print scores
          if index == 0:
            bestScore = max(scores)
          else:
            bestScore = min(scores)

          bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
          chosenIndex = random.choice(bestIndices) # Pick randomly among the best

          return bestScore, chosenIndex

        legalMoves = gameState.getLegalActions(0)
        return legalMoves[helper(gameState, self.depth, 0)[1]]





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def helper(gameState, depth, index, mini = 100000, maxi = -100000):
          # Collect legal moves and successor states
          legalMoves = gameState.getLegalActions(index)
          # print depth, index, legalMoves
          if len(legalMoves) == 0:
            return ()
          flag = 0
          scores = []
          bestScore = 0
          chosenAction = -1

          if index == gameState.getNumAgents()-1:
            if depth == 1:
              flag = 1
              for action in legalMoves:
                tmp = self.evaluationFunction(gameState.generateSuccessor(index, action))
                scores.append(tmp)
                if tmp < maxi:
                  bestScore = tmp
                  chosenAction = action
                  break
                mini = min(tmp, mini)
            else:
              nextIndex = 0
              depth -= 1
          else:
            nextIndex = index+1

          if flag == 0:
            for action in legalMoves:
              re = helper(gameState.generateSuccessor(index, action), depth, nextIndex, mini, maxi)
              if re == ():
                tmp = self.evaluationFunction(gameState.generateSuccessor(index, action))
              else:
                tmp = re[0]
              scores.append(tmp)
              if index == 0:
                if tmp > mini:
                  bestScore = tmp
                  chosenAction = action
                  break
                else:
                  maxi = max(tmp, maxi)
              else:
                if tmp < maxi:
                  bestScore = tmp
                  chosenAction = action
                  break
                else:
                  mini = min(tmp, mini)


          # print depth, index, len(legalMoves)
          # print scores
          if chosenAction == -1:
            if index == 0:
              bestScore = max(scores)
            else:
              bestScore = min(scores)

            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = random.choice(bestIndices) # Pick randomly among the best
            chosenAction = legalMoves[chosenIndex]

          return bestScore, chosenAction

        return helper(gameState, self.depth, 0)[1]

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
        def helper(gameState, depth, index):
          # Collect legal moves and successor states
          legalMoves = gameState.getLegalActions(index)
          # print depth, index, legalMoves
          if len(legalMoves) == 0:
            return ()
          flag = 0
          scores = []

          if index == gameState.getNumAgents()-1:
            if depth == 1:
              flag = 1
              scores = [self.evaluationFunction(gameState.generateSuccessor(index, action)) for action in legalMoves]
            else:
              nextIndex = 0
              depth -= 1
          else:
            nextIndex = index+1

          if flag == 0:
            for action in legalMoves:
              tmp = helper(gameState.generateSuccessor(index, action), depth, nextIndex)
              if tmp == ():
                scores.append(self.evaluationFunction(gameState.generateSuccessor(index, action)))
              else:
                scores.append(tmp[0])

          # print depth, index, len(legalMoves)
          # print scores
          if index == 0:
            bestScore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = random.choice(bestIndices) # Pick randomly among the best
          else:
            return sum(scores)/len(scores), -1

          return bestScore, chosenIndex

        legalMoves = gameState.getLegalActions(0)
        return legalMoves[helper(gameState, self.depth, 0)[1]]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    def helper(current, dep = 2, visited={}):
          # successorGameState = current.generatePacmanSuccessor(act)
          # newPos = successorGameState.getPacmanPosition()
          # newFood = successorGameState.getFood()
          # newGhostStates = successorGameState.getGhostStates()
          # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
          legalMoves = current.getLegalActions()
          Food = current.getFood()
          capsule = current.getCapsules()
          ghostStates = current.getGhostStates()
          scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
          Pos = current.getPacmanPosition()
          s = 0
          n = 0
          flag = 0
          a = []
          if Pos in visited:
            return visited[Pos]

          s = -200*Food.count()
          for k in Food.asList():
              s += -manhattanDistance(k,Pos)

          for x in capsule:
            s += -10*manhattanDistance(x, Pos)

          for i in range(len(ghostStates)):
            gp = ghostStates[i].getPosition()
            if scaredTimes[i] > 2:
              if manhattanDistance(gp, Pos) <= 1:
                s += 300
              else:
                s += -20*manhattanDistance(gp, Pos)
              continue
            a.append(manhattanDistance(gp,Pos))
            if a[i] == 0:
              s -= 1000
              flag = 1
            elif a[i] < 4:
              s -= 10.0/a[i]
              flag = 1
          return s
    return helper(currentGameState)

# Abbreviation
better = betterEvaluationFunction

