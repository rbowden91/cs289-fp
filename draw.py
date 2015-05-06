#!/opt/local/bin/python

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from vector import Vector3
from math import pi, acos, atan2
from sphere import draw_sphere
from food import Food
from predator import Predator
import arcball

class DrawFlock:

    FOV = 45

    def __init__(self, flock, env, predators, updater):
        self.flock = flock
        self.env = env
        self.predators = predators
        self.update = updater
        self.following = False
        self.rotating = False
        self.display = None
        self.mouse_prev = None
        self.zoom = -200
        self.world_center = Vector3(0,0,0)
        self.world_quaternion = (1, Vector3(0,0,0))
        self.draw_arcball = True

    def main(self):
        pygame.init()
        self.display = (800,800)
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)

        glMatrixMode(GL_PROJECTION);
        gluPerspective(self.FOV, (self.display[0]/self.display[1]), 0.1, 100000)

        glMatrixMode(GL_MODELVIEW)

        # main drawing loop
        while True:

            # set to true if `p` key is pressed
            generate_food = False
            generate_predator = False

            # handle mouse and keyboard events
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_f:
                        self.following = not self.following
                    elif event.key == pygame.K_a:
                        self.draw_arcball = not self.draw_arcball
                    elif event.key == pygame.K_z:
                        self.zoom -= 10
                    elif event.key == pygame.K_x:
                        self.zoom += 10
                    elif event.key == pygame.K_p:
                        generate_food = True
                    elif event.key == pygame.K_o:
                        generate_predator = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_prev = pygame.mouse.get_pos()
                    self.rotating = True
                    #pygame.mouse.set_visible(False)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_prev = None
                    self.rotating = False
                    pygame.mouse.set_visible(True)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            flock_center = Vector3(0.,0.,0.)
            for bat in self.flock:
                flock_center += bat.center
            flock_center /= len(self.flock)

            glLoadIdentity()

            if self.following:
                self.world_center = flock_center * -1

            # zoom out
            glTranslate(0,0,self.zoom)

            # rotate the world
            arcball.rotateQuat(self.world_quaternion)

            # bring the scene to the camera
            glTranslate(self.world_center[0],
                        self.world_center[1],
                        self.world_center[2])


            if self.following:

                if self.rotating:
                    pos = pygame.mouse.get_pos()
                    self.world_quaternion = arcball.get_arcball_quaternion(flock_center, self.mouse_prev, pos, self.display[1], self.world_quaternion)
                    self.mouse_prev = pos

                if self.draw_arcball:
                    glPushMatrix()
                    # bring the ball to the flock center
                    glTranslatef(flock_center[0],
                                flock_center[1],
                                flock_center[2])
                    arcball.draw_arcball(flock_center, self.FOV, self.world_center[2] + self.zoom, self.display[1])
                    glPopMatrix()

            for bat in self.flock:
                glPushMatrix()

                # move bat to correct position
                glTranslate(bat.center[0],
                            bat.center[1],
                            bat.center[2])

                # have the cone face in the direction of the velocity vector
                x,y,z = bat.velocity.toList()
                if x < .00001 and y < .00001:
                	yaw = 0
                else:
                	yaw = atan2(x,z) * 180 / pi
                pitch = -atan2(y, (x * x + z * z) ** .5) * 180 / pi
                glRotatef(yaw, 0, 1, 0)
                glRotatef(pitch, 1, 0, 0)

                # draw the bat cone
                glColor3fv(bat.color.toList())
                quadric = gluNewQuadric()
                gluCylinder(quadric, 2, 0, 5, 100, 100)
                gluDeleteQuadric(quadric)

                glPopMatrix()

            for food in self.env:
                glPushMatrix()
                #print food.eaten, food.center.coords, len(self.env)
                glTranslate(food.center[0], food.center[1], food.center[2])
                draw_sphere(1, food.color)
                glPopMatrix()

            for p in self.predators:
                glPushMatrix()
                glTranslate(p.center[0], p.center[1], p.center[2])
                draw_sphere(1, p.color)
                glPopMatrix()

            # XXX food doesn't work when rotating
            if generate_food:
                food_center = Vector3.random() * 50
                food_center += flock_center
                self.env.append(Food(food_center))
            if generate_predator:
                predator_center = Vector3.random() * 50
                predator_center += flock_center
                self.predators.append(Predator(predator_center))


            pygame.display.flip()

            self.update()
            pygame.time.wait(0)
        pygame.quit()
        quit()
