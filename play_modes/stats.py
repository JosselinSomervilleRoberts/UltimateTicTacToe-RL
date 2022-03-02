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
from agents.agent_mcts import MCTSAgent
import tqdm

agents1 = [
    RandomAgent(1),
    MinimaxPruningAgent(1,1,True),
    MinimaxPruningAgent(1,3,True),
    MinimaxPruningAgent(1,3,False),
    MinimaxPruningAgent(1,5,True),
    MCTSAgent(1, 100),
    MCTSAgent(1, 500),
    MCTSAgent(1, 1000)
]

agents2 = [
    RandomAgent(2),
    MinimaxPruningAgent(2,1,True),
    MinimaxPruningAgent(2,3,True),
    MinimaxPruningAgent(2,3,False),
    MinimaxPruningAgent(2,5,True),
    MCTSAgent(2, 100),
    MCTSAgent(2, 500),
    MCTSAgent(2, 1000)
]

display = False

if __name__ == '__main__':
    N = 40
    n = len(agents1)
    wins = [[0 for i in range(n)] for j in range(n)]
    equalities = [[0 for i in range(n)] for j in range(n)]
    losses = [[0 for i in range(n)] for j in range(n)]
    env = SinglePlayerEnv(agents2[0])

    for it in tqdm.tqdm(range(N)):
        for i1 in range(n):
            for i2 in range(i1, n):
                #print(i1,i2)
                agent = agents1[i1]
                agent2 = agents2[i2]
                
                env.agent2 = agent2
                obs = env.reset()

                done = False
                game = True
                while not(done):

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

                if env.pygame.board.state == 1:
                    wins[i1][i2] += 1
                elif env.pygame.board.state == 2:
                    losses[i1][i2] += 1
                elif env.pygame.board.state == 3:
                    equalities[i1][i2] += 1


    print("WINS")
    print(wins)
    print("\nLOSSES")
    print(losses)
    print("\nEQUALITIES")
    print(equalities)

    pygame.quit()
    env.close()