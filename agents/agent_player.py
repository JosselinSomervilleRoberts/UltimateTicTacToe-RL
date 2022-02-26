from agents.agent import Agent
import pygame


class PlayerAgent(Agent):

    def __init__(self, player = 1):
        super().__init__(player)

    def getAction(self, env, observation):
        while True:
            pygame.time.delay(1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit cross
                    return -1
                if event.type == pygame.MOUSEBUTTONUP: # Mouse click released
                    x, y = pygame.mouse.get_pos()
                    action = env.pygame.board.getActionFromClick(x, y)
                    if action >= 0:
                        return action

            # Render the game
            env.pygame.view(True)