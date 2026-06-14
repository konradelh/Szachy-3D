import pygame
import pygame_menu
import math as m
import random as r
from logika import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

display = (2400,1200)
made_moves = []

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

def lightup(position=[],color=[]):
    glPushMatrix()
    glTranslatef(position[0],position[1],position[2])
    glLineWidth(12)
    glBegin(GL_LINES)
    for edge in edges:
        glColor(color)
        for vertex in edge:
            glVertex3fv(vertices[vertex])

    glEnd()
    glPopMatrix()

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

def draw_cone(height,radius,color=[]):
    segments=16
    # height=0.5
    # radius=0.3
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

def draw_cross(color=[]):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_QUADS)
    glColor(color)
    cross_vertices = (
        (-0.075,0,0),
        (0.075,0,0),
        (0.075,0.25,0),
        (-0.075,0.25,0),
        
        
        (0.2,0.325,0),
        (-0.2,0.325,0),
        (-0.2,0.25,0),
        (0.2,0.25,0),

        (0.075,0.3,0),
        (0.075,0.4,0),
        (-0.075,0.4,0),
        (-0.075,0.3,0)
        
    )
    for i in range(0,len(cross_vertices)):
        glVertex3fv(cross_vertices[i])
    glEnd()

def draw_knight_top(color=[]):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_QUADS)
    glColor(color)
    knight_vertices = (
        (-0.15,0,0.1),
        (0.45,0.08,0.1),
        (0.45,0.15,0.2),
        (-0.2,0.15,0.2),

        (-0.15,0,-0.1),
        (0.45,0.08,-0.1),
        (0.45,0.15,-0.2),
        (-0.2,0.15,-0.2),

        (-0.15,0,0.1),
        (-0.15,0,-0.1),
        (0.45,0.08,-0.1),
        (0.45,0.08,0.1),
        
        (0.45,0.08,0.1),
        (0.45,0.08,-0.1),
        (0.45,0.15,-0.2),
        (0.45,0.15,0.2),
        
        (-0.15,0,0.1),
        (-0.15,0,-0.1),
        (-0.2,0.15,-0.2),
        (-0.2,0.15,0.2),

        (-0.15,0.3,0.1),
        (0.45,0.2,0.1),
        (0.45,0.15,0.2),
        (-0.2,0.15,0.2),

        (-0.15,0.3,-0.1),
        (0.45,0.2,-0.1),
        (0.45,0.15,-0.2),
        (-0.2,0.15,-0.2),

        (-0.15,0.3,0.1),
        (-0.15,0.3,-0.1),
        (0.45,0.2,-0.1),
        (0.45,0.2,0.1),
        
        (0.45,0.2,0.1),
        (0.45,0.2,-0.1),
        (0.45,0.15,-0.2),
        (0.45,0.15,0.2),
        
        (-0.15,0.3,0.1),
        (-0.15,0.3,-0.1),
        (-0.2,0.15,-0.2),
        (-0.2,0.15,0.2),

    )
    for i in range(0,len(knight_vertices)):
        glVertex3fv(knight_vertices[i])
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
    glTranslatef(position[0],position[1]+0.25,position[2])
    draw_cone(0.5,0.3,color)
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

def king(color = [], position = []):
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
    glTranslatef(0,0.025,0) 
    draw_cross(color)
    glPopMatrix()

def knight(color = [], position = []):
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
    draw_knight_top(color)
    glTranslatef(-0.1,0.325,0.07)
    draw_cone(0.15,0.06,color)
    glTranslatef(0,0,-0.14)
    draw_cone(0.15,0.06,color)
    glPopMatrix()

def draw_board(square_positions = []):
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    counter = 1
    for i in range(0, len(square_positions)):
        glPushMatrix()
        glTranslatef(square_positions[i][0],square_positions[i][1],square_positions[i][2])

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

def draw_pieces(gra):
    positions_black_pawns = convert_BitBoard_to_position(gra.piecesTable[gra.BLACK][0])
    for i in range(0,len(positions_black_pawns)):
        pawn(PIECE_BLACK,positions_black_pawns[i])
    positions_white_pawns = convert_BitBoard_to_position(gra.piecesTable[gra.WHITE][0])
    for i in range(0,len(positions_white_pawns)):
        pawn(PIECE_WHITE,positions_white_pawns[i])

    positions_black_rooks = convert_BitBoard_to_position(gra.piecesTable[gra.BLACK][2])
    for i in range (0,len(positions_black_rooks)):
        rook(PIECE_BLACK,positions_black_rooks[i])
    positions_white_rooks = convert_BitBoard_to_position(gra.piecesTable[gra.WHITE][2])
    for i in range (0,len(positions_white_rooks)):
        rook(PIECE_WHITE,positions_white_rooks[i])

    positions_black_queens = convert_BitBoard_to_position(gra.piecesTable[gra.BLACK][5])
    for i in range (0,len(positions_black_queens)):
        queen(PIECE_BLACK,positions_black_queens[i])
    positions_white_queens = convert_BitBoard_to_position(gra.piecesTable[gra.WHITE][5])
    for i in range (0,len(positions_white_queens)):
        queen(PIECE_WHITE,positions_white_queens[i])

    positions_black_bishops = convert_BitBoard_to_position(gra.piecesTable[gra.BLACK][4])
    for i in range(0,len(positions_black_bishops)):
        bishop(PIECE_BLACK,positions_black_bishops[i])
    positions_white_bishops = convert_BitBoard_to_position(gra.piecesTable[gra.WHITE][4])
    for i in range(0,len(positions_white_bishops)):
        bishop(PIECE_WHITE,positions_white_bishops[i])

    positions_black_kings = convert_BitBoard_to_position(gra.piecesTable[gra.BLACK][1])
    for i in range(0,len(positions_black_kings)):
        king(PIECE_BLACK,positions_black_kings[i])
    positions_white_kings = convert_BitBoard_to_position(gra.piecesTable[gra.WHITE][1])
    for i in range(0,len(positions_white_kings)):
        king(PIECE_WHITE,positions_white_kings[i])

    positions_black_knights = convert_BitBoard_to_position(gra.piecesTable[gra.BLACK][3])
    for i in range(0,len(positions_black_knights)):
        knight(PIECE_BLACK,positions_black_knights[i])
    positions_white_knights = convert_BitBoard_to_position(gra.piecesTable[gra.WHITE][3])
    for i in range(0,len(positions_white_knights)):
        knight(PIECE_WHITE,positions_white_knights[i])


def convert_BitBoard_to_position(bitboard):
    temp = bitboard
    positions = []
    while temp != 0:
            y = -2.5
            index = chess.getMSB(temp)
            if index is None or index < 0:
                break
            x = index % 8 - 3.5
            z = -(index // 8) - 5
            positions.append([x,y,z])
            temp = chess.popBit(temp,index)
    return positions

def convert_position_to_index(position = []):
    return int(position[0] + 3.5 + (-position[2] - 5)*8)

def convert_index_to_position(index):
    y = -2.5
    x = index % 8 - 3.5
    z = -(index // 8) - 5
    return [x,y,z]
    
def inicjalizacja():
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(60, display[0] / display[1], 0.1, 50)
    glViewport(0,0,display[0],int(display[1]*2))

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION,[-1,0,-13,1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 0.4, 0.6, 1.0])
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION,[-1,0,-5,1])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1, 1, 1, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1, 0.4, 0.6, 1.0])
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)

def menu(kto_wygral):
    screen = pygame.display.set_mode(display)
    baner = pygame_menu.themes.THEME_DARK.copy()
    baner.title_background_color = (230, 80, 130)
    baner.background_color = (90, 0, 150, 200)
    baner.widget_font = pygame_menu.font.FONT_8BIT
    baner.title_font = pygame_menu.font.FONT_8BIT

    menu = pygame_menu.Menu(title=f'Game finished - {kto_wygral}', width=display[0], height=display[1],theme=baner)

    menu.add.button('NEW GAME', main)
    menu.add.button('VIEW GAME', view_game)
    menu.add.button('QUIT', pygame_menu.events.EXIT)

    menu.mainloop(screen)

def view_game():
    inicjalizacja()

    gra = chess()

    square_positions = []
    for j in range(0,8):
        for i in range (0,8):
            square_positions.append((-3.5+i,-2,-j-5))
    
    ktory_ruch = 0
    # for move in made_moves:
    czy_koniec = 0
    while czy_koniec != 1:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if ktory_ruch == (len(made_moves) - 1):
                    czy_koniec = 1
                gra.makeMove(made_moves[ktory_ruch])
                ktory_ruch += 1
                draw_board(square_positions)
                draw_pieces(gra)
                pygame.display.flip()
                pygame.time.wait(10)
    pygame.time.wait(2000)
    made_moves = []
    menu('viewing complete')    

def main():
    inicjalizacja()

    square_positions = []
    for j in range(0,8):
        for i in range (0,8):
            square_positions.append((-3.5+i,-2,-j-5))

    gra = chess()

    lightup_position = [-3.5,-1.97,-5]
    posible_moves_lightup_positions = []
    czy_aktualizacja = 1
    czy_wybrane_pole = 0
    wybrane_pole = []
    currentPlayer = 1
    czy_biale_wygraly = 0
    czy_czarne_wygraly = 0

    while True:
        
        for event in pygame.event.get():  
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()  
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("---------------------------------------")
                if czy_wybrane_pole == 0:

                    wybrane_pole = lightup_position.copy()

                    if ((1 << convert_position_to_index(wybrane_pole)) & gra.allPiecesTable[currentPlayer]):
                        posible_moves_lightup_positions = []

                        for index in range(64):
                            gra.generateMoves(index)

                        for move in gra.pseudoMoves:
                            if move.getFromSquare() == convert_position_to_index(wybrane_pole):
                                pole = convert_index_to_position(move.getToSquare()).copy()
                                pole[1] += 0.52
                                posible_moves_lightup_positions.append(pole)

                        czy_aktualizacja = 1
                        czy_wybrane_pole = 1
                else:
                    for move in gra.pseudoMoves:
                        if move.getToSquare() == convert_position_to_index(lightup_position) and move.getFromSquare() == convert_position_to_index(wybrane_pole):
                            posible_moves_lightup_positions = []
                            gluLookAt(0,0,-17,0,0,-9,0,1,0)
                            czy_wybrane_pole = 0
                            czy_aktualizacja = 1
                            currentPlayer  = (currentPlayer + 1) % 2
                            # print(currentPlayer)
                            # print(len(gra.pseudoMoves))
                            gra.makeMove(move)
                            made_moves.append(move)

                            if gra.isCheckmate(gra.WHITE):
                                czy_czarne_wygraly = 1
                            elif gra.isCheckmate(gra.BLACK):
                                czy_biale_wygraly = 1

                            gra.pseudoMoves = []
                            
                    
#region sterowanie kursorem
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if currentPlayer  == 1:
                    if lightup_position[0] != 3.5:
                        lightup_position[0] += 1
                        czy_aktualizacja = 1
                else:
                    if lightup_position[0] != -3.5:
                        lightup_position[0] -= 1
                        czy_aktualizacja = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if currentPlayer  == 1:
                    if lightup_position[0] != -3.5:
                        lightup_position[0] -= 1
                        czy_aktualizacja = 1
                else:
                    if lightup_position[0] != 3.5:
                        lightup_position[0] += 1
                        czy_aktualizacja = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if currentPlayer  == 1:
                    if lightup_position[2] != -12:
                        lightup_position[2] -= 1
                        czy_aktualizacja = 1
                else:
                    if lightup_position[2] != -5:
                        lightup_position[2] += 1
                        czy_aktualizacja = 1

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if currentPlayer  == 1:
                    if lightup_position[2] != -5:
                        lightup_position[2] += 1
                        czy_aktualizacja = 1
                else:
                    if lightup_position[2] != -12:
                        lightup_position[2] -= 1
                        czy_aktualizacja = 1
#endregion
        
        if czy_aktualizacja == 1 and czy_biale_wygraly == 0 and czy_czarne_wygraly == 0:
            draw_board(square_positions)
            draw_pieces(gra)

            for i in range(0,len(posible_moves_lightup_positions)):
                lightup(posible_moves_lightup_positions[i],[1,0,0])
            lightup(lightup_position,[0,1,0])
            czy_aktualizacja = 0
            pygame.display.flip()
            pygame.time.wait(10)
        elif czy_biale_wygraly == 1:
            menu('white won')
        elif czy_czarne_wygraly == 1:
            menu('black won')
            


main()