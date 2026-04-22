# Use the Pygame package to develop a 2D arcade game where the player shoots down a fleet of aliens.
# The aliens drop down the screen in waves that increase in speed and difficulty.

import pygame

# Initialize Pygame
pygame.init()

# Set the screen width and height
screen_width, screen_height = 800, 600

def draw_level_counter(screen, level, width, font_size, x_margin, y_margin): 
    # Draws the current game level counter at the top-right corner of the screen.
    font = pygame.font.SysFont(None, font_size)
    # Create a rendered surface for the level text
    level_surf = font.render(f"Level: {level}", True, (255, 255, 255))
    # Position the level text
    level_rect = level_surf.get_rect(topright=(width - x_margin, y_margin))
    screen.blit(level_surf, level_rect)

def draw_points_counter(screen, points, font_size, x_margin, y_margin): 
    # Draws the current points counter at the top-left corner of the screen.
    font = pygame.font.SysFont(None, font_size)
    # Create a rendered surface for the points text
    points_surf = font.render(f"Points: {points}", True, (255, 255, 255))
    # Position the points text
    points_rect = points_surf.get_rect(topleft=(x_margin, y_margin))
    screen.blit(points_surf, points_rect)

def create_player(player_color, bottom_margin): 
    # Creates the horizontally centered player rectangle and returns a dictionary holding its rect and color.
    w, h = 60, 15  # Dimensions of the player paddle
    rect = pygame.Rect((screen_width - w) // 2, screen_height - h - bottom_margin, w, h)
    return {'rect': rect, 'color': player_color}

def create_bullet(player_rect, bullet_color, bullet_width, bullet_height, bullet_speed): 
    # Creates a bullet as a dict with rendering info, using the player's current position.
    # Surface for the round bullet
    s = pygame.Surface((bullet_width, bullet_height), pygame.SRCALPHA)
    pygame.draw.circle(
        s, bullet_color,
        (bullet_width // 2, bullet_height // 2),
        min(bullet_width, bullet_height) // 2 - 1
    )
    # Bullet spawns at the center top of the player
    r = pygame.Rect(
        player_rect.centerx - bullet_width // 2,
        player_rect.top - bullet_height,
        bullet_width, bullet_height
    )
    return {
        'surface': s,
        'rect': r,
        'color': bullet_color,
        'speed': bullet_speed,
        'width': bullet_width,
        'height': bullet_height
    }

def create_aliens(padding, rows, cols, alien_width, alien_height):
    # Generates a list of aliens for the given arrangement (rows x cols), centered at the top of the screen.
    aliens = []
    # Calculate offset to center the fleet
    sx = (screen_width - (cols * alien_width + (cols - 1) * padding)) // 2
    sy = 60  # Top margin of fleet
    for row in range(rows):
        for col in range(cols):
            x = sx + col * (alien_width + padding)
            y = sy + row * (alien_height + padding)
            # Each alien is a dict with its rect and color
            aliens.append({
                'rect': pygame.Rect(x, y, alien_width, alien_height),
                'color': (255, 255, 255)  # White aliens
            })
    return aliens

def draw_game_over(screen, width, height):
    # Draws a prominent "GAME OVER!" message centered on the screen.
    font = pygame.font.SysFont(None, 80)
    msg = font.render("GAME OVER!", True, (255, 0, 0))
    # Center the game over message
    screen.blit(msg, msg.get_rect(center=(width // 2, height // 2)))
    pygame.display.flip()

def main():
    # Create game window
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Initialize game variables
    level, points = 1, 0
    neon_green = (57, 255, 20)  # Player color

    player = create_player(neon_green, bottom_margin=30)

    # Bullet properties
    bullet_color = (255, 0, 255)
    bullet_width, bullet_height = 10, 20
    bullet_speed = 7
    bullets = []
    player_speed = 7

    # Alien fleet properties
    alien_rows, alien_cols = 3, 8
    alien_width, alien_height, alien_padding = 25, 25, 5

    # Alien movement tracking
    frame_counter = 0 
    alien_pending_drop = False

    # Create initial alien fleet
    aliens = create_aliens(alien_padding, alien_rows, alien_cols, alien_width, alien_height)

    # Fleet horizontal movement direction (1: right, -1: left)
    alien_speed_x, alien_direction = 4, 1
    frames_per_col, current_col = 5, 0
    drop_rate = 3  # How much to move down during a "drop"
    alien_left_margin, alien_right_margin = 20, 20

    # Set up game state
    clock = pygame.time.Clock()
    running = True
    game_over = False

    # MAIN GAME LOOP
    while running:
        clock.tick(60)  # Limit to 60 frames per second
        screen.fill((0, 0, 0))  # Clear the screen to black

        if not game_over:
            # ------------ PLAYER MOVEMENT CONTROLS -----------------
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player['rect'].x -= player_speed
            if keys[pygame.K_RIGHT]:
                player['rect'].x += player_speed
            # Restrict player to screen bounds
            player['rect'].left = max(player['rect'].left, 20)
            player['rect'].right = min(player['rect'].right, screen_width - 20)

            # ------------ ALIEN MOVEMENT AND DROP LOGIC -------------
            if aliens:
                # Get edges of fleet
                leftmost_x = min(alien['rect'].left for alien in aliens)
                rightmost_x = max(alien['rect'].right for alien in aliens)
                hit_left = leftmost_x <= alien_left_margin
                hit_right = rightmost_x >= screen_width - alien_right_margin

                if not alien_pending_drop:
                    # At fleet edge: begin drop and reverse direction
                    if hit_left and alien_direction == -1:
                        alien_direction = 1
                        alien_pending_drop = True
                        current_col = 0
                        frame_counter = 0
                    elif hit_right and alien_direction == 1:
                        alien_direction = -1
                        alien_pending_drop = True
                        current_col = alien_cols - 1
                        frame_counter = 0

                # Controlled "drop" of each alien column, staggered per frame
                if alien_pending_drop:
                    col_ok = (alien_direction == -1 and current_col >= 0) or (alien_direction == 1 and current_col < alien_cols)
                    if col_ok:
                        dx = drop_rate if alien_direction == 1 else -drop_rate
                        # Only drop one full column at a time
                        for alien in reversed(aliens[current_col::alien_cols]):
                            alien['rect'].x += dx
                            alien['rect'].y += drop_rate
                        frame_counter += 1

                        # After enough frames, move to next column
                        if frame_counter >= frames_per_col:
                            current_col += 1 if alien_direction == 1 else -1
                            frame_counter = 0
                        # End of drop phase for all columns
                        if current_col < 0 or current_col == alien_cols:
                            alien_pending_drop = False
                else:
                    # Regular horizontal fleet movement
                    for alien in aliens:
                        alien['rect'].x += alien_speed_x * alien_direction

            # ------------ DRAW UI, PLAYER, ALIENS -------------------
            draw_level_counter(screen, level, screen_width, 30, 20, 20)

            draw_points_counter(screen, points, 30, 20, 20)
            
            pygame.draw.rect(screen, player['color'], player['rect'])

            for alien in aliens:
                pygame.draw.rect(screen, alien['color'], alien['rect'])

            # ----------- BULLET MOTION/COLLISION DETECTION ----------
            for bullet in bullets[:]:
                bullet['rect'].y -= bullet['speed']  # Move bullet up screen
                screen.blit(bullet['surface'], bullet['rect'])

                # Remove bullet if offscreen
                if bullet['rect'].bottom < 0:
                    bullets.remove(bullet)
                    continue

                # Bullet/alien collision detection (skip if in drop phase)
                if not alien_pending_drop:
                    for alien in aliens[:]:
                        if bullet['rect'].colliderect(alien['rect']):
                            points += 1
                            aliens.remove(alien)
                            bullets.remove(bullet)
                            break

            # ----------- LEVEL UP, CHECK GAME OVER ------------------
            if not aliens:
                # Player cleared the wave: advance level, reset state
                level += 1
                bullets.clear()
                alien_speed_x += 1  # Speed up aliens for next level
                aliens = create_aliens(alien_padding, alien_rows, alien_cols, alien_width, alien_height)

            # Check for alien-player collision: if so, end game
            if any(alien['rect'].colliderect(player['rect']) for alien in aliens):
                game_over = True
                draw_game_over(screen, screen_width, screen_height)

        else:
            # Draw the "game over" message if the player lost
            draw_game_over(screen, screen_width, screen_height)

        # Flip the Pygame display buffers to render everything
        pygame.display.flip()

        # ------------ EVENT HANDLING (QUIT, SHOOT) ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE and not game_over:
                    # Fire bullet on spacebar if not game over
                    bullets.append(create_bullet(
                        player['rect'], bullet_color, bullet_width, bullet_height, bullet_speed
                    ))

# Main program entrypoint
if __name__ == "__main__":
    main()