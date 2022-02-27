import time
import numpy as np
import pygame


def current_milli_time():
    return round(time.time() * 1000)


class Board:
    SIZE = 600 #810
    BOTTOM_SIZE = 66 #90

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
            if grid[i,0] == grid[i,1] == grid[i,2] != 0:
                return grid[i,0]
            if grid[0,i] == grid[1,i] == grid[2,i] != 0:
                return grid[0,i]

        # Diagonals
        if grid[0,0] == grid[1,1] == grid[2,2] != 0:
            return grid[0,0]
        if grid[0,2] == grid[1,1] == grid[2,0] != 0:
            return grid[0,2]

        return 0

    def gridIsFull(grid):
        '''
        Checks if a given grid is full
        Input: grid (3 x 3)
        Output: False if at least one cell is equal to 0, True otherwise
        '''
        for ix in range(3):
            for iy in range(3):
                if grid[ix,iy] == 0:
                    return False
        return True

    def gridValue(grid):
        value = 0

        if True:
            lines1 = set()
            lines2 = set()
            used = set()

            # Lignes horizontales
            for i in range(3):
                nb1 = 0
                nb2 = 0
                zero = None
                addToUsed = False
                for j in range(3):
                    if grid[i,j] == 1: nb1 += 1
                    elif grid[i,j] == 2: nb2 += 1
                    else: zero = (i,j)
                if nb1 == 2 and nb2 == 0:
                    lines1.add(zero)
                    addToUsed = True
                elif nb2 == 2 and nb1 == 0:
                    lines2.add(zero)
                    addToUsed = True
                if addToUsed:
                    for j in range(3):
                        used.add((i,j))

            # Lignes verticales
            for j in range(3):
                nb1 = 0
                nb2 = 0
                zero = None
                addToUsed = False
                for i in range(3):
                    if grid[i,j] == 1: nb1 += 1
                    elif grid[i,j] == 2: nb2 += 1
                    else: zero = (i,j)
                if nb1 == 2 and nb2 == 0:
                    lines1.add(zero)
                    addToUsed = True
                elif nb2 == 2 and nb1 == 0:
                    lines2.add(zero)
                    addToUsed = True
                if addToUsed:
                    for i in range(3):
                        used.add((i,j))

            # Diagonale 1
            nb1 = 0
            nb2 = 0
            zero = None
            addToUsed = False
            for i in range(3):
                if grid[i,i] == 1: nb1 += 1
                elif grid[i,i] == 2: nb2 += 1
                else: zero = (i,i)
            if nb1 == 2 and nb2 == 0:
                lines1.add(zero)
                addToUsed = True
            elif nb2 == 2 and nb1 == 0:
                lines2.add(zero)
                addToUsed = True
            if addToUsed:
                for i in range(3):
                    used.add((i,i))

            # Diagonale 2
            nb1 = 0
            nb2 = 0
            zero = None
            addToUsed = False
            for i in range(3):
                if grid[2-i,i] == 1: nb1 += 1
                elif grid[2-i,i] == 2: nb2 += 1
                else: zero = (2-i,i)
            if nb1 == 2 and nb2 == 0:
                lines1.add(zero)
                addToUsed = True
            elif nb2 == 2 and nb1 == 0:
                lines2.add(zero)
                addToUsed = True
            if addToUsed:
                for i in range(3):
                    used.add((2-i,i))

            value += 5 * min(2, len(lines1))
            value -= 5 * min(2, len(lines2))

            for i in range(3):
                for j in range(3):
                    if grid[i,j] != 0 and not((i,j) in used):
                        val = 1 # edge
                        if i == j == 1: # Middle
                            val = 2
                        elif (i != 1) and (j != 1): # Corner
                            val = 1.5
                        value += val * (3-2*grid[i,j])

            return value
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
        self.reward_factor = 1
        Board.FONT = pygame.font.Font(None, 50)

    def reset(self):
        '''Resets the game'''
        self.reward_reset()
        self.resetGrid()
        self.currentPlayer = 1
        self.text = "Player 1 plays"
        self.textColor = Board.COLOR_PLAYER_1
        self.state = 0
        self.possible = np.array([[True for _ in range(3)] for _ in range(3)])

    def resetGrid(self):
        '''Builds empty grids (large and normal)'''
        self.grid = np.zeros((3,3,3,3), dtype=int)
        self.largeGrid = np.zeros((3,3), dtype=int)
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
        Move played (to reverse)
        '''
        if self.state != 0:
            return 1, None # Move not aload since the game is already finished
        if not(self.possible[ixLarge,iyLarge]):
            return 2, None # Move not aload since not in the correct large cell
        elif self.grid[ixLarge,iyLarge,ixSmall,iySmall] != 0:
            return 3, None # Move not aload since the small cell is already occupied

        self.reward_reset()

        # Play
        self.grid[ixLarge,iyLarge,ixSmall,iySmall] = self.currentPlayer
        move = [self.possible.copy(), (ixLarge,iyLarge,ixSmall,iySmall)]
        self.reward_update_playing_on(ixLarge, iyLarge, ixSmall, iySmall)

        # Check if a cell or the game is won
        self.checkWinLargeCell(ixLarge, iyLarge, move)

        # Update possibilities
        self.updatePossible(ixSmall, iySmall)

        # Update player
        self.currentPlayer = 3 - self.currentPlayer # Swap player

        # Text
        if self.state == 0:
            self.text = "Player " + str(self.currentPlayer) + " plays"
            self.textColor = Board.COLOR_PLAYER_2
            if self.currentPlayer == 1:
                self.textColor = Board.COLOR_PLAYER_1

        # Everything went fine
        return 0, move

    def checkWinLargeCell(self, ix, iy, move):
        '''
        Checks if a player won the large cell queried. If so, it also checks if the player globally won the game
        Input: ix, iy (indexes of the large cell)
        NO OUTPUT -> Automatically updates self.largeGrid and self.state'''
        g = self.grid[ix,iy]
        res = Board.checkWinBoard(g)
        if res != 0:
            # Win lage cell
            self.largeGrid[ix,iy] = res
            self.reward_update_winning_large_cell(ix, iy)
            move.append((ix, iy))

            # Check if the game was won
            resWin = Board.checkWinBoard(self.largeGrid)
            if resWin != 0: # A player won
                self.state = resWin
                self.reward_update_winning()

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
        if self.largeGrid[ix,iy] != 0: # If the cell is already won, play anywhere
            self.possible = self.getAvailableLargeCells()
        elif Board.gridIsFull(self.grid[ix,iy]): # If the cell is full play anywhere
            self.possible = self.getAvailableLargeCells()
        else: # The cell is not won and not full, play in this one
            self.possible = np.array([[False for _ in range(3)] for _ in range(3)])
            self.possible[ix,iy] = True

    def getAvailableLargeCells(self):
        '''
        Checks all larges cells that are available (not won and not full)
        NO INPUT
        Output: 3x3 boolean matrix filled accordingly to the availableness of a large cell
        '''
        available = np.array([[True for _ in range(3)] for _ in range(3)])
        nbFull = 0
        for ix in range(3):
            for iy in range(3):
                if self.largeGrid[ix,iy] != 0: # If the cell is already won
                    available[ix,iy] = False
                    nbFull += 1
                elif Board.gridIsFull(self.grid[ix,iy]): # If the cell is full
                    available[ix,iy] = False
                    nbFull += 1
        if self.state == 0 and nbFull == 9:
            self.state = 3
        return available
    # ========================================================= #



    # =================== REWARD FUNCTIONS ==================== #
    def reward_reset(self):
        '''
        Simply resets the reward to zero
        '''
        self.reward = 0

    def reward_update(self, reward):
        '''
        Updates self.reward considering the sign based on the current player
        INPUT: reward of the move
        NO OUTPUT -> updates self.reward
        '''
        if self.currentPlayer == 1:
            self.reward += reward
        else:
            self.reward -= self.reward_factor * reward

    def reward_update_playing_on(self, ixLarge, iyLarge, ixSmall, iySmall):
        '''
        Updates the reward playing in the given cell
        INPUT: ixLarge, iyLarge, ixSmall, iySmall (indexes of the small cell)
        NO OUTPUT -> updates self.reward
        '''
        # TODO: do it
        valueLargeGrid_prev = Board.gridValue(self.largeGrid)
        self.largeGrid[ixLarge,iyLarge] = self.currentPlayer
        valueLargeGrid = Board.gridValue(self.largeGrid)
        self.largeGrid[ixLarge,iyLarge] = 0

        valueSmallGrid = Board.gridValue(self.grid[ixLarge,iyLarge])
        self.grid[ixLarge, iyLarge, ixSmall, iySmall] = 0
        valueSmallGrid_prev = Board.gridValue(self.largeGrid)
        self.grid[ixLarge, iyLarge, ixSmall, iySmall] = self.currentPlayer

        reward = abs((valueSmallGrid - valueSmallGrid_prev) * (valueLargeGrid - valueLargeGrid_prev))
        self.reward_update(reward)

    def reward_update_winning_large_cell(self, ixLarge, iyLarge):
        '''
        Updates the reward winning a given large cell
        INPUT: ixLarge, iyLarge (indexes of the large cell)
        NO OUTPUT -> updates self.reward
        '''
        self.reward_reset()

        valueLargeGrid = Board.gridValue(self.largeGrid)
        self.largeGrid[ixLarge,iyLarge] = 0
        valueLargeGrid_prev = Board.gridValue(self.largeGrid)
        self.largeGrid[ixLarge,iyLarge] = self.currentPlayer

        reward = abs(20 * (valueLargeGrid - valueLargeGrid_prev))
        self.reward_update(reward)

    def reward_update_winning(self):
        '''
        Updates the reward winning the game
        NO INPUT
        NO OUTPUT -> updates self.reward
        '''
        self.reward_reset()
        reward = 400
        self.reward_update(reward)
    """
    def reward_reset(self):
        '''
        Simply resets the reward to zero
        '''
        self.reward = 0

    def reward_update(self, reward):
        '''
        Updates self.reward considering the sign based on the current player
        INPUT: reward of the move
        NO OUTPUT -> updates self.reward
        '''
        if self.currentPlayer == 1:
            self.reward += reward
        else:
            self.reward -= self.reward_factor * reward

    def reward_update_playing_on(self, ixLarge, iyLarge, ixSmall, iySmall):
        '''
        Updates the reward playing in the given cell
        INPUT: ixLarge, iyLarge, ixSmall, iySmall (indexes of the small cell)
        NO OUTPUT -> updates self.reward
        '''
        # TODO: do it
        pass

    def reward_update_winning_large_cell(self, ixLarge, iyLarge):
        '''
        Updates the reward winning a given large cell
        INPUT: ixLarge, iyLarge (indexes of the large cell)
        NO OUTPUT -> updates self.reward
        '''
        reward = 10 # TODO: Change
        self.reward_update(reward)

    def reward_update_winning(self):
        '''
        Updates the reward winning the game
        NO INPUT
        NO OUTPUT -> updates self.reward
        '''
        reward = 100
        self.reward_update(reward)
    """
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
                gridValue = self.largeGrid[ix,iy]
                pos = Board.getLargeTopLeftPx(ix, iy)
                color = Board.COLOR_BACKGROUND
                if gridValue == 1:
                    color = Board.COLOR_BACKGROUND_PLAYER_1
                elif gridValue == 2:
                    color = Board.COLOR_BACKGROUND_PLAYER_2
                elif blinkAvailableCells and (self.state == 0): # Blink possible moves
                    if self.possible[ix,iy]:
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
                        gridValue = self.grid[ixLarge,iyLarge,ixSmall,iySmall]
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
    def getActionFromClick(self, px, py):
        '''
        Interface for the player. Returns the action corresponding to the click
        INPUT; px, py (pixel coordinates of the click)
        Output: Action number (in the action space)
        '''
        (ixLarge, iyLarge, ixSmall, iySmall) = Board.getCellFromPx(px, py)
        if (ixLarge >= 3) or (iyLarge >= 3) or (ixSmall >= 3) or (iySmall >= 3): # Out of bounds
            return -1
        return 27*ixLarge + 9*iyLarge + 3*ixSmall + iySmall

    def click(self, px, py):
        '''
        Interface for the player. Plays a move where the mouse was clicked
        INPUT; px, py (pixel coordinates of the click)
        Output: Error number
            - 0: everything went fine
            - 1: the game is not running (not initiated or already won)
            - 2: the player cannot play in the desired large cell
            - 3: the desired small cell is not available (already occupied)
            - 4: the cell clicked is out of bounds
        '''
        (ixLarge, iyLarge, ixSmall, iySmall) = Board.getCellFromPx(px, py)
        if (ixLarge >= 3) or (iyLarge >= 3) or (ixSmall >= 3) or (iySmall >= 3): # Out of bounds
            return 4, None
        return self.play(ixLarge, iyLarge, ixSmall, iySmall)

    def getListOfPossibleMoves(self):
        '''
        Returns all possible moves (for minimax)
        NO INPUT
        Output: list of moves (a move is represented as an int: 27 * ixLarge + 9* iyLarge + 3*ixSmall + iySmall)
        '''
        moves = []
        for ixLarge in range(3):
            for iyLarge in range(3):
                if self.possible[ixLarge,iyLarge]:
                    for ixSmall in range(3):
                        for iySmall in range(3):
                            if self.grid[ixLarge,iyLarge,ixSmall,iySmall] == 0:
                                moves.append(27 * ixLarge + 9* iyLarge + 3*ixSmall + iySmall)
        return moves
    # ========================================================= #