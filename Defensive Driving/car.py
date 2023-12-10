from vector import vector
import math

class Car:
    def __init__(self, length=1, max_force=600, max_wheel_angle=25, map=vector(800, 600)):
        # Car parameters
        self.map = map
        self.alive = True
        self.drifting_allowed = True

        # Dimensions
        self.length = length
        self.width = self.length / 5

        # Movement
        self.max_velocity = 1750
        self.max_force = max_force
        self.acceleration = vector(0, 0)
        self.velocity = vector(0, 0)
        self.position = vector(0, 0)
        self.gas_force = 0

        # Steering
        self.max_turn_angle = math.radians(max_wheel_angle)
        self.direction = vector(1, 0)
        self.turn_radius = 0
        self.lateral_velocity = vector(0, 0)
        self.wheel_direction = self.direction
        self.wheel_angle = 0
        self.new_wheel_angle = 0
        self.lateral = vector(0, 0)
        self.lateral_friction = vector(0, 0)
        self.drifting = False
        self.target_velocity = vector(0, 0)
        self.wheel_turn_speed = math.pi * 2 / 3  # radians per second

    def calculate_turn_radius(self):
        # Calculate turn radius based on wheel angle
        if self.wheel_angle == 0:
            self.turn_radius = 0
        else:
            self.turn_radius = self.length / math.radians(self.wheel_angle)
        return self.turn_radius

    def in_bounds(self, v):
        # Check if the car is within the bounds of the map
        return -self.map[0] / 2 <= v[0] <= self.map[0] / 2 and -self.map[1] / 2 <= v[1] <= self.map[1] / 2

    def box(self):
        # Get the corners of the car's bounding box
        corner_list = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        return [self.position + vector(self.length / 2 * i[0], self.width * i[1]).rotate(-self.direction.angle(vector(1, 0))) for i in corner_list]

    def collide_point(self, v):
        # Check if a point collides with the car's bounding box
        prev_index = -1
        box = self.box()
        for index in range(len(box)):
            side_center = (box[index] + box[prev_index]) / 2
            if (side_center - self.position).dot(side_center - v) < 0:
                return False
            prev_index = index
        return True

    def collide_car(self, c):
        # Check if the car collides with another car
        for corner in self.box():
            if c.collide_point(corner):
                return True
        for corner in c.box():
            if self.collide_point(corner):
                return True

        prev_index = -1
        box = self.box()
        points_per_edge = 4
        for index in range(len(box)):
            for point_num in range(points_per_edge):
                point = (point_num * box[index] + (points_per_edge - point_num) * box[prev_index]) / points_per_edge
                if c.collide_point(point):
                    return True
            prev_index = index
        prev_index = -1
        box = c.box()
        for index in range(len(box)):
            for point_num in range(points_per_edge):
                point = (point_num * box[index] + (points_per_edge - point_num) * box[prev_index]) / points_per_edge
                if self.collide_point(point):
                    return True
            prev_index = index
        return False

    def turn(self, angle):
        # Set the new wheel angle based on input
        self.new_wheel_angle = -angle * self.max_turn_angle

    def turn_right(self):
        # Turn the car to the right
        self.turn(1)

    def turn_left(self):
        # Turn the car to the left
        self.turn(-1)

    def turn_center(self):
        # Turn the car to the center
        self.turn(0)

    def brake(self):
        # Apply braking force
        self.gas_force = -self.max_force * 1.5

    def accelerate(self):
        # Apply acceleration force
        self.gas_force = self.max_force

    def coast(self):
        # Set gas force to zero (coast)
        self.gas_force = 0

    def update(self, dt):
        # Update the car's state over time. Mimics realistic physics of a car (imperfectly of course).

        if not self.in_bounds(self.position):
            # If out of bounds, set alive to False
            self.alive = False
        if not self.alive:
            # If not alive, reset velocity and acceleration
            self.velocity = vector(0, 0)
            self.acceleration = vector(0, 0)
            return

        self.max_wheel_angle = self.new_wheel_angle * (1 - (abs(self.velocity) / self.max_velocity) ** 1.5)
        if self.wheel_angle < self.max_wheel_angle:
            # Adjust wheel angle based on turn speed
            self.wheel_angle = min(self.max_wheel_angle, self.wheel_angle + self.wheel_turn_speed * dt)
        elif self.wheel_angle > self.max_wheel_angle:
            self.wheel_angle = max(self.max_wheel_angle, self.wheel_angle - self.wheel_turn_speed * dt)
        self.wheel_direction = self.direction.rotate(self.wheel_angle)

        self.acceleration = vector(0, 0)
        if self.gas_force >= 0 or self.velocity.dot(self.direction) >= 0:
            # Apply gas force in the direction of the car
            self.acceleration += self.direction * self.gas_force

        #Lateral and backwards friction to keep car moving realistically
        trigger_lateral_velocity = 15
        lateral_friction_factor = 5
        backwards_friction_factor = 0.2
        right_vector = self.direction.rotate(math.radians(90))
        self.lateral_velocity = right_vector * right_vector.dot(self.velocity)
        self.lateral_friction = -1 * self.lateral_velocity * abs(self.lateral_velocity) * lateral_friction_factor
        backwards_friction = -1 * self.velocity * abs(self.velocity) * backwards_friction_factor
        backwards_friction.resize(min(backwards_friction.norm(), self.velocity.norm() / dt))
        if abs(self.lateral_velocity) >= trigger_lateral_velocity and (self.drifting or self.gas_force < 0) and self.drifting_allowed:
            # Enable drifting if conditions are met
            self.drifting = True
            self.lateral_friction = -1 * self.lateral_velocity * abs(self.lateral_velocity) * lateral_friction_factor
        else:
            self.drifting = False
            self.lateral_friction = (-1 * self.lateral_velocity).normalize(self.lateral_velocity.norm() / dt / dt)

        self.acceleration += (backwards_friction + self.lateral_friction) * dt

        # Update the car's direction based on wheel angle
        turn_correction_constant = 100
        if self.wheel_angle != 0:
            self.turn_radius = self.length / math.radians(self.wheel_angle)
            theta = turn_correction_constant * math.radians(self.wheel_angle) * abs(self.velocity) * dt / self.length
            self.direction = self.direction.rotate(theta)

        #Update velocity and position based on acceleration
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt