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

    def __init__(self):
        self.resetGrid()

    def resetGrid(self):
        self.grid = np.zeros((3,3,3,3), dtype=int).tolist()
        self.largeGrid = np.zeros((3,3), dtype=int).tolist()

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