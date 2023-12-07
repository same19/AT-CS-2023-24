import pygame
import sys
import math
from vector import vector
from fsm import FSM
import numpy as np
from rigid_body import rigid_body
import car
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

class Car:
    def __init__(self):
        self.original_image = None
        self.original_center = None
        self.image = None
        self.rect = None
        self.velocity = vector(1,0)
        self.position = vector(0,0)
        self.direction = vector(1,0)
        self.new_forward_vector = vector(1,0)
        self.gas_acceleration = 0
        self.acceleration = vector(0,0)
        self.torque = 0
        self.angle = 0
        self.new_wheel_angle = 0
        self.wheel_angle = 0
        self.angular_velocity = 0
        self.drifting = False
        self.offset = vector(0,0)
        self.back = vector(0,0)
        self.front = vector(1,0)
        self.wheel_direction = vector(1,0)
        # torque = sin(self.wheel_angle)

    def turn(self, angle):
        self.new_wheel_angle = -angle
        # if abs(self.wheel_angle + angle) < max_turn_angle:
            # self.wheel_angle += angle
        # self.torque = 50 * math.sin(angle)
    def brake(self):
        self.gas_acceleration = -1000
    def coast(self):
        self.gas_acceleration = 0
    def accelerate(self):
        self.gas_acceleration = 1000
    def update(self, dt):
        # print(self.wheel_angle)
        wheel_turn_speed = math.pi/2 #radians per second
        if self.wheel_angle < self.new_wheel_angle:
            self.wheel_angle = min(self.new_wheel_angle, self.wheel_angle + wheel_turn_speed*dt)
        elif self.wheel_angle > self.new_wheel_angle:
            self.wheel_angle = max(self.new_wheel_angle, self.wheel_angle - wheel_turn_speed*dt)

        self.wheel_direction = self.direction.rotate(self.wheel_angle)
            

        steer_angle = self.wheel_angle * abs(self.velocity) / max_speed
        self.new_forward_vector = self.direction.rotate(steer_angle)
        new_forward_vector = self.new_forward_vector
        amount = 0.1
        if self.drifting:
            amount = 0.3
        self.direction = amount*(new_forward_vector - self.direction) + self.direction
        self.direction.resize(1)
        # self.direction = new_forward_vector


        current_speed = abs(self.velocity)
        # if current_speed < max_speed:
        self.velocity += self.gas_acceleration * self.direction * dt
        self.acceleration = self.gas_acceleration * self.direction * dt

        trigger_lateral_velocity = 7
        lateral_friction_factor = 10
        backwards_friction_factor = 0.005
        right_vector = self.direction.rotate(math.radians(90))
        lateral_velocity = right_vector * right_vector.dot(self.velocity)
        if abs(lateral_velocity) > trigger_lateral_velocity:
            self.drifting = True
            lateral_friction_factor = 0.5
        else:
            self.drifting = False
        lateral_friction = -1*lateral_velocity * abs(lateral_velocity) * lateral_friction_factor
        backwards_friction = -1*self.velocity * abs(self.velocity) * backwards_friction_factor
        backwards_friction.resize(min(backwards_friction.norm(), self.velocity.norm() / dt))
        lateral_friction.resize(min(lateral_friction.norm(), lateral_velocity.norm() / dt))
        self.velocity += (backwards_friction + lateral_friction) * dt
        self.acceleration += (backwards_friction + lateral_friction) * dt

        self.position += self.velocity * dt
        # https://gamedev.stackexchange.com/questions/26845/i-am-looking-to-create-realistic-car-movement-using-vectors
        self.angle = -self.direction.angle(vector(1,0))
        print(abs(lateral_velocity))
        car.rect.y = height - self.position[1]
        car.rect.x = self.position[0]
        self.image = pygame.transform.rotate(self.original_image, math.degrees(self.angle))
        self.offset = vector(-15,0).rotate(self.angle)
        self.offset.arr[1] = -self.offset[1]
        self.offset = vector(0,0)
        # print(self.offset)
        self.rect = self.image.get_rect(center=tuple(vector(self.rect.center)-self.offset))

def init_car_fsm(fsm, car):
    #initialize the finite state machine for a car
    fsm.add_transition("Brake", "Accelerating",car.brake,"Braking")
    fsm.add_transition("Coast", "Accelerating",car.coast,"Coasting")
    # fsm.add_transition("Drift", "Accelerating",car.brake,"Drifting")

    fsm.add_transition("Accelerate", "Braking",car.accelerate,"Accelerating")
    fsm.add_transition("Coast", "Braking",car.coast,"Coasting")

    fsm.add_transition("Accelerate", "Coasting",car.accelerate,"Accelerating")
    fsm.add_transition("Brake", "Coasting",car.brake,"Braking")

# car = Car()
# car_fsm = FSM("Coasting")
# init_car_fsm(car_fsm, car)
# car.image = pygame.image.load("car.png")
# car.image = pygame.transform.scale(car.image, (60, 30))
# car.original_image = car.image
# car.rect = car.image.get_rect()
# car.velocity = vector(0,0)
# car.direction = vector(1,0)
# car.rect.center = (width // 2, height // 2)
# car.original_center = vector(width // 2, height // 2)
# car.position = vector(width // 2, height // 2)
# car.front = (width//2 + 60,height//2)
# car.back = (width//2,height//2)
# power = 10
turn_angle = math.radians(25)
car = car.Car(max_force = 600)
enemy = enemy_car.enemy_car(target=car, max_force = 750, max_wheel_angle = 25)
enemy2 = enemy_car.enemy_car(target=car, max_force = 750, max_wheel_angle = 25)
FPS = 120

# body = rigid_body()
# body.set_force("engine", vector(1,0), vector(0,1))

def draw_car(c, color = (255,0,0)):
    def flip_y(v):
        return vector(v[0], -v[1])
    center = vector(width//2, height//2) + flip_y(c.position)
    pygame.draw.line(screen, color, center, center + 50*flip_y(c.direction), width=2)
    pygame.draw.line(screen, (0,255,0), center, center + 25*flip_y(c.wheel_direction))
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
            if event.key == pygame.K_UP:
                car.accelerate()
            elif event.key == pygame.K_DOWN:
                car.brake()
            elif event.key == pygame.K_RIGHT:
                # Rotate the velocity vector clockwise
                car.turn(turn_angle)
            elif event.key == pygame.K_LEFT:
                # Rotate the velocity vector counterclockwise
                car.turn(-turn_angle)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                car.coast()
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                car.turn(0)
    screen.fill((0,0,0))
    
    car.update(dt)
    enemy.update(dt)
    enemy2.update(dt)
    draw_car(car, color=(255,255,0))
    draw_car(enemy)
    draw_car(enemy2)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)  # Adjust the value to control the speed of the game