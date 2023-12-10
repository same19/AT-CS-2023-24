"""
ChatGPT supplied a framework for working with pygame. I coded almost everything else. Note that ChatGPT helped organize code at the end as well but did not change any functionality.

Author: Sam Engel
Date: December 12th, 2023
"""

import pygame
import sys
from vector import vector
from fsm import FSM
import car as car_module
import enemy_car
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Driving Game")

# Set up the clock
clock = pygame.time.Clock()

# Initialize gas FSM for car
def init_gas_fsm(car):
    fsm = FSM("Coasting")
    fsm.add_transition("Brake", "Accelerating", car.brake, "Braking")
    fsm.add_transition("Unaccelerate", "Accelerating", car.coast, "Coasting")
    fsm.add_transition("Accelerate", "Braking", car.accelerate, "Accelerating")
    fsm.add_transition("Unbrake", "Braking", car.coast, "Coasting")
    fsm.add_transition("Accelerate", "Coasting", car.accelerate, "Accelerating")
    fsm.add_transition("Brake", "Coasting", car.brake, "Braking")
    return fsm

# Initialize turn FSM for car
def init_turn_fsm(car):
    fsm = FSM("Center")
    fsm.add_transition("Left", "Right", car.turn_left, "Left")
    fsm.add_transition("Unright", "Right", car.turn_center, "Center")
    fsm.add_transition("Right", "Left", car.turn_right, "Right")
    fsm.add_transition("Unleft", "Left", car.turn_center, "Center")
    fsm.add_transition("Right", "Center", car.turn_right, "Right")
    fsm.add_transition("Left", "Center", car.turn_left, "Left")
    return fsm

# Initialize enemy FSM
def init_enemy_fsm(enemy):
    fsm = FSM("Chasing")
    fsm.add_transition("Next", "Avoiding", enemy.chase, "Chasing")
    fsm.add_transition("Next", "Chasing", enemy.avoid, "Avoiding")
    return fsm

# Spawn player's car
def spawn_car():
    c = car_module.Car(length=50, max_force=500, max_wheel_angle=25, map=map_dimensions)
    c.position = vector(width // 2 - c.length, -height // 2 + c.length)
    c.direction = vector(-1, 0)
    return c

# Spawn enemy car
def spawn_enemy_car(car):
    e = enemy_car.enemy_car(length=50, target=(car, 1), max_force=700, max_wheel_angle=30, map=map_dimensions)
    e.position = vector(-width // 2 + e.length, height // 2 - e.length)
    return e

# Game parameters
map_dimensions = (width, height)
health = 100
start_time = time.time_ns()
add_enemy_delay = 15  # seconds

# Initialize car
car = spawn_car()
gas_fsm = init_gas_fsm(car)
turn_fsm = init_turn_fsm(car)

# Initialize enemy car
enemies = [spawn_enemy_car(car)]
enemy_fsm = [init_enemy_fsm(enemy) for enemy in enemies]
enemies_hitting_car = [False for _ in enemies]
FPS = 60

# Draw a specific car on the screen with a certain color
def draw_car(c, color=(255, 0, 0)):
    global health
    scale = 1
    screen_center = vector(width // 2, height // 2)

    def flip_y(v):
        return vector(v[0], -v[1])

    center = screen_center + scale * flip_y(c.position)

    if c == car and health < 100:
        pygame.draw.line(screen, color, center - scale * health / 100 * c.length / 2 * flip_y(c.direction),
                         center + scale * health / 100 * c.length / 2 * flip_y(c.direction), width=3)
    else:
        pygame.draw.line(screen, color, center - scale * c.length / 2 * flip_y(c.direction),
                         center + scale * c.length / 2 * flip_y(c.direction), width=3)
    pygame.draw.polygon(screen, color=color, points=[screen_center + scale * flip_y(corner) for corner in c.box()])

# Load background music
# "Jeremy Blake - Powerup! ♫ NO COPYRIGHT 8-bit Music" from Youtube
pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # repeat infinitely

# Set up font
font = pygame.font.Font('freesansbold.ttf', 32)


# Function to handle key down events
def handle_key_down_event(event):
    global gas_fsm, turn_fsm
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        gas_fsm.process("Accelerate")
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_SPACE:
        gas_fsm.process("Brake")
    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        turn_fsm.process("Right")
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        turn_fsm.process("Left")

# Function to handle key up events
def handle_key_up_event(event):
    global gas_fsm, turn_fsm
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        gas_fsm.process("Unaccelerate")
    if event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_SPACE:
        gas_fsm.process("Unbrake")
    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        turn_fsm.process("Unleft")
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        turn_fsm.process("Unright")

# Function to handle player's death
def handle_player_death():
    global health, car, enemies, gas_fsm, turn_fsm
    health -= 10
    car = spawn_car()
    gas_fsm = init_gas_fsm(car)
    turn_fsm = init_turn_fsm(car)
    for enemy in enemies:
        enemy.set_target(car)

# Function to handle enemy spawn
def handle_enemy_spawn():
    global start_time, add_enemy_delay, enemies, enemy_fsm, enemies_hitting_car
    if (time.time_ns() - start_time) % (add_enemy_delay * 1000000000) < 1000000000 / FPS:
        new_enemy = spawn_enemy_car(car)
        enemies.append(new_enemy)
        enemy_fsm.append(init_enemy_fsm(new_enemy))
        enemies_hitting_car.append(False)

# Function to update and draw enemy cars
def handle_enemy_update_and_draw():
    # Access global variables
    global health, enemies, enemy_fsm, enemies_hitting_car, car

    # Iterate over all enemy cars
    for i in range(len(enemies)):
        # Determine the color based on whether the enemy is chasing or not
        color = (255, 0, 0) if enemies[i].chasing else (0, 255, 0)

        # Update the position and state of the enemy car
        enemies[i].update(dt)

        # Check if the enemy is no longer alive
        if not enemies[i].alive:
            # Increase player's health as a reward for defeating the enemy
            health += 3 / len(enemies)

            # Save the current state and time for the next enemy
            state = enemies[i].chasing
            next_t = enemies[i].next_time_change_state

            # Respawn a new enemy
            enemies[i] = spawn_enemy_car(car)
            enemy_fsm[i] = init_enemy_fsm(enemies[i])

            # If the state has changed, process the transition
            if state != enemies[i].chasing:
                enemy_fsm[i].process("Next")

            # Restore the saved time for the next state change
            enemies[i].next_time_change_state = next_t

        # Check for collision with the player's car
        if enemies[i].collide_car(car):
            color = (255, 255, 255)
            # Check if the enemy is not already hitting the player's car
            if not enemies_hitting_car[i]:
                # Adjust player's health based on the collision
                health += 10 * (-1 if enemies[i].chasing else 1)
                enemies_hitting_car[i] = True
        else:
            enemies_hitting_car[i] = False

        # Check if it's time for the enemy to change its state
        if time.time_ns() > enemies[i].next_time_change_state:
            enemy_fsm[i].process("Next")

        # Draw the enemy car on the screen with the determined color
        draw_car(enemies[i], color=color)

# Function to display health on the screen
def display_health():
    health_text = font.render(str(int(health)), True, (255, 255, 255))
    health_text_rect = health_text.get_rect()
    health_text_rect.center = (width - 60, 30)
    screen.blit(health_text, health_text_rect)

# Function to handle game over
def handle_game_over():
    if health <= 0:
        print("You died!")
        print("Score:", (time.time_ns() - start_time) / 1000000000)
        end_text1 = font.render("You died!", True, (255, 255, 255))
        end_text2 = font.render("Score: " + str(int((time.time_ns() - start_time) / 1000000000)), True, (255, 255, 255))
        end_text1_rect = end_text1.get_rect()
        end_text2_rect = end_text2.get_rect()
        end_text1_rect.center = (width // 2, height // 2)
        end_text2_rect.center = (width // 2, height // 2 + 50)
        screen.blit(end_text1, end_text1_rect)
        screen.blit(end_text2, end_text2_rect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

#Game loop
while True:
    dt = clock.tick(FPS) / 1000

    # Handle all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            handle_key_down_event(event)
        elif event.type == pygame.KEYUP:
            handle_key_up_event(event)

    # Fill the screen with a black background color
    screen.fill((0, 0, 0))

    # Update player's car
    car.update(dt)
    draw_car(car, color=(255, 255, 0))

    # Handle player's death
    if not car.alive:
        handle_player_death()

    # Add new enemy cars at intervals
    handle_enemy_spawn()

    # Update and draw enemy cars
    handle_enemy_update_and_draw()

    # Display health on the screen
    display_health()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    # Check if player health is zero
    handle_game_over()