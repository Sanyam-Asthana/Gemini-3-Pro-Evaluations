import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# --- Constants ---
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FOV = 70    # Field of View
NEAR_CLIP = 0.1
FAR_CLIP = 50.0
LOOK_SPEED = 0.15
MOVE_SPEED = 0.3

# Colors for procedural generation
GRASS_COLOR = (34, 139, 34)
DIRT_COLOR = (139, 69, 19)
STONE_COLOR = (105, 105, 105)

class TextureManager:
    """Generates textures programmatically so no external files are needed."""
    def __init__(self):
        self.textures = {}

    def generate_texture(self, name, color, variation=20):
        # Create a surface
        surf = pygame.Surface((64, 64))
        surf.fill(color)
        
        # Add noise (grain)
        for x in range(64):
            for y in range(64):
                r = random.randint(-variation, variation)
                new_color = (
                    max(0, min(255, color[0] + r)),
                    max(0, min(255, color[1] + r)),
                    max(0, min(255, color[2] + r))
                )
                surf.set_at((x, y), new_color)
                
        # Convert to OpenGL texture
        texture_data = pygame.image.tostring(surf, "RGBA", 1)
        width = surf.get_width()
        height = surf.get_height()

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        
        # Texture filtering (Nearest for that pixelated Minecraft look)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        self.textures[name] = tex_id

# --- Cube Geometry ---
# Vertices of a 1x1x1 cube centered at local 0,0,0
VERTICES = [
    ( 0.5, -0.5, -0.5), ( 0.5,  0.5, -0.5), (-0.5,  0.5, -0.5), (-0.5, -0.5, -0.5), # Back
    ( 0.5, -0.5,  0.5), ( 0.5,  0.5,  0.5), (-0.5,  0.5,  0.5), (-0.5, -0.5,  0.5), # Front
]

# Indices defining the 6 faces (quads)
FACES = [
    (0,1,2,3), # Back
    (4,7,6,5), # Front
    (0,4,5,1), # Right
    (1,5,6,2), # Top
    (2,6,7,3), # Left
    (4,0,3,7)  # Bottom
]

# Texture Coordinates for mapping the image to the face
TEX_COORDS = [
    (0, 0), (1, 0), (1, 1), (0, 1)
]

class World:
    def __init__(self):
        self.blocks = {} # Dictionary: (x,y,z) -> texture_id
        self.generate_flat_world()

    def generate_flat_world(self):
        # Generate a simple 10x10 floor
        for x in range(-5, 5):
            for z in range(-5, 5):
                self.add_block((x, -2, z), 'grass')

    def add_block(self, pos, type_name):
        self.blocks[pos] = type_name

    def remove_block(self, pos):
        if pos in self.blocks:
            del self.blocks[pos]

    def draw(self, texture_mgr):
        glEnable(GL_TEXTURE_2D)
        
        # Start drawing Quads
        glBegin(GL_QUADS)
        
        for pos, type_name in self.blocks.items():
            x, y, z = pos
            tex_id = texture_mgr.textures.get(type_name)
            
            # Note: In a real engine, you'd batch these or sort by texture.
            # Here we are keeping it simple, which is inefficient but readable.
            
            # We have to unbind/bind inside loop because we are in immediate mode block
            # Actually, 'glEnd' and 'glBegin' inside a loop is bad practice, 
            # but we need to change texture state.
            glEnd() 
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glBegin(GL_QUADS)

            for face in FACES:
                for i, vertex_index in enumerate(face):
                    vx, vy, vz = VERTICES[vertex_index]
                    glTexCoord2f(*TEX_COORDS[i])
                    glVertex3f(vx + x, vy + y, vz + z)
        glEnd()
        glDisable(GL_TEXTURE_2D)

class Player:
    def __init__(self):
        self.pos = [0, 0, 0]   # x, y, z
        self.rot = [0, 0]      # yaw (azimuth), pitch (elevation)
    
    def update(self, dt, keys):
        # Mouse Look
        dx, dy = pygame.mouse.get_rel()
        self.rot[0] += dx * LOOK_SPEED
        self.rot[1] += dy * LOOK_SPEED
        
        # Clamp pitch (look up/down limits)
        self.rot[1] = max(-90, min(90, self.rot[1]))

        # Calculate movement vectors based on Yaw
        # Convert to radians
        yaw_rad = math.radians(self.rot[0])
        
        # Forward vector
        fx = math.sin(yaw_rad)
        fz = -math.cos(yaw_rad)
        
        # Right vector
        rx = math.cos(yaw_rad)
        rz = math.sin(yaw_rad)

        # Movement Logic
        if keys[K_w]:
            self.pos[0] += fx * MOVE_SPEED
            self.pos[2] += fz * MOVE_SPEED
        if keys[K_s]:
            self.pos[0] -= fx * MOVE_SPEED
            self.pos[2] -= fz * MOVE_SPEED
        if keys[K_a]:
            self.pos[0] -= rx * MOVE_SPEED
            self.pos[2] -= rz * MOVE_SPEED
        if keys[K_d]:
            self.pos[0] += rx * MOVE_SPEED
            self.pos[2] += rz * MOVE_SPEED
        
        # Fly Up/Down
        if keys[K_SPACE]:
            self.pos[1] += MOVE_SPEED
        if keys[K_LSHIFT]:
            self.pos[1] -= MOVE_SPEED

    def get_sight_vector(self):
        """ Returns the 3D vector the player is looking at """
        yaw_rad = math.radians(self.rot[0])
        pitch_rad = math.radians(self.rot[1])
        
        x = math.sin(yaw_rad) * math.cos(pitch_rad)
        y = -math.sin(pitch_rad)
        z = -math.cos(yaw_rad) * math.cos(pitch_rad)
        return (x, y, z)

def raycast(player, world, distance=5):
    """ Simple DDA algorithm to find looking-at block and previous block (for placement) """
    x, y, z = player.pos
    dx, dy, dz = player.get_sight_vector()
    
    step_x = 1 if dx > 0 else -1
    step_y = 1 if dy > 0 else -1
    step_z = 1 if dz > 0 else -1
    
    # Current voxel coordinates
    vx, vy, vz = int(round(x)), int(round(y)), int(round(z))
    
    # Steps to reach next voxel boundary
    # Avoid division by zero
    delta_x = abs(1/dx) if dx != 0 else 1e30
    delta_y = abs(1/dy) if dy != 0 else 1e30
    delta_z = abs(1/dz) if dz != 0 else 1e30
    
    # Initial distances
    dist_x = (vx + (1 if dx > 0 else 0) - x) * step_x * delta_x
    dist_y = (vy + (1 if dy > 0 else 0) - y) * step_y * delta_y
    dist_z = (vz + (1 if dz > 0 else 0) - z) * step_z * delta_z
    
    # Last open block (for placing)
    last_voxel = (vx, vy, vz)

    # Walk along ray
    for _ in range(int(distance * 3)): # rough iteration count
        if (vx, vy, vz) in world.blocks:
            return (vx, vy, vz), last_voxel
        
        last_voxel = (vx, vy, vz)
        
        if dist_x < dist_y:
            if dist_x < dist_z:
                dist_x += delta_x
                vx += step_x
            else:
                dist_z += delta_z
                vz += step_z
        else:
            if dist_y < dist_z:
                dist_y += delta_y
                vy += step_y
            else:
                dist_z += delta_z
                vz += step_z
                
    return None, None

def draw_crosshair():
    """ Draws a simple 2D crosshair in the center of the screen """
    # Switch to 2D Orthographic projection
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, DISPLAY_WIDTH, 0, DISPLAY_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)

    glColor3f(1, 1, 1)
    cx, cy = DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2
    size = 10
    
    glBegin(GL_LINES)
    glVertex2f(cx - size, cy)
    glVertex2f(cx + size, cy)
    glVertex2f(cx, cy - size)
    glVertex2f(cx, cy + size)
    glEnd()

    # Restore 3D perspective
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def main():
    pygame.init()
    pygame.display.set_caption("PyGame Minecraft Clone")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), DOUBLEBUF | OPENGL)
    
    # OpenGL Init
    glEnable(GL_DEPTH_TEST) # Enable depth buffering (z-buffer)
    glEnable(GL_CULL_FACE)  # Don't draw back faces
    
    # Projection
    glMatrixMode(GL_PROJECTION)
    gluPerspective(FOV, (DISPLAY_WIDTH / DISPLAY_HEIGHT), NEAR_CLIP, FAR_CLIP)
    
    # Initialize Systems
    tex_mgr = TextureManager()
    # Generate textures
    tex_mgr.generate_texture('grass', GRASS_COLOR)
    tex_mgr.generate_texture('dirt', DIRT_COLOR)
    tex_mgr.generate_texture('stone', STONE_COLOR)
    
    world = World()
    player = Player()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            
            # Mouse Clicks (Block interaction)
            if event.type == pygame.MOUSEBUTTONDOWN:
                hit_block, prev_block = raycast(player, world)
                if event.button == 1: # Left Click: Break
                    if hit_block:
                        world.remove_block(hit_block)
                elif event.button == 3: # Right Click: Place
                    if hit_block and prev_block:
                        # Prevent placing inside player
                        px, py, pz = int(round(player.pos[0])), int(round(player.pos[1])), int(round(player.pos[2]))
                        if prev_block != (px, py, pz):
                            world.add_block(prev_block, 'stone')

        # Update Player
        keys = pygame.key.get_pressed()
        player.update(dt, keys)
        
        # Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Camera Transform
        # Rotate camera based on pitch and yaw
        glRotatef(-player.rot[1], 1, 0, 0)
        glRotatef(-player.rot[0], 0, 1, 0)
        # Translate world opposite to player position
        glTranslatef(-player.pos[0], -player.pos[1], -player.pos[2])
        
        # Draw Scene
        world.draw(tex_mgr)
        draw_crosshair()
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
