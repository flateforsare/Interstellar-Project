import pygame
import math

# Initialize Pygame
pygame.init()

# Set screen size
scale = 3
screen_width = 256 * scale
screen_height = 256 * scale
screen = pygame.display.set_mode((screen_width, screen_height))

def check_collision(sprite, home_station):
    sprite_radius = max(sprite.width, sprite.height) / 2
    home_station_radius = max(home_station.width, home_station.height) / 2
    distance = math.sqrt((sprite.x - home_station.x)**2 + (sprite.y - home_station.y)**2)
    if distance <= sprite_radius + home_station_radius:
        # Collision detected, open menu
        print("Collision detected!")
        # Insert menu code here

class Sprite:
    def __init__(self, image_path, scale):
        self.font = pygame.font.SysFont(None, 24)
        # Load sprite image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width, self.height = self.image.get_size()

        # Scale sprite
        self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))

        # Set initial position and rotation
        self.x, self.y = 0, 0
        self.angle = 0
        self.speed = 0

        # Load alternative sprite image
        self.alt_image = pygame.image.load('ShipA2.png').convert_alpha()
        self.alt_image = pygame.transform.scale(self.alt_image, (self.width * scale, self.height * scale))
        self.use_alt_image = False

        # Dictionary to keep track of which keys are being pressed down
        self.keys_pressed = {pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}

    def rotate_left(self):
        self.angle -= 0.5
        self.angle %= 360

    def rotate_right(self):
        self.angle += 0.5
        self.angle %= 360

    def handle_key_down(self, key):
        if key == pygame.K_a:
            self.keys_pressed[pygame.K_a] = True
        elif key == pygame.K_d:
            self.keys_pressed[pygame.K_d] = True
        elif key == pygame.K_w:
            self.keys_pressed[pygame.K_w] = True

    def handle_key_up(self, key):
        if key == pygame.K_a:
            self.keys_pressed[pygame.K_a] = False
        elif key == pygame.K_d:
            self.keys_pressed[pygame.K_d] = False
        elif key == pygame.K_w:
            self.keys_pressed[pygame.K_w] = False

    def draw(self, surface, camera_x, camera_y):
        # Rotate sprite
        if self.use_alt_image:
            rotated_image = pygame.transform.rotate(self.alt_image, -self.angle)
        else:
            rotated_image = pygame.transform.rotate(self.image, -self.angle)

        # Draw sprite at its current position relative to the camera position
        surface.blit(rotated_image, (self.x - camera_x, self.y - camera_y))

    def update(self,w,a,d):
        # Handle key events
        if w:
            if self.speed < 6:
                self.speed += 0.1
            else:
                self.speed = 6
            if self.use_alt_image == False:
                self.use_alt_image = True
                self.image = pygame.image.load('ShipA2.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
                self.use_alt_image = True
        else:
            if self.speed > 0.5:
                self.speed -= 0.3
            else:
                self.speed = 0
            if self.use_alt_image == True:
                self.use_alt_image = False
                self.image = pygame.image.load('ShipA1.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
    
        if a:
            self.rotate_left()
        if d:
            self.rotate_right()
    
        self.x += math.sin(math.radians(self.angle)) * self.speed
        self.y -= math.cos(math.radians(self.angle)) * self.speed

class HomeStation:
    def __init__(self, image_path, scale):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width, self.height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))

        # Set initial position for home station
        self.x, self.y = 100, 100

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.x - camera_x, self.y - camera_y))

# Load sprite
sprite = Sprite('ShipA1.png', scale)
home_station = HomeStation('HomeStationA1.png', scale)

# Set up font for coordinates
font = pygame.font.Font(None, 36)

#fps
clock = pygame.time.Clock()

#Keyspressed?
keys_pressed = {}
i=0

# Main game loop
running = True
def outloop():
    # Handle input events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            keys_pressed[event.key] = False
    
    if keys_pressed.get(pygame.K_w):
        press_w=True
    else:
        press_w=False
    if keys_pressed.get(pygame.K_a):
        press_a=True
    else:
        press_a=False
    if keys_pressed.get(pygame.K_d):
        press_d=True
    else:
        press_d=False
     
    # Update the sprite
    sprite.update(press_w,press_a,press_d)
    check_collision(sprite, home_station)
    i+=1
    
    # Handle input events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Set the corresponding value in keys_pressed to True
            keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            # Set the corresponding value in keys_pressed to False
            keys_pressed[event.key] = False
    
    #Update Sprite
    sprite.update(press_w,press_a,press_d)

    # Draw black background
    screen.fill((0, 0, 0))

    # Find camera position
    camera_x = sprite.x - screen_width/2
    camera_y = sprite.y - screen_height/2

    # Draw sprite
    sprite.draw(screen, camera_x, camera_y)
    home_station.draw(screen, camera_x, camera_y)

    # Render coordinates as text surface
    coordinates = f"({int(sprite.x)}, {int(sprite.y)}, {i})"
    text_surface = font.render(coordinates, True, (255, 255, 255))

    # Blit text surface onto screen surface at top left position
    screen.blit(text_surface, (10, 10))

    # Update screen
    pygame.display.flip()

    clock.tick(60)

# Quit Pygame
pygame.quit()
out=True
#main loop
while running:
    if out:
        outloop()
    if home:
        homeloop()