import pygame as pg
import random
import asyncio

pg.init()

WIDTH = 800
HEIGHT = 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Falling Debris and Spikes")
clock = pg.time.Clock()
font = pg.font.Font(None, 30)

BLACK = (0, 0, 0)

# Player variables
player_size = 40
player_x = WIDTH // 2
player_y = HEIGHT - player_size
player_speed = 5
player_jump = False
player_vel_y = 0
jump_strength = 12
gravity = 0.5
lives = 3
score = 0
state = 1       # 1: Gameplay, 2: End screen

# Debris and Spike variables
debris = []
debris_speed = 5
debris_size = 40

spikes = []
spike_size = 40
spike_speed = 5

mushrooms = []  # List to hold mushrooms
mushroom_size = 40
mushroom_speed = 5  # Speed at which mushrooms move upward

# Star variables (move horizontally)
stars = []  # List to store stars
star_size = 20
star_speed = 5  # Speed at which stars move horizontally

# Laser variables (move horizontally in random direction)
lasers = []  # List to store lasers
laser_width = 10
laser_height = 5
laser_speed = 7  # Speed at which lasers move

# Load images
player_img = pg.image.load("./assets/images/mario.png")
player_img = pg.transform.scale(player_img, (player_size, player_size))

debris_img = pg.image.load("./assets/images/spike.png")
debris_img = pg.transform.scale(debris_img, (debris_size, debris_size))

star_img = pg.image.load("./assets/images/II.jpg")  # Assuming this is the star image
star_img = pg.transform.scale(star_img, (star_size, star_size))

spike_img = pg.image.load("./assets/images/e1.png")
spike_img = pg.transform.scale(spike_img, (spike_size, spike_size))

mushroom_img = pg.image.load("./assets/images/mushroom.png")  # Add your mushroom image here
mushroom_img = pg.transform.scale(mushroom_img, (mushroom_size, mushroom_size))

bg_img = pg.image.load("./assets/images/background.png")
bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))

# Restart game function
def restart_game():
    global player_x, player_y, player_jump, player_vel_y, lives, score, debris, spikes, mushrooms, lasers, stars
    player_x = WIDTH // 2
    player_y = HEIGHT - player_size
    player_jump = False
    player_vel_y = 0
    lives = 10
    score = 0
    debris = []
    spikes = []
    mushrooms = []
    lasers = []  # Clear the lasers as well
    stars = []  # Clear stars as well



running = True

def main():

    global running, state, score, lives
    global player_x, player_y, player_vel_y, player_jump

    while running:

        clock.tick(30)
        screen.blit(bg_img, (0, 0))

        if state == 1:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                player_x -= player_speed
            if keys[pg.K_RIGHT]:
                player_x += player_speed
            if keys[pg.K_UP] and not player_jump:
                player_jump = True
                player_vel_y = -jump_strength
            if keys[pg.K_d]:
                player_x -= 20
            if keys[pg.K_a]:
                player_x += 20

            if player_jump:
                player_vel_y += gravity
                player_y += player_vel_y
                if player_y >= HEIGHT - player_size:
                    player_y = HEIGHT - player_size
                    player_jump = False
                    player_vel_y = 0

            # Create debris from the bottom edges (moving horizontally)
            if random.randint(0,100) < 1:
                side = random.choice(["left", "right"])  # Randomly choose left or right side
                if side == "left":
                    x = 0  # Start from the left edge
                    dx = random.randint(3, 6)  # Move to the right
                else:
                    x = WIDTH - debris_size  # Start from the right edge
                    dx = random.randint(-6, -3)  # Move to the left
                y = HEIGHT - debris_size  # Spawn at the bottom of the screen
                debris.append([x, y, dx])  # Store x, y, and horizontal speed (dx)

            if random.randint(0,100) < 1:
                side = random.choice(["left", "right"])  # Randomly choose left or right side
                if side == "left":
                    x = 20  # Start from the left edge
                    dx = random.randint(3, 6)  # Move to the right
                else:
                    x = WIDTH - debris_size  # Start from the right edge
                    dx = random.randint(-6, -3)  # Move to the left
                y = HEIGHT - debris_size  # Spawn at the bottom of the screen
                debris.append([x, y, dx])

            # Create spikes (spawn at the bottom of the screen)
            if random.randint(0,100) < 1:
                x = random.randint(0, WIDTH - spike_size)
                spikes.append([x, HEIGHT])  # Spikes spawn from the ground (bottom)

            # Create mushrooms (spawn at the bottom of the screen)
            if random.randint(0,100) < 1:
                x = random.randint(0, WIDTH - mushroom_size)
                mushrooms.append([x, HEIGHT])  # Mushrooms spawn from the ground (bottom)

            # Create stars at the height of the player when they jump
            if player_jump and random.randint(0,100) < 5:  # Lower chance to spawn stars when jumping
                side = random.choice(["left", "right"])  # Randomly choose left or right side
                if side == "left":
                    x = 0  # Spawn on the left side
                else:
                    x = WIDTH - star_size  # Spawn on the right side
                y = player_y  # Spawn at the player's jump height
                dx = random.choice([3, -3])  # Move the star to the left or right
                stars.append([x, y, dx])  # Store x, y position and horizontal speed for stars

            # Create lasers at random heights (moving horizontally in random direction)
            if random.randint(0,100) < 1:
                side = random.choice(["left", "right"])  # Randomly choose left or right side
                y = random.randint(0, HEIGHT - laser_height)  # Randomly choose a height for laser
                if side == "left":
                    x = 0  # Spawn on the left edge
                    dx = random.randint(3, 6)  # Move to the right
                else:
                    x = WIDTH - laser_width  # Spawn on the right edge
                    dx = random.randint(-6, -3)  # Move to the left
                lasers.append([x, y, dx])  # Store x, y (random height), and horizontal speed

            # Update stars (move horizontally)
            for star in stars[:]:
                star[0] += star[2]  # Move the star horizontally (to the left or right)

                # If star moves off the screen, remove it
                if star[0] < 0 or star[0] > WIDTH:
                    stars.remove(star)

                # Draw the star on the screen
                screen.blit(star_img, (star[0], star[1]))

                # Collision detection with player
                player_rect = pg.Rect(player_x, player_y, player_size, player_size)
                star_rect = pg.Rect(star[0], star[1], star_size, star_size)
                if player_rect.colliderect(star_rect):
                    score += 1  # Increase score on collecting star
                    stars.remove(star)

            # Update lasers (move horizontally)
            for laser in lasers[:]:
                laser[0] += laser[2]  # Move the laser horizontally

                # If laser moves off the screen, remove it
                if laser[0] < 0 or laser[0] > WIDTH:
                    lasers.remove(laser)

                # Draw the laser on the screen
                pg.draw.rect(screen, (255, 0, 0), pg.Rect(laser[0], laser[1], laser_width, laser_height))

                # Collision detection with player
                player_rect = pg.Rect(player_x, player_y, player_size, player_size)
                laser_rect = pg.Rect(laser[0], laser[1], laser_width, laser_height)
                if player_rect.colliderect(laser_rect):
                    lives -= 1
                    lasers.remove(laser)
                    if lives <= 0:
                        state = 2

            # Update debris (moving horizontally without upward movement)
            for d in debris[:]:
                d[0] += d[2]  # Update the x position based on dx (horizontal speed)

                # If debris moves off the screen, remove it
                if d[0] < 0 or d[0] > WIDTH:
                    debris.remove(d)
                    score += 1

                # Draw the debris on the screen
                screen.blit(debris_img, (d[0], d[1]))

                # Collision detection with player
                player_rect = pg.Rect(player_x, player_y, player_size, player_size)
                debris_rect = pg.Rect(d[0], d[1], debris_size, debris_size)
                if player_rect.colliderect(debris_rect):
                    lives -= 1
                    debris.remove(d)
                    if lives <= 0:
                        state = 2

            # Update spikes (move upward)
            for s in spikes[:]:
                s[1] -= spike_speed + score // 10  # Move upward
                screen.blit(spike_img, (s[0], s[1]))

            # Update mushrooms (move upward and increase lives on collision)
            for m in mushrooms[:]:
                m[1] -= mushroom_speed + score // 10  # Move upward like spikes
                screen.blit(mushroom_img, (m[0], m[1]))

                player_rect = pg.Rect(player_x, player_y, player_size, player_size)
                mushroom_rect = pg.Rect(m[0], m[1], mushroom_size, mushroom_size)
                if player_rect.colliderect(mushroom_rect):
                    lives += 1  # Increase lives on collision with mushroom
                    mushrooms.remove(m)

                elif m[1] < -mushroom_size:  # If mushroom moves off-screen from the top
                    mushrooms.remove(m)

            # Display score and lives
            info = font.render(f"Score: {score}  Lives: {lives}", True, BLACK)
            screen.blit(info, (WIDTH - 200, HEIGHT - 40))

            # Draw the player
            screen.blit(player_img, (player_x, player_y))
        
        elif state == 2:
            # Game Over Screen
            game_over_text = font.render(f"Game Over! Score: {score}", True, BLACK)
            restart_text = font.render("Press R to Restart", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        restart_game()
                        state = 1

        pg.display.flip()

    pg.quit()

main()