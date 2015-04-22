#!/opt/local/bin/python2.7

from bat import Bat
from draw import DrawFlock
import random

NUM_BATS = 50

if __name__ == "__main__":

    # create our flock of bats
    flock = []
    for i in range(NUM_BATS):
        x = random.randrange(-10,10)
        y = random.randrange(-10,10)
        b = Bat(x,y,5,random.random(),random.random(),0,random.random(),random.random(),random.random())
        flock.append(b)

    # in order to prevent the order of the bats from mattering, updates are all applied at once
    def update():
        for f in flock:
            f.prepare_update(flock)
        for f in flock:
            f.apply_update()

    # draw our flock
    df = DrawFlock(flock, update)
    df.main()
