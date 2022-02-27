from agents.agent import Agent
import random
INFINITY = 1000


def minimaxPruning(env, depth, alpha = - INFINITY, beta = INFINITY, cumulated_reward = 0, done = False, maximize = True, rand = True):
    if (depth == 0) or done:
        return None, cumulated_reward

    actions = env.valid_actions()
    newDepth = depth - 1
    if len(actions) > 9: newDepth = max(0, depth - 2)

    if maximize:
        maxEval = - INFINITY
        maxAction = None
        for action in actions:
            reward, done = env.fast_step(action)
            move = env.getLastMove()
            _, eval = minimaxPruning(env, newDepth, alpha, beta, cumulated_reward + reward, done, False, rand)
            if eval > maxEval:
                maxEval = eval
                maxAction = [action]
            elif eval == maxEval:
                maxAction.append(action)
            alpha = max(alpha, eval)
            env.undoMove(move)
            if beta <= alpha: break
        if rand: return random.choice(maxAction), maxEval
        else: return maxAction[0], maxEval

    else:
        minEval = + INFINITY
        minAction = None
        for action in actions:
            reward, done = env.fast_step(action)
            move = env.getLastMove()
            _, eval = minimaxPruning(env, newDepth, alpha, beta, cumulated_reward + reward, done, True, rand)
            if eval < minEval:
                minEval = eval
                minAction = [action]
            elif eval == minEval:
                minAction.append(action)
            beta = min(beta, eval)
            env.undoMove(move)
            if beta <= alpha: break
        if rand: return random.choice(minAction), minEval
        else: return minAction[0], minEval


class MinimaxPruningAgent(Agent):

    def __init__(self, player = 1, stepMax = 4, rand = True):
        super().__init__(player)
        self.stepMax = stepMax
        self.rand = rand

    def getAction(self, env, observation):
        action, expected_reward = minimaxPruning(env, self.stepMax, maximize=(self.player == 1), rand=self.rand)
        print("Expected reward:", expected_reward)
        return action

    