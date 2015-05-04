#!/opt/local/bin/python

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from vector import Vector3
from math import pi
from sphere import draw_sphere
import arcball

class DrawFlock:

    FOV = 45

    def __init__(self, flock, updater):
        self.flock = flock
        self.update = updater
        self.following = False
        self.rotating = False
        self.display = None
        self.mouse_prev = None
        self.current_up = (0, 1, 0)
        self.camera_center = Vector3(0,0,-200)
        self.quaternion = (1, Vector3(0,0,0))

    def main(self):
        pygame.init()
        self.display = (800,800)
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)

        glMatrixMode(GL_PROJECTION);
        gluPerspective(self.FOV, (self.display[0]/self.display[1]), 0.1, 100000)

        glMatrixMode(GL_MODELVIEW)
        while True:

            for event in pygame.event.get():
            	if event.type == pygame.KEYUP:
            		if event.key == pygame.K_q:
            			pygame.quit()
            			quit()
            		elif event.key == pygame.K_f:
            		    self.following = not self.following

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_prev = pygame.mouse.get_pos()
                    self.rotating = True
                    pygame.mouse.set_visible(False)
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
            	self.camera_center[2] -= 200

            # arcball stuff
            if self.following:
            	if self.rotating:
                    pos = pygame.mouse.get_pos()
                    self.quaternion = arcball.get_arcball_quaternion(flock_center, self.mouse_prev, pos, self.display[1], self.quaternion)
                    self.mouse_prev = pos

                glPushMatrix()
                glTranslate(self.camera_center[0], self.camera_center[1], self.camera_center[2])

                glTranslate(flock_center[0], flock_center[1], flock_center[2])
                arcball.rotateQuat(self.quaternion)
                arcball.draw_arcball(flock_center, self.FOV, self.camera_center[2], self.display[1])
                glPopMatrix()

            #glTranslate(flock_center[0], flock_center[1], flock_center[2])
            #glRotatef(self.quaternion[0] * 180 / pi, self.quaternion[1][0], self.quaternion[1][1], self.quaternion[1][2])

            for bat in self.flock:
            	glPushMatrix()
            	glTranslate(self.camera_center[0], self.camera_center[1], self.camera_center[2])
            	glTranslate(flock_center[0], flock_center[1], flock_center[2])
                arcball.rotateQuat(self.quaternion)
            	glTranslate(bat.center[0] - flock_center[0], bat.center[1] - flock_center[1], bat.center[2] - flock_center[2])
                draw_sphere(1, bat.color)
                glPopMatrix()

            pygame.display.flip()

            self.update()
            pygame.time.wait(10)
        pygame.quit()
        quit()
