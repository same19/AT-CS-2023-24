from collections.abc import Sequence
import math

# I created my own vector class so that I could efficiently apply linear algebra techniques and manipulations. Adding, subtracting, and multiplying pairs is not easy; this vector class makes basic operations simple by overloading several magic methods. I know there are already libraries with linear algebra, but implementing this class was not very difficult, and I didn't have to look through a ton of documentation.

class vector(Sequence):
    def __init__(self, *arr):
        # Constructor for the vector class
        if len(arr) > 1:
            self.arr = list(arr)
        else:
            self.arr = list(arr[0])

    def __eq__(self, other):
        # Check if two vectors are equal
        if len(other) != len(self):
            return False
        for i in self.arr:
            if self.arr[i] != other[i]:
                return False
        return True

    def __tuple__(self):
        # Convert the vector to a tuple
        return tuple(self.arr)

    def __add__(self, other):
        # Add two vectors element-wise
        new = vector(self.arr)
        for i in range(len(new.arr)):
            new.arr[i] += other[i]
        return new

    def __mul__(self, k: float):
        # Multiply the vector by a scalar
        new = vector(self.arr)
        for i in range(len(new.arr)):
            new.arr[i] *= k
        return new

    def __radd__(self, other):
        # Reverse add, allows adding a scalar to a vector
        return self + other

    def __rmul__(self, k: float):
        # Reverse multiply, allows multiplying a vector by a scalar
        return self * k

    def __sub__(self, other):
        # Subtract two vectors element-wise
        return self + (-1) * other

    def __truediv__(self, k: float):
        # Divide the vector by a scalar
        if k == 0:
            return None
        return self * (1.0 / k)

    def __rsub__(self, other):
        # Reverse subtract, allows subtracting a vector from a scalar
        return (-1) * self + other

    def __getitem__(self, i):
        # Get the i-th element of the vector
        return self.arr[i]

    def __len__(self):
        # Get the length of the vector
        return len(self.arr)

    def __repr__(self):
        # String representation of the vector
        return "vec<" + str(self.arr) + ">"

    def magnitudeSquared(self):
        # Compute the squared magnitude of the vector
        s = 0
        for i in self.arr:
            s += i ** 2
        return s

    def magnitude(self):
        # Compute the magnitude of the vector
        return self.magnitudeSquared() ** 0.5

    def norm(self):
        # Synonym for magnitude
        return self.magnitude()

    def __abs__(self):
        # Synonym for magnitude
        return self.magnitude()

    def normalize(self, l=1):
        # Returns a new vector normalized to a given length.
        m = self.magnitude()
        if m == 0:
            return self
        else:
            return self * l / m

    def resize(self, l):
        # Resize the vector to a given length. Like normalize but actually changes this vector.
        n = self.norm()
        if n == 0:
            return
        for i in range(len(self.arr)):
            self.arr[i] *= l / n

    def dot(self, other):
        # Compute the dot product of two vectors:
        # = |a|*|b|*cos(theta)
        s = 0
        for i in range(len(self)):
            s += self[i] * other[i]
        return s

    def cross(self, other):
        # Compute the cross product of two vectors (for 2D vectors). Basically, this is the magnitude of the 3D cross product:
        # = |a|*|b|*sin(theta)
        return self[0] * other[1] - self[1] * other[0]

    def sin(self, other):
        # Compute the sine of the angle between two vectors
        c = self.cross(other)
        if c == 0:
            return 0
        else:
            return c / abs(self) / abs(other)

    def cos(self, other):
        # Compute the cosine of the angle between two vectors
        d = self.dot(other)
        if d == 0:
            return 0
        else:
            return d / abs(self) / abs(other)

    def angle(self, other):
        # Compute the angle between two vectors
        s = self.sin(other)
        a = math.acos(self.cos(other))
        if s < 0:
            a = 2 * math.pi - a
        return a

    def rotate(self, angle):
        # Rotate the vector by a given angle
        n = vector(
            self[0] * math.cos(angle) - self[1] * math.sin(angle),
            self[0] * math.sin(angle) + self[1] * math.cos(angle)
        )
        return n