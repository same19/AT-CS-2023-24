from vector import vector
class rigid_body:
    def __init__(self, mass=1, radius=50):
        self.mass = mass
        self.radius = radius
        self.moment = mass * (radius**2) #moment of inertia
        self.acceleration = vector(0,0)
        self.velocity = vector(0,0)
        self.position = vector(0,0)
        self.angular_acceleration = 0
        self.angular_speed = 0
        self.direction = vector(1,0)
        self.forces = {}
    def clear_forces(self):
        self.forces = {}
    def set_force(self, name, position, force): #position is relative to center of the object
        self.forces[name] = (position, force)
    def remove_force(self, name):
        if name in self.forces:
            del self.forces[name]
    def update(self, dt):
        self.angular_acceleration = 0
        self.acceleration = vector(0,0)
        for f in self.forces.values():
            position = f[0]
            force = f[1]
            self.angular_acceleration += force.cross(position) / self.moment
            self.acceleration += force / self.mass

        self.angular_speed += self.angular_acceleration * dt
        self.direction = self.direction.rotate(self.angular_speed * dt).normalize()
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt