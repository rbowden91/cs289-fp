#!/opt/local/bin/python2.7

from bat import Bat
from draw import DrawFlock
from vector import Vector3

NUM_BATS = 25

if __name__ == "__main__":

    # create our flock of bats
    flock = []
    for i in range(NUM_BATS):
    	center = Vector3.random() * 50
    	velocity = Vector3.random()
        b = Bat(center, velocity)
        flock.append(b)

    # environment, potentially including food and predators
    env = []

    predators = []

    # in order to prevent the order of the bats from mattering, updates are all applied at once
    def update():
        for i in flock + env + predators:
            i.prepare_update(flock, env, predators)
        for i in flock + env + predators:
            i.apply_update()

    # draw our flock
    df = DrawFlock(flock, env, predators, update)
    df.main()
