from basic_env import UltimateTicTacToeEnv
import pygame



def minimax(env, cumulated_reward = 0, step = 0):
    STEP_MAX = 4

    actions = env.valid_actions()
    state = env.getState()

    chosenMove = None
    chosenReward = 0
    for action in actions:

        obs, reward, done, info = env.step(action)
        r = cumulated_reward + reward

        if not(done) and step + 1 < STEP_MAX:
            _, r = minimax(env, r, step + 1)
        
        if (chosenMove is None) or (step%2==0 and r > chosenReward) or (step%2==1 and r < chosenReward):
            chosenReward = r
            chosenMove = action

        env.restoreFromState(state)

    return chosenMove, chosenReward


if __name__ == '__main__':
    env = UltimateTicTacToeEnv()
    obs = env.reset()

    game = True
    while game:
        pygame.time.delay(1)

        if env.pygame.board.currentPlayer == 1: # Player
            # Take a random action
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            if done == True:
                game = False
            # Render the game
            env.render()

        else: # Agent
            # Take a random action
            action, expected_reward = minimax(env)
            obs, reward, done, info = env.step(action)
            if done == True:
                game = False
            # Render the game
            env.render()
        
    pygame.quit()
    env.close()