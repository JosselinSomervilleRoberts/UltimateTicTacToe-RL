import gym
from game.ultimatetictactoe import UltimateTicTacToe

class UltimateTicTacToeEnv(gym.Env):

    def __init__(self):
        self.pygame = UltimateTicTacToe()
        self.action_space = gym.spaces.Discrete(81)
        self.observation_space = gym.spaces.MultiDiscrete([3]*81)

    def reset(self):
        del self.pygame
        self.pygame = UltimateTicTacToe()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.do_action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.view(False)