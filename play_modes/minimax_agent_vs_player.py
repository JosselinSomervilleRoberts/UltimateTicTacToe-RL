from basic_env import UltimateTicTacToeEnv
import pygame



def minimax(env, cumulated_reward = 0, step = 0, maximize = True):
    STEP_MAX = 4

    actions = env.valid_actions()
    state = env.getState()

    chosenMove = None
    chosenReward = 0
    for action in actions:

        obs, reward, done, info = env.step(action)
        r = cumulated_reward + reward
        a = None

        if not(done) and step + 1 < STEP_MAX:
            a, r = minimax(env, cumulated_reward + reward, step + 1, not(maximize))
        
        if (chosenMove is None) or (maximize and (r < chosenReward)) or (not(maximize) and (r > chosenReward)):
            chosenReward = r
            chosenMove = (action, a)

        env.restoreFromState(state)

    return chosenMove, chosenReward


if __name__ == '__main__':
    env = UltimateTicTacToeEnv()
    obs = env.reset()

    game = True
    while game:
        pygame.time.delay(1)

        if env.pygame.board.currentPlayer == 2: # Player
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
            action, expected_reward = minimax(env)
            print("Action:", action)
            print("Expected reward:", expected_reward)
            print("")
            obs, reward, done, info = env.step(action[0])
            if done == True:
                game = False
            # Render the game
            env.render()
        
    pygame.quit()
    env.close()