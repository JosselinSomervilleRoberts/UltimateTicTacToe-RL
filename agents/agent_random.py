from agents.agent import Agent


class RandomAgent(Agent):

    def __init__(self, player = 1):
        super().__init__(self)

    def getAction(self, env, observation):
        action = env.action_space.sample()
        return action