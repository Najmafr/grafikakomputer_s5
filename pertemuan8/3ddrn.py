import pygame
import math
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 600
FPS = 60

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 212, 255)
RED = (255, 107, 107)
YELLOW = (255, 215, 0)
GREEN = (0, 255, 100)
PURPLE = (200, 100, 255)

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚁 3D Drone Navigator")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Drone:
    def __init__(self):
        # TRANSLASI 3D
        self.x = 0
        self.y = 0
        self.z = 0
        
        # ROTASI 3D
        self.rot_x = 0
        self.rot_y = 0
        self.rot_z = 0
        
        # SKALA 3D
        self.scale = 1.0
        
        # REFLEKSI 3D
        self.mirror_mode = False
        
        self.speed = 5
        self.blade_rotation = 0
        
    def update(self, keys):
        # TRANSLASI 3D - Gerakan dalam ruang 3D
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_SPACE]:
            self.z += self.speed
            
        # ROTASI 3D - Putar drone
        if keys[pygame.K_q]:
            self.rot_z += 5
        if keys[pygame.K_e]:
            self.rot_z -= 5
        if keys[pygame.K_r]:
            self.rot_x += 5
        if keys[pygame.K_f]:
            self.rot_x -= 5
            
        # SKALA 3D - Ubah ukuran
        if keys[pygame.K_z] and self.scale > 0.3:
            self.scale -= 0.02
        if keys[pygame.K_x] and self.scale < 2.0:
            self.scale += 0.02
            
        # Batasi pergerakan
        self.x = max(-200, min(200, self.x))
        self.y = max(-200, min(200, self.y))
        self.z = max(0, self.z)
        
        # Rotasi baling-baling
        self.blade_rotation += 10
        
    def draw(self, surface):
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        # Terapkan SKALA 3D
        size = int(50 * self.scale)
        blade_size = int(30 * self.scale)
        
        # Body drone dengan rotasi
        angle_rad = math.radians(self.rot_z)
        
        # Hitung titik-titik body yang dirotasi
        points = []
        for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            x = dx * size
            y = dy * size
            # Rotasi
            rx = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            ry = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            points.append((center_x + rx, center_y + ry))
        
        # Gambar body
        pygame.draw.polygon(surface, CYAN, points)
        pygame.draw.polygon(surface, WHITE, points, 3)
        
        # Gambar baling-baling (4 motor)
        blade_angle = math.radians(self.blade_rotation)
        for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            motor_x = center_x + dx * blade_size * 1.5
            motor_y = center_y + dy * blade_size * 1.5
            
            # Baling-baling berputar
            for i in range(4):
                angle = blade_angle + i * math.pi / 2
                x1 = motor_x + math.cos(angle) * blade_size
                y1 = motor_y + math.sin(angle) * blade_size
                x2 = motor_x + math.cos(angle + math.pi) * blade_size
                y2 = motor_y + math.sin(angle + math.pi) * blade_size
                pygame.draw.line(surface, RED, (x1, y1), (x2, y2), 3)
            
            # Motor point
            pygame.draw.circle(surface, YELLOW, (int(motor_x), int(motor_y)), 5)

class Obstacle:
    def __init__(self, z, level):
        self.x = random.randint(-150, 150)
        self.y = random.randint(-150, 150)
        self.z = z
        self.width = 150 - level * 5
        self.height = 150 - level * 5
        self.type = random.choice(['vertical', 'horizontal'])
        
    def draw(self, surface, drone):
        distance = self.z - drone.z
        
        if distance > 0 and distance < 500:
            scale = 300 / (distance + 100)
            
            # REFLEKSI 3D - Balik koordinat Y jika mirror mode
            y_mult = -1 if drone.mirror_mode else 1
            
            screen_x = WIDTH // 2 + (self.x - drone.x) * scale
            screen_y = HEIGHT // 2 + (self.y - drone.y) * scale * y_mult
            w = self.width * scale
            h = self.height * scale
            
            # Opacity berdasarkan jarak
            alpha = int(200 / (distance / 100 + 1))
            color = (*RED, alpha)
            
            # Buat surface dengan alpha
            obstacle_surf = pygame.Surface((int(w * 2), int(h * 2)), pygame.SRCALPHA)
            
            if self.type == 'vertical':
                # Lubang vertikal (kiri-kanan terbuka)
                pygame.draw.rect(obstacle_surf, RED, (0, int(h/2), int(w), int(h)))
                pygame.draw.rect(obstacle_surf, RED, (int(w*2-w), int(h/2), int(w), int(h)))
            else:
                # Lubang horizontal (atas-bawah terbuka)
                pygame.draw.rect(obstacle_surf, RED, (int(w/2), 0, int(w), int(h)))
                pygame.draw.rect(obstacle_surf, RED, (int(w/2), int(h*2-h), int(w), int(h)))
            
            surface.blit(obstacle_surf, (int(screen_x - w), int(screen_y - h)))
            
            # Tanda jarak
            dist_text = small_font.render(f"{int(distance)}m", True, WHITE)
            surface.blit(dist_text, (int(screen_x - 20), int(screen_y - h - 20)))
    
    def check_collision(self, drone):
        distance = abs(self.z - drone.z)
        if distance < 50:
            drone_radius = 20 * drone.scale
            
            # Cek apakah drone di dalam lubang
            gap_x = self.width / 2 if self.type == 'vertical' else 0
            gap_y = self.height / 2 if self.type == 'horizontal' else 0
            
            if abs(drone.x) > gap_x or abs(drone.y) > gap_y:
                if drone_radius > 15:
                    return True
        return False

class Game:
    def __init__(self):
        self.drone = Drone()
        self.obstacles = []
        self.score = 0
        self.level = 1
        self.game_state = 'menu'  # menu, playing, gameover
        self.generate_obstacles()
        
    def generate_obstacles(self):
        self.obstacles = []
        for i in range(5 + self.level):
            self.obstacles.append(Obstacle(100 + i * 200, self.level))
    
    def update(self, keys, events):
        if self.game_state == 'playing':
            # Update drone
            old_mirror = self.drone.mirror_mode
            self.drone.update(keys)
            
            # Toggle mirror mode dengan M
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.drone.mirror_mode = not self.drone.mirror_mode
            
            # Cek tabrakan
            for obs in self.obstacles:
                if obs.check_collision(self.drone):
                    self.game_state = 'gameover'
                    return
            
            # Update score
            passed = sum(1 for obs in self.obstacles if obs.z < self.drone.z - 100)
            self.score = passed * 10
            
            # Level up
            if self.drone.z > 100 + len(self.obstacles) * 200:
                self.level += 1
                self.drone.z = 0
                self.drone.x = 0
                self.drone.y = 0
                self.generate_obstacles()
    
    def draw(self, surface):
        # Background
        surface.fill((15, 15, 30))
        
        # Grid
        for i in range(-300, 300, 50):
            y = HEIGHT // 2 + i - (self.drone.y // 2 if not self.drone.mirror_mode else -self.drone.y // 2)
            pygame.draw.line(surface, (50, 100, 150), (0, y), (WIDTH, y), 1)
        
        # Obstacles
        for obs in self.obstacles:
            obs.draw(surface, self.drone)
        
        # Drone
        self.drone.draw(surface)
        
        # Crosshair
        pygame.draw.circle(surface, GREEN, (WIDTH // 2, HEIGHT // 2), 40, 2)
        pygame.draw.line(surface, GREEN, (WIDTH // 2 - 30, HEIGHT // 2), (WIDTH // 2 - 10, HEIGHT // 2), 2)
        pygame.draw.line(surface, GREEN, (WIDTH // 2 + 10, HEIGHT // 2), (WIDTH // 2 + 30, HEIGHT // 2), 2)
        pygame.draw.line(surface, GREEN, (WIDTH // 2, HEIGHT // 2 - 30), (WIDTH // 2, HEIGHT // 2 - 10), 2)
        pygame.draw.line(surface, GREEN, (WIDTH // 2, HEIGHT // 2 + 10), (WIDTH // 2, HEIGHT // 2 + 30), 2)
        
        # HUD
        score_text = small_font.render(f"Score: {self.score}", True, YELLOW)
        level_text = small_font.render(f"Level: {self.level}", True, GREEN)
        scale_text = small_font.render(f"Scale: {self.drone.scale:.1f}x", True, PURPLE)
        rot_text = small_font.render(f"Rotation: {int(self.drone.rot_z)}°", True, CYAN)
        mirror_text = small_font.render(f"Mirror: {'ON' if self.drone.mirror_mode else 'OFF'}", True, YELLOW if self.drone.mirror_mode else WHITE)
        
        surface.blit(score_text, (10, 10))
        surface.blit(level_text, (10, 40))
        surface.blit(scale_text, (10, 70))
        surface.blit(rot_text, (10, 100))
        surface.blit(mirror_text, (10, 130))
        
        # Menu
        if self.game_state == 'menu':
            self.draw_menu(surface)
        elif self.game_state == 'gameover':
            self.draw_gameover(surface)
    
    def draw_menu(self, surface):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        title = font.render("🚁 3D DRONE NAVIGATOR", True, CYAN)
        subtitle = small_font.render("Transformasi 3D: Translasi, Rotasi, Skala, Refleksi", True, WHITE)
        
        controls = [
            "KONTROL:",
            "WASD/Arrow - Translasi 3D (Gerak X,Y)",
            "Space - Maju (Z)",
            "Q/E - Rotasi Z", 
            "R/F - Rotasi X",
            "Z/X - Skala (Perkecil/Perbesar)",
            "M - Refleksi (Mirror Mode)",
            "",
            "Tekan ENTER untuk mulai!"
        ]
        
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        surface.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 150))
        
        y = 220
        for line in controls:
            text = small_font.render(line, True, WHITE if line else CYAN)
            surface.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            y += 30
    
    def draw_gameover(self, surface):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        title = font.render("GAME OVER!", True, RED)
        score_text = font.render(f"Score: {self.score}", True, YELLOW)
        level_text = small_font.render(f"Level: {self.level}", True, WHITE)
        restart = small_font.render("Tekan ENTER untuk main lagi", True, CYAN)
        
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
        surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 270))
        surface.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 320))
        surface.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 400))
    
    def reset(self):
        self.drone = Drone()
        self.score = 0
        self.level = 1
        self.generate_obstacles()
        self.game_state = 'playing'

def main():
    game = Game()
    running = True
    
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game.game_state in ['menu', 'gameover']:
                        game.reset()
        
        keys = pygame.key.get_pressed()
        game.update(keys, events)
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()