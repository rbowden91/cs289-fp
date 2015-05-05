#!/opt/local/bin/python

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from vector import Vector3
from math import pi
from sphere import draw_sphere
from food import Food
import arcball

class DrawFlock:

    FOV = 45

    def __init__(self, flock, env, updater):
        self.flock = flock
        self.env = env
        self.update = updater
        self.following = False
        self.rotating = False
        self.display = None
        self.mouse_prev = None
        self.zoom = -200
        self.camera_center = [0,0,0]
        self.quaternion = (1, Vector3(0,0,0))

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

            # handle mouse and keyboard events
            for event in pygame.event.get():
            	if event.type == pygame.KEYUP:
            		if event.key == pygame.K_q:
            			pygame.quit()
            			quit()
            		elif event.key == pygame.K_f:
            		    self.following = not self.following
            		elif event.key == pygame.K_z:
            		    self.zoom -= 10
            		elif event.key == pygame.K_x:
            		    self.zoom += 10
            		elif event.key == pygame.K_p:
            		    generate_food = True

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
            	self.camera_center = [-x for x in flock_center.toList()]
            camera_center = self.camera_center[:]
            camera_center[2] += self.zoom

            # arcball stuff
            new_quaternion = None
            if self.following:

            	if self.rotating:
                    glPushMatrix()
                    # XXX why the eff is this what is necessary for it to be centered correctly?
                    glTranslate(-flock_center[0], -flock_center[1], flock_center[2] - 200)
                    #arcball.rotateQuat(self.quaternion)
                    pos = pygame.mouse.get_pos()
                    new_quaternion = arcball.get_arcball_quaternion(flock_center, self.mouse_prev, pos, self.display[1], self.quaternion)
                    self.mouse_prev = pos
                    glPopMatrix()

                glPushMatrix()
                glTranslate(camera_center[0], camera_center[1], camera_center[2])
                glTranslate(flock_center[0], flock_center[1], flock_center[2])
                arcball.rotateQuat(self.quaternion)
                arcball.draw_arcball(flock_center, self.FOV, camera_center[2], self.display[1])
                glPopMatrix()

            glTranslate(camera_center[0], camera_center[1], camera_center[2])

            glPushMatrix()
            glTranslate(flock_center[0], flock_center[1], flock_center[2])
            arcball.rotateQuat(self.quaternion)

            for bat in self.flock:
            	glPushMatrix()
                # XXX does this make sense when no longer following?
            	glTranslate(bat.center[0] - flock_center[0], bat.center[1] - flock_center[1], bat.center[2] - flock_center[2])
                draw_sphere(1, bat.color)
                glPopMatrix()
            glPopMatrix()

            for food in self.env:
            	glPushMatrix()
            	glTranslate(food.center[0], food.center[1], food.center[2])
            	draw_sphere(1, food.color)
            	glPopMatrix()

            if new_quaternion is not None:
            	self.quaternion = new_quaternion

            # XXX food doesn't work when rotating
            if generate_food:
            	food_center = Vector3.random() * 50
                food_center += flock_center
            	self.env.append(Food(food_center))

            pygame.display.flip()

            self.update()
            pygame.time.wait(0)
        pygame.quit()
        quit()
