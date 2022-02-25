
import time
import numpy as np
import pygame


def current_milli_time():
    return round(time.time() * 1000)


class Board:
    SIZE = 910
    BOTTOM_SIZE = 80

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
    FONT = None


    # =============== HELPER FUNCTIONS ON GRIDS =============== #
    def checkWinBoard(grid):
        '''
        Checks if a given grid has a winner (int tic tac toe)
        Input: grid (3 x 3)
        Output: True if a line of plays exists (classic tic tac toe)
        '''
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

    def gridIsFull(grid):
        '''
        Checks if a given grid is full
        Input: grid (3 x 3)
        Output: False if at least one cell is equal to 0, True otherwise
        '''
        for ix in range(3):
            for iy in range(3):
                if grid[ix][iy] == 0:
                    return False
        return True
    # ========================================================= #



    # ================ HELPER FUNCTIONS FOR UI ================ #
    def getCellFromPx(px, py):
        '''
        Input: px, py (Coordinates of the pixel clicked)
        Output: (ixLarge, iyLarge, ixSmall, iySmall) index of the cell clicked
        WARNING: There is no check for out of bounds
        '''
        start = Board.getLargeTopLeftPx(0,0)
        ixLarge = int((px - start[0]) // Board.getSizeLargeCell())
        iyLarge = int((py - start[1]) // Board.getSizeLargeCell())
        px2 = px - start[0] - ixLarge * Board.getSizeLargeCell()
        py2 = py - start[1] - iyLarge * Board.getSizeLargeCell()
        ixSmall = int(px2 // Board.getSizeSmallCell())
        iySmall = int(py2 // Board.getSizeSmallCell())
        return (ixLarge, iyLarge, ixSmall, iySmall)

    def getSizeLargeCell():
        '''Output: pixel size of a large cell'''
        return (Board.SIZE-Board.WIDTH_LARGE_GRID) / 3.

    def getSizeSmallCell():
        '''Output: pixel size of a small cell'''
        return (Board.SIZE-Board.WIDTH_LARGE_GRID) / 9.

    def getLargeTopLeftPx(ix, iy):
        '''
        Input: ix, iy (indexes of the large cell)
        Output: pixel coordinates of the top left of the large cell
        '''
        px = 0.5*Board.WIDTH_LARGE_GRID + ix * Board.getSizeLargeCell() - 1
        py = 0.5*Board.WIDTH_LARGE_GRID + iy * Board.getSizeLargeCell() - 1
        return (px, py)

    def getSmallTopLeftPx(ixLarge, iyLarge, ixSmall, iySmall):
        '''
        Input: ixLarge, iyLarge, ixSmall, iySmall (indexes of the small cell)
        Output: pixel coordinates of the top left of the small cell
        '''
        (pxLarge, pyLarge) = Board.getLargeTopLeftPx(ixLarge, iyLarge)
        px = pxLarge + ixSmall * Board.getSizeSmallCell()
        py = pyLarge + iySmall * Board.getSizeSmallCell()
        return (px, py)

    def getSmallMidddlePx(ixLarge, iyLarge, ixSmall, iySmall):
        '''
        Input: ixLarge, iyLarge, ixSmall, iySmall (indexes of the small cell)
        Output: pixel coordinates of the middle of the small cell
        '''
        (px, py) = Board.getSmallTopLeftPx(ixLarge, iyLarge, ixSmall, iySmall)
        px += 0.5 * Board.getSizeSmallCell()
        py += 0.5 * Board.getSizeSmallCell()
        return (px, py)
    # ========================================================= #



     # ==================== INITIALIZATION ==================== #
    def __init__(self):
        '''Constructor (automatically reset on construct)'''
        self.reset()
        Board.FONT = pygame.font.Font(None, 50)

    def reset(self):
        '''Resets the game'''
        self.resetGrid()
        self.currentPlayer = 1
        self.text = "Player 1 plays"
        self.textColor = Board.COLOR_PLAYER_1
        self.state = 0
        self.possible = [[True for _ in range(3)] for _ in range(3)]

    def resetGrid(self):
        '''Builds empty grids (large and normal)'''
        self.grid = np.zeros((3,3,3,3), dtype=int).tolist()
        self.largeGrid = np.zeros((3,3), dtype=int).tolist()
    # ========================================================= #



    # ================== INTERACTIONS TO PLAY ================= #
    def play(self, ixLarge, iyLarge, ixSmall, iySmall):
        '''
        Attempts to play for the current player in the given cell
        Input: ixLarge, iyLarge, ixSmall, iySmall (indexes of the small cell)
        Output: Error number
            - 0: everything went fine
            - 1: the game is not running (not initiated or already won)
            - 2: the player cannot play in the desired large cell
            - 3: the desired small cell is not available (already occupied)
        '''
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

        # Text
        if self.state == 0:
            self.text = "Player " + str(self.currentPlayer) + " plays"
            self.textColor = Board.COLOR_PLAYER_2
            if self.currentPlayer == 1:
                self.textColor = Board.COLOR_PLAYER_1

        # Everything went fine
        return 0

    def checkWinLargeCell(self, ix, iy):
        '''
        Checks if a player won the large cell queried. If so, it also checks if the player globally won the game
        Input: ix, iy (indexes of the large cell)
        NO OUTPUT -> Automatically updates self.largeGrid and self.state'''
        g = self.grid[ix][iy]
        res = Board.checkWinBoard(g)
        if res != 0:
            self.largeGrid[ix][iy] = res
            resWin = Board.checkWinBoard(self.largeGrid)
            if resWin != 0: # A player won
                self.state = resWin

                # Display winning message
                self.textColor = Board.COLOR_PLAYER_2
                if resWin == 1:
                    self.textColor = Board.COLOR_PLAYER_1
                self.text = "Player " + str(self.state) + " won !"

    def updatePossible(self, ix, iy):
        '''
        Computes the moves aload and fill self.possible accordingly
        Input:  ix, iy (indexes of the large cell just played)
        NO OUTPUT -> Automatically updates self.possible
        '''
        if self.largeGrid[ix][iy] != 0: # If the cell is already won, play anywhere
            self.possible = self.getAvailableLargeCells()
        elif Board.gridIsFull(self.grid[ix][iy]): # If the cell is full play anywhere
            self.possible = self.getAvailableLargeCells()
        else: # The cell is not won and not full, play in this one
            self.possible = [[False for _ in range(3)] for _ in range(3)]
            self.possible[ix][iy] = True
            
    def getAvailableLargeCells(self):
        '''
        Checks all larges cells that are available (not won and not full)
        NO INPUT
        Output: 3x3 boolean matrix filled accordingly to the availableness of a large cell
        '''
        available = [[True for _ in range(3)] for _ in range(3)]
        for ix in range(3):
            for iy in range(3):
                if self.largeGrid[ix][iy] != 0: # If the cell is already won
                    available[ix][iy] = False
                elif Board.gridIsFull(self.grid[ix][iy]): # If the cell is full
                    available[ix][iy] = False
        return available
    # ========================================================= #


    
    # ==================== DRAWING FUNCTION =================== #
    def draw(self, screen, blinkAvailableCells = True):
        '''
        Draws the game (board and UI on the bottom)
        Input: screen (pygame.display object), blinkAvailableCells (boolean, used to choose if we highlight possible moves)
        NO OUTPUT -> Draws on the screen without flipping it (use pygame.display.flip())
        '''
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
                elif blinkAvailableCells and (self.state == 0): # Blink possible moves
                    if self.possible[ix][iy]:
                        if current_milli_time() % Board.TIME_BLINK_AVAILABLE > 0.5 * Board.TIME_BLINK_AVAILABLE:
                            color = Board.COLOR_BACKGROUND_AVAILABLE
                pygame.draw.rect(screen, color, (pos[0], pos[1], s, s))

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

        # Text
        pygame.draw.rect(screen, Board.COLOR_BACKGROUND, (0, Board.SIZE, Board.SIZE, Board.BOTTOM_SIZE))
        text = Board.FONT.render(self.text, True, self.textColor)
        text_rect = text.get_rect(center=(Board.SIZE / 2., Board.SIZE + Board.BOTTOM_SIZE / 2.))
        screen.blit(text, text_rect)
    # ========================================================= #

    

    # ======================= INTERFACES ====================== #
    def click(self, px, py):
        '''
        Interface for the player. Plays a move where the mouse was clicked
        INPUT; px, py (pixel coordinates of the click)
        NO OUTPUT -> Plays the move
        '''
        (ixLarge, iyLarge, ixSmall, iySmall) = Board.getCellFromPx(px, py)
        self.play(ixLarge, iyLarge, ixSmall, iySmall)
    # ========================================================= #