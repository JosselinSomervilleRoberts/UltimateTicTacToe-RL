import pygame
import time
from board import Board


# Initialize game environment
pygame.init()
screen = pygame.display.set_mode((Board.SIZE, Board.SIZE + Board.BOTTOM_SIZE))
board = Board()


if __name__ == '__main__':

    game = True
    while game: # While the game is running
        pygame.time.delay(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit cross
                game = False
            if event.type == pygame.MOUSEBUTTONUP: # Mouse click released
                x, y = pygame.mouse.get_pos()
                board.click(x, y)

        # Update display
        board.draw(screen)
        pygame.display.flip()

    pygame.quit()