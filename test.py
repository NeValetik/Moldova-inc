import pygame
import math

pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rotate Sprite Towards Next Point")

# Colors
WHITE = (255, 255, 255)

# Load sprite image
sprite_image = pygame.image.load("images/plane.png")
sprite_rect = sprite_image.get_rect()

# Initial sprite position and angle
sprite_pos = pygame.math.Vector2(100, 100)
next_point = pygame.math.Vector2(200, 200)

def rotate_sprite_towards_point(sprite, next_point):
    # Calculate vector from sprite position to next point
    direction = next_point - sprite_pos

    # Calculate angle between sprite and next point
    angle = math.degrees(math.atan2(-direction.y, direction.x))

    # Rotate the sprite image
    rotated_sprite = pygame.transform.rotate(sprite, angle)
    new_rect = rotated_sprite.get_rect(center=sprite_rect.center)

    return rotated_sprite, new_rect

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate sprite towards next point
    rotated_sprite, new_rect = rotate_sprite_towards_point(sprite_image, next_point)

    # Update sprite position
    sprite_pos += (next_point - sprite_pos) * 0.05  # Example: Move towards next point

    # Draw rotated sprite
    screen.blit(rotated_sprite, new_rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
