
'''
# necessary for Marie
import sys
sys.path.append("C:\\Users\\Marie\\Organisation_Marie\\X\\3A\\INF 581 - Advanced machine learning\\Project\\UltimateTicTacToe-RL")
'''

# for Astrid
import sys
sys.path.append("/home/astrid/Documents/X/3A/P2/INF581 - Machine Learning and Autonomous Agents/project/UltimateTicTacToe-RL/")


from envs.env_single_player import SinglePlayerEnv
import pygame

from agents.agent_player import PlayerAgent
from agents.agent_random import RandomAgent
from agents.agent_minimax import MinimaxAgent
from agents.agent_minimax_pruning import MinimaxPruningAgent
from agents.agent_minimax_several_rewards import MinimaxPruningAgentSeveralRewards
from agents.agent_mcts import MCTSAgent

#agent = MinimaxPruningAgent(1, 5, True)
agent = PlayerAgent(1)#MinimaxPruningAgentSeveralRewards(1, 5, False, 3, 15)
#agent = MinimaxPruningAgent(1)
display = True

if __name__ == '__main__':
    agent2 =  MCTSAgent(2, 2000)#MinimaxPruningAgentSeveralRewards(2, 5, False, 2, 15)#MinimaxPruningAgent(2, 5, True)
    #agent2 = RandomAgent(1)
    env = SinglePlayerEnv(agent2)
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