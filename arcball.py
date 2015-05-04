#!/opt/local/bin/python

# loosely based on CS175 notes. See http://sites.fas.harvard.edu/~lib175/asst/asst3.pdf and http://sites.fas.harvard.edu/~lib175/notes/balls-handout.pdf

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random, sys
from vector import Vector3
from math import acos, cos, sin, tan, pi
from sphere import draw_sphere

ARCBALL_RADIUS = 50

# takes in the old quaternion, and returns a new one with the appropriate arcball rotation added
def get_arcball_quaternion(arcball_center, mouse1, mouse2, screen_height, quaternion):
    model = glGetDoublev(GL_MODELVIEW_MATRIX)
    view = glGetIntegerv(GL_VIEWPORT)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)

    # project the arcball center onto the screen
    arcball_screen_center = gluProject(
        arcball_center[0],
        arcball_center[1],
        arcball_center[2],
        model, projection, view)

    # convert from top-left coordinates to bottom-left
    m1 = Vector3(mouse1[0], (screen_height - 1) - mouse1[1], 0)
    m2 = Vector3(mouse2[0], (screen_height - 1) - mouse2[1], 0)

    # calculate the z coordinates of the mouse positions on the arcball
    m1[2] = ARCBALL_RADIUS ** 2 - ((m1[0] - arcball_screen_center[0]) ** 2. + (m1[1] - arcball_screen_center[1]) ** 2.)
    m2[2] = ARCBALL_RADIUS ** 2 - ((m2[0] - arcball_screen_center[0]) ** 2. + (m2[1] - arcball_screen_center[1]) ** 2.)

    # if mouse was off the ball, just clip the z coordinate to the ball
    if m1[2] < 0:
    	m1[2] = 0
    	m1.normalize()
    else:
    	m1[2] **= .5

    if m2[2] < 0:
    	m2[2] = 0
    	m2.normalize()
    else:
    	m2[2] **= .5

    m1.normalize()
    m2.normalize()

    axis_of_rotation = m1.cross(m2)

    # normalize for floating point imprecision
    if axis_of_rotation.length() != 0:
    	axis_of_rotation.normalize()

    # apply min, just in case floating point imprecision causes the dot product to be >1
    angle_of_rotation = acos(min(m1.dot(m2), 1))

    # transform this into a quaternian
    new_w = cos(.5 * angle_of_rotation)
    new_c = axis_of_rotation * sin(.5 * angle_of_rotation)

    old_w = quaternion[0]
    old_c = quaternion[1]

    # standard quaternion multiplication
    new_quaternion = (old_w * new_w - old_c.dot(new_c),
            new_c * old_w + old_c * new_w + old_c.cross(new_c))

    return new_quaternion

def draw_arcball(center, fov, eye_z, screen_height):
    # scale so the arcball is a constant size on screen
    scale = -((center[2] + eye_z) * tan(fov * pi / 360.)) * 2 / screen_height
    draw_sphere(ARCBALL_RADIUS * scale, Vector3(0.,1.,0.), False, 1)

def quat_to_rot(quaternion):
    (w,c) = quaternion
    x,y,z = c.coords
    return [
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

def quat_to_rot2(quaternion):
    (w,c) = quaternion
    x,y,z = c.coords
    new_rot = [
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
    return [list(i) for i in zip(*new_rot)]

def rotateQuat(quaternion):
    glMultMatrixf(quat_to_rot(quaternion))
