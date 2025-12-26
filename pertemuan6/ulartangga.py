import pygame
import random
import sys

pygame.init()

# --- WINDOW ---
WIDTH = 800
HEIGHT = 850
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ular Tangga")
clock = pygame.time.Clock()

# --- COLORS ---
CREAM = (255, 248, 220)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 90, 43)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- BOARD CONFIG ---
BOARD_SIZE = 10
CELL_SIZE = 70
BOARD_X = 50
BOARD_Y = 100

# --- FONTS ---
font_small = pygame.font.Font(None, 24)
font_medium = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 60)

# --- SNAKE AND LADDER DATA ---
# Format: {start: end}
snakes = {
    98: 28,
    87: 24,
    73: 19,
    64: 44,
    62: 18,
    54: 34,
    51: 11
}

ladders = {
    4: 25,
    13: 46,
    21: 82,
    33: 49,
    42: 63,
    50: 91,
    60: 83
}

# --- PLAYER CLASS ---
class Player:
    def __init__(self, name, color, number):
        self.name = name
        self.color = color
        self.position = 0
        self.number = number
        self.target_pos = 0
        self.is_moving = False
        
    def get_coords(self, position):
        if position == 0:
            return (BOARD_X - 30, BOARD_Y + BOARD_SIZE * CELL_SIZE + 10)
        
        row = (position - 1) // BOARD_SIZE
        col = (position - 1) % BOARD_SIZE
        
        # Zigzag pattern
        if row % 2 == 1:
            col = BOARD_SIZE - 1 - col
        
        x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_Y + (BOARD_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE // 2
        
        # Offset untuk multiple players
        offset = [(0, 0), (15, 0), (0, 15), (15, 15)]
        x += offset[self.number][0]
        y += offset[self.number][1]
        
        return (x, y)
    
    def move_to(self, new_position):
        self.target_pos = min(new_position, 100)
        self.is_moving = True
    
    def update(self):
        if self.is_moving:
            if self.position < self.target_pos:
                self.position += 1
            else:
                self.is_moving = False
                # Check for snake or ladder
                if self.position in snakes:
                    self.position = snakes[self.position]
                elif self.position in ladders:
                    self.position = ladders[self.position]
    
    def draw(self, surface):
        x, y = self.get_coords(self.position)
        pygame.draw.circle(surface, BLACK, (x, y), 18)
        pygame.draw.circle(surface, self.color, (x, y), 15)
        # Nomor player
        num_text = font_small.render(str(self.number + 1), True, WHITE)
        surface.blit(num_text, (x - 6, y - 8))

# --- DICE ---
class Dice:
    def __init__(self):
        self.value = 1
        self.rolling = False
        self.roll_timer = 0
        
    def roll(self):
        self.rolling = True
        self.roll_timer = 20
        
    def update(self):
        if self.rolling:
            self.roll_timer -= 1
            if self.roll_timer % 3 == 0:
                self.value = random.randint(1, 6)
            if self.roll_timer <= 0:
                self.rolling = False
                self.value = random.randint(1, 6)
    
    def draw(self, surface, x, y):
        # Dadu background
        pygame.draw.rect(surface, WHITE, (x, y, 80, 80), border_radius=10)
        pygame.draw.rect(surface, BLACK, (x, y, 80, 80), 3, border_radius=10)
        
        # Titik dadu
        dot_positions = {
            1: [(40, 40)],
            2: [(25, 25), (55, 55)],
            3: [(25, 25), (40, 40), (55, 55)],
            4: [(25, 25), (55, 25), (25, 55), (55, 55)],
            5: [(25, 25), (55, 25), (40, 40), (25, 55), (55, 55)],
            6: [(25, 25), (55, 25), (25, 40), (55, 40), (25, 55), (55, 55)]
        }
        
        for pos in dot_positions[self.value]:
            pygame.draw.circle(surface, BLACK, (x + pos[0], y + pos[1]), 6)

# --- DRAW BOARD ---
def draw_board(surface):
    # Background
    pygame.draw.rect(surface, LIGHT_BROWN, (BOARD_X - 5, BOARD_Y - 5, 
                     BOARD_SIZE * CELL_SIZE + 10, BOARD_SIZE * CELL_SIZE + 10))
    
    # Draw cells
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = BOARD_X + col * CELL_SIZE
            y = BOARD_Y + row * CELL_SIZE
            
            # Checkerboard pattern
            if (row + col) % 2 == 0:
                color = CREAM
            else:
                color = (245, 222, 179)
            
            pygame.draw.rect(surface, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, DARK_BROWN, (x, y, CELL_SIZE, CELL_SIZE), 2)
            
            # Cell number
            cell_num = (BOARD_SIZE - 1 - row) * BOARD_SIZE
            if (BOARD_SIZE - 1 - row) % 2 == 0:
                cell_num += col + 1
            else:
                cell_num += BOARD_SIZE - col
            
            num_text = font_small.render(str(cell_num), True, BLACK)
            surface.blit(num_text, (x + 5, y + 5))

# --- DRAW SNAKES ---
def draw_snakes(surface):
    for start, end in snakes.items():
        start_x, start_y = get_cell_center(start)
        end_x, end_y = get_cell_center(end)
        
        # Kurva ular
        points = []
        steps = 20
        for i in range(steps + 1):
            t = i / steps
            # Bezier curve
            mid_x = (start_x + end_x) / 2 + random.randint(-30, 30)
            mid_y = (start_y + end_y) / 2 - 50
            
            x = (1-t)**2 * start_x + 2*(1-t)*t * mid_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * mid_y + t**2 * end_y
            points.append((x, y))
        
        pygame.draw.lines(surface, RED, False, points, 8)
        
        # Kepala ular
        pygame.draw.circle(surface, (139, 0, 0), (int(end_x), int(end_y)), 12)
        pygame.draw.circle(surface, RED, (int(end_x - 3), int(end_y - 2)), 3)
        pygame.draw.circle(surface, RED, (int(end_x + 3), int(end_y - 2)), 3)

# --- DRAW LADDERS ---
def draw_ladders(surface):
    for start, end in ladders.items():
        start_x, start_y = get_cell_center(start)
        end_x, end_y = get_cell_center(end)
        
        # Tangga
        pygame.draw.line(surface, DARK_BROWN, (start_x - 10, start_y), (end_x - 10, end_y), 6)
        pygame.draw.line(surface, DARK_BROWN, (start_x + 10, start_y), (end_x + 10, end_y), 6)
        
        # Anak tangga
        steps = 5
        for i in range(steps):
            t = i / (steps - 1)
            x1 = start_x - 10 + t * (end_x - start_x)
            x2 = start_x + 10 + t * (end_x - start_x)
            y = start_y + t * (end_y - start_y)
            pygame.draw.line(surface, DARK_BROWN, (x1, y), (x2, y), 4)

def get_cell_center(position):
    row = (position - 1) // BOARD_SIZE
    col = (position - 1) % BOARD_SIZE
    
    if row % 2 == 1:
        col = BOARD_SIZE - 1 - col
    
    x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
    y = BOARD_Y + (BOARD_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE // 2
    
    return (x, y)

# --- GAME INIT ---
players = [
    Player("Pemain 1", RED, 0),
    Player("Pemain 2", BLUE, 1),
    Player("Pemain 3", GREEN, 2),
    Player("Pemain 4", YELLOW, 3)
]

num_players = 2
dice = Dice()
current_player = 0
game_state = "ROLL"  # ROLL, MOVING, WINNER
winner = None

# Buttons
roll_button = pygame.Rect(650, 300, 120, 50)

# --- MAIN LOOP ---
run = True
while run:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "ROLL" and roll_button.collidepoint(event.pos):
                dice.roll()
                game_state = "ROLLING"
            
            # Number of players selection at start
            if players[0].position == 0 and players[1].position == 0:
                for i in range(4):
                    btn = pygame.Rect(300 + i * 50, 780, 40, 40)
                    if btn.collidepoint(event.pos):
                        num_players = i + 1
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "WINNER":
                # Reset game
                for player in players:
                    player.position = 0
                    player.target_pos = 0
                current_player = 0
                game_state = "ROLL"
                winner = None
    
    # Update
    if game_state == "ROLLING":
        dice.update()
        if not dice.rolling:
            # Move player
            players[current_player].move_to(players[current_player].position + dice.value)
            game_state = "MOVING"
    
    if game_state == "MOVING":
        players[current_player].update()
        if not players[current_player].is_moving:
            # Check winner
            if players[current_player].position >= 100:
                game_state = "WINNER"
                winner = players[current_player]
            else:
                # Next player
                current_player = (current_player + 1) % num_players
                game_state = "ROLL"
    
    # --- DRAW ---
    win.fill((180, 140, 100))
    
    # Title
    title = font_large.render("ULAR TANGGA", True, WHITE)
    title_shadow = font_large.render("ULAR TANGGA", True, BLACK)
    win.blit(title_shadow, (WIDTH//2 - title.get_width()//2 + 2, 22))
    win.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Board
    draw_board(win)
    draw_ladders(win)
    draw_snakes(win)
    
    # Players
    for i in range(num_players):
        players[i].draw(win)
    
    # Dice
    dice.draw(win, 660, 150)
    
    # Roll button
    if game_state == "ROLL":
        pygame.draw.rect(win, GREEN, roll_button, border_radius=10)
        pygame.draw.rect(win, BLACK, roll_button, 3, border_radius=10)
        roll_text = font_medium.render("ROLL", True, WHITE)
        win.blit(roll_text, (roll_button.centerx - roll_text.get_width()//2, 
                            roll_button.centery - roll_text.get_height()//2))
    
    # Current player info
    info_text = font_medium.render(f"Giliran: Pemain {current_player + 1}", True, WHITE)
    win.blit(info_text, (620, 250))
    
    # Player status
    status_y = 400
    for i in range(num_players):
        pygame.draw.circle(win, players[i].color, (630, status_y + i * 40), 12)
        status = font_small.render(f"Pemain {i+1}: Kotak {players[i].position}", True, WHITE)
        win.blit(status, (650, status_y + i * 40 - 10))
    
    # Number of players selection
    if players[0].position == 0 and players[1].position == 0:
        select_text = font_medium.render("Pilih Jumlah Pemain:", True, WHITE)
        win.blit(select_text, (250, 730))
        
        for i in range(4):
            btn = pygame.Rect(300 + i * 50, 780, 40, 40)
            color = GREEN if num_players == i + 1 else LIGHT_BROWN
            pygame.draw.rect(win, color, btn, border_radius=5)
            pygame.draw.rect(win, BLACK, btn, 2, border_radius=5)
            num_text = font_medium.render(str(i + 1), True, BLACK)
            win.blit(num_text, (btn.centerx - 8, btn.centery - 12))
    
    # Winner screen
    if game_state == "WINNER":
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        win.blit(overlay, (0, 0))
        
        winner_text = font_large.render(f"PEMAIN {winner.number + 1} MENANG!", True, winner.color)
        restart_text = font_medium.render("Tekan SPACE untuk main lagi", True, WHITE)
        
        win.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, 300))
        win.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 400))
    
    pygame.display.update()

pygame.quit()
sys.exit()