

# necessary for Marie
import sys
sys.path.append("C:\\Users\\Marie\\Organisation_Marie\\X\\3A\\INF 581 - Advanced machine learning\\Project\\UltimateTicTacToe-RL")


from envs.env_two_player import TwoPlayerEnv
from envs.env_single_player import SinglePlayerEnv
import pygame

from agents.agent_player import PlayerAgent
from agents.agent_random import RandomAgent
from agents.agent_minimax import MinimaxAgent
from agents.agent_minimax_pruning import MinimaxPruningAgent
from agents.agent_dqn import DQNAgent

agent2 = RandomAgent(2)#MinimaxPruningAgent(2, 3, True)
env = SinglePlayerEnv(agent2)

agent = DQNAgent(1, env, True, "_overnight_final")
#agent.learnNN(env, False, 10000, 500, "_overnight")
display = True


if __name__ == '__main__':
    obs = env.reset()

    done = False
    game = True
    while game:

        if not(done):
            # Ask the agent to choose an action
            action = agent.getAction(env, obs)

            # If the aciton is negative this means that the agent asks to close the game
            if action < 0:
                done = True

            # Otherwise, if the action is valid we play it in the env
            elif action < 81:
                obs, reward, done, info = env.step(action)
                print("REWARD:", reward)

        if display:
            # Render the environment
            env.render()

            # Check for pygame event (to close the window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit cross
                    game = False

            # Delay to not spam
            pygame.time.delay(1)

    pygame.quit()
    print("ENV state:", env.pygame.board.state)
    env.close()