import pygame
import time
import numpy as np

def current_milli_time():
    return round(time.time() * 1000)

start_time = time.time()
pygame.init()



class Board:
    SIZE = 910

    COLOR_BACKGROUND = (255,255,255)
    COLOR_LARGE_GRID = (50, 50, 50 )
    COLOR_SMALL_GRID = (120,120,120)
    WIDTH_LARGE_GRID = 10
    WIDTH_SMALL_GRID = 5

    COLOR_PLAYER_1 = (255, 0, 0)
    COLOR_PLAYER_2 = (0, 0, 255)
    WIDTH_PLAYER_1 = 5
    WIDTH_PLAYER_2 = 5
    COLOR_BACKGROUND_PLAYER_1 = (255, 150, 150)
    COLOR_BACKGROUND_PLAYER_2 = (150, 150, 255)
    
    COLOR_BACKGROUND_AVAILABLE = (210,210,210)
    TIME_BLINK_AVAILABLE = 500 # ms


    def checkWinBoard(grid):
        for i in range(3):
            if grid[i][0] == grid[i][1] == grid[i][2] != 0:
                return grid[i][0]
            if grid[0][i] == grid[1][i] == grid[2][i] != 0:
                return grid[0][i]

        # Diagonals
        if grid[0][0] == grid[1][1] == grid[2][2] != 0:
            return grid[0][0]
        if grid[0][2] == grid[1][1] == grid[2][0] != 0:
            return grid[0][2]

        return 0

    def __init__(self):
        self.reset()

    def reset(self):
        self.resetGrid()
        self.currentPlayer = 1
        self.state = 0
        self.possible = [[True for _ in range(3)] for _ in range(3)]

    def resetGrid(self):
        self.grid = np.zeros((3,3,3,3), dtype=int).tolist()
        self.largeGrid = np.zeros((3,3), dtype=int).tolist()

    def play(self, ixLarge, iyLarge, ixSmall, iySmall):
        if self.state != 0:
            return 1 # Move not aload since the game is already finished
        if not(self.possible[ixLarge][iyLarge]):
            return 2 # Move not aload since not in the correct large cell
        elif self.grid[ixLarge][iyLarge][ixSmall][iySmall] != 0:
            return 3 # Move not aload since the small cell is already occupied

        self.grid[ixLarge][iyLarge][ixSmall][iySmall] = self.currentPlayer # Play
        self.currentPlayer = 3 - self.currentPlayer # Swap player
        self.checkWinLargeCell(ixLarge, iyLarge)
        self.updatePossible(ixSmall, iySmall)
        return 0

    def checkWinLargeCell(self, ix, iy):
        g = self.grid[ix][iy]
        res = Board.checkWinBoard(g)
        if res != 0:
            self.largeGrid[ix][iy] = res
            resWin = Board.checkWinBoard(self.largeGrid)
            if resWin != 0: # A player won
                self.state = resWin
                # TODO: Display a winning message

    def updatePossible(self, ix, iy):
        if self.largeGrid[ix][ix] != 0: # If the cell is already won, play anywhere
            self.possible = self.getAvailableLargeCells()
        elif np.count_nonzero(np.array(self.grid[ix][iy])) == 0: # If the cell is full play anywhere
            self.possible = self.getAvailableLargeCells()
        else: # The cell is not won and not full, play in this one
            self.possible = [[False for _ in range(3)] for _ in range(3)]
            self.possible[ix][iy] = True
            
    def getAvailableLargeCells(self):
        available = [[True for _ in range(3)] for _ in range(3)]
        for ix in range(3):
            for iy in range(3):
                if self.largeGrid[ix][iy] != 0: # If the cell is already won
                    available[ix][iy] = False
                elif np.count_nonzero(np.array(self.grid[ix][iy])) == 0: # If the cell is full
                    available[ix][iy] = False
        return available

    def getSizeLargeCell():
        return (Board.SIZE-Board.WIDTH_LARGE_GRID) / 3.

    def getSizeSmallCell():
        return (Board.SIZE-Board.WIDTH_LARGE_GRID) / 9.

    def getLargeTopLeftPx(ix, iy):
        px = 0.5*Board.WIDTH_LARGE_GRID + ix * Board.getSizeLargeCell() - 1
        py = 0.5*Board.WIDTH_LARGE_GRID + iy * Board.getSizeLargeCell() - 1
        return (px, py)

    def getSmallTopLeftPx(ixLarge, iyLarge, ixSmall, iySmall):
        (pxLarge, pyLarge) = Board.getLargeTopLeftPx(ixLarge, iyLarge)
        px = pxLarge + ixSmall * Board.getSizeSmallCell()
        py = pyLarge + iySmall * Board.getSizeSmallCell()
        return (px, py)

    def getSmallMidddlePx(ixLarge, iyLarge, ixSmall, iySmall):
        (px, py) = Board.getSmallTopLeftPx(ixLarge, iyLarge, ixSmall, iySmall)
        px += 0.5 * Board.getSizeSmallCell()
        py += 0.5 * Board.getSizeSmallCell()
        return (px, py)

    def draw(self, blinkAvailableCells = True):
        # Large grid background
        s = Board.getSizeLargeCell()
        for ix in range(3):
            for iy in range(3):
                gridValue = self.largeGrid[ix][iy]
                pos = Board.getLargeTopLeftPx(ix, iy)
                color = Board.COLOR_BACKGROUND
                if gridValue == 1:
                    color = Board.COLOR_BACKGROUND_PLAYER_1
                elif gridValue == 2:
                    color = Board.COLOR_BACKGROUND_PLAYER_2
                elif blinkAvailableCells: # Blink possible moves
                    if self.possible[ix][iy]:
                        if current_milli_time() % Board.TIME_BLINK_AVAILABLE > 0.5 * Board.TIME_BLINK_AVAILABLE:
                            color = Board.COLOR_BACKGROUND_AVAILABLE
                pygame.draw.rect(screen, color, (pos[0], pos[1], pos[0] + s, pos[1] + s))

        # Small grid lines
        for i in range(10):
            pos = 0.5 * Board.WIDTH_LARGE_GRID + (Board.SIZE - Board.WIDTH_LARGE_GRID) * i / 9. - 1
            pygame.draw.line(screen, Board.COLOR_SMALL_GRID, (pos,0), (pos,Board.SIZE), width = Board.WIDTH_SMALL_GRID) # Vertical
            pygame.draw.line(screen, Board.COLOR_SMALL_GRID, (0,pos), (Board.SIZE,pos), width = Board.WIDTH_SMALL_GRID) # Horizontal

        # Large grid lines
        for i in range(4):
            pos = Board.getLargeTopLeftPx(i,0)[0]
            pygame.draw.line(screen, Board.COLOR_LARGE_GRID, (pos,0), (pos,Board.SIZE), width = Board.WIDTH_LARGE_GRID) # Vertical
            pygame.draw.line(screen, Board.COLOR_LARGE_GRID, (0,pos), (Board.SIZE,pos), width = Board.WIDTH_LARGE_GRID) # Horizontal

        # Draw player moves
        inc = 0.35 * Board.getSizeSmallCell()
        for ixLarge in range(3):
            for iyLarge in range(3):
                for ixSmall in range(3):
                    for iySmall in range(3):
                        gridValue = self.grid[ixLarge][iyLarge][ixSmall][iySmall]
                        pos = Board.getSmallMidddlePx(ixLarge, iyLarge, ixSmall, iySmall)
                        if gridValue == 1: # Crosses
                            pygame.draw.line(screen, Board.COLOR_PLAYER_1, (pos[0] - inc, pos[1] - inc), (pos[0] + inc, pos[1] + inc), width = Board.WIDTH_PLAYER_1)
                            pygame.draw.line(screen, Board.COLOR_PLAYER_1, (pos[0] - inc, pos[1] + inc), (pos[0] + inc, pos[1] - inc), width = Board.WIDTH_PLAYER_1)
                        elif gridValue == 2: # Circles
                            pygame.draw.ellipse(screen, Board.COLOR_PLAYER_2, (pos[0] - inc, pos[1] - inc, 2*inc, 2*inc), width = Board.WIDTH_PLAYER_2)



screen = pygame.display.set_mode((Board.SIZE, Board.SIZE))
board = Board()
board.play(1,1,1,1)

if __name__ == '__main__':

    game = True
    while game:
        pygame.time.delay(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        # Draws things on screen

        board.draw()

        # Updates movements and events

        # Update display

        pygame.display.flip()

    pygame.QUIT()