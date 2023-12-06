from rigid_body import rigid_body
from vector import vector
import math
# brake_force = 500
# gas_force = 500
class Car(rigid_body):
    def __init__(self):
        super().__init__()
        self.wheel_direction = self.direction
        self.wheel_angle = 0
        self.new_wheel_angle = 0
        self.gas_force = 0
        self.lateral_vel = vector(0,0)
        self.lateral = vector(0,0)
        self.turn_radius = 0
    
    def front(self):
        return self.radius * self.direction
    def back(self):
        return -1 * self.radius * self.direction
    
    def turn(self, angle):
        self.new_wheel_angle = -angle * (1-(abs(self.velocity)/self.max_velocity)**2)   
    def brake(self):
        self.gas_force = -300
    def accelerate(self):
        self.gas_force = 300
    def coast(self):
        self.gas_force = 0

    def update(self, dt):
        self.clear_forces()
        self.acceleration = vector(0,0)
        wheel_turn_speed = math.pi/2 #radians per second
        if self.wheel_angle < self.new_wheel_angle:
            self.wheel_angle = min(self.new_wheel_angle, self.wheel_angle + wheel_turn_speed*dt)
        elif self.wheel_angle > self.new_wheel_angle:
            self.wheel_angle = max(self.new_wheel_angle, self.wheel_angle - wheel_turn_speed*dt)
        self.wheel_direction = self.direction.rotate(self.wheel_angle)

        max_speed = 1000
        steer_angle = self.wheel_angle * abs(self.velocity) / max_speed
        self.new_forward_vector = self.direction.rotate(steer_angle)
        new_forward_vector = self.new_forward_vector
        amount = 0.1
        # if self.drifting:
        #     amount = 0.3
        self.direction = amount*(new_forward_vector - self.direction) + self.direction
        self.direction.resize(1)

        self.acceleration += self.direction * self.gas_force
        lateral_angle = -90 if self.wheel_angle < 0 else 90
        self.lateral = self.direction.rotate(math.radians(lateral_angle))
        if self.wheel_angle != 0:
            self.turn_radius = 2 * self.radius / self.wheel_angle
            centripetal_acc = self.lateral * (abs(self.velocity)**2)/self.turn_radius
            self.acceleration += centripetal_acc
        else:
            self.turn_radius = 0

        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

    