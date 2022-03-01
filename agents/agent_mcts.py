from agents.agent import Agent
import random

class Node:
    #We need nodes to build a tree of game states

    def __init__(self, env, player, previousAction=None, parent=None):
        self.previousAction = previousAction  # the move that got us to this node - "None" for the root node
        self.parent = parent  # "None" for the root
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untriedActions = env.valid_actions()  # future children to explore
        #TODO make sure right player begins
        self.previousPlayer = 3 - player # the only part of the state that the Node needs later

    def selectChild(self):
        """select a child of the node using the UCB1 formula which balances exploration/exploitation"""
        #TODO?: possible to multiply one of the terms by a factor to balance exploration and exploitation
        sortedChildren = sorted(self.children, key=lambda node: node.wins / node.visits + sqrt(2*log(self.visits / node.visits)))
        return sortedChildren[-1]

    def addChild(self, action, env, player):
        child = Node(env, player, previousAction=action, parent=self)
        self.untriedActions.remove(action)
        self.children.append(child)

    def updateNode(self, result):
        """update a node given the result of the simulation,
        from the perspective of previousPlayer"""
        self.visits += 1
        self.wins += result

    def UCT(rootEnv, player, nb_iter):
        rootNode = Node(rootEnv, player)

        for i in range(nb_iter):
            node = rootNode
            env = rootEnv.getState()

            # Selection
            while node.untriedActions == [] and node.children != []:
                # explore tree until a node can be expanded/is terminal
                node = node.selectChild()
                env.fast_step(node.previousAction) #TODO: check if modifies action maybe?
            

            # Expansion
            if node.untriedActions:
                # node is not terminal
                action = random.choice(node.untriedActions)
                env.fast_step(action) #TODO: check if modifies action maybe?
                move = env.getLastMove()
                node = node.addChild(action, env, player) ## add child and get it as current node
            
            # Simulation
            done = False
            while not done:
                actions = env.valid_actions()
                if not actions:
                    done = True
                    break
                env.fast_step(random.choice(action))
            
            # BackPropagation
            while node is not None:
                #backpropagate result from the expanded node to the root
                node.visits += 1
                node.wins +=






class MCTSAgent(Agent):

    def __init__(self, player = 1):
        super().__init__(self)

    def getAction(self, env, observation):
        #action = env.action_space.sample()
        #TODO action =
        return action