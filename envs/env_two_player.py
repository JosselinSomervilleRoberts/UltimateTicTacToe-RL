import gym
from game.ultimatetictactoe import UltimateTicTacToe
import numpy as np


class TwoPlayerEnv(gym.Env):

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

    def fast_step(self, action):
        self.pygame.do_action(action)
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return reward, done
    
    def ultra_fast_step(self, action): #does not compute reward
        self.pygame.do_action_ultra_fast(action)
        done = self.pygame.is_done()
        return done        

    def render(self, mode="human", close=False):
        self.pygame.view(False)

    def valid_actions(self):
        return self.pygame.board.getListOfPossibleMoves()

    def getState(self):
        b = self.pygame.board
        return (b.grid.copy(), b.largeGrid.copy(), b.possible.copy(), b.currentPlayer, b.state)

    def restoreFromState(self, state):
        b = self.pygame.board
        b.grid = state[0].copy()
        b.largeGrid = state[1].copy()
        b.possible = state[2].copy()
        b.currentPlayer = state[3]
        b.state = state[4]

    def getLastMove(self):
        return self.pygame.move

    def undoMove(self, move):
        if move is None or len(move) == 0: return
        self.pygame.board.possible = move[0]
        self.pygame.board.grid[move[1]] = 0
        if len(move) > 2: self.pygame.board.largeGrid[move[2]] = 0
        self.pygame.board.currentPlayer = 3 - self.pygame.board.currentPlayer
        self.pygame.board.state = 0