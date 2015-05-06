import sys
from vector import Vector3
from math import acos, pi
from random import randint

class Bat:

    MAX_ACCEL = 1
    MAX_FORCE = .05
    MAX_VELOCITY = 2

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
                'weight' : 1,
                'distance_power' : 0,
                'angle_power' : 0,
                'update': lambda self, other: other.center,
                'post_update': lambda self, val: val - self.center
            },
            'get_away' : {
                'vector' : Vector3(0.,0.,0.),
                'radius' : 20,
                'count' : 0,
                'weight' : 1.5,
                'distance_power' : 1,
                'angle_power' : 0,
                'update': lambda self, other: (self.center - other.center).normalize()
            },
            'velocity' : {
                'vector' : Vector3(0.,0.,0.),
                'radius' : 100,
                'count' : 0,
                'weight' : 1,
                'distance_power' : 0,
                'angle_power' : 0,
                'update': lambda self, other: other.velocity
            }
        }

        env_accelerations = {
            'food' : {
                'vector' : Vector3(0.,0.,0.),
                'radius' : 100,
                'count' : 0,
                'weight' : 1,
                'distance_power' : 0,
                'angle_power' : 0,
                'update': lambda self, other: other.center,
                'post_update': lambda self, val: val - self.center
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
                    boost = accelerations[a]['update'](self, f)
                    boost /= d ** accelerations[a]['distance_power']
                    boost *= angle_factor ** accelerations[a]['angle_power']
                    accelerations[a]['vector'] += boost
                    accelerations[a]['count'] += 1

        for a in accelerations:
            if accelerations[a]['count'] > 0:
                accelerations[a]['vector'] /= accelerations[a]['count']
                if 'post_update' in accelerations[a]:
                    accelerations[a]['vector'] = accelerations[a]['post_update'](self, accelerations[a]['vector'])

        # XXX how should this work? for now just go in the average direction of food, but maybe
        # at a certain distance just pick a single item of food and go straight for it?
        for e in env:
            d = self.center.distance(e.center)

            if d < 1:
                e.eaten = True
                continue

            angle_factor = (1. - self.angle(e) / (2. * pi))

            for a in env_accelerations:
                if d < env_accelerations[a]['radius']:
                    boost = env_accelerations[a]['update'](self, e)
                    boost /= d ** env_accelerations[a]['distance_power']
                    boost *= angle_factor ** env_accelerations[a]['angle_power']
                    env_accelerations[a]['vector'] += boost
                    env_accelerations[a]['count'] += 1

        for a in env_accelerations:
            if env_accelerations[a]['count'] > 0:
                env_accelerations[a]['vector'] /= env_accelerations[a]['count']
                if 'post_update' in env_accelerations[a]:
                    env_accelerations[a]['vector'] = env_accelerations[a]['post_update'](self, env_accelerations[a]['vector'])

        # remove all eaten food from the environment
        env[:] = [e for e in env if not e.eaten]

        accelerations.update(env_accelerations)
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
            if accelerations[a]['vector'].length() > 0:
                steer = accelerations[a]['vector'].normalize() * self.MAX_VELOCITY
                steer -= self.velocity
                if steer.length() > self.MAX_FORCE:
                	steer = steer.normalize() * self.MAX_FORCE

                steer *= accelerations[a]['weight']
                acceleration += steer
            #print a,':',steer.coords

        #acceleration += Vector3.random() * .5
        #if acceleration.length() != 0 and acceleration.length() > self.MAX_ACCEL:
        #    acceleration = acceleration.normalize() * self.MAX_ACCEL

        return acceleration


    def apply_update(self):
        self.center += self.velocity
        self.velocity = self.updated_velocity
