import pygame
import sys
from vector import vector
from fsm import FSM
import numpy as np
from rigid_body import rigid_body
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

def init_gas_fsm(car):
    fsm = FSM("Coasting")
    #initialize the finite state machine for a car
    fsm.add_transition("Brake", "Accelerating",car.brake,"Braking")
    fsm.add_transition("Unaccelerate", "Accelerating",car.coast,"Coasting")

    fsm.add_transition("Accelerate", "Braking",car.accelerate,"Accelerating")
    fsm.add_transition("Unbrake", "Braking",car.coast,"Coasting")

    fsm.add_transition("Accelerate", "Coasting",car.accelerate,"Accelerating")
    fsm.add_transition("Brake", "Coasting",car.brake,"Braking")
    return fsm
def init_turn_fsm(car):
    fsm = FSM("Center")
    fsm.add_transition("Left", "Right",car.turn_left,"Left")
    fsm.add_transition("Unright", "Right",car.turn_center,"Center")

    fsm.add_transition("Right", "Left",car.turn_right,"Right")
    fsm.add_transition("Unleft", "Left",car.turn_center,"Center")

    fsm.add_transition("Right", "Center",car.turn_right,"Right")
    fsm.add_transition("Left", "Center",car.turn_left,"Left")
    return fsm
def init_enemy_fsm(enemy):
    fsm = FSM("Chasing")
    fsm.add_transition("Next", "Avoiding", enemy.chase, "Chasing")
    fsm.add_transition("Next", "Chasing", enemy.avoid, "Avoiding")
    return fsm
def spawn_car():
    c = car_module.Car(length=50, max_force = 500, max_wheel_angle = 25, map=map_dimensions)
    c.position = vector(width//2 - c.length, -height//2 + c.length)
    c.direction = vector(-1,0)
    return c
def spawn_enemy_car(car):
    e = enemy_car.enemy_car(length=50,target=(car,1), max_force = 700, max_wheel_angle = 30, map=map_dimensions)
    e.position = vector(-width//2 + e.length, height//2 - e.length)
    return e

map_dimensions = (width, height)
car = spawn_car()
gas_fsm = init_gas_fsm(car)
turn_fsm = init_turn_fsm(car)

enemies = [spawn_enemy_car(car)]
enemy_fsm = [init_enemy_fsm(enemy) for enemy in enemies]
enemies_hitting_car = [False for i in enemies]
FPS = 60


def draw_car(c, color = (255,0,0)):
    scale = 1
    screen_center = vector(width//2, height//2)
    def flip_y(v):
        return vector(v[0], -v[1])
    center = screen_center + scale*flip_y(c.position)
    m_pos = flip_y(pygame.mouse.get_pos()-screen_center)/scale
    # if c.collide_point(m_pos):
    #     color = (255,255,255)
    if c == car and health < 100:
        pygame.draw.line(screen, color, center - scale*health/100*c.length/2*flip_y(c.direction), center + scale*health/100*c.length/2*flip_y(c.direction), width=3)
    else:
        pygame.draw.line(screen, color, center - scale*c.length/2*flip_y(c.direction), center + scale*c.length/2*flip_y(c.direction), width=3)
    pygame.draw.polygon(screen, color=color, points=[screen_center + scale*flip_y(corner) for corner in c.box()])
    pygame.draw.line(screen, (0,255,0), center, center + (scale/2)*flip_y(c.wheel_direction))
    pygame.draw.line(screen, (0,0,255), center, center + flip_y(c.target_velocity))
    pygame.draw.line(screen, (0,255,255), center, center + scale*flip_y(c.turn_center_pos))

    box = c.box()
    prev_index = -1
    for index in range(len(box)):
        pygame.draw.line(screen, (255,255,255), center + scale*(flip_y(box[prev_index]-c.position)),center + scale*(flip_y(box[index]-c.position)))
        prev_index = index
# Game loop
health = 100
start_time = time.time_ns()
add_enemy_delay = 15 #seconds
while True:
    dt = clock.tick(FPS)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                gas_fsm.process("Accelerate")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                gas_fsm.process("Brake")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # Rotate the velocity vector clockwise (positive angle)
                turn_fsm.process("Right")
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                # Rotate the velocity vector counterclockwise (negative angle)
                turn_fsm.process("Left")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                gas_fsm.process("Unaccelerate")
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                gas_fsm.process("Unbrake")
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                turn_fsm.process("Unleft")
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                turn_fsm.process("Unright")
    screen.fill((0,0,0))
    
    car.update(dt)
    draw_car(car, color=(255,255,0))
    if not car.alive:
        health -= 5
        print(health)
        car = spawn_car()
        gas_fsm = init_gas_fsm(car)
        turn_fsm = init_turn_fsm(car)
        for enemy in enemies:
            enemy.set_target(car)
    # print((time.time_ns() - start_time) % (add_enemy_delay * 1000000000) - 1000000000/FPS)
    if (time.time_ns() - start_time) % (add_enemy_delay * 1000000000) < 1000000000/FPS:
        new_enemy = spawn_enemy_car(car)
        enemies.append(new_enemy)
        enemy_fsm.append(init_enemy_fsm(new_enemy))
        enemies_hitting_car.append(False)
    for i in range(len(enemies)):
        color = (255,0,0) if enemies[i].chasing else (0,255,0)
        enemies[i].update(dt)
        if not enemies[i].alive:
            health += 3/len(enemies)
            print(health)
            state = enemies[i].chasing
            next_t = enemies[i].next_time_change_state
            enemies[i] = spawn_enemy_car(car)
            enemy_fsm[i] = init_enemy_fsm(enemies[i])
            if state != enemies[i].chasing:
                enemy_fsm[i].process("Next")
            enemies[i].next_time_change_state = next_t
        if enemies[i].collide_car(car):
            color = (255,255,255)
            if enemies_hitting_car[i] == False:
                health += 10*(-1 if enemies[i].chasing else 1)
                print(health)
                enemies_hitting_car[i] = True
        else:
            enemies_hitting_car[i] = False
        if time.time_ns() > enemies[i].next_time_change_state:
            # print("CHANGE STATE TRIGGER", i)
            enemy_fsm[i].process("Next")
        draw_car(enemies[i], color=color)

    font = pygame.font.Font('freesansbold.ttf', 32)
    # create a text surface object,
    # on which text is drawn on it.
    text = font.render(str(int(health)), True, (255,255,255))
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    # set the center of the rectangular object.
    textRect.center = (width - 60, 30)
    screen.blit(text, textRect)

    # Update the display
    pygame.display.flip()
    # Cap the frame rate
    clock.tick(FPS)  # Adjust the value to control the speed of the game
    if health <= 0:
        print("You died!")
        print("Score:", (time.time_ns()-start_time)/1000000000)
        time.sleep(1)
        break