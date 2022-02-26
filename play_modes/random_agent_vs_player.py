from basic_env import UltimateTicTacToeEnv
import pygame


if __name__ == '__main__':
    env = UltimateTicTacToeEnv()
    obs = env.reset()

    game = True
    while game:
        pygame.time.delay(1)

        if env.pygame.board.currentPlayer == 1: # Player
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit cross
                    game = False
                if event.type == pygame.MOUSEBUTTONUP: # Mouse click released
                    x, y = pygame.mouse.get_pos()
                    env.pygame.board.click(x, y)
            # Render the game
            env.pygame.view(True)

        else: # Agent
            # Take a random action
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            if done == True:
                game = False
            # Render the game
            env.render()

    pygame.quit()
    env.close()