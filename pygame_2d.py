import pygame
import time
import numpy as np

start_time = time.time()
pygame.init()

boardSize = 910
screen = pygame.display.set_mode((boardSize, boardSize))


class Board:
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
        pass

    def getSizeLargeCell(self):
        return (boardSize-self.WIDTH_LARGE_GRID) / 3.

    def getSizeSmallCell(self):
        return (boardSize-self.WIDTH_LARGE_GRID) / 9.

    def getLargeTopLeftPx(self, ix, iy):
        px = 0.5*self.WIDTH_LARGE_GRID + ix * self.getSizeLargeCell() - 1
        py = 0.5*self.WIDTH_LARGE_GRID + iy * self.getSizeLargeCell() - 1
        return (px, py)

    def getSmallTopLeftPx(self, ixLarge, iyLarge, ixSmall, iySmall):
        (pxLarge, pyLarge) = self.getLargeTopLeftPx(ixLarge, iyLarge)
        px = pxLarge + ixSmall * self.getSizeSmallCell()
        py = pyLarge + iySmall * self.getSizeSmallCell()
        return (px, py)

    def getSmallMidddlePx(self, ixLarge, iyLarge, ixSmall, iySmall):
        (px, py) = self.getSmallTopLeftPx(ixLarge, iyLarge, ixSmall, iySmall)
        px += 0.5 * self.getSizeSmallCell()
        py += 0.5 * self.getSizeSmallCell()
        return (px, py)

    def draw(self):
        # Large grid background
        s = self.getSizeLargeCell()
        for ix in range(3):
            for iy in range(3):
                gridValue = self.largeGrid[ix][iy]
                pos = self.getLargeTopLeftPx(ix, iy)
                color = self.COLOR_BACKGROUND
                if gridValue == 1:
                    color = self.COLOR_BACKGROUND_PLAYER_1
                elif gridValue == 2:
                    color = self.COLOR_BACKGROUND_PLAYER_2
                pygame.draw.rect(screen, color, (pos[0], pos[1], pos[0] + s, pos[1] + s))

        # Small grid lines
        for i in range(10):
            pos = 0.5*self.WIDTH_LARGE_GRID + (boardSize-self.WIDTH_LARGE_GRID) * i / 9. - 1
            pygame.draw.line(screen, self.COLOR_SMALL_GRID, (pos,0), (pos,boardSize), width = self.WIDTH_SMALL_GRID) # Vertical
            pygame.draw.line(screen, self.COLOR_SMALL_GRID, (0,pos), (boardSize,pos), width = self.WIDTH_SMALL_GRID) # Horizontal

        # Large grid lines
        for i in range(4):
            pos = self.getLargeTopLeftPx(i,0)[0]
            pygame.draw.line(screen, self.COLOR_LARGE_GRID, (pos,0), (pos,boardSize), width = self.WIDTH_LARGE_GRID) # Vertical
            pygame.draw.line(screen, self.COLOR_LARGE_GRID, (0,pos), (boardSize,pos), width = self.WIDTH_LARGE_GRID) # Horizontal

        # Draw player moves
        inc = 0.35 * self.getSizeSmallCell()
        for ixLarge in range(3):
            for iyLarge in range(3):
                for ixSmall in range(3):
                    for iySmall in range(3):
                        gridValue = self.grid[ixLarge][iyLarge][ixSmall][iySmall]
                        pos = self.getSmallMidddlePx(ixLarge, iyLarge, ixSmall, iySmall)
                        if gridValue == 1: # Crosses
                            pygame.draw.line(screen, self.COLOR_PLAYER_1, (pos[0] - inc, pos[1] - inc), (pos[0] + inc, pos[1] + inc), width = self.WIDTH_PLAYER_1)
                            pygame.draw.line(screen, self.COLOR_PLAYER_1, (pos[0] - inc, pos[1] + inc), (pos[0] + inc, pos[1] - inc), width = self.WIDTH_PLAYER_1)
                        elif gridValue == 2: # Circles
                            pygame.draw.ellipse(screen, self.COLOR_PLAYER_2, (pos[0] - inc, pos[1] - inc, 2*inc, 2*inc), width = self.WIDTH_PLAYER_2)



board = Board()

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