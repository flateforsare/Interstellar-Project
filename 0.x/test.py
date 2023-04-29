import pygame

# Game XY = 2000 by 2000

# Initialize Pygame
pygame.init()

# Set screen size
scale = 6
screen_width = 128 * scale
screen_height = 128 * scale
screen = pygame.display.set_mode((screen_width, screen_height))

# Load sprite
sprite = pygame.image.load('ShipA.png').convert_alpha()
sprite_width = sprite.get_width()
sprite_height = sprite.get_height()

# Scale sprite
sprite = pygame.transform.scale(sprite, (sprite_width * scale, sprite_height * scale))

# Set up font for coordinates
font = pygame.font.Font(None, 36)

# Initialize sprite position
sprite_x = screen_width / 2 - sprite_width / 2
sprite_y = 0

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            sprite_y -= 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        sprite_y -= 1
    
    # Draw black background
    screen.fill((0, 0, 0))

    # Calculate center position
    center_x = sprite_x
    center_y = screen_height / 2
    
    # Draw sprite at center position
    screen.blit(sprite, (center_x, sprite_y))

    # Render coordinates as text surface
    coordinates = f"({center_x}, {center_y})"
    text_surface = font.render(coordinates, True, (255, 255, 255))
    
    # Blit text surface onto screen surface at top left position
    screen.blit(text_surface, (10, 10))

    # Update screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
