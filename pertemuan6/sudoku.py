import pygame
import random
import sys

pygame.init()

# --- WINDOW ---
WIDTH = 700
HEIGHT = 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")
clock = pygame.time.Clock()

# --- COLORS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
BLUE = (100, 149, 237)
GREEN = (144, 238, 144)
RED = (255, 99, 71)
DARK_BLUE = (70, 130, 180)
YELLOW = (255, 250, 205)

# --- FONTS ---
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

# --- SUDOKU CONFIG ---
GRID_SIZE = 9
CELL_SIZE = 60
GRID_X = 70
GRID_Y = 120

# --- SUDOKU GENERATOR ---
def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku(difficulty):
    # Create empty board
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill diagonal 3x3 boxes
    for box in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board[box + i][box + j] = nums[i * 3 + j]
    
    # Solve the board
    solve_sudoku(board)
    
    # Remove numbers based on difficulty
    remove_count = {"easy": 30, "medium": 40, "hard": 50}
    cells_to_remove = remove_count.get(difficulty, 40)
    
    solution = [row[:] for row in board]
    
    removed = 0
    while removed < cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            removed += 1
    
    return board, solution

# --- CELL CLASS ---
class Cell:
    def __init__(self, row, col, value, is_fixed):
        self.row = row
        self.col = col
        self.value = value
        self.is_fixed = is_fixed
        self.notes = set()
        self.is_error = False
    
    def draw(self, surface, selected):
        x = GRID_X + self.col * CELL_SIZE
        y = GRID_Y + self.row * CELL_SIZE
        
        # Background
        if selected:
            pygame.draw.rect(surface, YELLOW, (x, y, CELL_SIZE, CELL_SIZE))
        elif self.is_error:
            pygame.draw.rect(surface, (255, 200, 200), (x, y, CELL_SIZE, CELL_SIZE))
        elif self.is_fixed:
            pygame.draw.rect(surface, LIGHT_GRAY, (x, y, CELL_SIZE, CELL_SIZE))
        else:
            pygame.draw.rect(surface, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
        
        # Border
        pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Value
        if self.value != 0:
            color = BLACK if self.is_fixed else BLUE
            text = font_medium.render(str(self.value), True, color)
            text_rect = text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
            surface.blit(text, text_rect)
        elif self.notes:
            # Draw notes
            note_font = pygame.font.Font(None, 18)
            for note in self.notes:
                note_row = (note - 1) // 3
                note_col = (note - 1) % 3
                note_x = x + 8 + note_col * 16
                note_y = y + 8 + note_row * 16
                note_text = note_font.render(str(note), True, GRAY)
                surface.blit(note_text, (note_x, note_y))

# --- GAME CLASS ---
class SudokuGame:
    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        self.board, self.solution = generate_sudoku(difficulty)
        self.cells = []
        
        for row in range(9):
            cell_row = []
            for col in range(9):
                value = self.board[row][col]
                is_fixed = value != 0
                cell_row.append(Cell(row, col, value, is_fixed))
            self.cells.append(cell_row)
        
        self.selected_cell = None
        self.mistakes = 0
        self.max_mistakes = 3
        self.note_mode = False
    
    def select_cell(self, row, col):
        if 0 <= row < 9 and 0 <= col < 9:
            self.selected_cell = (row, col)
    
    def enter_number(self, num):
        if self.selected_cell:
            row, col = self.selected_cell
            cell = self.cells[row][col]
            
            if not cell.is_fixed:
                if self.note_mode:
                    # Toggle note
                    if num in cell.notes:
                        cell.notes.remove(num)
                    else:
                        cell.notes.add(num)
                else:
                    # Enter number
                    cell.value = num
                    cell.notes.clear()
                    
                    # Check if correct
                    if num != self.solution[row][col]:
                        cell.is_error = True
                        self.mistakes += 1
                        return False  # Wrong answer
                    else:
                        cell.is_error = False
                        return True  # Correct answer
        return None
    
    def clear_cell(self):
        if self.selected_cell:
            row, col = self.selected_cell
            cell = self.cells[row][col]
            if not cell.is_fixed:
                cell.value = 0
                cell.notes.clear()
                cell.is_error = False
    
    def check_complete(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value != self.solution[row][col]:
                    return False
        return True
    
    def draw(self, surface):
        # Draw grid
        for row in range(9):
            for col in range(9):
                is_selected = self.selected_cell == (row, col)
                self.cells[row][col].draw(surface, is_selected)
        
        # Draw thick borders for 3x3 boxes
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1
            # Horizontal lines
            pygame.draw.line(surface, BLACK, 
                           (GRID_X, GRID_Y + i * CELL_SIZE),
                           (GRID_X + 9 * CELL_SIZE, GRID_Y + i * CELL_SIZE), 
                           thickness)
            # Vertical lines
            pygame.draw.line(surface, BLACK,
                           (GRID_X + i * CELL_SIZE, GRID_Y),
                           (GRID_X + i * CELL_SIZE, GRID_Y + 9 * CELL_SIZE),
                           thickness)

# --- BUTTONS ---
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
    
    def draw(self, surface):
        color = tuple(min(c + 30, 255) for c in self.color) if self.hover else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)
        
        text_surf = font_small.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# --- GAME INIT ---
game = SudokuGame("medium")
game_state = "PLAYING"  # PLAYING, WON, GAME_OVER, MENU

# Buttons
new_game_btn = Button(70, 720, 120, 50, "New Game", GREEN)
hint_btn = Button(210, 720, 100, 50, "Hint", YELLOW)
note_btn = Button(330, 720, 100, 50, "Notes", GRAY)
check_btn = Button(450, 720, 100, 50, "Check", BLUE)

difficulty_btns = {
    "easy": Button(150, 300, 120, 50, "Easy", GREEN),
    "medium": Button(290, 300, 120, 50, "Medium", YELLOW),
    "hard": Button(430, 300, 120, 50, "Hard", RED)
}

# --- MAIN LOOP ---
run = True
show_menu = True

while run:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if show_menu:
                for difficulty, btn in difficulty_btns.items():
                    if btn.is_clicked(pos):
                        game = SudokuGame(difficulty)
                        show_menu = False
                        game_state = "PLAYING"
            
            elif game_state == "PLAYING":
                # Click on grid
                if GRID_X <= pos[0] <= GRID_X + 9 * CELL_SIZE and \
                   GRID_Y <= pos[1] <= GRID_Y + 9 * CELL_SIZE:
                    col = (pos[0] - GRID_X) // CELL_SIZE
                    row = (pos[1] - GRID_Y) // CELL_SIZE
                    game.select_cell(row, col)
                
                # Buttons
                if new_game_btn.is_clicked(pos):
                    show_menu = True
                
                if hint_btn.is_clicked(pos) and game.selected_cell:
                    row, col = game.selected_cell
                    if not game.cells[row][col].is_fixed:
                        game.cells[row][col].value = game.solution[row][col]
                        game.cells[row][col].is_error = False
                
                if note_btn.is_clicked(pos):
                    game.note_mode = not game.note_mode
                
                if check_btn.is_clicked(pos):
                    if game.check_complete():
                        game_state = "WON"
            
            elif game_state == "WON":
                if new_game_btn.is_clicked(pos):
                    show_menu = True
                    game_state = "PLAYING"
            
            elif game_state == "GAME_OVER":
                if new_game_btn.is_clicked(pos):
                    show_menu = True
                    game_state = "PLAYING"
        
        if event.type == pygame.KEYDOWN and game_state == "PLAYING":
            if event.key in [pygame.K_1, pygame.K_KP1]: 
                result = game.enter_number(1)
                if result == False and game.mistakes >= game.max_mistakes:
                    game_state = "GAME_OVER"
            elif event.key in [pygame.K_2, pygame.K_KP2]: 
                result = game.enter_number(2)
                if result == False and game.mistakes >= game.max_mistakes:
                    game_state = "GAME_OVER"
            elif event.key in [pygame.K_3, pygame.K_KP3]: 
                result = game.enter_number(3)
                if result == False and game.mistakes >= game.max_mistakes:
                    game_state = "GAME_OVER"
            elif event.key in [pygame.K_4, pygame.K_KP4]: 
                result = game.enter_number(4)
                if result == False and game.mistakes >= game.max_mistakes:
                    game_state = "GAME_OVER"
            elif event.key in [pygame.K_5, pygame.K_KP5]: 
                result = game.enter_number(5)
                if result == False and game.mistakes >= game.max_mistakes:
                    game_state = "GAME_OVER"
            elif event.key in [pygame.K_6, pygame.K_KP6]: 
                result = game.enter_number(6)
                if result == False and game.mistakes >= game.max_mistakes:
                    game_state = "GAME_OVER"
            elif event.key in [pygame.K_7, pygame.K_KP7]: 
                result = game.enter_number(7)
                if result == False and game.mistakes >= game.max_mistakes:
                    game_state = "GAME_OVER"
            elif event.key in [pygame.K_8, pygame.K_KP8]: 
                result = game.enter_number(8)
                if result == False and game.mistakes >= game.max_mistakes:
                    game_state = "GAME_OVER"
            elif event.key in [pygame.K_9, pygame.K_KP9]: 
                result = game.enter_number(9)
                if result == False and game.mistakes >= game.max_mistakes:
                    game_state = "GAME_OVER"
            elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_0]:
                game.clear_cell()
            elif event.key == pygame.K_n:
                game.note_mode = not game.note_mode
            
            # Arrow keys
            if game.selected_cell:
                row, col = game.selected_cell
                if event.key == pygame.K_UP and row > 0:
                    game.select_cell(row - 1, col)
                elif event.key == pygame.K_DOWN and row < 8:
                    game.select_cell(row + 1, col)
                elif event.key == pygame.K_LEFT and col > 0:
                    game.select_cell(row, col - 1)
                elif event.key == pygame.K_RIGHT and col < 8:
                    game.select_cell(row, col + 1)
        
        if event.type == pygame.MOUSEMOTION:
            # Button hover effect
            for btn in [new_game_btn, hint_btn, note_btn, check_btn]:
                btn.hover = btn.is_clicked(event.pos)
            
            if show_menu:
                for btn in difficulty_btns.values():
                    btn.hover = btn.is_clicked(event.pos)
    
    # --- DRAW ---
    win.fill((250, 250, 250))
    
    if show_menu:
        # Menu screen
        title = font_large.render("SUDOKU", True, DARK_BLUE)
        win.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        
        subtitle = font_medium.render("Pilih Tingkat Kesulitan:", True, BLACK)
        win.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 230))
        
        for btn in difficulty_btns.values():
            btn.draw(win)
    
    else:
        # Title
        title = font_large.render("SUDOKU", True, DARK_BLUE)
        win.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        # Game board
        game.draw(win)
        
        # Mistakes counter with hearts
        hearts_remaining = game.max_mistakes - game.mistakes
        mistakes_text = font_small.render(f"Nyawa:", True, BLACK)
        win.blit(mistakes_text, (70, 680))
        
        for i in range(game.max_mistakes):
            if i < hearts_remaining:
                color = RED
            else:
                color = GRAY
            # Draw heart
            heart_x = 140 + i * 35
            heart_y = 688
            pygame.draw.circle(win, color, (heart_x, heart_y), 10)
            pygame.draw.circle(win, color, (heart_x + 14, heart_y), 10)
            pygame.draw.polygon(win, color, [
                (heart_x - 10, heart_y + 2),
                (heart_x + 24, heart_y + 2),
                (heart_x + 7, heart_y + 18)
            ])
        
        # Note mode indicator
        if game.note_mode:
            note_text = font_small.render("MODE: Notes", True, BLUE)
            win.blit(note_text, (400, 680))
        
        # Buttons
        new_game_btn.draw(win)
        hint_btn.draw(win)
        note_btn.draw(win)
        check_btn.draw(win)
        
        # Winner screen
        if game_state == "WON":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((255, 255, 255))
            win.blit(overlay, (0, 0))
            
            win_text = font_large.render("SELAMAT!", True, GREEN)
            win.blit(win_text, (WIDTH//2 - win_text.get_width()//2, 250))
            
            score_text = font_medium.render(f"Sudoku Selesai!", True, BLACK)
            win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 330))
            
            mistakes_final = font_medium.render(f"Kesalahan: {game.mistakes}/{game.max_mistakes}", True, BLACK)
            win.blit(mistakes_final, (WIDTH//2 - mistakes_final.get_width()//2, 380))
            
            new_game_btn.draw(win)
        
        # Game Over screen
        elif game_state == "GAME_OVER":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((50, 50, 50))
            win.blit(overlay, (0, 0))
            
            game_over_text = font_large.render("GAME OVER", True, RED)
            win.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 250))
            
            reason_text = font_medium.render(f"3 Kesalahan Berturut-turut!", True, WHITE)
            win.blit(reason_text, (WIDTH//2 - reason_text.get_width()//2, 330))
            
            try_again_text = font_small.render("Klik New Game untuk coba lagi", True, WHITE)
            win.blit(try_again_text, (WIDTH//2 - try_again_text.get_width()//2, 390))
            
            new_game_btn.draw(win)
    
    pygame.display.update()

pygame.quit()
sys.exit()