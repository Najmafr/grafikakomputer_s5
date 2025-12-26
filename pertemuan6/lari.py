import pygame
import random
import math
import sys

pygame.init()

# --- WINDOW ---
WIDTH = 900
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Zombie Tsunami")
clock = pygame.time.Clock()

# --- COLORS ---
SKY_BLUE = (135, 206, 250)
GROUND = (101, 67, 33)
GRASS = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (147, 112, 219)
GRAY = (128, 128, 128)

# --- FONTS ---
font_large = pygame.font.Font(None, 60)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 28)

# --- PLAYER (DUCK) CLASS ---
class Duck:
    def __init__(self):
        self.x = 150
        self.y = HEIGHT - 180
        self.width = 50
        self.height = 50
        self.speed = 6
        self.dash_speed = 20
        self.dash_cooldown = 0
        self.dash_duration = 0
        self.is_dashing = False
        self.dash_direction = [0, 0]
        
        # Pull ability
        self.pull_cooldown = 0
        self.pull_range = 150
        self.pull_active = False
        self.pull_duration = 0
        
        self.health = 100
        self.max_health = 100
        self.invulnerable = 0
    
    def move(self, keys):
        if self.is_dashing:
            return
        
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
        
        self.x += dx
        self.y += dy
        
        # Keep in bounds
        self.x = max(50, min(self.x, WIDTH - self.width - 50))
        self.y = max(50, min(self.y, HEIGHT - self.height - 80))
    
    def dash(self, keys):
        if self.dash_cooldown == 0 and not self.is_dashing:
            dx = 0
            dy = 0
            
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 1
            
            if dx != 0 or dy != 0:
                # Normalize direction
                length = math.sqrt(dx*dx + dy*dy)
                self.dash_direction = [dx/length, dy/length]
                self.is_dashing = True
                self.dash_duration = 10
                self.dash_cooldown = 60
                self.invulnerable = 15
    
    def pull(self, zombies):
        if self.pull_cooldown == 0:
            self.pull_active = True
            self.pull_duration = 20
            self.pull_cooldown = 120
            
            # Pull nearby zombies
            for zombie in zombies:
                dist = math.sqrt((zombie.x - self.x)**2 + (zombie.y - self.y)**2)
                if dist < self.pull_range and dist > 0:
                    # Calculate pull direction
                    dx = self.x - zombie.x
                    dy = self.y - zombie.y
                    pull_force = 8
                    zombie.vx = (dx / dist) * pull_force
                    zombie.vy = (dy / dist) * pull_force
                    zombie.pulled = 10
    
    def update(self):
        # Dash movement
        if self.is_dashing:
            self.x += self.dash_direction[0] * self.dash_speed
            self.y += self.dash_direction[1] * self.dash_speed
            self.dash_duration -= 1
            if self.dash_duration <= 0:
                self.is_dashing = False
        
        # Update cooldowns
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.pull_cooldown > 0:
            self.pull_cooldown -= 1
        if self.pull_duration > 0:
            self.pull_duration -= 1
        else:
            self.pull_active = False
        if self.invulnerable > 0:
            self.invulnerable -= 1
        
        # Keep in bounds
        self.x = max(50, min(self.x, WIDTH - self.width - 50))
        self.y = max(50, min(self.y, HEIGHT - self.height - 80))
    
    def draw(self, surface):
        # Draw pull effect
        if self.pull_active:
            for i in range(3):
                radius = self.pull_range - i * 30
                alpha = 100 - i * 30
                s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (100, 100, 255, alpha), (radius, radius), radius, 3)
                surface.blit(s, (self.x + 25 - radius, self.y + 25 - radius))
        
        # Flash when invulnerable
        if self.invulnerable > 0 and self.invulnerable % 4 < 2:
            return
        
        # Dash trail
        if self.is_dashing:
            pygame.draw.circle(surface, (255, 255, 0, 100), 
                             (int(self.x + 25), int(self.y + 25)), 30)
        
        # Duck body (yellow)
        pygame.draw.ellipse(surface, YELLOW, (self.x + 10, self.y + 20, 35, 30))
        
        # Duck head
        pygame.draw.circle(surface, YELLOW, (int(self.x + 25), int(self.y + 15)), 15)
        
        # Duck bill (orange)
        bill_points = [
            (self.x + 35, self.y + 15),
            (self.x + 45, self.y + 13),
            (self.x + 45, self.y + 17)
        ]
        pygame.draw.polygon(surface, ORANGE, bill_points)
        
        # Eyes
        pygame.draw.circle(surface, BLACK, (int(self.x + 22), int(self.y + 12)), 3)
        pygame.draw.circle(surface, BLACK, (int(self.x + 28), int(self.y + 12)), 3)
        
        # Wings
        if not self.is_dashing:
            pygame.draw.ellipse(surface, ORANGE, (self.x + 5, self.y + 25, 15, 12))
            pygame.draw.ellipse(surface, ORANGE, (self.x + 35, self.y + 25, 15, 12))
        else:
            # Flapping wings during dash
            pygame.draw.ellipse(surface, ORANGE, (self.x, self.y + 20, 15, 12))
            pygame.draw.ellipse(surface, ORANGE, (self.x + 40, self.y + 20, 15, 12))
        
        # Feet
        pygame.draw.rect(surface, ORANGE, (self.x + 18, self.y + 48, 6, 4))
        pygame.draw.rect(surface, ORANGE, (self.x + 28, self.y + 48, 6, 4))

# --- ZOMBIE CLASS ---
class Zombie:
    def __init__(self, zombie_type, wave):
        self.type = zombie_type
        self.x = WIDTH + random.randint(0, 300)
        self.y = random.randint(100, HEIGHT - 150)
        self.width = 45
        self.height = 55
        self.vx = 0
        self.vy = 0
        self.pulled = 0
        
        # Different zombie types
        if zombie_type == "normal":
            self.speed = 2 + wave * 0.2
            self.health = 2
            self.color = GREEN
        elif zombie_type == "fast":
            self.speed = 3.5 + wave * 0.2
            self.health = 1
            self.color = YELLOW
        elif zombie_type == "tank":
            self.speed = 1 + wave * 0.1
            self.health = 4
            self.color = PURPLE
        
        self.max_health = self.health
    
    def update(self, player):
        if self.pulled > 0:
            # Being pulled
            self.x += self.vx
            self.y += self.vy
            self.vx *= 0.9
            self.vy *= 0.9
            self.pulled -= 1
        else:
            # Chase player
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist > 0:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
    
    def draw(self, surface):
        # Zombie body
        pygame.draw.rect(surface, self.color, (self.x + 10, self.y + 25, 25, 30))
        
        # Zombie head
        pygame.draw.circle(surface, self.color, (int(self.x + 22), int(self.y + 18)), 12)
        
        # Eyes (red evil eyes)
        pygame.draw.circle(surface, RED, (int(self.x + 18), int(self.y + 15)), 3)
        pygame.draw.circle(surface, RED, (int(self.x + 26), int(self.y + 15)), 3)
        
        # Mouth
        pygame.draw.arc(surface, BLACK, (self.x + 15, self.y + 18, 14, 8), 0, 3.14, 2)
        
        # Arms (reaching forward)
        pygame.draw.rect(surface, self.color, (self.x + 5, self.y + 28, 8, 15))
        pygame.draw.rect(surface, self.color, (self.x + 32, self.y + 28, 8, 15))
        
        # Legs
        pygame.draw.rect(surface, self.color, (self.x + 12, self.y + 50, 8, 12))
        pygame.draw.rect(surface, self.color, (self.x + 25, self.y + 50, 8, 12))
        
        # Health bar
        if self.health < self.max_health:
            bar_width = 40
            bar_height = 5
            health_ratio = self.health / self.max_health
            pygame.draw.rect(surface, RED, (self.x, self.y - 10, bar_width, bar_height))
            pygame.draw.rect(surface, GREEN, (self.x, self.y - 10, bar_width * health_ratio, bar_height))

# --- GAME CLASS ---
class Game:
    def __init__(self):
        self.duck = Duck()
        self.zombies = []
        self.wave = 1
        self.zombies_per_wave = 8
        self.zombies_spawned = 0
        self.spawn_timer = 0
        self.score = 0
        self.kills = 0
        self.game_over = False
        self.wave_complete = False
        self.wave_timer = 0
    
    def spawn_zombie(self):
        rand = random.random()
        if rand < 0.6:
            zombie_type = "normal"
        elif rand < 0.85:
            zombie_type = "fast"
        else:
            zombie_type = "tank"
        
        zombie = Zombie(zombie_type, self.wave)
        self.zombies.append(zombie)
        self.zombies_spawned += 1
    
    def update(self):
        if self.game_over:
            return
        
        # Spawn zombies
        if self.zombies_spawned < self.zombies_per_wave:
            self.spawn_timer += 1
            spawn_rate = max(25, 50 - self.wave * 3)
            if self.spawn_timer > spawn_rate:
                self.spawn_zombie()
                self.spawn_timer = 0
        
        # Update duck
        self.duck.update()
        
        # Update zombies
        for zombie in self.zombies[:]:
            zombie.update(self.duck)
            
            # Check if zombie is off screen (pulled away)
            if zombie.x < -100 or zombie.x > WIDTH + 100 or \
               zombie.y < -100 or zombie.y > HEIGHT + 100:
                self.zombies.remove(zombie)
                continue
            
            # Check collision with duck
            if not self.duck.invulnerable:
                duck_rect = pygame.Rect(self.duck.x, self.duck.y, self.duck.width, self.duck.height)
                zombie_rect = pygame.Rect(zombie.x, zombie.y, zombie.width, zombie.height)
                
                if duck_rect.colliderect(zombie_rect):
                    if self.duck.is_dashing:
                        # Kill zombie when dashing
                        zombie.health -= 2
                        if zombie.health <= 0:
                            self.zombies.remove(zombie)
                            self.score += 20
                            self.kills += 1
                    else:
                        # Take damage
                        self.duck.health -= 10
                        self.duck.invulnerable = 30
                        if self.duck.health <= 0:
                            self.game_over = True
        
        # Check wave complete
        if self.zombies_spawned >= self.zombies_per_wave and len(self.zombies) == 0:
            self.wave_complete = True
            self.wave_timer += 1
            if self.wave_timer > 120:
                self.next_wave()
    
    def next_wave(self):
        self.wave += 1
        self.zombies_per_wave += 4
        self.zombies_spawned = 0
        self.wave_complete = False
        self.wave_timer = 0
        # Heal duck
        self.duck.health = min(self.duck.health + 30, self.duck.max_health)
    
    def draw(self, surface):
        # Sky
        surface.fill(SKY_BLUE)
        
        # Ground
        pygame.draw.rect(surface, GRASS, (0, HEIGHT - 80, WIDTH, 30))
        pygame.draw.rect(surface, GROUND, (0, HEIGHT - 50, WIDTH, 50))
        
        # Draw zombies
        for zombie in self.zombies:
            zombie.draw(surface)
        
        # Draw duck
        self.duck.draw(surface)
        
        # UI Background
        ui_bg = pygame.Surface((WIDTH, 100))
        ui_bg.set_alpha(180)
        ui_bg.fill((0, 0, 0))
        surface.blit(ui_bg, (0, 0))
        
        # Health bar
        pygame.draw.rect(surface, RED, (10, 10, 200, 25))
        health_width = (self.duck.health / self.duck.max_health) * 200
        pygame.draw.rect(surface, GREEN, (10, 10, health_width, 25))
        pygame.draw.rect(surface, BLACK, (10, 10, 200, 25), 2)
        health_text = font_small.render(f"HP: {self.duck.health}", True, WHITE)
        surface.blit(health_text, (15, 13))
        
        # Dash cooldown
        dash_color = GREEN if self.duck.dash_cooldown == 0 else GRAY
        pygame.draw.rect(surface, dash_color, (10, 45, 90, 20))
        pygame.draw.rect(surface, BLACK, (10, 45, 90, 20), 2)
        if self.duck.dash_cooldown > 0:
            cooldown_ratio = 1 - (self.duck.dash_cooldown / 60)
            pygame.draw.rect(surface, GREEN, (10, 45, 90 * cooldown_ratio, 20))
        dash_text = font_small.render("DASH", True, WHITE)
        surface.blit(dash_text, (25, 47))
        
        # Pull cooldown
        pull_color = GREEN if self.duck.pull_cooldown == 0 else GRAY
        pygame.draw.rect(surface, pull_color, (110, 45, 90, 20))
        pygame.draw.rect(surface, BLACK, (110, 45, 90, 20), 2)
        if self.duck.pull_cooldown > 0:
            cooldown_ratio = 1 - (self.duck.pull_cooldown / 120)
            pygame.draw.rect(surface, GREEN, (110, 45, 90 * cooldown_ratio, 20))
        pull_text = font_small.render("PULL", True, WHITE)
        surface.blit(pull_text, (127, 47))
        
        # Wave and score
        wave_text = font_small.render(f"Wave: {self.wave}", True, WHITE)
        surface.blit(wave_text, (WIDTH - 180, 10))
        
        score_text = font_small.render(f"Score: {self.score}", True, YELLOW)
        surface.blit(score_text, (WIDTH - 180, 35))
        
        kills_text = font_small.render(f"Kills: {self.kills}", True, WHITE)
        surface.blit(kills_text, (WIDTH - 180, 60))
        
        # Controls hint
        controls = font_small.render("WASD: Move | SHIFT: Dash | SPACE: Pull", True, WHITE)
        surface.blit(controls, (WIDTH//2 - 200, 75))
        
        # Wave complete
        if self.wave_complete:
            overlay = pygame.Surface((WIDTH, 150))
            overlay.set_alpha(200)
            overlay.fill((0, 100, 0))
            surface.blit(overlay, (0, HEIGHT//2 - 75))
            
            complete_text = font_large.render(f"WAVE {self.wave} COMPLETE!", True, WHITE)
            surface.blit(complete_text, (WIDTH//2 - complete_text.get_width()//2, HEIGHT//2 - 40))
            next_text = font_medium.render(f"Next wave incoming...", True, YELLOW)
            surface.blit(next_text, (WIDTH//2 - next_text.get_width()//2, HEIGHT//2 + 20))
        
        # Game Over
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            
            game_over_text = font_large.render("GAME OVER", True, RED)
            surface.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 200))
            
            final_score = font_medium.render(f"Final Score: {self.score}", True, WHITE)
            surface.blit(final_score, (WIDTH//2 - final_score.get_width()//2, 280))
            
            kills_final = font_medium.render(f"Zombies Killed: {self.kills}", True, WHITE)
            surface.blit(kills_final, (WIDTH//2 - kills_final.get_width()//2, 330))
            
            wave_reached = font_medium.render(f"Wave Reached: {self.wave}", True, WHITE)
            surface.blit(wave_reached, (WIDTH//2 - wave_reached.get_width()//2, 380))
            
            restart_text = font_small.render("Press R to Restart", True, WHITE)
            surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 450))

# --- GAME INIT ---
game = Game()

# --- MAIN LOOP ---
run = True
while run:
    clock.tick(60)
    
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game.game_over:
                game = Game()
            
            if not game.game_over:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    game.duck.dash(keys)
                
                if event.key == pygame.K_SPACE:
                    game.duck.pull(game.zombies)
    
    # Move duck
    if not game.game_over:
        game.duck.move(keys)
    
    # Update game
    game.update()
    
    # Draw
    game.draw(win)
    
    pygame.display.update()

pygame.quit()
sys.exit()