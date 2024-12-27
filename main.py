import pygame
import pygame.font
from enum import Enum

pygame.init()

class GameState(Enum):
    INSTRUCTIONS = 0
    PLAYING = 1
    WON = 2

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Color Fill Puzzle")

BOARD_SIZE = 5
SQUARE_SIZE = 80
BOARD_OFFSET_X = (WINDOW_SIZE[0] - (BOARD_SIZE * SQUARE_SIZE)) // 2
BOARD_OFFSET_Y = 150

COLORS = {
    'R': (255, 0, 0),   
    'G': (0, 255, 0),   
    'B': (0, 0, 255),   
    'Y': (255, 255, 0)  
}

COLOR_PANEL_Y = BOARD_OFFSET_Y + (BOARD_SIZE * SQUARE_SIZE) + 50
COLOR_PANEL_HEIGHT = 100
color_keys = list(COLORS.keys())
selected_color = None

board = [[(255, 255, 255) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)
win_font = pygame.font.Font(None, 96)

def is_board_filled(board):
    return all(board[row][col] != (255, 255, 255) 
              for row in range(BOARD_SIZE) 
              for col in range(BOARD_SIZE))

def has_adjacent_same_colors(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = board[row][col]
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    if board[new_row][new_col] == color:
                        return True
    return False

def is_winning_state(board):
    return is_board_filled(board) and not has_adjacent_same_colors(board)

def draw_board(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(
                BOARD_OFFSET_X + col * SQUARE_SIZE, 
                BOARD_OFFSET_Y + row * SQUARE_SIZE, 
                SQUARE_SIZE, 
                SQUARE_SIZE
            )
            pygame.draw.rect(screen, board[row][col], rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

def draw_color_panel():
    panel_start_x = BOARD_OFFSET_X
    label = font.render("Choose color by clicking:", True, (0, 0, 0))
    screen.blit(label, (panel_start_x, COLOR_PANEL_Y - 40))

    for idx, color_key in enumerate(color_keys):
        color = COLORS[color_key]
        rect = pygame.Rect(
            panel_start_x + idx * SQUARE_SIZE,
            COLOR_PANEL_Y,
            SQUARE_SIZE,
            COLOR_PANEL_HEIGHT
        )
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)

def draw_instructions():
    title = title_font.render("Color Fill Puzzle", True, (0, 0, 0))
    screen.blit(title, (WINDOW_SIZE[0]//2 - title.get_width()//2, 50))
    
    instructions = [
        "Fill the board with colors following these rules:",
        "1. No adjacent squares can have the same color",
        "2. Fill all squares to win",
        "",
        "Click anywhere to start"
    ]
    
    for i, line in enumerate(instructions):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (WINDOW_SIZE[0]//2 - text.get_width()//2, 200 + i*40))

def get_color_from_panel(x, y):
    if COLOR_PANEL_Y <= y <= COLOR_PANEL_Y + COLOR_PANEL_HEIGHT:
        panel_x = x - BOARD_OFFSET_X
        idx = panel_x // SQUARE_SIZE
        if 0 <= idx < len(color_keys):
            return COLORS[color_keys[idx]]
    return None

def get_board_position(x, y):
    board_x = x - BOARD_OFFSET_X
    board_y = y - BOARD_OFFSET_Y
    col = board_x // SQUARE_SIZE
    row = board_y // SQUARE_SIZE
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return row, col
    return None

def reset_board():
    global board
    board = [[(255, 255, 255) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def main():
    global selected_color
    running = True
    game_state = GameState.INSTRUCTIONS

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == GameState.INSTRUCTIONS:
                    game_state = GameState.PLAYING
                elif game_state == GameState.WON:
                    x, y = event.pos
                    restart_button = pygame.Rect(
                        WINDOW_SIZE[0]//2 - 100,
                        COLOR_PANEL_Y + COLOR_PANEL_HEIGHT + 20,
                        200,
                        50
                    )
                    if restart_button.collidepoint(x, y):
                        game_state = GameState.PLAYING
                        reset_board()
                else:
                    x, y = event.pos
                    color = get_color_from_panel(x, y)
                    if color:
                        selected_color = color
                    else:
                        board_pos = get_board_position(x, y)
                        if board_pos and selected_color:
                            row, col = board_pos
                            board[row][col] = selected_color
                            if is_winning_state(board):
                                game_state = GameState.WON

        screen.fill((255, 255, 255))
        
        if game_state == GameState.INSTRUCTIONS:
            draw_instructions()
        else:
            draw_board(board)
            draw_color_panel()
            
            if is_board_filled(board) and has_adjacent_same_colors(board):
                message = font.render("Adjacent colors detected - try changing some colors", True, (255, 0, 0))
                screen.blit(message, (WINDOW_SIZE[0]//2 - message.get_width()//2, COLOR_PANEL_Y - 500))
            
            if game_state == GameState.WON:
                win_surface = win_font.render("You Won!", True, (0, 128, 0))
                screen.blit(win_surface, (WINDOW_SIZE[0]//2 - win_surface.get_width()//2, 50))
                
                restart_button = pygame.Rect(
                    WINDOW_SIZE[0]//2 - 100,
                    COLOR_PANEL_Y + COLOR_PANEL_HEIGHT + 20,
                    200,
                    50
                )
                pygame.draw.rect(screen, (0, 128, 0), restart_button)
                pygame.draw.rect(screen, (0, 0, 0), restart_button, 2)
                
                restart_text = font.render("Start Over", True, (255, 255, 255))
                screen.blit(restart_text, (
                    restart_button.centerx - restart_text.get_width()//2,
                    restart_button.centery - restart_text.get_height()//2
                ))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()