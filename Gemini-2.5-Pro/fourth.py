import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 20
PLAYER_SIZE = 20
PLAYER_SPEED = 5

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
GRAY = (128, 128, 128)
DARK_GRAY = (100, 100, 100)
SKY_BLUE = (135, 206, 235)

# --- Block Types ---
GRASS = 1
DIRT = 2
STONE = 3

BLOCK_COLORS = {
    GRASS: (GREEN, DARK_GREEN),
    DIRT: (BROWN, DARK_BROWN),
    STONE: (GRAY, DARK_GRAY)
}

class Block:
    """Represents a single block in the world."""
    def __init__(self, block_type, x, y, z):
        self.block_type = block_type
        self.x = x
        self.y = y
        self.z = z

class Player:
    """Represents the player."""
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.y = 0 # Player's vertical position

    def move(self, dx, dz, world):
        """Moves the player and handles basic collision."""
        new_x = self.x + dx
        new_z = self.z + dz

        # Simple boundary check
        if 0 <= new_x < GRID_WIDTH and 0 <= new_z < GRID_HEIGHT:
            self.x = new_x
            self.z = new_z

class World:
    """Manages the grid of blocks."""
    def __init__(self):
        self.grid = [[[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] for _ in range(10)] # 10 layers of height
        self.generate_world()

    def generate_world(self):
        """Creates the initial landscape."""
        for x in range(GRID_WIDTH):
            for z in range(GRID_HEIGHT):
                # Base layer of stone
                self.grid[0][x][z] = Block(STONE, x, 0, z)
                # Next layer of dirt
                self.grid[1][x][z] = Block(DIRT, x, 1, z)
                # Top layer of grass
                self.grid[2][x][z] = Block(GRASS, x, 2, z)


    def draw_isometric(self, screen, player):
        """Draws the world in an isometric view, centered on the player."""
        # Sort blocks for proper rendering order (painter's algorithm)
        blocks_to_draw = []
        for y in range(len(self.grid)):
            for x in range(GRID_WIDTH):
                for z in range(GRID_HEIGHT):
                    if self.grid[y][x][z]:
                        blocks_to_draw.append(self.grid[y][x][z])
        
        blocks_to_draw.sort(key=lambda b: (b.y, b.x + b.z))

        for block in blocks_to_draw:
            iso_x = (block.x - block.z) * (TILE_SIZE / 2) + SCREEN_WIDTH / 2
            iso_y = (block.x + block.z) * (TILE_SIZE / 4) + SCREEN_HEIGHT / 2 - (block.y * TILE_SIZE / 2)
            self.draw_iso_cube(screen, iso_x, iso_y, BLOCK_COLORS[block.block_type])

    def draw_iso_cube(self, screen, x, y, colors):
        """Draws a single isometric cube."""
        main_color, dark_color = colors
        # Top face
        pygame.draw.polygon(screen, main_color, [
            (x, y),
            (x + TILE_SIZE / 2, y + TILE_SIZE / 4),
            (x, y + TILE_SIZE / 2),
            (x - TILE_SIZE / 2, y + TILE_SIZE / 4)
        ])
        # Left face
        pygame.draw.polygon(screen, dark_color, [
            (x - TILE_SIZE / 2, y + TILE_SIZE / 4),
            (x, y + TILE_SIZE / 2),
            (x, y + TILE_SIZE),
            (x - TILE_SIZE / 2, y + TILE_SIZE * 0.75)
        ])
        # Right face
        pygame.draw.polygon(screen, dark_color, [
            (x + TILE_SIZE / 2, y + TILE_SIZE / 4),
            (x, y + TILE_SIZE / 2),
            (x, y + TILE_SIZE),
            (x + TILE_SIZE / 2, y + TILE_SIZE * 0.75)
        ])

def main():
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PyGame Minecraft Clone")
    clock = pygame.time.Clock()

    world = World()
    player = Player(GRID_WIDTH // 2, GRID_HEIGHT // 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -1, world)
                if event.key == pygame.K_DOWN:
                    player.move(0, 1, world)
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0, world)
                if event.key == pygame.K_RIGHT:
                    player.move(1, 0, world)

        screen.fill(SKY_BLUE)
        world.draw_isometric(screen, player)
        
        # Draw Player
        player_iso_x = (player.x - player.z) * (TILE_SIZE / 2) + SCREEN_WIDTH / 2
        player_iso_y = (player.x + player.z) * (TILE_SIZE / 4) + SCREEN_HEIGHT / 2 - (player.y * TILE_SIZE / 2)
        pygame.draw.rect(screen, (255, 0, 0), (player_iso_x - PLAYER_SIZE / 2, player_iso_y - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE * 2))


        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
