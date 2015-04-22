import sys
from vector import Vector3

class Bat:

    def __init__(self, x=0, y=0, z=0, dx=0, dy=0, dz=0, r=0, g=0, b=0):
        self.center = Vector3(x,y,z)
        self.velocity = Vector3(dx,dy,dz)
        self.color = Vector3(r,g,b)

    def prepare_update(self, flock):
        average_center = Vector3(0.,0.,0.)
        get_away = Vector3(0.,0.,0.)
        average_velocity = Vector3(0.,0.,0.)

        average_center_count = 0
        average_velocity_count = 0
        for f in flock:
            if f == self:
                continue
            d = self.center.distance(f.center)
            # necessary?
            if d == 0:
                d = 0.1
            if d < 5.0:
                get_away += (self.center - f.center) / (d ** 2.)
            if d < 20.0:
                average_center += f.center
                average_center_count += 1
            average_velocity += f.velocity / (d ** 2.)
            average_velocity_count += 1

        average_center /= average_center_count
        center_vector = average_center - self.center

        average_velocity /= average_velocity_count

        acceleration = Vector3(0,0,0)
        if get_away.length() != 0:
            acceleration += get_away.normalize() * 5
        if average_velocity.length() != 0:
            acceleration += average_velocity.normalize() * 8
        if center_vector.length() != 0:
            acceleration += center_vector.normalize() * 5
        acceleration = acceleration.normalize() * .5

        self.updated_velocity = self.velocity + acceleration
        self.updated_velocity.normalize()

    def apply_update(self):
        self.center += self.velocity
        self.velocity = self.updated_velocity

    def getCenter(self):
        return self.center.toList()

    def getColor(self):
        return self.color.toList()

    def getVelocity(self):
        return self.velocity.toList()
