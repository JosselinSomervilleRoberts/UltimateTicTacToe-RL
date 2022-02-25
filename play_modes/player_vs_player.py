from basic_env import UltimateTicTacToeEnv
import pygame


if __name__ == '__main__':
    env = UltimateTicTacToeEnv()
    obs = env.reset()

    game = True
    while game:
        pygame.time.delay(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit cross
                game = False
            if event.type == pygame.MOUSEBUTTONUP: # Mouse click released
                x, y = pygame.mouse.get_pos()
                env.pygame.board.click(x, y)
        # Render the game
        env.pygame.view(True)
        

    pygame.quit()
    env.close()