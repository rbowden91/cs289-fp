import sys
from vector import Vector3

class Bat:

    MAX_ACCEL = 10

    def __init__(self, center, velocity, color):
        self.center = center
        self.velocity = velocity
        self.color = color

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

        acceleration = self.priority_acceleration(get_away, average_velocity, center_vector)
        # acceleration = self.weighted_acceleration(get_away, average_velocity, center_vector)

        self.updated_velocity = self.velocity + acceleration
        self.updated_velocity.normalize()

    # Static priority: get away, average center, then average velocity
    def priority_acceleration(self, get_away, average_velocity, center_vector):
        acceleration = Vector3(0,0,0)
        acceleration_magnitude = 0

        # Get away
        if self.MAX_ACCEL > acceleration_magnitude + get_away.length():
            acceleration_magnitude += get_away.length()
            acceleration += get_away
        else:
            scale = (self.MAX_ACCEL - acceleration_magnitude) / get_away.length()
            get_away *= scale
            acceleration += get_away
            return acceleration

        # Center
        if self.MAX_ACCEL > acceleration_magnitude + center_vector.length():
            acceleration_magnitude += center_vector.length()
            acceleration += center_vector
        else:
            scale = (self.MAX_ACCEL - acceleration_magnitude) / center_vector.length()
            center_vector *= scale
            acceleration += center_vector
            return acceleration

        # Average Velocity
        if self.MAX_ACCEL > acceleration_magnitude + average_velocity.length():
            acceleration_magnitude += average_velocity.length()
            acceleration += average_velocity * 100
        else:
            scale = (self.MAX_ACCEL - acceleration_magnitude) / average_velocity.length()
            average_velocity *= scale
            acceleration += average_velocity * 100
            return acceleration

        return acceleration.normalize()

    def weighted_acceleration(self, get_away, average_velocity, center_vector):
        acceleration = Vector3(0,0,0)
        if get_away.length() != 0:
            acceleration += get_away.normalize() * 5
        if average_velocity.length() != 0:
            acceleration += average_velocity.normalize() * 8
        if center_vector.length() != 0:
            acceleration += center_vector.normalize() * 5
        acceleration = acceleration.normalize() * .5
        return acceleration


    def apply_update(self):
        self.center += self.velocity
        self.velocity = self.updated_velocity
