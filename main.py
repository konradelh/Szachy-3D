import pygame
import math as m
import random as r
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#region kolorki
PIECE_WHITE = [1,1,0.7]
PIECE_BLACK = [0.1, 0.1, 0.1]
BOARD_BLACK = [0,0,0]
BOARD_WHITE = [1,1,1]
#endregion

#region funkcje
vertices = (
    (0.5, -0.5, -0.5),
    (-0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),
    (-0.5, -0.5, 0.5),
)

edges = (
    (0,1),
    (0,2),
    (2,3),
    (1,3)
)

def draw_square(fill_color=[]):
    glLineWidth(5)
    glBegin(GL_LINES)
    for edge in edges:
        glColor(1,0.45,0.8)
        for vertex in edge:
            glVertex3fv(vertices[vertex])

    glEnd()

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_QUADS)
    glColor(fill_color)
    for vertex in (0,2,3,1):
        glVertex3fv(vertices[vertex])
    glEnd()

def draw_circle(radius,color=[]):
    segments=16
    glBegin(GL_TRIANGLES)
    for i in range(segments):
        angle = i * 2 * m.pi / segments
        next_angle = (i + 1) * 2 * m.pi / segments
        
        glColor3fv(color)
        glVertex3f(0, 0, 0)
        glVertex3f(radius * m.cos(angle), 0, radius * m.sin(angle))
        glVertex3f(radius * m.cos(next_angle), 0, radius * m.sin(next_angle))
    glEnd()

def draw_cone(color=[]):
    segments=16
    height=0.5
    radius=0.3
    glBegin(GL_TRIANGLES)
    for i in range(segments):
        angle = i * 2 * m.pi / segments
        next_angle = (i + 1) * 2 * m.pi / segments
        
        glColor3fv(color)
        glVertex3f(0, height/2, 0)
        glVertex3f(radius * m.cos(angle), -height/2, radius * m.sin(angle))
        glVertex3f(radius * m.cos(next_angle), -height/2, radius * m.sin(next_angle))
    glEnd()

def draw_sphere(radius, color=[]):
    lats=12
    longs=24
    for i in range(lats):
        lat0 = m.pi * (-0.5 + i / lats)
        z0 = radius * m.sin(lat0)
        zr0 = radius * m.cos(lat0)

        lat1 = m.pi * (-0.5 + (i + 1) / lats)
        z1 = radius * m.sin(lat1)
        zr1 = radius * m.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(longs + 1):
            lng = 2 * m.pi * j / longs
            x = m.cos(lng)
            y = m.sin(lng)
            
            glColor3fv(color)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def draw_donut(color=[]):
    radius=0.5
    c=1
    sides=24
    rings=24

    for i in range(rings):
        glBegin(GL_QUAD_STRIP)
        for j in range(sides + 1):
            for k in range(2):
                s = (i + k) % rings + 0.5
                t = j % sides
                
                theta = 2 * m.pi * s / rings
                phi = 2 * m.pi * t / sides
                
                x = (c + radius * m.cos(phi)) * m.cos(theta)
                y = (c + radius * m.cos(phi)) * m.sin(theta)
                z = radius * m.sin(phi)
                
                glColor3fv(color)
                glVertex3f(x, y, z)
        glEnd()

def draw_cylinder(radius,height,color=[]):
    sides = 24
    cylinder_vertices =[]
    
    for j in range(sides + 1):
        for k in range(2):
            t = j % sides
            h_idx = k
                
            theta = 2 * m.pi * t / sides

            x = radius * m.cos(theta)  
            z = radius * m.sin(theta)     
            y = (h_idx) * height
            
            cylinder_vertices.append([x,y,z])
                
    glBegin(GL_QUAD_STRIP)
    for i in range(0,len(cylinder_vertices)):
        glColor3fv(color)
        glVertex3fv(cylinder_vertices[i])
    glEnd()

def draw_rook_top(radius,height,color=[]):
    sides = 24
    cylinder_vertices =[]
    
    for j in range(sides + 1):
        for k in range(2):
            t = j % sides
            h_idx = k
                
            theta = 2 * m.pi * t / sides

            x = radius * m.cos(theta)  
            z = radius * m.sin(theta)     
            if j%3 == 0 or j%3 == 1:       
                y = 1.5*(h_idx) * height
            else:
                y = (h_idx) * height
            
            cylinder_vertices.append([x,y,z])
                
    glBegin(GL_QUAD_STRIP)
    for i in range(0,len(cylinder_vertices)):
        glColor3fv(color)
        glVertex3fv(cylinder_vertices[i])
    glEnd()

def draw_crown(radius,height,color=[]):
    sides = 24
    glBegin(GL_QUAD_STRIP)
    for j in range(sides + 1):
        for k in range(2):
            t = j % sides
            h_idx = k
                
            theta = 2 * m.pi * t / sides

            x = radius * m.cos(theta)
            if j%3 == 0:       
                y = 1.5*(h_idx) * height
            else:
                y = (h_idx) * height
            z = radius * m.sin(theta)
                
            glColor3fv(color)
            glVertex3f(x, y, z)
    glEnd()

def draw_bishop_top(radius, color=[]):
    lats=12
    longs=24
    for i in range(lats):
        lat0 = m.pi * (-0.5 + i / lats)
        z0 = 5*radius * m.sin(lat0)
        zr0 = radius * m.cos(lat0)

        lat1 = m.pi * (-0.5 + (i + 1) / lats)
        z1 = -5*radius * m.sin(lat1)
        zr1 = radius * m.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(longs + 1):
            lng = 2 * m.pi * j / longs
            x = m.cos(lng)
            y = m.sin(lng)
            
            
            glColor3fv(color)
            glVertex3f(x * zr0,0.2*z0 , y * zr0)
            glVertex3f(x * zr1,0.2*z1 , y * zr1)
        glEnd()

def queen(color = [],position = []):
    glPushMatrix()
    glTranslatef(position[0],position[1],position[2])
    draw_cylinder(0.3,0.15,color)
    glTranslatef(0,0.02,0)
    draw_circle(0.25,color)
    glTranslatef(0,-0.02,0)
    draw_cylinder(0.25,0.6,color)
    glTranslatef(0,0.6,0)
    glTranslatef(0,0.02,0)
    draw_circle(0.3,color)
    glTranslatef(0,-0.02,0)
    draw_crown(0.3,0.15,color)
    glTranslatef(0.3,0.225,0)
    draw_sphere(0.05,color)
    glTranslatef(-0.6,0,0)
    draw_sphere(0.04,color)
    glTranslatef(0.3,0,0.3)
    draw_sphere(0.04,color)
    glTranslatef(0,0,-0.6)
    draw_sphere(0.04,color)
    glTranslatef(0.2,0,0.15)
    draw_sphere(0.04,color)
    glTranslatef(-0.4,0,0)
    draw_sphere(0.04,color)
    glTranslatef(0,0,0.3)
    draw_sphere(0.04,color)
    glTranslatef(0.4,0,0)
    draw_sphere(0.04,color)
    glPopMatrix()

def rook(color = [], position = []):
    glPushMatrix()
    glTranslatef(position[0],position[1],position[2])
    draw_cylinder(0.35,0.15,color)
    glTranslatef(0,0.02,0)
    draw_circle(0.35,color)
    glTranslatef(0,-0.02,0)
    draw_cylinder(0.25,0.4,color)
    glTranslatef(0,0.4,0)
    glTranslatef(0,0.02,0)
    draw_circle(0.35,color)
    glTranslatef(0,-0.02,0)
    draw_rook_top(0.35,0.15,color)
    glPopMatrix()

def pawn(color = [], position = []):
    glPushMatrix()
    glTranslatef(position[0],position[1],position[2])
    draw_cone(color)
    glTranslatef(0,-0.25,0)
    draw_cylinder(0.3,0.2,color)
    glTranslatef(0,0.65,0)
    draw_sphere(0.2,color)
    glPopMatrix()

def bishop(color = [], position = []):
    glPushMatrix()
    glTranslatef(position[0],position[1],position[2])
    draw_cylinder(0.35,0.15,color)
    glTranslatef(0,0.02,0)
    draw_circle(0.35,color)
    glTranslatef(0,-0.02,0)
    draw_cylinder(0.25,0.4,color)
    glTranslatef(0,0.4,0)
    draw_circle(0.3,color)
    glTranslatef(0,0.2,0)
    draw_bishop_top(0.2,color)
    glTranslatef(0,0.25,0)
    draw_sphere(0.08,color)
    glPopMatrix()
#endregion

def main():
    pygame.init()
    display = (2400,1200)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(60, display[0] / display[1], 0.1, 50)
    glViewport(0,0,display[0],int(display[1]*2))

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glLightfv(GL_LIGHT0,GL_POSITION,[5,1,-3,1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.2, 0.3, 1.0])
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    position = []
    for j in range(0,8):
        for i in range (0,8):
            position.append((-3.5+i,-2,-j-5))

    while True:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #rysowanie planszy
        counter = 1
        for i in range(0, len(position)):
            glPushMatrix()
            glTranslatef(position[i][0],position[i][1],position[i][2])

            if i%8 == 0 and i != 0 and counter == 0:
                counter = 1
            elif i%8 == 0 and i != 0 and counter == 1:
                counter = 0
                
            if counter == 0:
                draw_square(BOARD_WHITE)
                counter = 1
            else:
                draw_square(BOARD_BLACK)
                counter = 0
            
            glPopMatrix() 

        #rysowanie figur
        positions_black_pawns = []
        for i in range(0,8):
            positions_black_pawns.append([-3.5+i,-2.25,-11])
        for i in range(0,len(positions_black_pawns)):
            pawn(PIECE_BLACK,positions_black_pawns[i])

        positions_white_pawns = []
        for i in range(0,8):
            positions_white_pawns.append([-3.5+i,-2.25,-6])
        for i in range(0,len(positions_white_pawns)):
            pawn(PIECE_WHITE,positions_white_pawns[i])

        positions_rooks = [
            [-3.5,-2.5,-5],
            [3.5,-2.5,-5],
            [-3.5,-2.5,-12],
            [3.5,-2.5,-12]
        ]
        rook(PIECE_BLACK,positions_rooks[2])
        rook(PIECE_BLACK,positions_rooks[3])
        rook(PIECE_WHITE,positions_rooks[0])
        rook(PIECE_WHITE,positions_rooks[1])

        positions_queens = [
            [-0.5,-2.5,-5],
            [-0.5,-2.5,-12]
        ]
        queen(PIECE_BLACK,positions_queens[1])
        queen([PIECE_WHITE],positions_queens[0])

        positions_bishops = [
            [-1.5,-2.5,-5],
            [1.5,-2.5,-5],
            [-1.5,-2.5,-12],
            [1.5,-2.5,-12]
        ]
        bishop(PIECE_BLACK,positions_bishops[2])
        bishop(PIECE_BLACK,positions_bishops[3])
        bishop(PIECE_WHITE,positions_bishops[0])
        bishop(PIECE_WHITE,positions_bishops[1])
        pygame.display.flip()
        pygame.time.wait(10)

        for event in pygame.event.get():  
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()  
                
main()