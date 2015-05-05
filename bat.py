import sys
from vector import Vector3
from math import acos, pi
from random import randint

class Bat:

    MAX_ACCEL = .1
    MAX_VELOCITY = 3

    def __init__(self, center, velocity):
        self.center = center
        self.velocity = velocity
    	self.color = Vector3(0, randint(0, 150) / 255., randint(100, 255) / 255.)

    def angle(self, other):
        p = other.center - self.center
        return acos(self.velocity.dot(p) / (p.length() * self.velocity.length()))

    def prepare_update(self, flock, env):
        accelerations = {
            'center' : {
            	'vector' : Vector3(0.,0.,0.),
                'radius' : 100,
                'count' : 0,
                'weight' : 5,
                'update': lambda self, other, d, angle_factor: (other.center - self.center) / (d ** 2.) * angle_factor
            },
            'get_away' : {
            	'vector' : Vector3(0.,0.,0.),
                'radius' : 0,
                'count' : 0,
                'weight' : 8,
                'update': lambda self, other, d, angle_factor: (self.center - other.center) / (d ** 2.) * angle_factor
            },
            'velocity' : {
            	'vector' : Vector3(0.,0.,0.),
                'radius' : 100,
                'count' : 0,
                'weight' : 4,
                'update': lambda self, other, d, angle_factor: (other.velocity - self.velocity) / (d ** 2.) * angle_factor ** 0.
            }
        }

        for f in flock:
            if f == self:
                continue
            d = self.center.distance(f.center)

            # if the bats somehow occupy same point in space, ignore
            if d == 0:
            	continue

            angle_factor = (1. - self.angle(f) / (2. * pi))

            for a in accelerations:
                if d < accelerations[a]['radius']:
                	accelerations[a]['vector'] += accelerations[a]['update'](self, f, d, angle_factor)
                	accelerations[a]['count'] += 1

            for a in accelerations:
            	if accelerations[a]['count'] > 0:
                    accelerations[a]['vector'] /= accelerations[a]['count']

        # XXX how should this work? for now just go in the average direction of food, but maybe
        # at a certain distance just pick a single item of food and go straight for it?
        #average_food_velocity = Vector3(0.,0.,0.)
        #avreage_food_count = 0
        #for e in env:
        #	d = self.center.distance(e.center)

        #	if d == 0:
        #		e.eaten = True
        #		continue
        #	if d = 


        # remove all eaten food from the environment
        #env[:] = [e for e in env if not e.eaten]

        acceleration = self.weighted_acceleration(accelerations)
        #acceleration = self.priority_acceleration(accelerations)

        self.updated_velocity = self.velocity + acceleration

        # XXX some different way of handling this?
        if self.updated_velocity.length() > self.MAX_VELOCITY:
        	self.updated_velocity = self.updated_velocity.normalize() * self.MAX_VELOCITY

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

    def weighted_acceleration(self, accelerations):
        acceleration = Vector3(0,0,0)

        for a in accelerations:
            #print accelerations[a]['vector'].coords
            acceleration += accelerations[a]['vector'] * accelerations[a]['weight']

        #acceleration += Vector3.random() * .5
        if acceleration.length() != 0 and acceleration.length() > self.MAX_ACCEL:
            acceleration = acceleration.normalize() * self.MAX_ACCEL

        return acceleration


    def apply_update(self):
        self.center += self.velocity
        self.velocity = self.updated_velocity
