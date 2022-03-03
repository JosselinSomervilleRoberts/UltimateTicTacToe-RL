
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

#agent = MinimaxPruningAgent(1, 5, True)
agent = MCTSAgent(1, 2000)
#agent = MinimaxPruningAgent(1)
display = True

WINS =[[20, 3, 0, 0, 0, 1, 0, 0], [0, 17, 1, 1, 1, 27, 15, 1], [0, 0, 25, 19, 14, 37, 27, 21], [0, 0, 0, 40, 23, 34, 33, 25], [0, 0, 0, 0, 18, 38, 30, 34], [0, 0, 0, 0, 0, 18, 1, 1], [0, 0, 0, 0, 0, 0, 13, 6], [0, 0, 0, 0, 0, 0, 0, 14]]
LOSSES = [[14, 36, 39, 40, 39, 38, 40, 40], [0, 22, 38, 39, 36, 9, 22, 36], [0, 0, 10, 13, 15, 2, 10, 11], [0, 0, 0, 0, 10, 3, 2, 8], [0, 0, 0, 0, 15, 0, 6, 3], [0, 0, 0, 0, 0, 14, 36, 36], [0, 0, 0, 0, 0, 0, 15, 23], [0, 0, 0, 0, 0, 0, 0, 14]]
EQUALITIES =[[6, 1, 1, 0, 1, 1, 0, 0], [0, 1, 1, 0, 3, 4, 3, 3], [0, 0, 5, 8, 11, 1, 3, 8], [0, 0, 0, 0, 7, 3, 5, 7], [0, 0, 0, 0, 7, 2, 4, 3], [0, 0, 0, 0, 0, 8, 3, 3], [0, 0, 0, 0, 0, 0, 12, 11], [0, 0, 0, 0, 0, 0, 0, 12]]

n = len(WINS)
N = 40
CELL_SIZE = 80
LINE_SIZE = 7
SIZE = n*(CELL_SIZE + LINE_SIZE) + LINE_SIZE
pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))

# Small grid lines
screen.fill((255,255,255))
font = pygame.font.Font(None, 50)
for i in range(n+1):
    pos = int(LINE_SIZE*0.5) + i*(CELL_SIZE+LINE_SIZE)
    pygame.draw.line(screen, (0,0,0), (pos,0), (pos,SIZE), width = LINE_SIZE) # Vertical
    pygame.draw.line(screen, (0,0,0), (0,pos), (SIZE,pos), width = LINE_SIZE) # Horizontal

for i in range(n):
    for j in range(n):
        w = WINS[i][j]
        l = LOSSES[i][j]
        e = EQUALITIES[i][j]
        if j < i:
            w = LOSSES[j][i]
            l = WINS[j][i]
            e = EQUALITIES[j][i]

        w *= CELL_SIZE/float(N)
        l *= CELL_SIZE/float(N)
        e *= CELL_SIZE/float(N)

        px = int(LINE_SIZE) + i*(CELL_SIZE+LINE_SIZE)
        py = int(LINE_SIZE) + j*(CELL_SIZE+LINE_SIZE)

        pygame.draw.rect(screen, (0,255,0), (px, py, w, CELL_SIZE))
        pygame.draw.rect(screen, (150,150,150), (px+w, py, e, CELL_SIZE))
        pygame.draw.rect(screen, (255,0,0), (px+w+e, py, l, CELL_SIZE))

        # Text
        score = int(round(100 * (w + 0.5*e) / (w+e+l)))
        text = font.render(str(score), True, (0,0,0))
        text_rect = text.get_rect(center=(px + CELL_SIZE / 2., py + CELL_SIZE/ 2.))
        screen.blit(text, text_rect)

if __name__ == '__main__':
    game = True
    while game:
        if display:
            # Render the environment

            # Check for pygame event (to close the window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit cross
                    game = False

            # Delay to not spam
            pygame.time.delay(1)
            pygame.display.flip()

    pygame.quit()