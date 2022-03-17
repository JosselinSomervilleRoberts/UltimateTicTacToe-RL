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
        self.move = None
        self.action_space = gym.spaces.Discrete(81)
        self.observation_space = gym.spaces.MultiDiscrete([3]*81 + [3]*9 + [2]*9)
        self.plays = 0

    def observe(self):
        return (self.board.grid, self.board.largeGrid, self.board.possible)

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
        self.error, self.move = self.board.play(ixLarge, iyLarge, ixSmall, iySmall)

    def do_action_ultra_fast(self, action):
        iySmall = action % 3
        action = int((action - iySmall) // 3)
        ixSmall = action % 3
        action = int((action - ixSmall) // 3)
        iyLarge = action % 3
        action = int((action - iyLarge) // 3)
        ixLarge = action % 3
        self.error = self.board.play_ultra_fast(ixLarge, iyLarge, ixSmall, iySmall)

    def evaluate(self):
        if self.error > 0: return -100
        return self.board.reward.value

    def view(self, blink):
        self.board.draw(self.screen, blink)
        pygame.display.flip()