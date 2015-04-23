import random

class Vector3:
    @staticmethod
    def random():
        return Vector3(random.random(), random.random(), random.random())

    def __init__(self, pt1, pt2, pt3):
        self.coords = [pt1, pt2, pt3]

    def __sub__(self, other):
        tmp = Vector3(self.coords[0], self.coords[1], self.coords[2])
        if isinstance(other, int) or isinstance(other, float):
            for i in range(3):
                tmp.coords[i] -= other
        elif isinstance(other, type(self)):
            for i in range(3):
                tmp.coords[i] -= other.coords[i]
        else:
            raise TypeError("Unexpected type.")
        return tmp

    def __add__(self, other):
        tmp = Vector3(self.coords[0], self.coords[1], self.coords[2])
        if isinstance(other, int) or isinstance(other, float):
            for i in range(3):
                tmp.coords[i] += other
        elif isinstance(other, type(self)):
            for i in range(3):
                tmp.coords[i] += other.coords[i]
        else:
            raise TypeError("Unexpected type.")
        return tmp

    def __iadd__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            for i in range(3):
                self.coords[i] += other
        elif isinstance(other, type(self)):
            for i in range(3):
                self.coords[i] += other.coords[i]
        else:
            raise TypeError("Unexpected type.")
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __div__(self, other):
        tmp = Vector3(self.coords[0], self.coords[1], self.coords[2])
        if isinstance(other, int) or isinstance(other, float):
            for i in range(3):
                tmp.coords[i] /= other
        elif isinstance(other, type(self)):
            for i in range(3):
                tmp.coords[i] /= other.coords[i]
        else:
            raise TypeError("Unexpected type.")
        return tmp

    def __truediv__(self, other):
        self.__div__(other)

    def __idiv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            for i in range(3):
                self.coords[i] /= other
        elif isinstance(other, type(self)):
            for i in range(3):
                self.coords[i] /= other.coords[i]
        else:
            raise TypeError("Unexpected type.")
        return self

    def __mul__(self, other):
        tmp = Vector3(self.coords[0], self.coords[1], self.coords[2])
        if isinstance(other, int) or isinstance(other, float):
            for i in range(3):
                tmp.coords[i] *= other
        elif isinstance(other, type(self)):
            for i in range(3):
                tmp.coords[i] *= other.coords[i]
        else:
            raise TypeError("Unexpected type.")
        return tmp

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            for i in range(3):
                self.coords[i] *= other
        elif isinstance(other, type(self)):
            for i in range(3):
                self.coords[i] *= other.coords[i]
        else:
            raise TypeError("Unexpected type.")
        return self

    def __itruediv__(self, other):
        self.__idiv__(other)

    def normalize(self):
        normalizer = (self.coords[0] ** 2. + self.coords[1] ** 2. + self.coords[2] ** 2.) ** .5
        self.__itruediv__(normalizer)
        return self

    def distance(self, other):
        tmp = 0.0
        for i in range(3):
            tmp += (self.coords[i] - other.coords[i]) ** 2.
        return tmp ** .5

    def length(self):
        return self.distance(Vector3(0,0,0))

    def toList(self):
        return self.coords[:]

    def __getitem__(self, idx):
        assert idx < 3
        return self.coords[idx]

    def __setitem__(self, idx, value):
        assert idx < 3
        self.coords[idx] = value

    def dot(self, other):
        tmp = 0
        for i in range(3):
        	tmp += self.coords[i] * other.coords[i]
        return tmp

    def cross(self, other):
        return Vector3(self.coords[2] * other.coords[3] - self.coords[3] * other.coords[2],
            self.coords[3] * other.coords[1] - self.coords[1] * other.coords[3],
            self.coords[1] * other.coords[2] - self.coords[2] * other.coords[1])
