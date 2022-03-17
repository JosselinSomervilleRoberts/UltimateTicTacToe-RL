from agents.agent import Agent
import random
INFINITY = 1000


def minimaxPruning(env, depth, alpha = - INFINITY, beta = INFINITY, cumulated_reward = 0, done = False, maximize = True, rand = True, rewardMode = None):
    if(rewardMode != None):
        env.pygame.board.reward.mode = rewardMode

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
            _, eval = minimaxPruning(env, newDepth, alpha, beta, cumulated_reward + reward, done, False, rand = False)
            if eval > maxEval:
                maxEval = eval
                if rand: maxAction = [action]
                else: maxAction = action
            elif rand and eval == maxEval:
                maxAction.append(action)
            env.undoMove(move)
            alpha = max(alpha, eval)
            if beta <= alpha: break
        if rand: return random.choice(maxAction), maxEval
        else: return maxAction, maxEval

    else:
        minEval = + INFINITY
        minAction = None
        for action in actions:
            reward, done = env.fast_step(action)
            move = env.getLastMove()
            _, eval = minimaxPruning(env, newDepth, alpha, beta, cumulated_reward + reward, done, True, rand = False)
            if eval < minEval:
                minEval = eval
                if rand: minAction = [action]
                else: minAction = action
            elif rand and eval == minEval:
                minAction.append(action)
            env.undoMove(move)
            beta = min(beta, eval)
            if beta <= alpha: break
        if rand: return random.choice(minAction), minEval
        else: return minAction, minEval


class MinimaxPruningAgent(Agent):

    def __init__(self, player = 1, stepMax = 4, rand = True, rewardMode = 2):
        super().__init__(player)
        self.stepMax = stepMax
        self.rand = rand
        self.rewardMode = rewardMode
        self.expected_reward = 0

    def getAction(self, env, observation, rewardMode = None, nbSteps = None):
        if rewardMode is None: 
            rewardMode = self.rewardMode

        if nbSteps is None:
            nbSteps = self.stepMax

        action, expected_reward = minimaxPruning(env, nbSteps, maximize=(self.player == 1), rand=self.rand, rewardMode=rewardMode)
        self.expected_reward = expected_reward
        return action

