# Shalini Bhakta ID: 74028480
# ICS 32 W22
# Project #5: The Fall of the World's Own Optimist (Part 2)

# project5.py
# Implements GUI of Columns game from mechanics5.py
# using third-party library, Pygame.

import pygame
import mechanics5
import random

WINDOW_W = 600
WINDOW_H = 700
EMPTY = '   '
COLORS_DICT = {'S': (202, 161, 255),
               'T': (255, 156, 210),
               'V': (153, 228, 255),
               'W': (120, 255, 178),
               'X': (239, 255, 150),
               'Y': (255, 117, 117),
               'Z': (117, 119, 255)}


class ColumnsGame():
    def __init__(self):
        self._running = True
        self.game = mechanics5.GameState(13, 6)

    
    def run(self) -> None:
        pygame.init()
        
        try:
            self._resize_display((WINDOW_W, WINDOW_H))
            clock = pygame.time.Clock()
            count = 30
            while self._running:
                clock.tick(30)
                self._handle_events()

                if count == 30:
                    self._auto_faller()
                    count = 0
                    
                count += 1
                self._redraw()

        finally:
            pygame.quit()


    def _resize_display(self, size: (int, int)) -> None:
        '''Sets display size.'''
        pygame.display.set_mode(size, pygame.RESIZABLE)
        

    def _handle_events(self) -> None:
        '''Handles events from user.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                self._key_commands()
        
                
    def _end_game(self) -> None:
        '''Stops running game.'''
        self._running = False
        

    def _redraw(self) -> None:
        '''Draws display.'''
        surface = pygame.display.get_surface()
        surface.fill(pygame.Color(40, 14, 74))
        self._draw_board(surface)
        pygame.display.flip()
        

    def _key_commands(self):
        '''Sends key commands to mechanics5.'''
        keys = pygame.key.get_pressed()
        keyClock = pygame.time.Clock()

        if keys[pygame.K_LEFT]:
            self.game.faller_left()

        if keys[pygame.K_RIGHT]:
            self.game.faller_right()

        if keys[pygame.K_SPACE]:
            self.game.rotate_faller()
        
    
    def _generate_faller(self) -> str:
        '''Randomly generates a new faller.'''
        colors = random.choices(['S', 'T', 'V', 'W', 'X', 'Y', 'Z'], k = 3)
        invalid_col = True
        col = 0
        while invalid_col:
            col = random.randint(1, 6)
            for element in self.game.get_board()[col - 1]:
                if element == EMPTY:
                    invalid_col = False
                    
        faller = str(col)
        faller += f' {colors[0]}'
        faller += f' {colors[1]}'
        faller += f' {colors[2]}'
        return faller
    

    def _auto_faller(self) -> None:
        '''Automates faller to continuously fall once per second
        until there is something beneath it.'''
        
        if self.game.faller_state == '':
            rand_faller = self._generate_faller()
            self.game.create_faller(rand_faller)
        elif self.game.faller_state == 'falling':
            self.game.continue_fall()
        elif self.game.faller_state == 'landed':
            self.game.check_landed_can_still_fall()
        else:
            pass


    def _draw_board(self, surface: pygame.Surface) -> None:
        '''Draws list[list[str]] board from mechanics onto pygame display.'''
        board = self.game.get_board()
        WINDOW_W = surface.get_width()
        WINDOW_H = surface.get_height()
        COL_FRAC_DIF = 0.1
        ROW_FRAC_DIF = (0.8 / 13)

        TL_frac_x = WINDOW_W * 0.2
        TL_frac_y = WINDOW_H * 0.1
        board_rect_w = WINDOW_W * 0.6
        board_rect_h = WINDOW_H * 0.8
        board_rect = pygame.Rect(TL_frac_x, TL_frac_y, board_rect_w, board_rect_h)
        pygame.draw.rect(surface, (255, 255, 255), board_rect)

        col_div = 0.2
        while col_div <= 0.7:
            pygame.draw.line(surface, (0,0,0), (WINDOW_W * col_div, TL_frac_y), (WINDOW_W * col_div, WINDOW_H * 0.9))
            col_div += COL_FRAC_DIF
        row_div = 0.1
        while row_div <= 0.9:
            pygame.draw.line(surface, (0,0,0), (TL_frac_x, WINDOW_H * row_div), (WINDOW_W * 0.8, WINDOW_H * row_div))
            row_div += ROW_FRAC_DIF

        for col_num in range(6):
            for row_num in range(13):                    
                if board[col_num][row_num] == EMPTY:
                    pass
                else:
                    pygame.draw.rect(surface, COLORS_DICT[board[col_num][row_num][1]],
                                     pygame.Rect(TL_frac_x + (WINDOW_W * (col_num / 10)) + 1,
                                                 TL_frac_y + (WINDOW_H * ROW_FRAC_DIF * row_num) + 1,
                                                 WINDOW_W * COL_FRAC_DIF - 1,
                                                 WINDOW_H * ROW_FRAC_DIF - 1))
                    if board[col_num][row_num][0] == '|':
                        TL_element_x = TL_frac_x + (WINDOW_W * (col_num / 10))
                        TL_element_y = TL_frac_y + (WINDOW_H * ROW_FRAC_DIF * row_num)
                        BR_element_x = (TL_frac_x + (WINDOW_W * (col_num / 10)) + 1) + (WINDOW_W * COL_FRAC_DIF - 1)
                        BR_element_y = (TL_frac_y + (WINDOW_H * ROW_FRAC_DIF * row_num) + 1) + (WINDOW_H * ROW_FRAC_DIF - 1)
                        
                        pygame.draw.line(surface, (255,255,255),
                                         (TL_element_x + 3, TL_element_y + 3),
                                         (BR_element_x - 2, BR_element_y - 3), width = 5)
                        pygame.draw.line(surface, (255,255,255),
                                         (TL_element_x + 2, BR_element_y - 2),
                                         (BR_element_x - 2, TL_element_y + 2), width = 5)

        if self._check_game_over(board):
            self._draw_text(surface, 'GAME OVER')
        else:
            self._draw_text(surface, 'PLAYING: COLUMNS GAME')
            

    def _draw_text(self, surface: pygame.Surface, text: str) -> None:
        '''Draws text onto surface.'''
        font = pygame.font.SysFont(None, 24)
        text_image = font.render(text, True, pygame.Color(255, 255, 255))
        surface.blit(text_image, (10, 10))
            

        
    def _check_game_over(self, board: list[list[str]]) -> bool:
        '''If board is full, game is over.'''
        game_over = True
        for c in range(6):
            for r in range(13):
                if board[c][r] == EMPTY:
                    game_over = False
        return game_over



if __name__ == '__main__':
    ColumnsGame().run()
