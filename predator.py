from vector import Vector3
from random import randint, choice

class Predator:

    ACTIVE_RADIUS = 1000
    PURSUE_RADIUS = 25

    MAX_VELOCITY = 3
    MAX_FORCE = .1
    CENTER_WEIGHT = 1.5

    def __init__(self, center):
        self.center = center
        self.updated_velocity = None
        self.velocity = Vector3.random()
        self.color = Vector3(0, randint(100, 255) / 255., 0)
        self.pursue = None

    def seek(self, obj):
        direction = self.pursue.center - self.center
        direction = direction.normalize() * self.MAX_VELOCITY
        direction -= self.velocity
        direction.limit(self.MAX_FORCE)
        self.updated_velocity = self.velocity + direction * 1.5

    def prepare_update(self, flock, food, predators):
        if self.pursue is not None:
        	d = self.center.distance(self.pursue.center)

            # bat has gotten too far
        	if d > self.PURSUE_RADIUS:
        		self.pursue = None
        	else:
        		self.seek(self.pursue)
        		return

        # if we aren't already pursuing a bat
        potential_pursuit = []
        flock_center = Vector3(0.,0.,0.)
        count = 0
        for f in flock:
            d = self.center.distance(f.center)
            if d < self.ACTIVE_RADIUS:
            	potential_pursuit.append(f)
            if d < self.PURSUE_RADIUS:
                flock_center += f.center
                count += 1

        # if we're close enough to a bat, pursue it
        if len(potential_pursuit) != 0:
        	self.pursue = choice(potential_pursuit)
        	self.seek(self.pursue)
        	return

        # go toward the center of the nearby flock
        flock_center /= count
        direction = flock_center - self.center
        direction = direction.normalize() * self.MAX_VELOCITY
        direction -= self.velocity
        direction.limit(self.MAX_FORCE)
        self.updated_velocity = self.velocity + direction * 1.5

    def apply_update(self):
        self.center += self.velocity
        self.velocity = self.updated_velocity
