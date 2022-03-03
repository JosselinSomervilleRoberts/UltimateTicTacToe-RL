from agents.agent import Agent
import random
import math

class Node:
    #We need nodes to build a tree of game states

    def __init__(self, env, previousPlayer, previousAction=None, parent=None):
        self.previousAction = previousAction  # the move that got us to this node - "None" for the root node
        self.parent = parent  # "None" for the root
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untriedActions = env.valid_actions()  # future children to explore
        #TODO make sure right player begins
        self.previousPlayer = previousPlayer # the only part of the state that the Node needs later

    def selectChild(self):
        """select a child of the node using the UCB1 formula which balances exploration/exploitation"""
        #TODO?: possible to multiply one of the terms by a factor to balance exploration and exploitation
        sortedChildren = sorted(self.children, key=lambda node: node.wins / node.visits + math.sqrt(2*math.log(self.visits / node.visits)))
        return sortedChildren[-1]

    def addChild(self, action, env):
        child = Node(env, previousPlayer = 3-self.previousPlayer, previousAction=action, parent=self)
        self.untriedActions.remove(action)
        self.children.append(child)
        return child

def getResult(winner, player):
    """returns the result of the finished game from the pov of player:
    -> 0 if loss/ 1 if win/ 0.5 if draw"""
    if winner == player: #win
        return 1
    elif winner == 3 - player: #loss
        return 0
    else: #draw
        return 0.5
        
def UCT(rootEnv, previousPlayer, nb_iter):
    rootNode = Node(rootEnv, previousPlayer)
    rootState = rootEnv.getState()

    for i in range(nb_iter):
        node = rootNode
        # Selection
        while node.untriedActions == [] and node.children != []:
            # explore tree until a node can be expanded/is terminal
            node = node.selectChild()
            rootEnv.ultra_fast_step(node.previousAction) #TODO: check if modifies action maybe?
        #print("         selection")

        # Expansion
        if node.untriedActions != []:
            # node is not terminal
            action = random.choice(node.untriedActions)
            done = rootEnv.ultra_fast_step(action) #TODO: check if modifies action maybe?
            node = node.addChild(action, rootEnv) # add child and get it as current node
        #print("         expansion")

        # Simulation
        while not done:
            actions = rootEnv.valid_actions()
            done = rootEnv.ultra_fast_step(random.choice(actions))
        winner = rootEnv.pygame.board.state
        #print("         simulation")
        
        # Back Propagation
        while node is not None:
            """update a node given the result of the simulation,
            from the perspective of previousPlayer"""
            #backpropagate result from the expanded node to the root
            node.visits += 1
            node.wins += getResult(winner, node.previousPlayer)
            node = node.parent
        #print("         backpropagation")

        #restore rootEnv
        rootEnv.restoreFromState(rootState)

    #return the best child of the root node
    sortedChildren = sorted(rootNode.children, key = lambda node: node.visits)
    return sortedChildren[-1].previousAction

class MCTSAgent(Agent):

    def __init__(self, player = 1, nb_iter = 1000):
        super().__init__(player)
        self.nb_iter = nb_iter

    def getAction(self, env, observation):
        #action = env.action_space.sample()
        #TODO: find good value for nb_iter
        action = UCT(env, 3 - self.player, self.nb_iter)
        #print("MCTS chose an action!")
        return action