import sys
from vector import Vector3
from math import acos, pi
from random import randint

class Bat:

    MAX_ACCEL = 1
    MAX_FORCE = .05
    MAX_VELOCITY = 2

    def __init__(self, id, center, velocity):
        self.id = id
        self.center = center
        self.velocity = velocity
        color = Vector3(0, randint(0, 150) / 255., randint(100, 255) / 255.)
        self.color = color
        self.original_color = color
        self.rounds_in_front = 0
        self.arbitrary_point = Vector3(0,0,0)

    def angle(self, other):
        p = other.center - self.center
        res = self.velocity.dot(p) / (p.length() * self.velocity.length())
        if res < -1:
            res = -1
        elif res > 1:
            res = 1
        return acos(res)

    def prepare_update(self, flock, env, predators):
        accelerations = {
            'center' : {
                'type' : 'flock',
                'vector' : Vector3(0.,0.,0.),
                'radius' : 100,
                'count' : 0,
                'weight' : 2,
                'distance_power' : 0,
                'angle_power' : -1,
                'update': lambda self, other: other.center,
                'post_update': lambda self, val: val - self.center
            },
            'avoid_predator' : {
                'type' : 'predators',
                'vector' : Vector3(0.,0.,0.),
                'radius' : 20,
                'count' : 0,
                'weight' : 3,
                'distance_power' : 1,
                'angle_power' : 0,
                'update': lambda self, other: (self.center - other.center).normalize()
            },
            'get_away' : {
                'type' : 'flock',
                'vector' : Vector3(0.,0.,0.),
                'radius' : 30,
                'count' : 0,
                'weight' : 1.5,
                'distance_power' : 1,
                'angle_power' : 1,
                'update': lambda self, other: (self.center - other.center).normalize()
            },
            'velocity' : {
                'type' : 'flock',
                'vector' : Vector3(0.,0.,0.),
                'radius' : 100,
                'count' : 0,
                'weight' : 1,
                'distance_power' : 0,
                'angle_power' : 0,
                'update': lambda self, other: other.velocity
            },
            'food_seek' : {
                'type' : 'food',
                'vector' : Vector3(0.,0.,0.),
                'radius' : 100,
                'count' : 0,
                'weight' : 1,
                'distance_power' : 0,
                'angle_power' : 0,
                'update': lambda self, other: other.center,
                'post_update': lambda self, val: val - self.center
            },
            'food_target' : {
                'type' : 'food',
                'vector' : Vector3(0.,0.,0.),
                'radius' : 10,
                'count' : 0,
                'weight' : 5,
                'distance_power' : 1,
                'angle_power' : 0,
                'update': lambda self, other: other.center,
                'post_update': lambda self, val: val - self.center
            }
        }

        def print_accelerations():
            for a in accelerations:
                print a, accelerations[a]["vector"].toList()
            print "__"

        def update_acceleration(self, accel, obj):
            d = self.center.distance(obj.center)

            # if somehow occupy same point in space, ignore
            if d == 0:
                return

            if accel['type'] == 'food' and d < 1:
                obj.eaten = True
                return

            # XXX should just be pi
            angle_factor = 1. - self.angle(obj) / (2 * pi)
            if d < accel['radius']:
                boost = accel['update'](self, obj) + 0
                boost /= d ** accel['distance_power']
                boost *= angle_factor ** accel['angle_power']
                accel['vector'] += boost
                accel['count'] += 1

        type_to_list = {
            'flock' : flock,
            'predators' : predators,
            'food' : env
        }

        for a in accelerations:
            if a == 'food_target':
                for e in env:
                    d = self.center.distance(e.center)
                    angle_factor = (1. - self.angle(e) / (2. * pi))

                    # If you're close to a particular piece of food, only target it
                    if d < accelerations['food_target']['radius']:
                        # hackish +0 to make a copy of the returned vector
                        boost = accelerations['food_target']['update'](self, e) + 0
                        boost /= d ** accelerations['food_target']['distance_power']
                        boost *= angle_factor ** accelerations['food_target']['angle_power']
                        accelerations['food_target']['vector'] = boost
                        accelerations['food_target']['count'] = 1
                        break

            else:
                # loop over the appropriate list for this acceleration type
                for i in type_to_list[accelerations[a]['type']]:
                    if (accelerations[a]['type'] == 'flock' and i == self) or (accelerations[a]['type'] == 'food' and i.eaten):
                        continue
                    update_acceleration(self, accelerations[a], i)

            if accelerations[a]['count'] > 0:
                accelerations[a]['vector'] /= accelerations[a]['count']
                if 'post_update' in accelerations[a]:
                    accelerations[a]['vector'] = accelerations[a]['post_update'](self, accelerations[a]['vector'])

        # remove all eaten food from the environment
        env[:] = [e for e in env if not e.eaten]

        # calculate the number of bats in front of this one
        front_bats = 0
        for f in flock:
        	if (f.center - self.center).length() == 0:
        		continue
        	if self.angle(f) / pi < .2:
        		front_bats += 1

        if front_bats == 0:
        	self.rounds_in_front += 1
        else:
        	self.rounds_in_front = 0

        # the bat seems to be at the front, and so can choose to lead the tunnel in some direction
        if self.rounds_in_front > 40:
            self.color = Vector3(150.,  0., 0.)
            acceleration = self.leader_acceleration()
        else:
            self.color = self.original_color
            acceleration = self.weighted_acceleration(accelerations)

        self.updated_velocity = self.velocity + acceleration
        self.updated_velocity.limit(self.MAX_VELOCITY)

    def weighted_acceleration(self, accelerations):
        acceleration = Vector3(0,0,0)

        for a in accelerations:
            if accelerations[a]['vector'].length() > 0:
                steer = accelerations[a]['vector'].normalize() * self.MAX_VELOCITY
                steer -= self.velocity
                steer.limit(self.MAX_FORCE)

                steer *= accelerations[a]['weight']
                acceleration += steer

        return acceleration


    def leader_acceleration(self):
        return (self.center - self.arbitrary_point).normalize()

    def apply_update(self):
        self.center += self.velocity
        self.velocity = self.updated_velocity
