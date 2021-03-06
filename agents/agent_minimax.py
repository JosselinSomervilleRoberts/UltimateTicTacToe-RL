from agents.agent import Agent


def minimax(env, stepMax, cumulated_reward = 0, step = 0, maximize = True):
    actions = env.valid_actions()

    chosenMove = None
    chosenReward = 0
    for action in actions:

        reward, done = env.fast_step(action)
        move = env.getLastMove()
        r = cumulated_reward + reward

        if not(done) and step + 1 < stepMax:
            _, r = minimax(env, stepMax, cumulated_reward + reward, step + 1, not(maximize))
        
        if (chosenMove is None) or (maximize and (r > chosenReward)) or (not(maximize) and (r < chosenReward)):
            chosenReward = r
            chosenMove = action

        env.undoMove(move)

    return chosenMove, chosenReward


class MinimaxAgent(Agent):

    def __init__(self, player = 1, stepMax = 4):
        super().__init__(player)
        self.stepMax = stepMax

    def getAction(self, env, observation):
        action, expected_reward = minimax(env, self.stepMax, maximize=(self.player == 1))
        return action

    