from car import Car
import math
import random
from vector import vector
class enemy_car(Car):
    #Only chase for now
    def __init__(self, target : Car, length=1, max_force = 1000, max_wheel_angle = 20, map = vector(760,560)):
        super().__init__(length=length, map=map)
        self.target = target
        self.max_turn_angle = math.radians(max_wheel_angle)
        self.max_velocity = 10000
        self.max_gas_force = max_force
        self.wheel_turn_speed = math.pi/2
    def turn(self, angle):
        self.new_wheel_angle = -angle
    def update(self, dt):
        random_coefficient = 1+2*(random.random()-0.5)
        #AI Part: steering the enemy cars
        if abs(self.velocity) == 0:
            self.target_position = self.target.position
        else:
            self.target_position = self.target.position + self.target.velocity * (abs(self.target.position-self.position)/abs(self.velocity)) #calculate where the target will theoretically be when reached

        wall_aversion = 2000
        self.to_edge = vector(0,0)
        # self.position = vector(6,0)
        x_dist = abs(abs(self.position[0]) - self.map[0]/2)
        y_dist = abs(abs(self.position[1]) - self.map[1]/2)
        if x_dist < y_dist:
            if self.position[0] > 0:
                self.to_edge = vector(self.map[0]/2-self.position[0], 0)
            else:
                self.to_edge = vector(-self.map[0]/2-self.position[0], 0)
        else:# y_dist <= abs(self.calculate_turn_radius()):
            if self.position[1] > 0:
                self.to_edge = vector(0, self.map[1]/2-self.position[1])
            else:
                self.to_edge = vector(0, -self.map[1]/2-self.position[1])
        wall_avoid_vector = vector(0,0)
        if abs(self.to_edge) != 0:
            wall_avoid_vector = -1 * self.to_edge * wall_aversion / (abs(self.to_edge)**2)
            self.target_position += wall_avoid_vector

        self.target_velocity = self.target_position - self.position
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
        wall_avoid_power_constant = 0 #0.1 * abs(wall_avoid_vector) #higher when closer to the wall
        wall_avoid_power = 1-((wall_avoid_power_constant)/(wall_avoid_power_constant+1))**2
        percent_gas = 1-(1 - (cos_theta if cos_theta > 0 else 0.2) * random_coefficient * wall_avoid_power)**4
        self.gas_force = -0.5*self.max_gas_force + 1.5*self.max_gas_force*percent_gas# * (1-abs(self.velocity)/self.max_velocity)

        super().update(dt)