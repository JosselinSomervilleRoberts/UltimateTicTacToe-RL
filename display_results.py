
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

WINS= [[36, 48, 8, 0, 0, 0, 0, 0, 0], [0, 100, 1, 0, 0, 1, 0, 0, 0], [0, 0, 36, 4, 4, 60, 29, 11, 8], [0, 0, 0, 51, 41, 91, 71, 57, 38], [0, 0, 0, 0, 45, 97, 72, 61, 54], [0, 0, 0, 0, 0, 38, 4, 1, 2], [0, 0, 0, 0, 0, 0, 52, 18, 16], [0, 0, 0, 0, 0, 0, 0, 47, 46], [0, 0, 0, 0, 0, 0, 0, 0, 51]]
LOSSES= [[32, 38, 92, 100, 99, 98, 100, 100, 100], [0, 0, 95, 99, 100, 95, 100, 100, 100], [0, 0, 60, 87, 91, 30, 66, 85, 92], [0, 0, 0, 39, 43, 5, 18, 25, 48], [0, 0, 0, 0, 33, 2, 19, 31, 35], [0, 0, 0, 0, 0, 49, 91, 94, 98], [0, 0, 0, 0, 0, 0, 39, 72, 77], [0, 0, 0, 0, 0, 0, 0, 38, 42], [0, 0, 0, 0, 0, 0, 0, 0, 39]]
EQUALITIES= [[32, 14, 0, 0, 1, 2, 0, 0, 0], [0, 0, 4, 1, 0, 4, 0, 0, 0], [0, 0, 4, 9, 5, 10, 5, 4, 0], [0, 0, 0, 10, 16, 4, 11, 18, 14], [0, 0, 0, 0, 22, 1, 9, 8, 11], [0, 0, 0, 0, 0, 13, 5, 5, 0], [0, 0, 0, 0, 0, 0, 9, 10, 7], [0, 0, 0, 0, 0, 0, 0, 15, 12], [0, 0, 0, 0, 0, 0, 0, 0, 10]]
NAMES = ["Random Agent", "DQN Agent (trained for 15k games)", "1-step Minimax Agent (random)", "3-step Minimax Agent (random)", "5-step Minimax Agent (random)", "MCTS Agent (N=100)", "MCTS Agent (N=500)", "MCTS Agent (N=1000)", "MCTS Agent (N=2000)"]
n = len(WINS)
N = 100

CELL_SIZE = 80
LINE_SIZE = 7
PADDING = 60
LEGEND_SIZE = 700
SIZE = PADDING + n*(CELL_SIZE + LINE_SIZE) + LINE_SIZE
pygame.init()
screen = pygame.display.set_mode((SIZE+LEGEND_SIZE, SIZE))

# Small grid lines
screen.fill((255,255,255))
font = pygame.font.Font(None, 50)
for i in range(n+1):
    pos = PADDING + int(LINE_SIZE*0.5) + i*(CELL_SIZE+LINE_SIZE)
    pygame.draw.line(screen, (0,0,0), (pos,PADDING), (pos,PADDING+n*(CELL_SIZE+LINE_SIZE)+LINE_SIZE), width = LINE_SIZE) # Vertical
    pygame.draw.line(screen, (0,0,0), (PADDING,pos), (PADDING+n*(CELL_SIZE+LINE_SIZE),pos), width = LINE_SIZE) # Horizontal

for i in range(n):
    for j in range(n):
        w = WINS[i][j]
        l = LOSSES[i][j]
        e = EQUALITIES[i][j]
        if j < i:
            w = LOSSES[j][i]
            l = WINS[j][i]
            e = EQUALITIES[j][i]

        w = int(round(w*CELL_SIZE/float(N)))
        l = int(round(l*CELL_SIZE/float(N)))
        e = int(round(e*CELL_SIZE/float(N)))

        px = PADDING + int(LINE_SIZE) + j*(CELL_SIZE+LINE_SIZE)
        py = PADDING + int(LINE_SIZE) + i*(CELL_SIZE+LINE_SIZE)

        pygame.draw.rect(screen, (0,255,0), (px, py, w, CELL_SIZE))
        pygame.draw.rect(screen, (150,150,150), (px+w, py, e, CELL_SIZE))
        pygame.draw.rect(screen, (255,0,0), (px+w+e, py, CELL_SIZE-w-e, CELL_SIZE))

        # Text
        score = int(round(100 * (w + 0.5*e) / (w+e+l)))
        text = font.render(str(score), True, (0,0,0))
        text_rect = text.get_rect(center=(px + CELL_SIZE / 2., py + CELL_SIZE/ 2.))
        screen.blit(text, text_rect)

for i in range(n):
    text = font.render("(" + str(1+i) + ")", True, (0,0,0))
    p1 = PADDING / 2.
    p2 = LINE_SIZE + PADDING + (i+0.5) * (CELL_SIZE + LINE_SIZE)
    text_rect = text.get_rect(center=(p1, p2))
    screen.blit(text, text_rect)
    text_rect = text.get_rect(center=(p2, p1))
    screen.blit(text, text_rect)

    text2 = font.render("(" + str(1+i) + ") " + NAMES[i], True, (0,0,0))
    text_rect = text.get_rect(center=(SIZE + 2*p1, p2))
    screen.blit(text2, text_rect)

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