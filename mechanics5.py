# Shalini Bhakta ID: 74028480
# ICS 32 W22
# Project #5: The Fall of the World's Own Optimist (Part 2)

# mechanics5.py
# Handles the mechanics of Columns Python game, modified for Project 5.
# Includes GameState class. Does not support matching aspects of game.

import random
EMPTY = '   '


class InvalidMoveError(Exception):
    '''Raised if an invalid move is tried.'''
    pass

class GameState:
    def __init__(self, nrow: int, ncol: int) -> None:
        self._rows = nrow
        self._cols = ncol
        self._board = self.new_board()
        self.CURRENT_FALLER = []
        self.FALLER_HEADER_ROW = 0
        self.faller_state = ''


    def new_board(self) -> list[list[str]]:
        '''Craetes new empty board as a list of lists.'''
        board = []
        for col in range(self._cols):
            board.append([])
            for row in range(self._rows):
                board[-1].append(EMPTY)
        return board


    def get_board(self) -> list[list[str]]:
        '''Returns board in form of list of lists.'''
        return self._board

    def faller_state(self) -> str:
        '''Returns state of faller [falling, landed, or frozen].'''
        return self.faller_state


    def create_faller(self, inp: str) -> None:
        '''Creates a new faller, sets faller_state to 'falling'.'''        
        
        if self.CURRENT_FALLER == []:
            new = inp.split(' ')
            elements = []
            for n in new[1:]:
                elements.append(f'[{n}]')
            self.CURRENT_FALLER.append(int(new[0]) - 1)
            self.CURRENT_FALLER += elements
            self.faller_state = 'falling'

            self._board[self.CURRENT_FALLER[0]][0] = self.CURRENT_FALLER[3]
        else:
            raise InvalidMoveError()

              

    def faller_left(self) -> None:
        '''Shifts all elemnents of faller one column to the left, if
            next left column in empty in every parallel row of the faller's elements.'''
        '''
        if self.faller_state == 'landed':
            if self.FALLER_HEADER_ROW < 12 and self.CURRENT_FALLER[0] != 0 and self._board[self.CURRENT_FALLER[0] - 1][self.FALLER_HEADER_ROW + 1] == EMPTY:
                self.faller_state == 'falling'
        '''

        if self.faller_state == '':
            pass
        elif self.CURRENT_FALLER[0] - 1 < 0:
            pass
        elif self._board[self.CURRENT_FALLER[0] - 1][self.FALLER_HEADER_ROW] != EMPTY:
            pass
        else:
            loop_index = 2
            current_row = self.FALLER_HEADER_ROW

            while current_row >= 0 and loop_index >= 0:
                self._board[self.CURRENT_FALLER[0] - 1][current_row] = self._board[self.CURRENT_FALLER[0]][current_row]
                self._board[self.CURRENT_FALLER[0]][current_row] = EMPTY
                 
                current_row -= 1
                loop_index -= 1
            self.CURRENT_FALLER[0] -= 1
                

    def faller_right(self) -> None:
        '''Shifts all elements of faller one column to the right, if
            next right column is empty in every paralllel row of the faller's elements.'''
        
        if self.faller_state == 'landed':
            if self.FALLER_HEADER_ROW < 12 and self.CURRENT_FALLER[0] != (self._cols - 1) and self._board[self.CURRENT_FALLER[0] + 1][self.FALLER_HEADER_ROW + 1] == EMPTY:
                self.faller_state == 'falling'

        if self.faller_state == '':
            pass
        elif self.CURRENT_FALLER[0] + 1 >= 6:
            pass
        elif self._board[self.CURRENT_FALLER[0] + 1][self.FALLER_HEADER_ROW] != EMPTY:
            pass
        else:
            loop_index = 2
            current_row = self.FALLER_HEADER_ROW

            while current_row >= 0 and loop_index >= 0:
                self._board[self.CURRENT_FALLER[0] + 1][current_row] = self._board[self.CURRENT_FALLER[0]][current_row]
                self._board[self.CURRENT_FALLER[0]][current_row] = EMPTY
                 
                current_row -= 1
                loop_index -= 1
            self.CURRENT_FALLER[0] += 1
        
                        
    def rotate_faller(self) -> None:
        '''Rotates elements of faller one index over. Moves last element
        of faller to index 0 of faller.'''

        if self.faller_state == '':
            pass
        else:
            if self.faller_state == 'landed':
                count = 1
                for letter in self.CURRENT_FALLER[1:]:
                    if letter[0] == '[':
                        self.CURRENT_FALLER[count] = f'|{letter[1]}|'
                        count += 1
            
            new = []
            element = self.CURRENT_FALLER[1:]
            new.append(self.CURRENT_FALLER[0])
            new.append(element[2])
            new.append(element[0])
            new.append(element[1])
            self.CURRENT_FALLER = new

            n = 3
            current_row = self.FALLER_HEADER_ROW
            while current_row >= 0 and n > 0:
                self._board[self.CURRENT_FALLER[0]][current_row] = new[n]
                current_row -= 1
                n -= 1

    def check_landed_can_still_fall(self):
        if self.FALLER_HEADER_ROW < 12:
            if self._board[self.CURRENT_FALLER[0]][self.FALLER_HEADER_ROW + 1] == EMPTY:
                self.faller_state = 'falling'
            else:
                self.frozen()
        else:
            self.frozen()
        

    def continue_fall(self) -> str:
        '''Moves faller one row down, in falling state.'''
 
        if self.FALLER_HEADER_ROW + 1 >= self._rows:
            if self.faller_state == 'frozen':
                raise InvalidMoveError()
            elif self.faller_state == 'landed':
                self.frozen()
                
        if self._board[self.CURRENT_FALLER[0]][self.FALLER_HEADER_ROW + 1] != EMPTY:
            self.landed()
            
        else:
            current_row = self.FALLER_HEADER_ROW
            faller_header_counter = 3

            while current_row >= 0 and faller_header_counter > 0:
                
                self._board[self.CURRENT_FALLER[0]][current_row + 1] = self.CURRENT_FALLER[faller_header_counter]
                if faller_header_counter > 1:
                    self._board[self.CURRENT_FALLER[0]][current_row] = self.CURRENT_FALLER[faller_header_counter - 1]
                else:
                    self._board[self.CURRENT_FALLER[0]][current_row] = EMPTY

                current_row -= 1
                faller_header_counter -= 1

            self.FALLER_HEADER_ROW += 1

            if self.FALLER_HEADER_ROW + 1 == self._rows or (self._board[self.CURRENT_FALLER[0]][self.FALLER_HEADER_ROW + 1] != EMPTY):
                self.landed()


    def landed(self) -> None:
        '''Sets faller_state to 'landed'.'''
        self.faller_state = 'landed'

        current_row = 0
    
        for element in self._board[self.CURRENT_FALLER[0]]:
            if element[0] == '[':
                self._board[self.CURRENT_FALLER[0]][current_row] = f'|{element[1]}|'
                
            current_row += 1

        
    def frozen(self) -> None:
        '''Sets faller_state to 'frozen'. Resets faller.'''
        self.faller_state = 'frozen'
        
        current_row = 0
    
        for element in self._board[self.CURRENT_FALLER[0]]:
            if element[0] == '|':
                
                self._board[self.CURRENT_FALLER[0]][current_row] = f' {element[1]} '
            current_row += 1

        self.CURRENT_FALLER = []
        self.FALLER_HEADER_ROW = 0
        self.faller_state = ''
        
        

    def rows(self) -> int:
        '''Returns number of rows in board.'''
        return len(self._board[0])
    

    def columns(self) -> int:
        '''Returns number of columns in board.'''
        return len(self._board)

    def check_game_over(self) -> bool:
        '''Checks if game is over by checking if all cells in
        board are full. Returns True if game is over, else False.'''
        game_over = True
        for r in range(self._rows):
            for c in range(self._cols):
                if self._board[c][r] == EMPTY:
                    game_over = False
        return game_over
        

    def end_game(self) -> None:
        '''Ends program.'''
        raise SystemExit()
    
