#!/opt/local/bin/python

# for arcball mouse rotation, see http://en.wikibooks.org/wiki/OpenGL_Programming/Modern_OpenGL_Tutorial_Arcball

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
        self.following = False
        self.rotating = False
        self.display = None
        self.prev_mouse = None
        self.current_up = (0, 1, 0)

    def get_arcball_vector(x, y):
        P = Vector3(x / self.display[0] * 2 - 1, y / self.display[1] * 2 - 1, 0)

        P[1] = -P[1]
        d = P[0] * P[0] + P[1] * P[1]

    def __sphere(self, center, radius, color, solid=True, limit=0):

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


        for i in range(limit):
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


        def drawVertex(vertex):
            glColor3fv(color.toList())
            glVertex3fv((vertices[vertex][0] * radius + center[0], vertices[vertex][1] * radius + center[1], vertices[vertex][2] * radius + center[2]))


        if solid:
            glBegin(GL_TRIANGLES)
            for face in faces:
                for vertex in face:
                	drawVertex(vertex)
        else:
        	glBegin(GL_LINES)
        	for face in faces:
        		drawVertex(face[0])
        		drawVertex(face[1])
        		drawVertex(face[1])
        		drawVertex(face[2])
        		drawVertex(face[2])
        		drawVertex(face[0])
        glEnd()


    def main(self):
        pygame.init()
        self.display = (800,600)
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)

        glMatrixMode(GL_PROJECTION);
        gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 100000)

        while True:
            #if self.rotating:
            #    model = glGetDoublev(GL_MODELVIEW_MATRIX)
            #    view = glGetIntegerv(GL_VIEWPORT)
            #    projection = glGetDoublev(GL_PROJECTION_MATRIX)

            #	world_point = gluUnProject(self.prev_mouse[0], self.prev_mouse[1], 0, model, projection, view)
            #	if (world_point[0]
            #	ball_point = 

            #    x, y = pygame.mouse.get_pos()

            #    #get_arcball_vector(
            #    self.current_up[0]

            for event in pygame.event.get():
            	if event.type == pygame.KEYUP:
            		if event.key == pygame.K_q:
            			pygame.quit()
            			quit()
            		elif event.key == pygame.K_f:
            		    self.following = not self.following

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.prev_mouse = pygame.mouse.get_pos()
                    self.rotating = True
                    pygame.mouse.set_visible(False)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.prev_mouse = None
                    self.rotating = False
                    pygame.mouse.set_visible(True)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            flock_center = Vector3(0.,0.,0.)
            for bat in self.flock:
                flock_center += bat.center
            flock_center /= len(self.flock)

            if self.following:
                glMatrixMode(GL_MODELVIEW);
                glLoadIdentity();
                gluLookAt(flock_center[0], flock_center[1], flock_center[2] + 35, flock_center[0], flock_center[1], flock_center[2], self.current_up[0], self.current_up[1], self.current_up[0])

            #self.__sphere(flock_center, 1, Vector3(0.,1.,0.), False, 1)

            for bat in self.flock:
                self.__sphere(bat.center, 0.1, bat.color)

            pygame.display.flip()

            self.update()
            pygame.time.wait(10)
        pygame.quit()
        quit()
