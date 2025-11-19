import pygame
import random
import sys

# --- CONSTANTS & SETTINGS ---
TILE_SIZE = 32
WIDTH, HEIGHT = 800, 640  # Screen size
FPS = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
DARK_GRAY = (40, 40, 40)
FLOOR_COLOR = (30, 30, 30)

# Simple Map Layout (P=Player, E=Enemy, #=Wall, .=Floor)
# You can edit this list to change the level design
GAME_MAP = [
    "#########################",
    "#.......................#",
    "#..P....................#",
    "#.......#####...........#",
    "#.......#...............#",
    "#.......#......E........#",
    "#.......#...............#",
    "#...E...#####...........#",
    "#.......................#",
    "#..............#####....#",
    "#..............#...#....#",
    "#...E..........#...#....#",
    "#..............#...#....#",
    "#..............#####....#",
    "#.......................#",
    "#...E...................#",
    "#.........E.............#",
    "#.......................#",
    "#########################",
]

# --- ASSET GENERATION (Making pixel art via code) ---
def create_block_surface(color, width, height):
    """Creates a surface with a colored border to look like a tile."""
    surf = pygame.Surface((width, height))
    surf.fill(color)
    # Draw a lighter border to give it a "pixel art" block look
    pygame.draw.rect(surf, [c + 40 if c < 215 else 255 for c in color], (0, 0, width, height), 2)
    return surf

# --- CLASSES ---

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)
        self.image = create_block_surface(DARK_GRAY, TILE_SIZE, TILE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacles_group, enemies_group, groups):
        super().__init__(groups)
        self.image = create_block_surface(GREEN, TILE_SIZE, TILE_SIZE)
        # Add eyes to make it look like a character
        pygame.draw.rect(self.image, BLACK, (8, 8, 4, 4))
        pygame.draw.rect(self.image, BLACK, (20, 8, 4, 4))
        
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
        self.obstacles = obstacles_group
        self.enemies = enemies_group
        
        self.speed = 4
        self.health = 100
        self.max_health = 100
        self.attack_cooldown = 0

    def input(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            
        # Attack mechanic
        if keys[pygame.K_SPACE] and self.attack_cooldown == 0:
            self.attack()

        if dx != 0 or dy != 0:
            self.move(dx, dy)

    def move(self, dx, dy):
        # Move on X axis and check collision
        self.rect.x += dx
        self.collision('x')
        # Move on Y axis and check collision
        self.rect.y += dy
        self.collision('y')

    def collision(self, direction):
        hits = pygame.sprite.spritecollide(self, self.obstacles, False)
        if hits:
            if direction == 'x':
                if self.rect.centerx < hits[0].rect.centerx: # Moving Right
                    self.rect.right = hits[0].rect.left
                else: # Moving Left
                    self.rect.left = hits[0].rect.right
            if direction == 'y':
                if self.rect.centery < hits[0].rect.centery: # Moving Down
                    self.rect.bottom = hits[0].rect.top
                else: # Moving Up
                    self.rect.top = hits[0].rect.bottom

    def attack(self):
        self.attack_cooldown = 30 # Frames until next attack
        # Simple area attack
        center = self.rect.center
        # Create a temporary hit box around player
        attack_rect = pygame.Rect(0, 0, TILE_SIZE * 2, TILE_SIZE * 2)
        attack_rect.center = center
        
        # Check if any enemy is in this box
        for enemy in self.enemies:
            if attack_rect.colliderect(enemy.rect):
                enemy.take_damage(50)
                print("Enemy Hit!")

    def update(self):
        self.input()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
    def draw_ui(self, screen):
        # Health Bar
        bar_width = 200
        bar_height = 20
        fill = (self.health / self.max_health) * bar_width
        border_rect = pygame.Rect(10, 10, bar_width, bar_height)
        fill_rect = pygame.Rect(10, 10, fill, bar_height)
        
        pygame.draw.rect(screen, RED, fill_rect)
        pygame.draw.rect(screen, WHITE, border_rect, 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, obstacles, groups):
        super().__init__(groups)
        self.image = create_block_surface(RED, TILE_SIZE, TILE_SIZE)
        # Angry eyes
        pygame.draw.polygon(self.image, BLACK, [(5, 5), (15, 10), (5, 15)])
        
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
        self.player = player
        self.obstacles = obstacles
        self.speed = 2
        self.health = 100

    def move_towards_player(self):
        # Simple AI: Move directly toward player
        dx, dy = 0, 0
        if self.rect.x < self.player.rect.x:
            dx = self.speed
        elif self.rect.x > self.player.rect.x:
            dx = -self.speed
        
        if self.rect.y < self.player.rect.y:
            dy = self.speed
        elif self.rect.y > self.player.rect.y:
            dy = -self.speed

        self.rect.x += dx
        self.collide('x')
        self.rect.y += dy
        self.collide('y')

    def collide(self, direction):
        # Wall collision for enemies
        hits = pygame.sprite.spritecollide(self, self.obstacles, False)
        if hits:
            if direction == 'x':
                if self.rect.centerx < hits[0].rect.centerx:
                    self.rect.right = hits[0].rect.left
                else:
                    self.rect.left = hits[0].rect.right
            if direction == 'y':
                if self.rect.centery < hits[0].rect.centery:
                    self.rect.bottom = hits[0].rect.top
                else:
                    self.rect.top = hits[0].rect.bottom

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill() # Remove from all groups

    def update(self):
        dist = ((self.rect.x - self.player.rect.x)**2 + (self.rect.y - self.player.rect.y)**2)**0.5
        if dist < 300: # Only chase if within range
            self.move_towards_player()
            
        # Damage Player on touch
        if self.rect.colliderect(self.player.rect):
            # In a real game, you'd add invincibility frames here
            self.player.health -= 1
            if self.player.health <= 0:
                print("GAME OVER")
                pygame.quit()
                sys.exit()

# --- CAMERA SYSTEM ---
class CameraGroup(pygame.sprite.Group):
    """Custom Sprite Group that acts as a Camera (follows player)."""
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player):
        self.center_target_camera(player)

        # Draw floor
        # (In a real game, you would blit a large background image here)
        # For now, we just fill screen with dark color, tiles handle themselves
        self.display_surface.fill(FLOOR_COLOR)

        # Sort sprites by Y coordinate so sprites lower down overlap ones higher up (depth)
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

# --- MAIN GAME SETUP ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Top-Down RPG")
    clock = pygame.time.Clock()

    # Groups
    camera_group = CameraGroup()
    obstacles_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()

    # Map Generation
    player = None
    for row_index, row in enumerate(GAME_MAP):
        for col_index, col in enumerate(row):
            x = col_index
            y = row_index
            if col == '#':
                Wall(x, y, [camera_group, obstacles_group])
            elif col == 'P':
                player = Player(x, y, obstacles_group, enemies_group, [camera_group])
            elif col == 'E':
                Enemy(x, y, player, obstacles_group, [camera_group, enemies_group])

    # Pass player reference to enemies after creation (if any existed before player)
    for enemy in enemies_group:
        enemy.player = player

    # --- GAME LOOP ---
    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 2. Update
        camera_group.update()

        # 3. Draw
        camera_group.custom_draw(player)
        
        # Draw HUD (Health bar) separate from camera offset
        player.draw_ui(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
