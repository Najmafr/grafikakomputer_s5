import pygame
import random
import sys

pygame.init()

# --- WINDOW ---
WIDTH = 500
HEIGHT = 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Subway Surf Luffy")
clock = pygame.time.Clock()

# --- SAFE LOAD IMAGE ---
try:
    luffy_img = pygame.image.load("stock-vector-monkey-d-luffy-straw-hat-pirates-2370797475-removebg-preview.png").convert_alpha()
    luffy_img = pygame.transform.smoothscale(luffy_img, (90, 90))
except:
    print("WARNING: File 'luffy_head.png' tidak ditemukan! Menggunakan straw hat placeholder.")
    # Buat surface pengganti dengan topi jerami Luffy
    luffy_img = pygame.Surface((90, 90), pygame.SRCALPHA)
    # Gambar topi jerami sederhana
    pygame.draw.circle(luffy_img, (255, 220, 150), (45, 50), 35)
    pygame.draw.circle(luffy_img, (220, 180, 100), (45, 35), 30)
    pygame.draw.rect(luffy_img, (200, 50, 50), (15, 32, 60, 8))
    # Mata
    pygame.draw.circle(luffy_img, (0, 0, 0), (35, 55), 3)
    pygame.draw.circle(luffy_img, (0, 0, 0), (55, 55), 3)
    # Senyum
    pygame.draw.arc(luffy_img, (0, 0, 0), (30, 55, 30, 20), 3.14, 6.28, 2)

# --- PLAYER ---
LANES = [100, 200, 300]  # 3 jalur yang lebih jelas
player_lane = 1  # mulai di tengah
player_x = LANES[player_lane]
player_y = 550
player_width = 80
player_height = 80

# --- OBSTACLE ---
obstacles = []
OBSTACLE_SPEED = 7
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 60

# --- SCORE ---
score = 0
font = pygame.font.Font(None, 36)

def spawn_obstacle():
    lane = random.randint(0, 2)
    x = LANES[lane]
    obstacles.append(pygame.Rect(x, -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

def reset_game():
    global obstacles, score, player_lane, player_x, spawn_timer
    obstacles = []
    score = 0
    player_lane = 1
    player_x = LANES[player_lane]
    spawn_timer = 0

def game_over_screen():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    win.blit(overlay, (0, 0))
    
    game_over_font = pygame.font.Font(None, 70)
    score_font = pygame.font.Font(None, 40)
    restart_font = pygame.font.Font(None, 30)
    
    game_over_text = game_over_font.render("GAME OVER", True, (255, 100, 100))
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = restart_font.render("Tekan SPACE untuk main lagi", True, (200, 200, 200))
    quit_text = restart_font.render("Tekan ESC untuk keluar", True, (200, 200, 200))
    
    win.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 250))
    win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 330))
    win.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 400))
    win.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, 440))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# --- MAIN LOOP ---
run = True
spawn_timer = 0
move_cooldown = 0

while run:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Kontrol menggunakan key press (lebih responsif)
        if event.type == pygame.KEYDOWN and move_cooldown == 0:
            if event.key == pygame.K_LEFT and player_lane > 0:
                player_lane -= 1
                player_x = LANES[player_lane]
                move_cooldown = 10
            elif event.key == pygame.K_RIGHT and player_lane < 2:
                player_lane += 1
                player_x = LANES[player_lane]
                move_cooldown = 10
    
    if move_cooldown > 0:
        move_cooldown -= 1
    
    # --- BACKGROUND ---
    win.fill((30, 30, 30))
    
    # Gambar jalur
    for i in range(3):
        pygame.draw.rect(win, (50, 50, 50), (LANES[i] - 40, 0, 80, HEIGHT), 2)
    
    # --- SPAWN ---
    spawn_timer += 1
    spawn_rate = max(30, 50 - score // 10)  # semakin cepat seiring score naik
    if spawn_timer > spawn_rate:
        spawn_obstacle()
        spawn_timer = 0
    
    # --- MOVE OBSTACLES ---
    for obs in obstacles[:]:
        obs.y += OBSTACLE_SPEED
        pygame.draw.rect(win, (255, 80, 80), obs, border_radius=5)
        
        # Tambah score saat obstacle melewati player
        if obs.y > player_y + player_height and obs.y < player_y + player_height + OBSTACLE_SPEED:
            score += 1
        
        if obs.y > HEIGHT:
            obstacles.remove(obs)
    
    # --- DRAW PLAYER ---
    win.blit(luffy_img, (player_x - 40, player_y))
    
    # --- COLLISION ---
    player_rect = pygame.Rect(player_x - 35, player_y + 10, player_width, player_height - 10)
    
    for obs in obstacles:
        if player_rect.colliderect(obs):
            game_over_screen()
    
    # --- DRAW SCORE ---
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))
    
    pygame.display.update()

pygame.quit()
sys.exit()