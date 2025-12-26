import pygame
import random
import math

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 600
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Memanah - Skeleton")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 72)

class Skeleton:
    def __init__(self):
        self.x = 100
        self.y = 500
        self.flesh_level = 0
        
    def draw(self):
        # Warna berubah sesuai level daging
        flesh_colors = [
            (240, 240, 240), (255, 224, 224), (255, 204, 204), 
            (255, 179, 179), (255, 153, 153), (255, 128, 128),
            (255, 102, 102), (255, 77, 77), (255, 51, 51),
            (255, 26, 26), (255, 0, 0)
        ]
        color = flesh_colors[min(self.flesh_level, 10)]
        
        # Kepala
        pygame.draw.circle(screen, color, (self.x, self.y - 80), 20, 0)
        pygame.draw.circle(screen, BLACK, (self.x, self.y - 80), 20, 2)
        
        # Mata
        pygame.draw.circle(screen, BLACK, (self.x - 8, self.y - 85), 3)
        pygame.draw.circle(screen, BLACK, (self.x + 8, self.y - 85), 3)
        
        # Badan
        pygame.draw.line(screen, color, (self.x, self.y - 60), (self.x, self.y - 20), 15)
        
        # Tangan kiri (memegang busur)
        pygame.draw.line(screen, color, (self.x, self.y - 50), (self.x - 40, self.y - 40), 10)
        
        # Tangan kanan
        pygame.draw.line(screen, color, (self.x, self.y - 50), (self.x + 40, self.y - 30), 10)
        
        # Kaki
        pygame.draw.line(screen, color, (self.x, self.y - 20), (self.x - 20, self.y + 20), 10)
        pygame.draw.line(screen, color, (self.x, self.y - 20), (self.x + 20, self.y + 20), 10)
        
        # Busur
        pygame.draw.arc(screen, BROWN, (self.x - 60, self.y - 60, 30, 50), 0, math.pi, 3)
        pygame.draw.line(screen, GRAY, (self.x - 45, self.y - 55), (self.x - 45, self.y - 15), 1)

class Arrow:
    def __init__(self, x, y, power, angle):
        self.x = x
        self.y = y
        self.power = power
        self.angle = angle
        self.speed_x = power * math.cos(math.radians(angle)) / 5
        self.speed_y = power * math.sin(math.radians(angle)) / 5
        self.active = True
        
    def update(self):
        if self.active:
            self.x += self.speed_x
            self.speed_y += 0.3  # Gravitasi
            self.y -= self.speed_y
            
            # Hapus jika keluar layar
            if self.x > WIDTH or self.y > HEIGHT or self.x < 0 or self.y < 0:
                self.active = False
                
    def draw(self):
        if self.active:
            # Hitung sudut panah berdasarkan kecepatan
            angle = math.degrees(math.atan2(-self.speed_y, self.speed_x))
            
            # Gambar panah
            end_x = self.x + 30 * math.cos(math.radians(angle))
            end_y = self.y - 30 * math.sin(math.radians(angle))
            pygame.draw.line(screen, BROWN, (self.x, self.y), (end_x, end_y), 3)
            
            # Ujung panah
            tip_x = end_x + 10 * math.cos(math.radians(angle))
            tip_y = end_y - 10 * math.sin(math.radians(angle))
            pygame.draw.polygon(screen, GRAY, [
                (tip_x, tip_y),
                (end_x - 5 * math.sin(math.radians(angle)), end_y - 5 * math.cos(math.radians(angle))),
                (end_x + 5 * math.sin(math.radians(angle)), end_y + 5 * math.cos(math.radians(angle)))
            ])

class Target:
    def __init__(self):
        self.x = random.randint(400, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 200)
        self.size = 30
        self.active = True
        self.hit = False
        self.lifetime = 0
        
    def update(self):
        self.lifetime += 1
        if self.lifetime > 180:  # 3 detik
            self.active = False
            
    def draw(self):
        if self.active and not self.hit:
            # Gambar target tengkorak sederhana
            # Kepala
            pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size, 0)
            pygame.draw.circle(screen, BLACK, (self.x, self.y), self.size, 2)
            
            # Mata
            pygame.draw.circle(screen, BLACK, (self.x - 10, self.y - 5), 5)
            pygame.draw.circle(screen, BLACK, (self.x + 10, self.y - 5), 5)
            
            # Hidung
            pygame.draw.polygon(screen, BLACK, [
                (self.x - 5, self.y + 5),
                (self.x + 5, self.y + 5),
                (self.x, self.y + 15)
            ])
        elif self.hit:
            # Animasi hit
            pygame.draw.circle(screen, RED, (self.x, self.y), self.size + 10, 3)
            
    def check_collision(self, arrow):
        if not self.hit and self.active and arrow.active:
            distance = math.sqrt((self.x - arrow.x)**2 + (self.y - arrow.y)**2)
            if distance < self.size + 5:
                self.hit = True
                arrow.active = False
                return True
        return False

def draw_aim_indicator(skeleton_x, skeleton_y, angle, power, charging):
    """Menggambar indikator bidikan dengan garis lengkung"""
    if charging or power > 0:
        # Titik awal panah
        start_x = skeleton_x
        start_y = skeleton_y - 50
        
        # Gambar garis lintasan prediksi
        points = []
        speed_x = power * math.cos(math.radians(angle)) / 5
        speed_y = power * math.sin(math.radians(angle)) / 5
        
        # Simulasi lintasan
        sim_x = start_x
        sim_y = start_y
        for i in range(30):
            points.append((int(sim_x), int(sim_y)))
            sim_x += speed_x
            speed_y += 0.3  # Gravitasi
            sim_y -= speed_y
            
            if sim_x > WIDTH or sim_y > HEIGHT:
                break
        
        # Gambar garis lintasan dengan titik-titik
        for i in range(len(points) - 1):
            alpha = 255 - (i * 8)  # Fade out
            if alpha > 0:
                pygame.draw.circle(screen, YELLOW, points[i], 2)
        
        # Gambar garis sudut langsung dari skeleton
        aim_length = 80
        aim_end_x = start_x + aim_length * math.cos(math.radians(angle))
        aim_end_y = start_y - aim_length * math.sin(math.radians(angle))
        pygame.draw.line(screen, RED, (start_x, start_y), (aim_end_x, aim_end_y), 3)
        
        # Panah di ujung garis
        arrow_size = 10
        arrow_angle1 = math.radians(angle + 150)
        arrow_angle2 = math.radians(angle - 150)
        arrow_x1 = aim_end_x - arrow_size * math.cos(arrow_angle1)
        arrow_y1 = aim_end_y + arrow_size * math.sin(arrow_angle1)
        arrow_x2 = aim_end_x - arrow_size * math.cos(arrow_angle2)
        arrow_y2 = aim_end_y + arrow_size * math.sin(arrow_angle2)
        pygame.draw.polygon(screen, RED, [(aim_end_x, aim_end_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)])

def draw_power_and_angle_bar(power, angle):
    """Menggambar bar daya dan sudut secara bersamaan"""
    bar_width = 300
    bar_height = 30
    bar_x = WIDTH // 2 - bar_width // 2
    bar_y = HEIGHT - 120
    
    # === POWER BAR ===
    # Background bar
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
    
    # Power bar fill
    power_width = (power / 100) * bar_width
    if power < 30:
        color = GREEN
    elif power < 70:
        color = ORANGE
    else:
        color = RED
    pygame.draw.rect(screen, color, (bar_x, bar_y, power_width, bar_height))
    
    # Border
    pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 2)
    
    # Text
    power_text = font.render(f"Daya: {int(power)}%", True, WHITE)
    screen.blit(power_text, (bar_x + bar_width // 2 - power_text.get_width() // 2, bar_y - 35))
    
    # === ANGLE BAR ===
    angle_bar_y = bar_y + 45
    
    # Background
    pygame.draw.rect(screen, GRAY, (bar_x, angle_bar_y, bar_width, bar_height))
    
    # Angle indicator (sudut 0-90 derajat)
    angle_pos = (angle / 90) * bar_width
    
    # Color gradient based on angle
    if angle < 30:
        angle_color = BLUE
    elif angle < 60:
        angle_color = GREEN
    else:
        angle_color = ORANGE
    
    # Fill bar sampai posisi sudut
    pygame.draw.rect(screen, angle_color, (bar_x, angle_bar_y, angle_pos, bar_height))
    
    # Marker untuk posisi sudut saat ini
    marker_x = bar_x + angle_pos
    pygame.draw.rect(screen, RED, (marker_x - 3, angle_bar_y - 5, 6, bar_height + 10))
    
    # Border
    pygame.draw.rect(screen, BLACK, (bar_x, angle_bar_y, bar_width, bar_height), 2)
    
    # Text sudut
    angle_text = font.render(f"Sudut: {int(angle)}°", True, WHITE)
    screen.blit(angle_text, (bar_x + bar_width // 2 - angle_text.get_width() // 2, angle_bar_y - 35))
    
    # Indicator marks (0, 30, 45, 60, 90 derajat)
    marks = [0, 30, 45, 60, 90]
    for mark in marks:
        mark_x = bar_x + (mark / 90) * bar_width
        pygame.draw.line(screen, WHITE, (mark_x, angle_bar_y + bar_height), (mark_x, angle_bar_y + bar_height + 5), 2)
        mark_text = small_font.render(str(mark), True, WHITE)
        screen.blit(mark_text, (mark_x - mark_text.get_width() // 2, angle_bar_y + bar_height + 8))

def main():
    running = True
    game_state = "menu"  # menu, playing, game_over
    
    skeleton = Skeleton()
    arrows = []
    targets = []
    
    score = 0
    power = 0
    angle = 45  # Sudut awal
    charging = False
    
    target_spawn_timer = 0
    
    while running:
        clock.tick(FPS)
        
        # Input keys
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if game_state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "playing"
                        score = 0
                        skeleton.flesh_level = 0
                        arrows = []
                        targets = []
                        angle = 45
                        
            elif game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        charging = True
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE and charging:
                        charging = False
                        # Tembak panah
                        arrow = Arrow(skeleton.x, skeleton.y - 50, power, angle)
                        arrows.append(arrow)
                        power = 0
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = "menu"
        
        # Update game
        if game_state == "playing":
            # Atur sudut dengan tombol panah atau Q/E
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                angle = min(angle + 1.5, 90)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                angle = max(angle - 1.5, 0)
            
            # Charging power
            if charging:
                power = min(power + 2, 100)
            
            # Update arrows
            for arrow in arrows:
                arrow.update()
            
            # Remove inactive arrows
            arrows = [arrow for arrow in arrows if arrow.active]
            
            # Spawn targets
            target_spawn_timer += 1
            if target_spawn_timer > 90:  # Setiap 1.5 detik
                targets.append(Target())
                target_spawn_timer = 0
            
            # Update targets
            for target in targets:
                target.update()
                
                # Check collision
                for arrow in arrows:
                    if target.check_collision(arrow):
                        score += 10
                        skeleton.flesh_level = min(skeleton.flesh_level + 1, 10)
            
            # Remove inactive targets
            targets = [target for target in targets if target.active or target.hit]
            targets = [target for target in targets if not target.hit or target.lifetime < 200]
        
        # Draw
        screen.fill(SKY_BLUE)
        
        if game_state == "menu":
            # Menu
            title = big_font.render("GAME MEMANAH", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
            
            subtitle = font.render("Tekan SPASI untuk Mulai", True, WHITE)
            screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2))
            
            info1 = small_font.render("Tahan SPASI = Isi Daya, Lepas = Tembak", True, WHITE)
            screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, HEIGHT // 2 + 50))
            
            info2 = small_font.render("W/S atau Panah Atas/Bawah = Atur Sudut", True, WHITE)
            screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, HEIGHT // 2 + 85))
            
        elif game_state == "playing":
            # Gambar background
            pygame.draw.rect(screen, GREEN, (0, HEIGHT - 100, WIDTH, 100))
            
            # Gambar gunung
            pygame.draw.polygon(screen, GRAY, [
                (600, HEIGHT - 100),
                (750, 200),
                (WIDTH, HEIGHT - 100)
            ])
            
            # Draw aim indicator
            draw_aim_indicator(skeleton.x, skeleton.y, angle, power, charging)
            
            # Draw game objects
            skeleton.draw()
            
            for target in targets:
                target.draw()
            
            for arrow in arrows:
                arrow.draw()
            
            # Draw UI
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            flesh_text = font.render(f"Daging: {skeleton.flesh_level}/10", True, WHITE)
            screen.blit(flesh_text, (10, 50))
            
            # Draw power and angle bars
            draw_power_and_angle_bar(power, angle)
            
            # Instructions
            inst_text = small_font.render("SPASI = Tembak | W/S = Sudut | R = Reset", True, WHITE)
            screen.blit(inst_text, (WIDTH // 2 - inst_text.get_width() // 2, 10))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()