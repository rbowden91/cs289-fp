#!/opt/local/bin/python

# for arcball mouse rotation, see http://en.wikibooks.org/wiki/OpenGL_Programming/Modern_OpenGL_Tutorial_Arcball

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random, sys
from vector import Vector3
from math import acos, cos, sin, tan, pi
from sphere import draw_sphere

ARCBALL_RADIUS = 100

## takes in the position of the arcball, 
#def get_arcball_point(self, x, y):
#    model = glGetDoublev(GL_MODELVIEW_MATRIX)
#    view = glGetIntegerv(GL_VIEWPORT)
#    projection = glGetDoublev(GL_PROJECTION_MATRIX)
#
#    # convert from top-left coordinates to bottom-left
#    new_y = (self.display[1] - 1) - y
#
#    world_point = gluUnProject(x, new_y, 0, model, projection, view)
#    print world_point, self.arcball_center.coords
#
#    d = (world_point[0] - self.arcball_center[0]) ** 2. + (world_point[1] - self.arcball_center[1]) ** 2.
#    print d
#
#    # we clicked within the arcball
#    if (d < ARCBALL_RADIUS ** 2.):
#        z = (ARCBALL_RADIUS ** 2. - d) ** .5
#    else:
#        z = 0
#
#    return Vector3(world_point[0], world_point[1], z)
#
#            # see http://rainwarrior.ca/dragon/arcball.html
#            if self.rotating:
#            	mouse_prev = self.get_arcball_point(self.mouse_prev[0], self.mouse_prev[1]).normalize()
#
#                x, y = pygame.mouse.get_pos()
#                new_point = self.get_arcball_point(x, y).normalize()
#                axis_of_rotation = mouse_prev.cross(new_point)
#                angle_of_rotation = acos(min(mouse_prev.dot(new_point), 1))
#
#                # transform this into a quaternian
#                axis_of_rotation *= sin(.5 * angle_of_rotation)
#                quaternion = axis_of_rotation.toList()
#                quaternion.append(cos(.5 * angle_of_rotation))
#
#                for i in range(4):
#                    self.arcball_quaternion[i] += quaternion[i]
#                self.mouse_prev = (x, y)


def draw_arcball(center, fov, screen_height):
    # scale so the arcball is a constant size on screen
    model = glGetDoublev(GL_MODELVIEW_MATRIX)
    eye_z = model[3][2]
    scale = -((center[2] + eye_z) * tan(fov * pi / 360.)) / screen_height
    #print scale
    draw_sphere(center, ARCBALL_RADIUS * scale, Vector3(0.,1.,0.), False, 1)
