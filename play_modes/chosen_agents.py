from basic_env import UltimateTicTacToeEnv
import pygame

from agents.agent_player import PlayerAgent
from agents.agent_random import RandomAgent
from agents.agent_minimax import MinimaxAgent

agent1 = MinimaxAgent(1)
agent2 = RandomAgent(2)
display = True

if __name__ == '__main__':
    env = UltimateTicTacToeEnv()
    obs = env.reset()

    done = False
    while not(done):

        # Get the agent whose turn it is
        agent = agent1 if (env.pygame.board.currentPlayer == 1) else agent2
        
        # Ask the agent to choose an action
        action = agent.getAction(env, obs)

        # If the aciton is negative this means that the agent asks to close the game
        if action < 0:
            done = True

        # Otherwise, if the action is valid we play it in the env
        elif action < 81:
            obs, reward, done, info = env.step(action)

        if display:
            # Render the environment
            env.render()

            # Check for pygame event (to close the window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit cross
                    done = True

            # Delay to not spam
            pygame.time.delay(1)
        
    pygame.quit()
    print("ENV state:", env.pygame.board.state)
    env.close()