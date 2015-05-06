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

    def prepare_update(self, flock, env, predators):
        accelerations = {
            'center' : {
                'type' : 'flock',
                'vector' : Vector3(0.,0.,0.),
                'radius' : 100,
                'count' : 0,
                'weight' : 1,
                'distance_power' : 0,
                'angle_power' : 0,
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
                'radius' : 20,
                'count' : 0,
                'weight' : 1.5,
                'distance_power' : 1,
                'angle_power' : 0,
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

        def update_acceleration(self, accel, obj):
            d = self.center.distance(obj.center)

            # if somehow occupy same point in space, ignore
            if d == 0:
                return

            if accel['type'] == 'food' and d < 1:
            	obj.eaten = True
            	return

            angle_factor = (1. - self.angle(obj) / (2. * pi))
            if d < accel['radius']:
                boost = accel['update'](self, obj)
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
                        boost = accelerations['food_target']['update'](self, e)
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

        acceleration = self.weighted_acceleration(accelerations)
        #acceleration = self.priority_acceleration(accelerations)

        self.updated_velocity = self.velocity + acceleration
        self.updated_velocity.limit(self.MAX_VELOCITY)

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
                steer.limit(self.MAX_FORCE)

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
