from car import Car
import math
import random
from vector import vector
class enemy_car(Car):
    #Only chase for now
    def __init__(self, targets = [], length=1, max_force = 800, max_wheel_angle = 30, map = vector(800,600)):
        super().__init__(length=length, max_wheel_angle = max_wheel_angle, map=map)
        self.targets = targets
        # self.max_velocity = 1000
        self.max_gas_force = max_force
        self.wheel_turn_speed = math.pi/2
        self.drifting_allowed = False
        self.wall_margin = self.length/2
        self.max_velocity = 1750
    def update(self, dt):
        random_coefficient = 1+0.3*(random.random()-0.5)

        #AI Part: steering the enemy cars

        def wall_factor(vel):
            return 1*10**4 * vel
        self.to_edge = vector(0,0)
        # self.position = vector(6,0)
        x_dist = abs(abs(self.position[0]) - self.map[0]/2)
        y_dist = abs(abs(self.position[1]) - self.map[1]/2)
        if x_dist < y_dist:
            if self.position[0] > 0:
                self.to_edge = vector(self.map[0]/2-self.position[0] - self.wall_margin, 0)
            else:
                self.to_edge = vector(-self.map[0]/2-self.position[0] + self.wall_margin, 0)
        else:# y_dist <= x_dist:
            if self.position[1] > 0:
                self.to_edge = vector(0, self.map[1]/2-self.position[1] - self.wall_margin)
            else:
                self.to_edge = vector(0, -self.map[1]/2-self.position[1] + self.wall_margin)
        target_velocity_from_wall_avoid = vector(0,0)
        if abs(self.to_edge) != 0:
            target_velocity_from_wall_avoid = -1 * self.to_edge / (abs(self.to_edge)**2)

        target_velocity_from_target_chase = vector(0,0)
        for (target, factor) in self.targets:
            def chase_factor(vel):
                if abs(target.position - self.position) != 0:
                    return factor * 5 * 10**4 * vel / (abs(target.position - self.position))**2
                else:
                    return vector(0,0)
            target_velocity_movement = vector(0,0)
            if abs(self.velocity) != 0:
                target_velocity_factor = 0.25
                #calculate where the target will theoretically be when reached
                target_velocity_movement = target_velocity_factor * target.velocity * (abs(target.position-self.position)/abs(self.velocity))
            target_velocity_from_target_chase += chase_factor(target_velocity_movement + target.position - self.position)
        
        
        self.target_velocity = target_velocity_from_target_chase + wall_factor(target_velocity_from_wall_avoid)

        #sin of the angle between current velocity and desired velocity - 0 when on the right path, 1 when not
        sin_theta = self.velocity.sin(self.target_velocity)
        #cos of that angle
        cos_theta = self.velocity.cos(self.target_velocity)

        if cos_theta > 0:
            #target is in front
            #turn at an angle proportional to the square of sin_theta
            self.turn(-1 * sin_theta * random_coefficient)
        elif cos_theta <= 0 and sin_theta != 0:
            #target is behind
            self.turn(-1 * sin_theta/abs(sin_theta) * random_coefficient)
        else:
            #target is directly behind
            self.turn(1 * random_coefficient)


        #set gas_force based on how much turning
        # wall_avoid_power_constant = 0 #0.1 * abs(wall_avoid_vector) #higher when closer to the wall
        # wall_avoid_power = 1-((wall_avoid_power_constant)/(wall_avoid_power_constant+1))**2
        # toward_car_power = 1#cos_theta if cos_theta > 0 else 0.2
        # percent_gas = 1-(1 - toward_car_power * random_coefficient * wall_avoid_power)**2
        # self.gas_force = -0.5*self.max_gas_force + 1.5*self.max_gas_force*percent_gas
        print(self.direction.dot(self.target_velocity), abs(self.velocity))
        power_constant = 5000
        velocity_constant = 4*10**10
        # power_scaled_vel = 2 + self.direction.dot(self.target_velocity) / (abs(self.velocity)/velocity_constant if abs(self.velocity) != 0 else 0.0001)**1 * power_constant
        power_scaled_vel = power_constant * (self.direction.dot(self.target_velocity) + 1/(abs(self.velocity)+0.01)**3 *velocity_constant)
        percent_gas_force = power_scaled_vel/(abs(power_scaled_vel)+1)
        self.gas_force = -0.5 * self.max_gas_force + 1.5 * self.max_gas_force * percent_gas_force
        super().update(dt)