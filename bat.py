import sys
from vector import Vector3
from math import acos, pi

class Bat:

    MAX_ACCEL = 1
    VELOCITY_RADIUS = 40
    CENTER_RADIUS = 40
    GET_AWAY_RADIUS = 5

    def __init__(self, center, velocity, color):
        self.center = center
        self.velocity = velocity
        self.color = color

    def angle(self, other):
        p = other.center - self.center
        return acos(self.velocity.dot(p) / (p.length() * self.velocity.length()))

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

            # if the bats somehow occupy same point in space, ignore
            if d == 0:
            	continue

            # XXX changing the power here is one way to tweak degree
            # of angle dependence
            angle_factor = (1. - self.angle(f) / (2. * pi)) ** 3.
            if d < self.GET_AWAY_RADIUS:
                get_away += (self.center - f.center) / (d ** 2.) * angle_factor
            if d < self.CENTER_RADIUS:
                average_center += f.center * angle_factor
                average_center_count += 1
            if d < self.VELOCITY_RADIUS:
                average_velocity += f.velocity / (d ** 2.) * angle_factor
                average_velocity_count += 1

        # in case no other bats are around
        if average_center_count > 0:
            average_center /= average_center_count
        center_vector = average_center - self.center

        if average_velocity_count > 0:
            average_velocity /= average_velocity_count

        # acceleration = self.priority_acceleration(get_away, average_velocity, center_vector)
        acceleration = self.weighted_acceleration(get_away, average_velocity, center_vector)

        self.updated_velocity = self.velocity + acceleration
        self.updated_velocity.normalize()

    # Static priority: get away, average center, then average velocity
    def priority_acceleration(self, get_away, average_velocity, center_vector):
        acceleration = Vector3(0,0,0)
        acceleration_magnitude = 0

        for vector in [get_away, center_vector, average_velocity * 100]:
            if self.MAX_ACCEL > acceleration_magnitude + vector.length():
                acceleration_magnitude += vector.length()
                acceleration += vector
            else:
                scale = (self.MAX_ACCEL - acceleration_magnitude) / vector.length()
                vector *= scale
                acceleration += vector
                break
        return acceleration

    def weighted_acceleration(self, get_away, average_velocity, center_vector):
        acceleration = Vector3(0,0,0)
        if get_away.length() != 0:
            acceleration += get_away.normalize() * 10
        if average_velocity.length() != 0:
            acceleration += average_velocity.normalize() * 5
        if center_vector.length() != 0:
            acceleration += center_vector.normalize() * 8
        acceleration = acceleration.normalize() * .1
        return acceleration


    def apply_update(self):
        self.center += self.velocity
        self.velocity = self.updated_velocity
