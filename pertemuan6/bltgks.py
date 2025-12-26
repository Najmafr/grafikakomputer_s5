import pygame
import random
import math
import sys

pygame.init()

# --- WINDOW ---
WIDTH = 900
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Badminton Game vs AI")
clock = pygame.time.Clock()

# --- COLORS ---
SKY_BLUE = (135, 206, 250)
COURT_GREEN = (34, 139, 34)
COURT_DARK = (0, 100, 0)
LINE_WHITE = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
BROWN = (139, 90, 43)
GRAY = (128, 128, 128)

# --- FONTS ---
font_large = pygame.font.Font(None, 80)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 35)

# --- PLAYER CLASS ---
class Player:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.speed = 6
        self.color = color
        self.controls = controls
        self.can_hit = True
        self.hit_cooldown = 0
        self.is_swinging = False
        self.swing_timer = 0
        
    def move(self, keys, bounds):
        dx = 0
        dy = 0
        
        if keys[self.controls['up']]:
            dy -= self.speed
        if keys[self.controls['down']]:
            dy += self.speed
        if keys[self.controls['left']]:
            dx -= self.speed
        if keys[self.controls['right']]:
            dx += self.speed
        
        self.x += dx
        self.y += dy
        
        # Keep in bounds
        self.x = max(bounds[0], min(self.x, bounds[1]))
        self.y = max(100, min(self.y, HEIGHT - 100))
    
    def hit(self, shuttlecock):
        if self.can_hit and not self.is_swinging:
            # Check if near shuttlecock
            dist = math.sqrt((self.x - shuttlecock.x)**2 + (self.y - shuttlecock.y)**2)
            if dist < 60:
                self.is_swinging = True
                self.swing_timer = 10
                self.can_hit = False
                self.hit_cooldown = 20
                return True
        return False
    
    def update(self):
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
        else:
            self.can_hit = True
        
        if self.swing_timer > 0:
            self.swing_timer -= 1
        else:
            self.is_swinging = False
    
    def draw(self, surface):
        # Body
        pygame.draw.rect(surface, self.color, (self.x - 15, self.y - 20, 30, 40), border_radius=5)
        
        # Head
        pygame.draw.circle(surface, (255, 220, 177), (int(self.x), int(self.y - 35)), 12)
        
        # Arms
        pygame.draw.line(surface, self.color, (self.x - 15, self.y - 10), (self.x - 25, self.y + 5), 5)
        pygame.draw.line(surface, self.color, (self.x + 15, self.y - 10), (self.x + 25, self.y + 5), 5)
        
        # Legs
        pygame.draw.line(surface, self.color, (self.x - 8, self.y + 20), (self.x - 12, self.y + 45), 5)
        pygame.draw.line(surface, self.color, (self.x + 8, self.y + 20), (self.x + 12, self.y + 45), 5)
        
        # Racket
        if self.is_swinging:
            # Swinging animation
            angle = self.swing_timer * 10
            racket_x = self.x + 30 * math.cos(math.radians(angle))
            racket_y = self.y - 20 + 30 * math.sin(math.radians(angle))
        else:
            racket_x = self.x + 30
            racket_y = self.y - 20
        
        # Racket handle
        pygame.draw.line(surface, BROWN, (self.x + 20, self.y), (racket_x, racket_y), 4)
        
        # Racket head
        pygame.draw.circle(surface, GRAY, (int(racket_x), int(racket_y)), 15, 3)
        # Strings
        pygame.draw.line(surface, WHITE, (racket_x - 10, racket_y), (racket_x + 10, racket_y), 1)
        pygame.draw.line(surface, WHITE, (racket_x, racket_y - 10), (racket_x, racket_y + 10), 1)

# --- AI PLAYER CLASS ---
class AIPlayer(Player):
    def __init__(self, x, y, color, difficulty='medium'):
        # Dummy controls for AI
        super().__init__(x, y, color, {
            'up': None,
            'down': None,
            'left': None,
            'right': None,
            'hit': None
        })
        self.difficulty = difficulty
        self.reaction_delay = 0
        self.target_x = x
        self.target_y = y
        
        # Set AI parameters based on difficulty
        if difficulty == 'easy':
            self.speed = 4
            self.reaction_time = 15
            self.accuracy = 0.6
        elif difficulty == 'hard':
            self.speed = 7
            self.reaction_time = 3
            self.accuracy = 0.95
        else:  # medium
            self.speed = 5.5
            self.reaction_time = 8
            self.accuracy = 0.8
    
    def ai_move(self, shuttlecock, bounds):
        # React to shuttlecock if it's coming towards AI's side
        if shuttlecock.in_play and shuttlecock.x > WIDTH // 2:
            # Predict where shuttlecock will land
            if shuttlecock.vx != 0:
                # Calculate intercept point
                time_to_reach = abs((shuttlecock.y - (HEIGHT - 150)) / shuttlecock.vy) if shuttlecock.vy > 0 else 0
                predicted_x = shuttlecock.x + shuttlecock.vx * time_to_reach
                predicted_y = shuttlecock.y
                
                # Add some inaccuracy based on difficulty
                predicted_x += random.randint(-int(50 * (1 - self.accuracy)), int(50 * (1 - self.accuracy)))
                
                self.target_x = predicted_x
                self.target_y = shuttlecock.y
            else:
                self.target_x = shuttlecock.x
                self.target_y = shuttlecock.y
        else:
            # Return to center position
            self.target_x = 700
            self.target_y = HEIGHT - 250
        
        # Move towards target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 5:
            # Normalize and apply speed
            dx = (dx / dist) * self.speed
            dy = (dy / dist) * self.speed
            
            self.x += dx
            self.y += dy
            
            # Keep in bounds
            self.x = max(bounds[0], min(self.x, bounds[1]))
            self.y = max(100, min(self.y, HEIGHT - 100))
    
    def ai_hit(self, shuttlecock):
        # Check if should hit
        if shuttlecock.in_play and shuttlecock.x > WIDTH // 2:
            dist = math.sqrt((self.x - shuttlecock.x)**2 + (self.y - shuttlecock.y)**2)
            
            # React with delay based on difficulty
            if self.reaction_delay > 0:
                self.reaction_delay -= 1
            elif dist < 70 and self.can_hit:
                if self.hit(shuttlecock):
                    # Aim towards player 1 side with AI accuracy
                    target_x = random.randint(100, 350)
                    # Add accuracy variation
                    if random.random() > self.accuracy:
                        # Occasionally hit less accurate shots
                        target_x = random.randint(50, 450)
                    power = random.uniform(0.9, 1.3)
                    shuttlecock.hit(self, target_x, power)
                    self.reaction_delay = self.reaction_time

# --- SHUTTLECOCK CLASS ---
class Shuttlecock:
    def __init__(self):
        self.reset()
        
    def reset(self, serve_left=True):
        if serve_left:
            self.x = 250
        else:
            self.x = 650
        self.y = HEIGHT - 150
        self.vx = 0
        self.vy = 0
        self.gravity = 0.3
        self.in_play = False
        self.last_hit_by = None
    
    def hit(self, player, target_x, power=1.0):
        # Calculate direction to target
        dx = target_x - self.x
        dy = -200  # Arc height
        
        # Apply power
        self.vx = dx * 0.03 * power
        self.vy = dy * 0.03 * power
        self.in_play = True
        self.last_hit_by = player
    
    def update(self):
        if self.in_play:
            # Apply gravity
            self.vy += self.gravity
            
            # Update position
            self.x += self.vx
            self.y += self.vy
            
            # Air resistance
            self.vx *= 0.99
            
            # Check if hit ground
            if self.y >= HEIGHT - 100:
                self.y = HEIGHT - 100
                self.in_play = False
                return True  # Return True when hits ground
        
        return False
    
    def draw(self, surface):
        # Shuttlecock body (cone)
        points = [
            (self.x, self.y - 15),
            (self.x - 8, self.y + 5),
            (self.x + 8, self.y + 5)
        ]
        pygame.draw.polygon(surface, WHITE, points)
        
        # Cork (top part)
        pygame.draw.circle(surface, (255, 200, 150), (int(self.x), int(self.y - 15)), 5)
        
        # Feathers lines
        pygame.draw.line(surface, WHITE, (self.x - 6, self.y), (self.x - 8, self.y + 5), 1)
        pygame.draw.line(surface, WHITE, (self.x + 6, self.y), (self.x + 8, self.y + 5), 1)

# --- GAME CLASS ---
class Game:
    def __init__(self, difficulty='medium'):
        self.player1 = Player(200, HEIGHT - 200, RED, {
            'up': pygame.K_w,
            'down': pygame.K_s,
            'left': pygame.K_a,
            'right': pygame.K_d,
            'hit': pygame.K_SPACE
        })
        
        # AI Player
        self.player2 = AIPlayer(700, HEIGHT - 200, BLUE, difficulty)
        
        self.shuttlecock = Shuttlecock()
        self.score1 = 0
        self.score2 = 0
        self.serving_player = 1
        self.game_state = "SERVE"  # SERVE, PLAY, SCORE, GAME_OVER
        self.score_timer = 0
        self.winner = None
        self.max_score = 21
        self.difficulty = difficulty
    
    def serve(self):
        if self.serving_player == 1:
            self.shuttlecock.reset(serve_left=True)
            self.shuttlecock.hit(self.player1, 700, 1.2)
        else:
            self.shuttlecock.reset(serve_left=False)
            self.shuttlecock.hit(self.player2, 200, 1.2)
        self.game_state = "PLAY"
    
    def update(self, keys):
        if self.game_state == "SERVE":
            # Wait for space to serve
            if keys[pygame.K_SPACE]:
                self.serve()
        
        elif self.game_state == "PLAY":
            # Update player 1
            self.player1.move(keys, (50, WIDTH // 2 - 20))
            self.player1.update()
            
            # Update AI player 2
            self.player2.ai_move(self.shuttlecock, (WIDTH // 2 + 20, WIDTH - 50))
            self.player2.update()
            self.player2.ai_hit(self.shuttlecock)
            
            # Check player 1 hit
            if keys[self.player1.controls['hit']]:
                if self.player1.hit(self.shuttlecock):
                    # Aim towards player 2 side with some randomness
                    target_x = random.randint(550, 800)
                    power = random.uniform(0.9, 1.3)
                    self.shuttlecock.hit(self.player1, target_x, power)
            
            # Update shuttlecock
            if self.shuttlecock.update():
                # Shuttlecock hit ground
                self.check_score()
        
        elif self.game_state == "SCORE":
            self.score_timer += 1
            if self.score_timer > 120:
                if self.score1 >= self.max_score or self.score2 >= self.max_score:
                    self.game_state = "GAME_OVER"
                    self.winner = 1 if self.score1 >= self.max_score else 2
                else:
                    self.game_state = "SERVE"
                    self.score_timer = 0
    
    def check_score(self):
        # Check which side the shuttlecock landed
        if self.shuttlecock.x < WIDTH // 2:
            # Landed on player 1 side
            if self.shuttlecock.last_hit_by == self.player1:
                # Player 1 hit it out
                self.score2 += 1
                self.serving_player = 2
            else:
                # Player 2 scored
                self.score2 += 1
                self.serving_player = 2
        else:
            # Landed on player 2 side
            if self.shuttlecock.last_hit_by == self.player2:
                # Player 2 hit it out
                self.score1 += 1
                self.serving_player = 1
            else:
                # Player 1 scored
                self.score1 += 1
                self.serving_player = 1
        
        self.game_state = "SCORE"
    
    def draw_court(self, surface):
        # Sky
        surface.fill(SKY_BLUE)
        
        # Court
        pygame.draw.rect(surface, COURT_GREEN, (50, 100, WIDTH - 100, HEIGHT - 200))
        
        # Court lines
        # Outer boundary
        pygame.draw.rect(surface, LINE_WHITE, (50, 100, WIDTH - 100, HEIGHT - 200), 3)
        
        # Center line
        pygame.draw.line(surface, LINE_WHITE, (WIDTH // 2, 100), (WIDTH // 2, HEIGHT - 100), 3)
        
        # Service lines
        pygame.draw.line(surface, LINE_WHITE, (50, HEIGHT // 2), (WIDTH - 50, HEIGHT // 2), 2)
        
        # Net
        net_height = 120
        pygame.draw.rect(surface, BLACK, (WIDTH // 2 - 3, HEIGHT - 100 - net_height, 6, net_height))
        
        # Net mesh
        for i in range(0, net_height, 10):
            y = HEIGHT - 100 - i
            pygame.draw.line(surface, WHITE, (WIDTH // 2 - 20, y), (WIDTH // 2 + 20, y), 1)
        
        # Net top
        pygame.draw.rect(surface, WHITE, (WIDTH // 2 - 25, HEIGHT - 100 - net_height - 5, 50, 8))
    
    def draw_ui(self, surface):
        # Score board background
        pygame.draw.rect(surface, (0, 0, 0, 180), (WIDTH // 2 - 150, 20, 300, 70))
        
        # Player 1 score (left)
        score1_text = font_large.render(str(self.score1), True, RED)
        surface.blit(score1_text, (WIDTH // 2 - 100, 35))
        
        # Separator
        separator = font_medium.render("-", True, WHITE)
        surface.blit(separator, (WIDTH // 2 - 15, 40))
        
        # Player 2 score (right)
        score2_text = font_large.render(str(self.score2), True, BLUE)
        surface.blit(score2_text, (WIDTH // 2 + 60, 35))
        
        # Controls
        controls1 = font_small.render("YOU: WASD + SPACE", True, RED)
        surface.blit(controls1, (20, 20))
        
        ai_text = font_small.render(f"AI: {self.difficulty.upper()}", True, BLUE)
        surface.blit(ai_text, (WIDTH - 200, 20))
        
        # Serve indicator
        if self.game_state == "SERVE":
            serve_text = font_medium.render(f"Player {self.serving_player} Serve", True, YELLOW)
            surface.blit(serve_text, (WIDTH // 2 - serve_text.get_width() // 2, HEIGHT - 60))
            
            if self.serving_player == 1:
                prompt = font_small.render("Press SPACE to serve", True, WHITE)
                surface.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT - 30))
    
    def draw(self, surface):
        # Draw court
        self.draw_court(surface)
        
        # Draw players
        self.player1.draw(surface)
        self.player2.draw(surface)
        
        # Draw shuttlecock
        self.shuttlecock.draw(surface)
        
        # Draw UI
        self.draw_ui(surface)
        
        # Score message
        if self.game_state == "SCORE":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            
            point_text = font_large.render("POINT!", True, YELLOW)
            surface.blit(point_text, (WIDTH // 2 - point_text.get_width() // 2, HEIGHT // 2 - 50))
            
            score_text = font_medium.render(f"{self.score1} - {self.score2}", True, WHITE)
            surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))
        
        # Game Over
        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            
            if self.winner == 1:
                winner_text = font_large.render("YOU WIN!", True, RED)
            else:
                winner_text = font_large.render("AI WINS!", True, BLUE)
            surface.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 80))
            
            final_score = font_medium.render(f"Final Score: {self.score1} - {self.score2}", True, WHITE)
            surface.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 - 10))
            
            restart_text = font_small.render("Press R to Restart | 1=Easy 2=Medium 3=Hard", True, WHITE)
            surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

# --- GAME INIT ---
game = Game('medium')

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
            if event.key == pygame.K_r:
                if game.game_state == "GAME_OVER":
                    game = Game(game.difficulty)
            # Change difficulty
            elif event.key == pygame.K_1:
                game = Game('easy')
            elif event.key == pygame.K_2:
                game = Game('medium')
            elif event.key == pygame.K_3:
                game = Game('hard')
    
    # Update game
    game.update(keys)
    
    # Draw
    game.draw(win)
    
    pygame.display.update()

pygame.quit()
sys.exit()