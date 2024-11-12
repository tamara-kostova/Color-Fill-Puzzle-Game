import pygame
import pygame.font

pygame.init()

WINDOW_SIZE = (500, 650)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Color Fill Puzzle")

BOARD_SIZE = 5
SQUARE_SIZE = 80

COLORS = {
    'R': (255, 0, 0),   
    'G': (0, 255, 0),   
    'B': (0, 0, 255),   
    'Y': (255, 255, 0)  
}

COLOR_PANEL_Y = BOARD_SIZE * SQUARE_SIZE + 50  
COLOR_PANEL_HEIGHT = 100
color_keys = list(COLORS.keys())
selected_color = None

board = [[(255, 255, 255) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
font = pygame.font.Font(None, 36)
win_font = pygame.font.Font(None, 48)

def is_valid_move(board, row, col, color):
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
            if board[new_row][new_col] == color:
                return False
    return True

def update_board(board, row, col, color):
    board[row][col] = color

def is_winning_state(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == (255, 255, 255):
                return False
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = board[row][col]
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    if board[new_row][new_col] == color:
                        return False
    return True

def draw_board(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, board[row][col], rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  

def draw_color_panel():
    label = font.render("Choose color by clicking:", True, (0, 0, 0))
    screen.blit(label, (10, COLOR_PANEL_Y - 40))

    for idx, color_key in enumerate(color_keys):
        color = COLORS[color_key]
        rect = pygame.Rect(idx * SQUARE_SIZE, COLOR_PANEL_Y, SQUARE_SIZE, COLOR_PANEL_HEIGHT)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)

def get_color_from_panel(x, y):
    if y >= COLOR_PANEL_Y:
        idx = x // SQUARE_SIZE
        if idx < len(color_keys):
            return COLORS[color_keys[idx]]
    return None

def reset_board():
    global board
    board = [[(255, 255, 255) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def main():
    global selected_color
    running = True
    game_won = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_won:
                    x, y = event.pos
                    if 150 <= x <= 350 and COLOR_PANEL_Y + COLOR_PANEL_HEIGHT + 20 <= y <= COLOR_PANEL_Y + COLOR_PANEL_HEIGHT + 70:
                        game_won = False
                        reset_board()
                else:
                    pos = pygame.mouse.get_pos()
                    x, y = pos[0], pos[1]
                    color = get_color_from_panel(x, y)
                    if color:
                        selected_color = color
                    else:
                        col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and selected_color:
                            if is_valid_move(board, row, col, selected_color):
                                update_board(board, row, col, selected_color)
                                if is_winning_state(board):
                                    game_won = True  # Set game to won state

        screen.fill((255, 255, 255))
        draw_board(board)
        draw_color_panel()
        
        if game_won:
            win_message = win_font.render("You won!", True, (0, 128, 0))
            screen.blit(win_message, (180, COLOR_PANEL_Y - 60))
            restart_button = pygame.Rect(150, COLOR_PANEL_Y + COLOR_PANEL_HEIGHT + 20, 200, 50)
            pygame.draw.rect(screen, (0, 128, 0), restart_button)
            pygame.draw.rect(screen, (0, 0, 0), restart_button, 2)
            restart_text = font.render("Start Over", True, (255, 255, 255))
            screen.blit(restart_text, (restart_button.x + 20, restart_button.y + 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
