

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

agent2 = RandomAgent(2) #, 6, True)
agent1 = DQNAgent(1,SinglePlayerEnv(RandomAgent(2)))
display = True

if __name__ == '__main__':
    env = TwoPlayerEnv()
    obs = env.reset()

    done = False
    game = True
    while game:

        if not(done):
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
                #print("REWARD =", reward)

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