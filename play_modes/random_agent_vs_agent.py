from envs.env_two_player import TwoPlayerEnv
import pygame


if __name__ == '__main__':
    env = TwoPlayerEnv()
    obs = env.reset()

    game = True
    while game:
        pygame.time.delay(1)

        # Take a random action
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        if done == True:
            game = False
        # Render the game
        env.render()
        
    pygame.quit()
    env.close()