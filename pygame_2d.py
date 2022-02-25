import pygame
import time

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

    def __init__(self):
        pass

    def getLargeTopLeftPx(self, ix, iy):
        px = 0.5*self.WIDTH_LARGE_GRID + (boardSize-self.WIDTH_LARGE_GRID) * ix / 3. - 1
        py = 0.5*self.WIDTH_LARGE_GRID + (boardSize-self.WIDTH_LARGE_GRID) * ix / 3. - 1
        return (px, py)

    def getSmallTopLeftPx(self, ixLarge, iyLarge, ixSmall, iySmall):
        (pxLarge, pyLarge) = self.getLargeTopLeftPx(ixLarge, iyLarge)
        px = pxLarge + (boardSize-self.WIDTH_LARGE_GRID) * ixSmall / 9.
        py = pyLarge + (boardSize-self.WIDTH_LARGE_GRID) * iySmall / 9.
        return (px, py)

    def draw(self):
        screen.fill(self.COLOR_BACKGROUND)

        # Small grid
        for i in range(10):
            pos = 0.5*self.WIDTH_LARGE_GRID + (boardSize-self.WIDTH_LARGE_GRID) * i / 9. - 1
            pygame.draw.line(screen, self.COLOR_SMALL_GRID, (pos,0), (pos,boardSize), width = self.WIDTH_SMALL_GRID) # Vertical
            pygame.draw.line(screen, self.COLOR_SMALL_GRID, (0,pos), (boardSize,pos), width = self.WIDTH_SMALL_GRID) # Horizontal

        # Large grid
        for i in range(4):
            pos = self.getLargeTopLeftPx(i,0)[0]
            pygame.draw.line(screen, self.COLOR_LARGE_GRID, (pos,0), (pos,boardSize), width = self.WIDTH_LARGE_GRID) # Vertical
            pygame.draw.line(screen, self.COLOR_LARGE_GRID, (0,pos), (boardSize,pos), width = self.WIDTH_LARGE_GRID) # Horizontal


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