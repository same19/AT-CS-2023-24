from car import Car
import math
import random
from vector import vector
import time
WALL_CONSTANT = 1 * 10**4
CHASE_CONSTANT = 1 * 10**6
class enemy_car(Car):
    #Only chase for now
    def __init__(self, target = (), length=1, max_force = 800, max_wheel_angle = 30, map = vector(800,600)):
        super().__init__(length=length, max_wheel_angle = max_wheel_angle, map=map)
        self.target = target
        self.max_gas_force = max_force
        self.wheel_turn_speed = math.pi/2
        self.drifting_allowed = False
        self.wall_margin = self.length/2
        self.max_velocity = 1250
        self.chasing = True
        self.avg_state_time = 10000 #millis
        self.next_time_change_state = time.time_ns() + self.avg_state_time * 1000000
    def set_target(self, target):
        self.target = (target, self.target[1])
    def chase(self):
        factor = 1
        self.chasing = True
        self.target = (self.target[0], factor)
        self.next_time_change_state = time.time_ns() + 1000000*(0.75 * self.avg_state_time + 0.5 * self.avg_state_time * random.random())
        # print("CHANGING STATE", self.target, time.time_ns()-self.next_time_change_state)
    def avoid(self):
        factor = -0.05
        self.chasing = False
        self.target = (self.target[0], factor)
        self.next_time_change_state = time.time_ns() + 1000000*(0.75 * self.avg_state_time + 0.5 * self.avg_state_time * random.random())
        # print("CHANGING STATE", self.target, self.next_time_change_state-time.time_ns())
    def update(self, dt):
        random_coefficient = 0.8+0.5*(random.random()-0.5)

        #AI Part: steering the enemy cars

        self.to_edge = vector(0,0)
        # self.position = vector(6,0)
        x_dist = abs(abs(self.position[0]) - self.map[0]/2)
        y_dist = abs(abs(self.position[1]) - self.map[1]/2)
        target_velocity_from_wall_avoid = vector(0,0)
        def generate_wall_force(to_edge):
            return WALL_CONSTANT * -1 * to_edge * (1/(abs(to_edge)**1.5) + 1/(abs(to_edge)**3) + 1/(abs(to_edge)**5))
        
        # generate forces for each wall based on how far from that wall
        self.wall_margin = 0
        # if self.position[0] > 0:
        to_edge = vector(self.map[0]/2-self.position[0] - self.wall_margin, 0)
        if abs(to_edge) != 0:
            target_velocity_from_wall_avoid += generate_wall_force(to_edge)
        # else:
        to_edge = vector(-self.map[0]/2-self.position[0] + self.wall_margin, 0)
        if abs(to_edge) != 0:
            target_velocity_from_wall_avoid += generate_wall_force(to_edge)
        # if self.position[1] > 0:
        to_edge = vector(0, self.map[1]/2-self.position[1] - self.wall_margin)
        if abs(to_edge) != 0:
            target_velocity_from_wall_avoid += generate_wall_force(to_edge)
        # else:
        to_edge = vector(0, -self.map[1]/2-self.position[1] + self.wall_margin)
        if abs(to_edge) != 0:
            target_velocity_from_wall_avoid += generate_wall_force(to_edge)
        

        target_velocity_from_target_chase = vector(0,0)
        target, factor = self.target[0], self.target[1]
        def chase_factor(vel):
            if abs(target.position - self.position) != 0:
                return factor * CHASE_CONSTANT * vel * (1 / abs(target.position - self.position)**2 + 1/abs(target.position - self.position)**3)
            else:
                return vector(0,0)
        target_velocity_movement = vector(0,0)
        target_acceleration_movement = vector(0,0)
        target_velocity_factor = 1
        if abs(self.velocity) != 0:
            target_velocity_factor = 0.25
            target_acceleration_factor = 0
            #calculate where the target will theoretically be when reached
            time = abs(target.position-self.position)/abs(self.velocity)
            target_velocity_movement = target_velocity_factor * target.velocity * time
            target_acceleration_movement = target_acceleration_factor * 0.5 * target.acceleration * abs(target.acceleration) * time

        #if this enemy cannot possibly reach its target with its max_turn_radius, then don't try
        perpendicular_chase_constant = 1
        if factor > 0 and abs(self.velocity) > 0:
            target_pos = target.position# + target.velocity * abs(target.position-self.position)/abs(self.velocity) - self.position
            for corner in target.box():
                if abs(corner-self.position) > abs(target_pos-self.position):
                    target_pos = corner
            max_turn_radius = self.length / self.max_turn_angle
            self.turn_center_pos = max_turn_radius*self.direction.rotate(math.radians(90 if (target_pos-self.position).sin(self.direction)<0 else -90))
            if abs(target_pos-(self.turn_center_pos + self.position)) < 1*max_turn_radius:
                perpendicular_chase_constant = -0.05
                # print("IN TURN RADIUS", self.position)

        target_velocity_from_target_chase += perpendicular_chase_constant * chase_factor(target_velocity_movement + target_acceleration_movement + target.position - self.position)
        
        #set actual target velocity
        self.target_velocity = target_velocity_from_wall_avoid + target_velocity_from_target_chase

        #sin of the angle between current velocity and desired velocity - 0 when on the right path, 1 when not
        sin_theta = self.velocity.sin(self.target_velocity)
        #cos of that angle
        cos_theta = self.velocity.cos(self.target_velocity)

        if cos_theta > 0:
            #target is in front
            #turn at an angle proportional to sin_theta
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
        # print(self.direction.dot(self.target_velocity), abs(self.velocity))

        power_constant = 0.001
        # power_scaled_vel = 2 + self.direction.dot(self.target_velocity) / (abs(self.velocity)/velocity_constant if abs(self.velocity) != 0 else 0.0001)**1 * power_constant
        power_scaled_vel = power_constant * self.direction.dot(self.target_velocity)
        if power_scaled_vel > 10:
            percent_velocity = 1
        elif power_scaled_vel < -10:
            percent_velocity = 0
        else:
            percent_velocity = math.exp(power_scaled_vel)/(math.exp(power_scaled_vel)+1)
        new_velocity = (300 + 700 * percent_velocity) - abs(self.velocity)

        self.gas_force = self.max_gas_force * (new_velocity/abs(new_velocity) if new_velocity != 0 else 0)
        # print(percent_velocity, new_velocity + abs(self.velocity), self.gas_force)
        super().update(dt)