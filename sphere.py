from OpenGL.GL import *
from vector import Vector3

# based on http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html
def draw_sphere(radius, color, solid=True, limit=0):
    t = (1. + 5. ** .5) / 2.

    vertices = [
        Vector3(-1,  t,  0),
        Vector3( 1,  t,  0),
        Vector3(-1, -t,  0),
        Vector3( 1, -t,  0),

        Vector3( 0, -1,  t),
        Vector3( 0,  1,  t),
        Vector3( 0, -1, -t),
        Vector3( 0,  1, -t),

        Vector3( t,  0, -1),
        Vector3( t,  0,  1),
        Vector3(-t,  0, -1),
        Vector3(-t,  0,  1),
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

    for i in range(len(vertices)):
    	vertices[i] = vertices[i].normalize() * radius

    # return index of point in the middle of p1 and p2
    point_cache = {}
    def getMiddlePoint(p1, p2):
        # first check if we have it already
        if (p1 in point_cache and p2 in point_cache[p1]):
            return point_cache[p1][p2]
        elif (p2 in point_cache and p1 in point_cache[p2]):
            return point_cache[p2][p1]

        middle = Vector3(
            (p1[0] + p2[0]) / 2.0,
            (p1[1] + p2[1]) / 2.0,
            (p1[2] + p2[2]) / 2.0
        )

        middle = middle.normalize() * radius
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
        glVertex3fv(vertices[vertex].toList())


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
