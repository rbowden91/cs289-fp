from vector import Vector3
from random import randint

class Food:

    def __init__(self, center):
        self.eaten = False
        self.center = center
    	self.color = Vector3(randint(100, 255) / 255., randint(0, 150) / 255., 0)
    def prepare_update(self, flock, food, predators):
        pass

    def apply_update(self):
        pass
