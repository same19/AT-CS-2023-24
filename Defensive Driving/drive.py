import pygame
import sys
import math
from vector import vector
from fsm import FSM
import numpy as np
from rigid_body import rigid_body
import car as car_module
import enemy_car

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Driving Game")

# Set up the clock
clock = pygame.time.Clock()

turn_angle = math.radians(35)  # Adjust the turning angle as needed
max_speed = 400

# class Car:
#     def __init__(self):
#         self.original_image = None
#         self.original_center = None
#         self.image = None
#         self.rect = None
#         self.velocity = vector(1,0)
#         self.position = vector(0,0)
#         self.direction = vector(1,0)
#         self.new_forward_vector = vector(1,0)
#         self.gas_acceleration = 0
#         self.acceleration = vector(0,0)
#         self.torque = 0
#         self.angle = 0
#         self.new_wheel_angle = 0
#         self.wheel_angle = 0
#         self.angular_velocity = 0
#         self.drifting = False
#         self.offset = vector(0,0)
#         self.back = vector(0,0)
#         self.front = vector(1,0)
#         self.wheel_direction = vector(1,0)
#         # torque = sin(self.wheel_angle)

#     def turn(self, angle):
#         self.new_wheel_angle = -angle
#         # if abs(self.wheel_angle + angle) < max_turn_angle:
#             # self.wheel_angle += angle
#         # self.torque = 50 * math.sin(angle)
#     def brake(self):
#         self.gas_acceleration = -1000
#     def coast(self):
#         self.gas_acceleration = 0
#     def accelerate(self):
#         self.gas_acceleration = 1000
#     def update(self, dt):
#         # print(self.wheel_angle)
#         wheel_turn_speed = math.pi/2 #radians per second
#         if self.wheel_angle < self.new_wheel_angle:
#             self.wheel_angle = min(self.new_wheel_angle, self.wheel_angle + wheel_turn_speed*dt)
#         elif self.wheel_angle > self.new_wheel_angle:
#             self.wheel_angle = max(self.new_wheel_angle, self.wheel_angle - wheel_turn_speed*dt)

#         self.wheel_direction = self.direction.rotate(self.wheel_angle)
            

#         steer_angle = self.wheel_angle * abs(self.velocity) / max_speed
#         self.new_forward_vector = self.direction.rotate(steer_angle)
#         new_forward_vector = self.new_forward_vector
#         amount = 0.1
#         if self.drifting:
#             amount = 0.3
#         self.direction = amount*(new_forward_vector - self.direction) + self.direction
#         self.direction.resize(1)
#         # self.direction = new_forward_vector


#         current_speed = abs(self.velocity)
#         # if current_speed < max_speed:
#         self.velocity += self.gas_acceleration * self.direction * dt
#         self.acceleration = self.gas_acceleration * self.direction * dt

#         trigger_lateral_velocity = 7
#         lateral_friction_factor = 10
#         backwards_friction_factor = 0.005
#         right_vector = self.direction.rotate(math.radians(90))
#         lateral_velocity = right_vector * right_vector.dot(self.velocity)
#         if abs(lateral_velocity) > trigger_lateral_velocity:
#             self.drifting = True
#             lateral_friction_factor = 0.5
#         else:
#             self.drifting = False
#         lateral_friction = -1*lateral_velocity * abs(lateral_velocity) * lateral_friction_factor
#         backwards_friction = -1*self.velocity * abs(self.velocity) * backwards_friction_factor
#         backwards_friction.resize(min(backwards_friction.norm(), self.velocity.norm() / dt))
#         lateral_friction.resize(min(lateral_friction.norm(), lateral_velocity.norm() / dt))
#         self.velocity += (backwards_friction + lateral_friction) * dt
#         self.acceleration += (backwards_friction + lateral_friction) * dt

#         self.position += self.velocity * dt
#         # https://gamedev.stackexchange.com/questions/26845/i-am-looking-to-create-realistic-car-movement-using-vectors
#         self.angle = -self.direction.angle(vector(1,0))
#         print(abs(lateral_velocity))
#         car.rect.y = height - self.position[1]
#         car.rect.x = self.position[0]
#         self.image = pygame.transform.rotate(self.original_image, math.degrees(self.angle))
#         self.offset = vector(-15,0).rotate(self.angle)
#         self.offset.arr[1] = -self.offset[1]
#         self.offset = vector(0,0)
#         # print(self.offset)
#         self.rect = self.image.get_rect(center=tuple(vector(self.rect.center)-self.offset))

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



map_dimensions = (width*0.9, height*0.9)
turn_angle = math.radians(25)
car = car_module.Car(max_force = 600, max_wheel_angle = 25, map=map_dimensions)
gas_fsm = init_gas_fsm(car)
turn_fsm = init_turn_fsm(car)
enemy = enemy_car.enemy_car(targets=[(car,1)], max_force = 700, max_wheel_angle = 30, map=map_dimensions)
enemy2 = enemy_car.enemy_car(targets=[(car,1)], max_force = 700, max_wheel_angle = 30, map=map_dimensions)
# enemy.targets.append((enemy2, -0.1))
# enemy2.targets.append((enemy, -0.1))
FPS = 120

# body = rigid_body()
# body.set_force("engine", vector(1,0), vector(0,1))

def draw_car(c, color = (255,0,0)):
    def flip_y(v):
        return vector(v[0], -v[1])
    center = vector(width//2, height//2) + flip_y(c.position)
    pygame.draw.line(screen, color, center - 25*flip_y(c.direction), center + 25*flip_y(c.direction), width=2)
    pygame.draw.line(screen, (0,255,0), center, center + 12.5*flip_y(c.wheel_direction))
    # pygame.draw.line(screen, (0,0,255), center, center + 0.5*flip_y(c.lateral * c.turn_radius))
    pygame.draw.line(screen, (0,0,255), center, center + flip_y(c.target_velocity))

# Game loop
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
    enemy.update(dt)
    enemy2.update(dt)
    if not enemy.alive:
        enemy = enemy_car.enemy_car(targets=[(car,0)], max_force = 700, max_wheel_angle = 30, map=map_dimensions)
    if not enemy2.alive:
        enemy2 = enemy_car.enemy_car(targets=[(car,0)], max_force = 700, max_wheel_angle = 30, map=map_dimensions)
    draw_car(car, color=(255,255,0))
    draw_car(enemy)
    draw_car(enemy2)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)  # Adjust the value to control the speed of the game