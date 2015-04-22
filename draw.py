#!/opt/local/bin/python
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random, sys
from vector import Vector3

class DrawFlock:

    def __init__(self, flock, updater):
        self.flock = flock
        self.update = updater

    def __sphere(self, center, radius, color):

        # based on http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html
        t = (1. + 5. ** .5) / 2.

        vertices = [
            (-1,  t,  0),
            ( 1,  t,  0),
            (-1, -t,  0),
            ( 1, -t,  0),

            ( 0, -1,  t),
            ( 0,  1,  t),
            ( 0, -1, -t),
            ( 0,  1, -t),

            ( t,  0, -1),
            ( t,  0,  1),
            (-t,  0, -1),
            (-t,  0,  1),
        ]

        faces = [
            (0, 11, 5),
            (0, 5, 1),
            (0, 1, 7),
            (0, 7, 10),
            (0, 10, 11),
            (1, 5, 9),
            (5, 11, 4),
            (11, 10, 2),
            (10, 7, 6),
            (7, 1, 8),
            (3, 9, 4),
            (3, 4, 2),
            (3, 2, 6),
            (3, 6, 8),
            (3, 8, 9),
            (4, 9, 5),
            (2, 4, 11),
            (6, 2, 10),
            (8, 6, 7),
            (9, 8, 1)
        ]


        # return index of point in the middle of p1 and p2
        point_cache = {}
        def getMiddlePoint(p1, p2):
            # first check if we have it already
            if (p1 in point_cache and p2 in point_cache[p1]):
                return point_cache[p1][p2]
            elif (p2 in point_cache and p1 in point_cache[p2]):
                return point_cache[p2][p1]

            middle = (
                (p1[0] + p2[0]) / 2.0,
                (p1[1] + p2[1]) / 2.0,
                (p1[2] + p2[2]) / 2.0
            )
            vertices.append(middle)
            if p1 not in point_cache:
                point_cache[p1] = {}
            point_cache[p1][p2] = len(vertices) - 1


            return len(vertices) - 1;


        for i in range(0):
            faces2 = []
            for f in faces:
                a = getMiddlePoint(vertices[f[0]], vertices[f[1]]);
                b = getMiddlePoint(vertices[f[1]], vertices[f[2]]);
                c = getMiddlePoint(vertices[f[2]], vertices[f[0]]);

                faces2.append((f[0], a, c));
                faces2.append((f[1], b, a));
                faces2.append((f[2], c, b));
                faces2.append((a, b, c));
            faces = faces2;



        glBegin(GL_TRIANGLES)
        for face in faces:
            for vertex in face:
                glColor3fv(color.toList())
                glVertex3fv((vertices[vertex][0] * radius + center[0], vertices[vertex][1] * radius + center[1], vertices[vertex][2] * radius + center[2]))
        glEnd()


    def main(self):
        pygame.init()
        display = (800,600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        glMatrixMode(GL_PROJECTION);
        gluPerspective(45, (display[0]/display[1]), 0.1, 100000)

        x_move = 0
        y_move = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_move = 3
                    if event.key == pygame.K_RIGHT:
                        x_move = -3

                    if event.key == pygame.K_UP:
                        y_move = -3
                    if event.key == pygame.K_DOWN:
                        y_move = 3


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_move = 0

                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        y_move = 0

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            glMatrixMode(GL_MODELVIEW);
            glLoadIdentity();
            flock_center = Vector3(0.,0.,0.)
            for bat in self.flock:
                flock_center += bat.center
            flock_center /= len(self.flock)
            gluLookAt(flock_center[0], flock_center[1], 0, flock_center[0], flock_center[1], flock_center[2], 0, 1, 0)
            print flock_center.toList()

            for bat in self.flock:
                self.__sphere(bat.center, 0.1, bat.color)

            #glPopMatrix()
            #glPushMatrix()
            #glTranslatef(flock_center.coords[0],flock_center.coords[1], 0.0)
            #x = glGetDoublev(GL_MODELVIEW_MATRIX)

            #camera_x = x[3][0]
            #camera_y = x[3][1]
            #camera_z = x[3][2]
            #print (camera_x, camera_y, camera_z, flock_center.coords)

            pygame.display.flip()

            self.update()
            pygame.time.wait(100)
        pygame.quit()
        quit()
