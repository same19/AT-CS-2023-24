from vector import vector
import math
# brake_force = 500
# gas_force = 500
class Car:
    def __init__(self, length=1):
        self.length = length
        # self.moment = mass * (half_length**2) #moment of inertia
        self.acceleration = vector(0,0)
        self.velocity = vector(0,0)
        self.position = vector(0,0)
        # self.angular_acceleration = 0
        # self.angular_speed = 0
        self.direction = vector(1,0)
        self.turn_radius = 0
        self.lateral_velocity = vector(0,0)
        self.gas_force = 0
        self.wheel_direction = self.direction
        self.wheel_angle = 0
        self.new_wheel_angle = 0
        self.lateral = vector(0,0)
        self.lateral_friction = vector(0,0)
        self.max_velocity = 1000
        self.drifting = False
        self.target_velocity = vector(0,0)

    def turn(self, angle):
        self.new_wheel_angle = -angle   
    def brake(self):
        self.gas_force = -1200
    def accelerate(self):
        self.gas_force = 600
    def coast(self):
        self.gas_force = 0
    
    def update(self, dt):
        print(self.velocity)
        wheel_turn_speed = math.pi/3 #radians per second
        self.max_wheel_angle = self.new_wheel_angle * (1-(abs(self.velocity)/self.max_velocity)**1.5)
        if self.wheel_angle < self.max_wheel_angle:
            self.wheel_angle = min(self.max_wheel_angle, self.wheel_angle + wheel_turn_speed*dt)
        elif self.wheel_angle > self.max_wheel_angle:
            self.wheel_angle = max(self.max_wheel_angle, self.wheel_angle - wheel_turn_speed*dt)
        self.wheel_direction = self.direction.rotate(self.wheel_angle)


        self.acceleration = vector(0,0)
        if self.gas_force >= 0 or self.velocity.dot(self.direction) >= 0:
            self.acceleration += self.direction * self.gas_force


        #Add lateral acceleration to damp lateral velocity
        
        trigger_lateral_velocity = 7
        lateral_friction_factor = 100
        backwards_friction_factor = 0.1
        right_vector = self.direction.rotate(math.radians(90))
        self.lateral_velocity = right_vector * right_vector.dot(self.velocity)
        self.lateral_friction = -1*self.lateral_velocity * abs(self.lateral_velocity) * lateral_friction_factor
        backwards_friction = -1*self.velocity * abs(self.velocity) * backwards_friction_factor
        backwards_friction.resize(min(backwards_friction.norm(), self.velocity.norm() / dt))
        if abs(self.lateral_velocity) > trigger_lateral_velocity:
            self.drifting = True
            self.lateral_friction = (-1 * self.lateral_velocity).normalize(self.lateral_velocity.norm() / dt/dt)
        else:
            self.drifting = False
            self.lateral_friction = -1*self.lateral_velocity * abs(self.lateral_velocity) * lateral_friction_factor

        self.acceleration += (backwards_friction + self.lateral_friction) * dt


        lateral_angle = -90 if self.wheel_angle < 0 else 90
        self.lateral = self.direction.rotate(math.radians(lateral_angle))

        turn_correction_constant = 2

        if self.wheel_angle != 0:
            self.turn_radius = self.length / math.radians(self.wheel_angle) # in radians
            
            theta = turn_correction_constant * math.radians(self.wheel_angle) * abs(self.velocity) * dt / self.length
            self.direction = self.direction.rotate(theta)

        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

