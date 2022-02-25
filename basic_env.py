import gym
from game.ultimatetictactoe import UltimateTicTacToe
import numpy as np

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

    def valid_actions(self):
        return self.pygame.board.getListOfPossibleMoves()

    def getState(self):
        b = self.pygame.board
        return (np.array(b.grid).copy(), np.array(b.largeGrid).copy(), np.array(b.possible).copy(), b.currentPlayer, b.state)

    def restoreFromState(self, state):
        b = self.pygame.board
        b.grid = state[0].copy().tolist()
        b.largeGrid = state[1].copy().tolist()
        b.possible = state[2].copy().tolist()
        b.currentPlayer = state[3]
        b.state = state[4]