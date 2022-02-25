from game.board import Board
import pygame
import numpy as np
import gym

class UltimateTicTacToe:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Board.SIZE, Board.SIZE + Board.BOTTOM_SIZE))
        self.board = Board()
        self.error = 0
        self.action_space = gym.spaces.Discrete(81)
        self.observation_space = gym.spaces.MultiDiscrete([3]*81)

    def observe(self):
        return np.array(self.board.grid).flatten()

    def is_done(self):
        return (self.board.state != 0)

    def do_action(self, action):
        iySmall = action % 3
        action = int((action - iySmall) // 3)
        ixSmall = action % 3
        action = int((action - ixSmall) // 3)
        iyLarge = action % 3
        action = int((action - iyLarge) // 3)
        ixLarge = action % 3
        self.error = self.board.play(ixLarge, iyLarge, ixSmall, iySmall)

    def evaluate(self):
        return - self.error

    def view(self, blink):
        self.board.draw(self.screen, blink)
        pygame.display.flip()