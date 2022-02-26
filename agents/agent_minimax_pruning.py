from json.encoder import INFINITY
from agents.agent import Agent
INFINITY = 1000


def minimaxPruning(env, depth, alpha = - INFINITY, beta = INFINITY, cumulated_reward = 0, done = False, maximize = True):
    if (depth == 0) or done:
        return None, cumulated_reward

    if maximize:
        maxEval = - INFINITY
        maxAction = None
        for action in env.valid_actions():
            reward, done = env.fast_step(action)
            move = env.getLastMove()
            _, eval = minimaxPruning(env, depth - 1, alpha, beta, cumulated_reward + reward, done, False)
            if eval > maxEval:
                maxEval = eval
                maxAction = action
            alpha = max(alpha, eval)
            env.undoMove(move)
            if beta <= alpha: break
        return maxAction, maxEval
    else:
        minEval = + INFINITY
        minAction = None
        for action in env.valid_actions():
            reward, done = env.fast_step(action)
            move = env.getLastMove()
            _, eval = minimaxPruning(env, depth - 1, alpha, beta, cumulated_reward + reward, done, True)
            if eval < minEval:
                minEval = eval
                minAction = action
            beta = min(beta, eval)
            env.undoMove(move)
            if beta <= alpha: break
        return minAction, minEval


class MinimaxPruningAgent(Agent):

    def __init__(self, player = 1, stepMax = 4):
        super().__init__(player)
        self.stepMax = stepMax

    def getAction(self, env, observation):
        action, expected_reward = minimaxPruning(env, self.stepMax, maximize=(self.player == 1))
        return action

    