from collections.abc import Sequence
import math
class vector(Sequence):
    def __init__(self, *arr):
        if len(arr) > 1:
            self.arr = list(arr)
        else:
            self.arr = list(arr[0])
    def __eq__(self, other):
        if len(other) != len(self):
            return False
        for i in self.arr:
            if self.arr[i] != other[i]:
                return False
        return True
    def __tuple__(self):
        return tuple(self.arr)
    def __add__(self, other):
        new = vector(self.arr)
        for i in range(len(new.arr)):
            new.arr[i] += other[i]
        return new
    def __mul__(self, k : float):
        new = vector(self.arr)
        for i in range(len(new.arr)):
            new.arr[i] *= k
        return new
    def __radd__(self, other):
        return self + other
    def __rmul__(self, k : float):
        return self*k
    def __sub__(self, other):
        return self + (-1)*other
    def __truediv__(self, k : float):
        if k == 0:
            return None
        return self * (1.0/k)
    def __rsub__(self, other):
        return (-1)*self + other
    def __getitem__(self, i):
        return self.arr[i]
    def __len__(self):
        return len(self.arr)
    def __repr__(self):
        return "vec<"+str(self.arr)+">"
    def magnitudeSquared(self):
        s = 0
        for i in self.arr:
            s += i**2
        return s
    def magnitude(self):
        return self.magnitudeSquared()**0.5
    def norm(self):
        return self.magnitude()
    def __abs__(self):
        return self.magnitude()
    def normalize(self, l = 1):
        m = self.magnitude()
        if m == 0:
            return self
        else:
            return self * l / m
    def resize(self, l):
        n = self.norm()
        if n == 0:
            return
        for i in range(len(self.arr)):
            self.arr[i] *= l / n
    def dot(self, other):
        s = 0
        for i in range(len(self)):
            s += self[i] * other[i]
        return s
    def cross(self, other):
        return self[0]*other[1] - self[1] * other[0]
    def sin(self, other):
        c = self.cross(other)
        if c == 0:
            return 0
        else:
            return c / abs(self) / abs(other)
    def cos(self, other):
        d = self.dot(other)
        if d == 0:
            return 0
        else:
            return d / abs(self) / abs(other)
    def angle(self, other):
        s = self.sin(other)
        a = math.acos(self.cos(other))
        if s < 0:
            a = 2*math.pi - a
        return a
    def rotate(self, angle):
        n = vector(
            self[0] * math.cos(angle) - self[1] * math.sin(angle),
            self[0] * math.sin(angle) + self[1] * math.cos(angle)
        )
        return n