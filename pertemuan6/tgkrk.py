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
PURPLE = (128, 0, 128)

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Memanah - Skeleton Army")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 72)

class Skeleton:
    def __init__(self, x=100, y=500):
        self.x = x
        self.y = y
        self.ground_y = y  # Posisi tanah
        self.flesh_level = 0
        self.is_clone = False
        self.clone_timer = 0
        self.max_clone_time = 300  # 5 detik
        # Jumping mechanics
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 0.8
        self.jump_power = -15
        # Movement
        self.move_speed = 5
        # AI shooting for clones
        self.shoot_cooldown = 0
        self.shoot_delay = 60  # Frame antara tembakan clone
        
    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = self.jump_power
    
    def can_shoot(self):
        """Check if clone can shoot"""
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_delay
            return True
        return False
        
    def update(self, keys=None):
        # Handle movement for main skeleton (not clones)
        if not self.is_clone and keys:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.x = max(50, self.x - self.move_speed)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.x = min(300, self.x + self.move_speed)
        
        # Handle jumping physics
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity
            
            # Check if landed
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.jump_velocity = 0
        
        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # Clone timer
        if self.is_clone:
            self.clone_timer += 1
            if self.clone_timer >= self.max_clone_time:
                return False  # Hapus clone
        return True
    
    def clone_shoot(self, targets):
        """Clone AI untuk menembak target terdekat"""
        if not self.is_clone or not self.can_shoot():
            return None
        
        # Cari target terdekat
        closest_target = None
        min_distance = float('inf')
        
        for target in targets:
            if target.active and not target.hit:
                distance = math.sqrt((self.x - target.x)**2 + (self.y - target.y)**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_target = target
        
        if closest_target:
            # Hitung sudut dan daya untuk menembak target
            dx = closest_target.x - self.x
            dy = self.y - closest_target.y
            
            # Hitung sudut
            angle = math.degrees(math.atan2(dy, dx))
            angle = max(10, min(80, angle))  # Batasi sudut
            
            # Hitung daya berdasarkan jarak
            distance = math.sqrt(dx**2 + dy**2)
            power = min(100, 40 + distance * 0.15)
            
            return Arrow(self.x, self.y - 50, power, angle)
        
        return None
        
    def draw(self):
        # Warna berubah sesuai level daging
        flesh_colors = [
            (240, 240, 240), (255, 224, 224), (255, 204, 204), 
            (255, 179, 179), (255, 153, 153), (255, 128, 128),
            (255, 102, 102), (255, 77, 77), (255, 51, 51),
            (255, 26, 26), (255, 0, 0)
        ]
        color = flesh_colors[min(self.flesh_level, 10)]
        
        # Efek berkedip untuk clone
        if self.is_clone and self.clone_timer % 20 < 10:
            color = tuple(max(0, c - 50) for c in color)
        
        # Kepala
        pygame.draw.circle(screen, color, (int(self.x), int(self.y) - 80), 20, 0)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y) - 80), 20, 2)
        
        # Mata
        pygame.draw.circle(screen, BLACK, (int(self.x) - 8, int(self.y) - 85), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x) + 8, int(self.y) - 85), 3)
        
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
        pygame.draw.arc(screen, BROWN, (int(self.x) - 60, int(self.y) - 60, 30, 50), 0, math.pi, 3)
        pygame.draw.line(screen, GRAY, (self.x - 45, self.y - 55), (self.x - 45, self.y - 15), 1)
        
        # Label CLONE jika clone
        if self.is_clone:
            clone_text = small_font.render("CLONE", True, PURPLE)
            screen.blit(clone_text, (int(self.x) - clone_text.get_width() // 2, int(self.y) - 120))
            
            # Cooldown bar untuk clone
            if self.shoot_cooldown > 0:
                bar_width = 60
                bar_height = 5
                bar_x = self.x - bar_width // 2
                bar_y = self.y - 130
                
                # Background
                pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
                
                # Cooldown progress
                progress = (self.shoot_delay - self.shoot_cooldown) / self.shoot_delay
                pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * progress, bar_height))

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
    def __init__(self, speed_multiplier=1.0):
        self.x = random.randint(400, WIDTH - 50)
        self.y = random.randint(100, HEIGHT - 200)
        self.size = 30
        self.active = True
        self.hit = False
        self.lifetime = 0
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.5, 1.5) * speed_multiplier
        self.speed_y = random.uniform(-0.5, 0.5) * speed_multiplier
        
    def update(self):
        self.lifetime += 1
        if self.lifetime > 240:  # 4 detik
            self.active = False
        
        # Bergerak
        if not self.hit:
            self.x += self.speed_x
            self.y += self.speed_y
            
            # Bounce dari tepi
            if self.x < 350 or self.x > WIDTH - 50:
                self.speed_x *= -1
            if self.y < 100 or self.y > HEIGHT - 150:
                self.speed_y *= -1
            
    def draw(self):
        if self.active and not self.hit:
            # Gambar target tengkorak sederhana
            # Kepala
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size, 0)
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size, 2)
            
            # Mata
            pygame.draw.circle(screen, BLACK, (int(self.x) - 10, int(self.y) - 5), 5)
            pygame.draw.circle(screen, BLACK, (int(self.x) + 10, int(self.y) - 5), 5)
            
            # Hidung
            pygame.draw.polygon(screen, BLACK, [
                (self.x - 5, self.y + 5),
                (self.x + 5, self.y + 5),
                (self.x, self.y + 15)
            ])
        elif self.hit:
            # Animasi hit
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size + 10, 3)
            
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
            if i < len(points):
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

def draw_clone_aim(skeleton):
    """Gambar garis aim untuk clone"""
    if skeleton.is_clone and skeleton.shoot_cooldown <= 10:
        start_x = skeleton.x
        start_y = skeleton.y - 50
        
        # Garis sederhana ke arah target
        aim_length = 60
        pygame.draw.line(screen, PURPLE, (start_x, start_y), (start_x + aim_length, start_y - 30), 2)

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
    
    skeletons = [Skeleton()]  # List untuk menampung skeleton dan klonnya
    arrows = []
    targets = []
    
    score = 0
    power = 0
    angle = 45  # Sudut awal
    charging = False
    
    target_spawn_timer = 0
    target_spawn_rate = 90  # Frame antara spawn
    monster_speed_multiplier = 1.0
    
    clone_created = False
    transformation_timer = 0
    show_transformation = False
    
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
                        skeletons = [Skeleton()]
                        arrows = []
                        targets = []
                        angle = 45
                        target_spawn_rate = 90
                        monster_speed_multiplier = 1.0
                        clone_created = False
                        
            elif game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        charging = True
                    # Jump with J key or Up arrow (if not used for aiming)
                    elif event.key == pygame.K_j:
                        skeletons[0].jump()
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE and charging:
                        charging = False
                        # Tembak panah dari skeleton utama
                        main_skeleton = skeletons[0]
                        arrow = Arrow(main_skeleton.x, main_skeleton.y - 50, power, angle)
                        arrows.append(arrow)
                        power = 0
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = "menu"
        
        # Update game
        if game_state == "playing":
            # Atur sudut dengan tombol panah atau W/S
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
            if target_spawn_timer > target_spawn_rate:
                targets.append(Target(monster_speed_multiplier))
                target_spawn_timer = 0
            
            # Update targets
            for target in targets:
                target.update()
                
                # Check collision
                for arrow in arrows:
                    if target.check_collision(arrow):
                        score += 10
                        skeletons[0].flesh_level = min(skeletons[0].flesh_level + 1, 10)
                        
                        # Cek jika daging penuh dan belum ada clone
                        if skeletons[0].flesh_level >= 10 and not clone_created:
                            show_transformation = True
                            transformation_timer = 0
            
            # Update skeletons
            for skeleton in skeletons:
                if skeleton == skeletons[0]:  # Main skeleton
                    skeleton.update(keys)
                else:  # Clones
                    skeleton.update()
                    # Clone shoots automatically
                    clone_arrow = skeleton.clone_shoot(targets)
                    if clone_arrow:
                        arrows.append(clone_arrow)
            
            # Remove dead clones
            skeletons = [s for s in skeletons if s == skeletons[0] or s.update()]
            
            # Transformasi ketika daging penuh
            if show_transformation:
                transformation_timer += 1
                if transformation_timer >= 60:  # 1 detik
                    # Buat clone di posisi berbeda
                    clone_positions = [(200, 500), (250, 500), (150, 500), (100, 500)]
                    clone_x = clone_positions[min(len(skeletons) - 1, len(clone_positions) - 1)][0]
                    
                    clone = Skeleton(x=clone_x, y=500)
                    clone.flesh_level = 10
                    clone.is_clone = True
                    skeletons.append(clone)
                    
                    # Reset skeleton utama
                    skeletons[0].flesh_level = 0
                    
                    # Tingkatkan kesulitan
                    target_spawn_rate = max(30, target_spawn_rate - 15)
                    monster_speed_multiplier += 0.3
                    
                    # Spawn beberapa monster sekaligus
                    for _ in range(3):
                        targets.append(Target(monster_speed_multiplier))
                    
                    clone_created = True
                    show_transformation = False
                    transformation_timer = 0
                    
                    # Bisa buat clone lagi nanti
                    clone_created = False
            
            # Remove inactive targets
            targets = [target for target in targets if target.active or target.hit]
            targets = [target for target in targets if not target.hit or target.lifetime < 200]
        
        # Draw
        screen.fill(SKY_BLUE)
        
        if game_state == "menu":
            # Menu
            title = big_font.render("SKELETON ARMY", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3 - 50))
            
            subtitle = font.render("Tekan SPASI untuk Mulai", True, WHITE)
            screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2))
            
            info1 = small_font.render("Tahan SPASI = Isi Daya, Lepas = Tembak", True, WHITE)
            screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, HEIGHT // 2 + 50))
            
            info2 = small_font.render("W/S = Atur Sudut | A/D = Gerak | J = Lompat", True, WHITE)
            screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, HEIGHT // 2 + 85))
            
            info3 = small_font.render("Daging Penuh = Klon Muncul & Membantu!", True, PURPLE)
            screen.blit(info3, (WIDTH // 2 - info3.get_width() // 2, HEIGHT // 2 + 120))
            
        elif game_state == "playing":
            # Gambar background
            pygame.draw.rect(screen, GREEN, (0, HEIGHT - 100, WIDTH, 100))
            
            # Gambar gunung
            pygame.draw.polygon(screen, GRAY, [
                (600, HEIGHT - 100),
                (750, 200),
                (WIDTH, HEIGHT - 100)
            ])
            
            # Draw aim indicator (hanya untuk skeleton utama)
            draw_aim_indicator(skeletons[0].x, skeletons[0].y, angle, power, charging)
            
            # Draw game objects
            for skeleton in skeletons:
                draw_clone_aim(skeleton)  # Aim untuk clone
                skeleton.draw()
            
            for target in targets:
                target.draw()
            
            for arrow in arrows:
                arrow.draw()
            
            # Efek transformasi
            if show_transformation:
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(100)
                overlay.fill(PURPLE)
                screen.blit(overlay, (0, 0))
                
                transform_text = big_font.render("TRANSFORMASI!", True, WHITE)
                screen.blit(transform_text, (WIDTH // 2 - transform_text.get_width() // 2, HEIGHT // 2 - 50))
                
                clone_text = font.render("KLON MEMBANTU MENEMBAK!", True, YELLOW)
                screen.blit(clone_text, (WIDTH // 2 - clone_text.get_width() // 2, HEIGHT // 2 + 20))
            
            # Draw UI
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            flesh_text = font.render(f"Daging: {skeletons[0].flesh_level}/10", True, WHITE)
            screen.blit(flesh_text, (10, 50))
            
            clone_count_text = small_font.render(f"Klon Aktif: {len(skeletons) - 1}", True, PURPLE)
            screen.blit(clone_count_text, (10, 90))
            
            monster_text = small_font.render(f"Monster: {len([t for t in targets if not t.hit])}", True, RED)
            screen.blit(monster_text, (10, 120))
            
            # Draw power and angle bars
            draw_power_and_angle_bar(power, angle)
            
            # Instructions
            inst_text = small_font.render("SPASI = Tembak | W/S = Sudut | A/D = Gerak | J = Lompat | R = Menu", True, WHITE)
            screen.blit(inst_text, (WIDTH // 2 - inst_text.get_width() // 2, 10))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()