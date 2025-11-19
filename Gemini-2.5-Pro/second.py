import pygame
import sys
import random

# --- Initialization ---
pygame.init()

# --- Screen & Game Constants ---
TILE_SIZE = 24  # Increased tile size for a clearer view of procedural assets
SCREEN_WIDTH = 30 * TILE_SIZE  # 720 pixels
SCREEN_HEIGHT = 20 * TILE_SIZE # 480 pixels
FPS = 60

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 200, 0) # A golden-yellow for the player
GRASS_COLOR_DARK = (34, 139, 34)
GRASS_COLOR_LIGHT = (50, 205, 50)
WALL_MORTAR_COLOR = (139, 69, 19)
WALL_BRICK_COLOR = (160, 82, 45)

# --- Game Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Procedural Top-Down RPG")
clock = pygame.time.Clock()

# --- Asset Generation Functions ---
# These functions create pygame.Surface objects to be used as assets.

def create_player_asset(size):
    """Creates the player's visual appearance."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    # The SRCALPHA flag makes the surface background transparent.
    pygame.draw.rect(surface, PLAYER_COLOR, (0, size // 4, size, size // 2))
    pygame.draw.rect(surface, (0,0,0), (size // 2 - 1, 0, 2, size)) # Simple cross shape
    return surface

def create_grass_asset(size):
    """Creates a textured grass tile."""
    surface = pygame.Surface((size, size))
    surface.fill(GRASS_COLOR_DARK)
    # Add a few lighter green pixels for texture
    for _ in range(15):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        pygame.draw.rect(surface, GRASS_COLOR_LIGHT, (x, y, 1, 1))
    return surface

def create_wall_asset(size):
    """Creates a brick wall tile."""
    surface = pygame.Surface((size, size))
    surface.fill(WALL_MORTAR_COLOR)
    brick_width = size // 2
    brick_height = size // 4
    for row in range(4):
        for col in range(2):
            x = col * brick_width
            y = row * brick_height
            # Add horizontal offset for alternate rows to create a classic brick pattern
            if row % 2 == 1:
                x += brick_width // 2
            
            # Draw the main part of the brick
            pygame.draw.rect(surface, WALL_BRICK_COLOR, (x, y, brick_width - 1, brick_height - 1))
            
            # Handle the wrapped-around part of the offset brick
            if row % 2 == 1 and col == 0:
                 pygame.draw.rect(surface, WALL_BRICK_COLOR, (x - size, y, brick_width - 1, brick_height - 1))
    return surface

# --- Procedural Asset Creation ---
player_img = create_player_asset(TILE_SIZE)
grass_img = create_grass_asset(TILE_SIZE)
wall_img = create_wall_asset(TILE_SIZE)


# --- Player Class ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed

        # Move each axis separately for better collision handling
        if dx != 0:
            self.move_and_collide(dx, 0, walls)
        if dy != 0:
            self.move_and_collide(0, dy, walls)

    def move_and_collide(self, dx, dy, walls):
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: self.rect.right = wall.rect.left
                if dx < 0: self.rect.left = wall.rect.right
                if dy > 0: self.rect.bottom = wall.rect.top
                if dy < 0: self.rect.top = wall.rect.bottom

# --- Tile Class ---
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Map Definition ---
# W = Wall, G = Grass
game_map = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WGGGGGGGGGGGGGGGGGGGGGGGWWWWGW",
    "WGGGGGGGGGGWWWWWWWGGGGGGGGGGGW",
    "WGGGGGGGGGGWGGGGGWGGGGWWWWGGGW",
    "WGGGGWWWWGGWGGGGGWGGGGWGGGGGGW",
    "WGGGGWGGWGGWGGGGGWGGGGWGGGGGGW",
    "WGGGGWGGWGGWWWWWWWWWWWWGGGGGGW",
    "WGGGGWGGWGGGGGGGGGGGGGGGGGGGGW",
    "WGGGGWWWWGGGGGGGGGGGGGGWWWWGGW",
    "WGGGGGGGGGGGGWGGGGGGGGGGWGGGGW",
    "WGGWWWWWWWWGGWGGGGGGGGGGWGGGGW",
    "WGGGGGGGGGGGGWGGGGGGGGGGWGGGGW",
    "WGGGGGGGGGGGGWWWWWWWWWWWWGGGGW",
    "WGGGGWGGGGGGGGGGGGGGGGGGGGGGGW",
    "WGGGGWGGGGGGGGGGGGGGGGGGGGGGGW",
    "WGGGGWWWWWWWWWWWWWWWWWWWWGGGGW",
    "WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW",
    "WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW",
    "WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# --- Sprite Groups ---
all_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
map_sprites = pygame.sprite.Group() # For drawing background tiles

# --- Create Game Objects from Map ---
for y, row in enumerate(game_map):
    for x, char in enumerate(row):
        pos_x, pos_y = x * TILE_SIZE, y * TILE_SIZE
        grass_tile = Tile(pos_x, pos_y, grass_img)
        map_sprites.add(grass_tile)
        if char == 'W':
            wall_tile = Tile(pos_x, pos_y, wall_img)
            all_sprites.add(wall_tile)
            wall_sprites.add(wall_tile)

# Create player and add to the main sprite group
player = Player(2 * TILE_SIZE, 2 * TILE_SIZE)
all_sprites.add(player)

# --- Main Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # --- Updates ---
    player.update(wall_sprites)

    # --- Drawing ---
    screen.fill(BLACK)
    map_sprites.draw(screen) # Draw the grass background
    all_sprites.draw(screen) # Draw walls and the player
    
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(FPS)

# --- Quit Game ---
pygame.quit()
sys.exit()
