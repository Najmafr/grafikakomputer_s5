import pygame
import random
import sys

pygame.init()

# --- WINDOW ---
WIDTH = 600
HEIGHT = 750
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Blast")
clock = pygame.time.Clock()

# --- COLORS ---
BG_COLOR = (40, 40, 50)
GRID_BG = (50, 50, 60)
GRID_LINE = (70, 70, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLOCK_COLORS = [
    (255, 87, 87),   # Red
    (255, 195, 0),   # Yellow
    (0, 191, 255),   # Blue
    (144, 238, 144), # Green
    (255, 140, 255), # Pink
    (255, 165, 0),   # Orange
    (147, 112, 219), # Purple
    (64, 224, 208)   # Turquoise
]

# --- FONTS ---
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

# --- GRID CONFIG ---
GRID_SIZE = 8
CELL_SIZE = 60
GRID_X = 50
GRID_Y = 150

# --- BLOCK SHAPES ---
SHAPES = [
    # Single block
    [[1]],
    
    # 2x1 horizontal
    [[1, 1]],
    
    # 3x1 horizontal
    [[1, 1, 1]],
    
    # 2x1 vertical
    [[1],
     [1]],
    
    # 3x1 vertical
    [[1],
     [1],
     [1]],
    
    # 2x2 square
    [[1, 1],
     [1, 1]],
    
    # L shape
    [[1, 0],
     [1, 0],
     [1, 1]],
    
    # L shape flipped
    [[0, 1],
     [0, 1],
     [1, 1]],
    
    # T shape
    [[1, 1, 1],
     [0, 1, 0]],
    
    # Z shape
    [[1, 1, 0],
     [0, 1, 1]],
    
    # 3x3 square
    [[1, 1, 1],
     [1, 1, 1],
     [1, 1, 1]]
]

# --- BLOCK CLASS ---
class Block:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(BLOCK_COLORS)
        self.width = len(shape[0])
        self.height = len(shape)
        self.x = 0
        self.y = 0
        self.dragging = False
        self.placed = False
    
    def draw(self, surface, x, y, size=CELL_SIZE):
        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col] == 1:
                    cell_x = x + col * size
                    cell_y = y + row * size
                    
                    # Shadow
                    pygame.draw.rect(surface, (0, 0, 0, 100), 
                                   (cell_x + 3, cell_y + 3, size - 6, size - 6), 
                                   border_radius=8)
                    
                    # Block
                    pygame.draw.rect(surface, self.color, 
                                   (cell_x, cell_y, size - 4, size - 4), 
                                   border_radius=8)
                    
                    # Highlight
                    highlight_color = tuple(min(c + 50, 255) for c in self.color)
                    pygame.draw.rect(surface, highlight_color, 
                                   (cell_x + 5, cell_y + 5, size - 14, size - 14), 
                                   border_radius=6)
    
    def can_place(self, grid, grid_row, grid_col):
        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col] == 1:
                    target_row = grid_row + row
                    target_col = grid_col + col
                    
                    # Check bounds
                    if target_row < 0 or target_row >= GRID_SIZE or \
                       target_col < 0 or target_col >= GRID_SIZE:
                        return False
                    
                    # Check if cell is occupied
                    if grid[target_row][target_col] != 0:
                        return False
        
        return True
    
    def place(self, grid, grid_row, grid_col):
        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col] == 1:
                    grid[grid_row + row][grid_col + col] = self.color

# --- GAME CLASS ---
class BlockBlastGame:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.blocks = []
        self.spawn_blocks()
        self.dragged_block = None
        self.preview_pos = None
        self.can_place_preview = False
        self.game_over = False
    
    def spawn_blocks(self):
        self.blocks = []
        for i in range(3):
            shape = random.choice(SHAPES)
            block = Block(shape)
            block.x = 50 + i * 180
            block.y = 600
            self.blocks.append(block)
    
    def draw_grid(self, surface):
        # Grid background
        pygame.draw.rect(surface, GRID_BG, 
                        (GRID_X - 5, GRID_Y - 5, 
                         GRID_SIZE * CELL_SIZE + 10, GRID_SIZE * CELL_SIZE + 10),
                        border_radius=10)
        
        # Draw cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = GRID_X + col * CELL_SIZE
                y = GRID_Y + row * CELL_SIZE
                
                # Cell background
                if self.grid[row][col] == 0:
                    pygame.draw.rect(surface, (60, 60, 70), 
                                   (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4),
                                   border_radius=5)
                else:
                    # Filled cell
                    color = self.grid[row][col]
                    pygame.draw.rect(surface, color, 
                                   (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4),
                                   border_radius=5)
                    
                    # Highlight
                    highlight_color = tuple(min(c + 30, 255) for c in color)
                    pygame.draw.rect(surface, highlight_color, 
                                   (x + 7, y + 7, CELL_SIZE - 14, CELL_SIZE - 14),
                                   border_radius=4)
        
        # Draw preview
        if self.preview_pos and self.dragged_block:
            row, col = self.preview_pos
            color = (100, 255, 100) if self.can_place_preview else (255, 100, 100)
            
            for r in range(self.dragged_block.height):
                for c in range(self.dragged_block.width):
                    if self.dragged_block.shape[r][c] == 1:
                        px = GRID_X + (col + c) * CELL_SIZE
                        py = GRID_Y + (row + r) * CELL_SIZE
                        pygame.draw.rect(surface, color, 
                                       (px + 2, py + 2, CELL_SIZE - 4, CELL_SIZE - 4), 3,
                                       border_radius=5)
    
    def check_and_clear_lines(self):
        lines_cleared = 0
        rows_to_clear = []
        cols_to_clear = []
        
        # Check rows
        for row in range(GRID_SIZE):
            if all(self.grid[row][col] != 0 for col in range(GRID_SIZE)):
                rows_to_clear.append(row)
        
        # Check columns
        for col in range(GRID_SIZE):
            if all(self.grid[row][col] != 0 for row in range(GRID_SIZE)):
                cols_to_clear.append(col)
        
        # Clear rows
        for row in rows_to_clear:
            for col in range(GRID_SIZE):
                self.grid[row][col] = 0
            lines_cleared += 1
        
        # Clear columns
        for col in cols_to_clear:
            for row in range(GRID_SIZE):
                self.grid[row][col] = 0
            lines_cleared += 1
        
        # Award points
        if lines_cleared > 0:
            self.score += lines_cleared * 100
            if lines_cleared > 1:
                self.score += (lines_cleared - 1) * 50  # Bonus for multiple lines
        
        return lines_cleared
    
    def check_game_over(self):
        # Check if any remaining block can be placed
        for block in self.blocks:
            if not block.placed:
                for row in range(GRID_SIZE):
                    for col in range(GRID_SIZE):
                        if block.can_place(self.grid, row, col):
                            return False
        return True
    
    def get_grid_pos(self, mouse_x, mouse_y):
        if GRID_X <= mouse_x <= GRID_X + GRID_SIZE * CELL_SIZE and \
           GRID_Y <= mouse_y <= GRID_Y + GRID_SIZE * CELL_SIZE:
            col = (mouse_x - GRID_X) // CELL_SIZE
            row = (mouse_y - GRID_Y) // CELL_SIZE
            return (row, col)
        return None

# --- GAME INIT ---
game = BlockBlastGame()

# --- ANIMATION ---
clearing_animation = []
animation_timer = 0

# --- MAIN LOOP ---
run = True
while run:
    clock.tick(60)
    
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
            # Check if clicking on a block
            for block in game.blocks:
                if not block.placed:
                    block_rect = pygame.Rect(block.x, block.y, 
                                            block.width * 50, block.height * 50)
                    if block_rect.collidepoint(event.pos):
                        block.dragging = True
                        game.dragged_block = block
                        break
        
        if event.type == pygame.MOUSEBUTTONUP and not game.game_over:
            if game.dragged_block:
                # Try to place block
                grid_pos = game.get_grid_pos(mouse_pos[0], mouse_pos[1])
                if grid_pos and game.dragged_block.can_place(game.grid, grid_pos[0], grid_pos[1]):
                    # Place block
                    game.dragged_block.place(game.grid, grid_pos[0], grid_pos[1])
                    game.dragged_block.placed = True
                    
                    # Add score for placement
                    cells_placed = sum(sum(row) for row in game.dragged_block.shape)
                    game.score += cells_placed * 10
                    
                    # Check and clear lines
                    lines = game.check_and_clear_lines()
                    
                    # Check if all blocks placed
                    if all(b.placed for b in game.blocks):
                        game.spawn_blocks()
                    else:
                        # Check game over
                        if game.check_game_over():
                            game.game_over = True
                
                game.dragged_block.dragging = False
                game.dragged_block = None
                game.preview_pos = None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game.game_over:
                # Reset game
                game = BlockBlastGame()
    
    # Update preview
    if game.dragged_block and game.dragged_block.dragging:
        grid_pos = game.get_grid_pos(mouse_pos[0], mouse_pos[1])
        if grid_pos:
            game.preview_pos = grid_pos
            game.can_place_preview = game.dragged_block.can_place(game.grid, grid_pos[0], grid_pos[1])
        else:
            game.preview_pos = None
    
    # --- DRAW ---
    win.fill(BG_COLOR)
    
    # Title
    title = font_large.render("BALOK", True, WHITE)
    win.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Score
    score_text = font_medium.render(f"Score: {game.score}", True, WHITE)
    win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 90))
    
    # Grid
    game.draw_grid(win)
    
    # Blocks at bottom
    for block in game.blocks:
        if not block.placed and not block.dragging:
            block.draw(win, block.x, block.y, 50)
    
    # Dragged block
    if game.dragged_block and game.dragged_block.dragging:
        drag_x = mouse_pos[0] - (game.dragged_block.width * 50) // 2
        drag_y = mouse_pos[1] - (game.dragged_block.height * 50) // 2
        game.dragged_block.draw(win, drag_x, drag_y, 50)
    
    # Game Over
    if game.game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        win.blit(overlay, (0, 0))
        
        game_over_text = font_large.render("GAME OVER", True, (255, 100, 100))
        win.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 250))
        
        final_score = font_medium.render(f"Final Score: {game.score}", True, WHITE)
        win.blit(final_score, (WIDTH//2 - final_score.get_width()//2, 330))
        
        restart_text = font_small.render("Tekan SPACE untuk main lagi", True, WHITE)
        win.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 400))
    
    pygame.display.update()

pygame.quit()
sys.exit()