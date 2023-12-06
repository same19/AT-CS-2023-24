from car import Car
import math
import random
class enemy_car(Car):
    #Only chase for now
    def __init__(self, target : Car, length=1, max_force = 1000):
        super().__init__(length=length)
        self.target = target
        self.max_turn_angle = math.radians(20)
        self.max_velocity = 10**10
        self.max_gas_force = max_force
    def turn(self, angle):
        self.new_wheel_angle = -angle
    def update(self, dt):
        random_coefficient = 1+0.8*(random.random()-0.5)
        #AI Part: steering the enemy cars
        if abs(self.velocity) == 0:
            target_position = self.target.position
        else:
            target_position = self.target.position + self.target.velocity * (abs(self.target.position-self.position)/abs(self.velocity)) #calculate where the target will theoretically be when reached
        self.target_velocity = target_position - self.position
        sin_theta = self.velocity.sin(self.target_velocity) #sin of the angle between current velocity and desired velocity - 0 when on the right path, 1 when not
        cos_theta = self.velocity.cos(self.target_velocity) #cos of that angle

        if cos_theta > 0:
            #target is in front
            #turn at an angle proportional to the square of sin_theta
            self.turn(-self.max_turn_angle * sin_theta * random_coefficient)
        elif cos_theta <= 0 and sin_theta != 0:
            #target is behind
            self.turn(-self.max_turn_angle * sin_theta/abs(sin_theta) * random_coefficient)
        else:
            #target is directly behind
            self.turn(self.max_turn_angle * random_coefficient)

        #set gas_force based on how much turning
        percent_gas = (cos_theta if cos_theta > 0 else 0.2) * random_coefficient
        self.gas_force = 0 + self.max_gas_force*percent_gas

        super().update(dt)