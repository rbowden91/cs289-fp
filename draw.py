#!/opt/local/bin/python

# for arcball mouse rotation, see http://en.wikibooks.org/wiki/OpenGL_Programming/Modern_OpenGL_Tutorial_Arcball

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random, sys
from vector import Vector3
from math import acos, cos, sin
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
        self.arcball_quaternion = [0,0,0,1]
        self.arcball_center = Vector3(0,0,0)

    def main(self):
        pygame.init()
        self.display = (800,800)
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)

        glMatrixMode(GL_PROJECTION);
        gluPerspective(self.FOV, (self.display[0]/self.display[1]), 0.1, 100000)

        while True:
            # see http://rainwarrior.ca/dragon/arcball.html
            if self.rotating:
            	pass
            	#mouse_prev = self.get_arcball_point(self.mouse_prev[0], self.mouse_prev[1]).normalize()

                #x, y = pygame.mouse.get_pos()
                #new_point = self.get_arcball_point(x, y).normalize()
                #axis_of_rotation = mouse_prev.cross(new_point)
                #angle_of_rotation = acos(min(mouse_prev.dot(new_point), 1))

                ## transform this into a quaternian
                #axis_of_rotation *= sin(.5 * angle_of_rotation)
                #quaternion = axis_of_rotation.toList()
                #quaternion.append(cos(.5 * angle_of_rotation))

                #for i in range(4):
                #    self.arcball_quaternion[i] += quaternion[i]
                #self.mouse_prev = (x, y)

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
            self.arcball_center = flock_center

            if self.following:
                glMatrixMode(GL_MODELVIEW);
                glLoadIdentity();
                gluLookAt(flock_center[0], flock_center[1], flock_center[2] + 35, flock_center[0], flock_center[1], flock_center[2], self.current_up[0], self.current_up[1], self.current_up[0])

                (x,y,z,w) = self.arcball_quaternion
                rotation_matrix = [
                    [
                        w ** 2 + x ** 2 - y ** 2 - z ** 2,
                        2 * x * y + 2 * w * z,
                        2 * x * z - 2 * w * y,
                        0
                    ],
                    [
                        2 * x * y - 2 * w * z,
                        w ** 2 - x ** 2 + y ** 2 - z ** 2,
                        2 * y * z + 2 * w * x,
                        0
                    ],
                    [
                        2 * x * z + 2 * w * y,
                        2 * y * z - 2 * w * x,
                        w ** 2 - x ** 2 - y ** 2 + z ** 2,
                        0
                    ],
                    [
                        0,
                        0,
                        0,
                        w ** 2 + x ** 2 + y ** 2 + z ** 2
                    ]
                ]
                glMultMatrixf(rotation_matrix)


            # draw the arcball
            arcball.draw_arcball(flock_center, self.FOV, self.display[1])

            for bat in self.flock:
                draw_sphere(bat.center, .5, bat.color)

            pygame.display.flip()

            self.update()
            pygame.time.wait(10)
        pygame.quit()
        quit()
