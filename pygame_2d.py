import pygame
import time

start_time = time.time()
pygame.init()

win_dim = 800
screen = pygame.display.set_mode((win_dim, win_dim))




def draw_board():
    screen.fill((255,255,255))


if __name__ == '__main__':

    game = True
    while game:
        pygame.time.delay(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        # Draws things on screen

        draw_board()

        # Updates movements and events

        # Update display

        pygame.display.update()

    pygame.QUIT()