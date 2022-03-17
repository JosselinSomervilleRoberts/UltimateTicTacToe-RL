from agents.agent_minimax_pruning import MinimaxPruningAgent



class MinimaxPruningAgentSeveralRewards(MinimaxPruningAgent):

    def __init__(self, player = 1, stepMax = 4, rand = True, additionalSteps = 2, startMultipleAtXSteps = 20):
        super().__init__(player, stepMax, rand)
        self.additionalSteps = additionalSteps
        self.startMultipleAtXSteps = startMultipleAtXSteps

    def getAction(self, env, observation):
        env.pygame.plays += 1
        if env.pygame.plays >= self.startMultipleAtXSteps:
            action = super().getAction(env, observation, nbSteps=self.stepMax + self.additionalSteps, rewardMode=1)
            if self.expected_reward*(3-2*self.player) > 50: # The agent with simple reward has forecasted a victory
                pass
                print("ACTION CHOSEN BY SIMPLE: ", self.expected_reward)
            else: # Use complex reward on less steps
                action = super().getAction(env, observation, nbSteps=self.stepMax, rewardMode=2)
            return action
        else:
            return super().getAction(env, observation, nbSteps=self.stepMax, rewardMode=2)

