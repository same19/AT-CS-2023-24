from car import Car
import math
import random
from vector import vector
import time

WALL_CONSTANT = 1 * 10**4
CHASE_CONSTANT = 1 * 10**6

class enemy_car(Car):
    # Enemy Car class that extends the Car class. Drives just like a car but with no drifting allowed. It is also controlled by an AI instead of the user.

    def __init__(self, target=(), length=1, max_force=800, max_wheel_angle=30, map=vector(800, 600)):
        # Constructor for the enemy car.

        # Parameters:
        #     target (tuple): Target position and factor.
        #     length (float): Length of the car.
        #     max_force (float): Maximum force applied by the car.
        #     max_wheel_angle (float): Maximum wheel angle for steering.
        #     map (vector): Size of the map.

        super().__init__(length=length, max_wheel_angle=max_wheel_angle, map=map)

        # AI Parameters: target to chase/avoid and margin to avoid the wall
        self.target = target
        self.wall_margin = self.length / 2

        # Movement
        self.max_gas_force = max_force
        self.wheel_turn_speed = math.pi / 2
        self.drifting_allowed = True
        self.lateral_friction_factor = 15
        self.max_velocity = 1250

        # Enemy chasing/avoiding state
        self.chasing = True
        self.avg_state_time = 10000  # millis
        self.next_time_change_state = time.time_ns() + self.avg_state_time * 1000000

    def set_target(self, target):
        # Set the target for the enemy car.

        # Parameters:
        #     target (tuple): Target position and factor.
        self.target = (target, self.target[1])

    def chase(self):
        # Set the enemy car to chase mode.
        factor = 1
        self.chasing = True
        self.target = (self.target[0], factor)
        self.next_time_change_state = time.time_ns() + 1000000 * (
            0.75 * self.avg_state_time + 0.5 * self.avg_state_time * random.random()
        )

    def avoid(self):
        # Set the enemy car to avoid mode.
        factor = -0.05
        self.chasing = False
        self.target = (self.target[0], factor)
        self.next_time_change_state = time.time_ns() + 1000000 * (
            0.75 * self.avg_state_time + 0.5 * self.avg_state_time * random.random()
        )

    def update(self, dt):
        # Update the enemy car's state
        # AI Part: steering the enemy cars

        # Parameters:
        #     dt (float): Time elapsed since the last update.
        random_coefficient = 0.8 + 0.5 * (random.random() - 0.5)

        # Generate forces for avoiding walls
        target_velocity_from_wall_avoid = vector(0, 0)

        def generate_wall_force(to_edge):
            return WALL_CONSTANT * -1 * to_edge * (
                1 / (abs(to_edge) ** 1.5) + 1 / (abs(to_edge) ** 3) + 1 / (abs(to_edge) ** 5)
            )

        self.wall_margin = 0

        # Generate forces for each wall based on how far from that wall
        to_edge = vector(self.map[0] / 2 - self.position[0] - self.wall_margin, 0)
        if abs(to_edge) != 0:
            target_velocity_from_wall_avoid += generate_wall_force(to_edge)

        to_edge = vector(-self.map[0] / 2 - self.position[0] + self.wall_margin, 0)
        if abs(to_edge) != 0:
            target_velocity_from_wall_avoid += generate_wall_force(to_edge)

        to_edge = vector(0, self.map[1] / 2 - self.position[1] - self.wall_margin)
        if abs(to_edge) != 0:
            target_velocity_from_wall_avoid += generate_wall_force(to_edge)

        to_edge = vector(0, -self.map[1] / 2 - self.position[1] + self.wall_margin)
        if abs(to_edge) != 0:
            target_velocity_from_wall_avoid += generate_wall_force(to_edge)

        # Generate forces for car chasing or avoiding
        target_velocity_from_target_chase = vector(0, 0)

        target, factor = self.target[0], self.target[1]

        # Function to calculate chase factor based on velocity
        def chase_factor(vel):
            if abs(target.position - self.position) != 0:
                return factor * CHASE_CONSTANT * vel * (
                    1 / abs(target.position - self.position) ** 2
                    + 1 / abs(target.position - self.position) ** 3
                )
            else:
                return vector(0, 0)

        target_velocity_movement = vector(0, 0)
        target_acceleration_movement = vector(0, 0)
        target_velocity_factor = 1

        if abs(self.velocity) != 0:
            target_velocity_factor = 0.25
            target_acceleration_factor = 0

            # Calculate where the target will theoretically be when reached
            time = abs(target.position - self.position) / abs(self.velocity)
            target_velocity_movement = target_velocity_factor * target.velocity * time
            target_acceleration_movement = (
                target_acceleration_factor
                * 0.5
                * target.acceleration
                * abs(target.acceleration)
                * time
            )

        # If this enemy cannot possibly reach its target with its max_turn_radius, then don't try
        # The following section prevents the enemy from going in circles directly around the car it is chasing.
        perpendicular_chase_constant = 1

        if factor > 0 and abs(self.velocity) > 0:
            target_pos = target.position

            # Find the maximum turn radius
            for corner in target.box():
                if abs(corner - self.position) > abs(target_pos - self.position):
                    target_pos = corner

            max_turn_radius = self.length / self.max_turn_angle
            turn_center_pos = max_turn_radius * self.direction.rotate(
                math.radians(90 if (target_pos - self.position).sin(self.direction) < 0 else -90)
            )

            if abs(target_pos - (turn_center_pos + self.position)) < 1 * max_turn_radius:
                perpendicular_chase_constant = -0.05

        # Get direction this enemy should go from only car chase/avoid forces
        target_velocity_from_target_chase += perpendicular_chase_constant * chase_factor(
            target_velocity_movement + target_acceleration_movement + target.position - self.position
        )

        # Set overall target velocity: combination of wall and car chase forces
        self.target_velocity = target_velocity_from_wall_avoid + target_velocity_from_target_chase

        # Sin of the angle between current velocity and desired velocity - 0 when on the right path, 1 when not
        sin_theta = self.velocity.sin(self.target_velocity)
        # Cos of that angle
        cos_theta = self.velocity.cos(self.target_velocity)

        if cos_theta > 0:
            # Target is in front
            # Turn at an angle proportional to sin_theta
            self.turn(-1 * sin_theta * random_coefficient)
        elif cos_theta <= 0 and sin_theta != 0:
            # Target is behind
            self.turn(-1 * sin_theta / abs(sin_theta) * random_coefficient)
        else:
            # Target is directly behind: cos_theta <= 0, sin_theta = 0.
            self.turn(1 * random_coefficient)

        # Set gas_force based on how much turning is needed
        power_constant = 0.001
        power_scaled_vel = power_constant * self.direction.dot(self.target_velocity)

        if power_scaled_vel > 10:
            percent_velocity = 1
        elif power_scaled_vel < -10:
            percent_velocity = 0
        else:
            percent_velocity = math.exp(power_scaled_vel) / (math.exp(power_scaled_vel) + 1)

        new_velocity = (300 + 700 * percent_velocity) - abs(self.velocity)
        self.gas_force = self.max_gas_force * (new_velocity / abs(new_velocity) if new_velocity != 0 else 0)

        #Use the normal car physics to update the enemy_car's motion.
        super().update(dt)