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
    
    def front(self):
        return self.radius * self.direction
    def back(self):
        return -1 * self.radius * self.direction
    
    def turn(self, angle):
        self.new_wheel_angle = angle
        
    def brake(self):
        self.gas_force = -50
    def accelerate(self):
        self.gas_force = 50
    def coast(self):
        self.gas_force = 0

    def update(self, dt):
        self.clear_forces()
        wheel_turn_speed = math.pi/2 #radians per second
        if self.wheel_angle < self.new_wheel_angle:
            self.wheel_angle = min(self.new_wheel_angle, self.wheel_angle + wheel_turn_speed*dt)
        elif self.wheel_angle > self.new_wheel_angle:
            self.wheel_angle = max(self.new_wheel_angle, self.wheel_angle - wheel_turn_speed*dt)
        self.wheel_direction = self.direction.rotate(self.wheel_angle)

        self.set_force("front", self.front(), self.direction * self.gas_force)
        # self.set_force("back", self.front(), self.direction * self.gas_force)

        #turning force
        lateral = self.velocity.rotate(math.radians(-90)).normalize()
        if self.wheel_angle == 0:
            centripetal_force = vector(0,0)
        else:
            turn_radius = 2*self.radius/self.wheel_angle
            centripetal_force = self.mass * (abs(self.velocity)**2) / turn_radius * lateral
            print(abs(self.velocity), turn_radius, abs(centripetal_force))
        self.set_force("turn", self.position, centripetal_force)
        
        #lateral force
        lateral = self.wheel_direction.rotate(math.radians(-90)).normalize()
        lateral_vel = self.velocity.cos(lateral) * lateral.normalize() * abs(self.velocity)
        k = 0.1
        lateral_force = -1 * lateral_vel * abs(lateral_vel) * self.mass * k
        self.set_force("lat", self.position, lateral_force)

       

        super().update(dt)

    