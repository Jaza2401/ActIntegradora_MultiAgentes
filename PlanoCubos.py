#Autor: Ivan Olmos Pineda
#Curso: Multiagentes - Graficas Computacionales

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

# Se carga el archivo de la clase Carrito
import sys
sys.path.append('..')
from Carrito import Carrito
from Caja import Caja

# Se carga el archivo de la clase Caja

# Se carga la librería de agentpy
import agentpy as ap

screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=5.0
EYE_Y=15.0
EYE_Z=5.0
CENTER_X=0
CENTER_Y=3
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 50
#Variables para el control del observador
theta = 0.0
radius = DimBoard + 10

pygame.init()

#carrito = carrito(DimBoard, 1.0)
carritos = []
agCarritos = []
ncarritos = 5

#cajas = Caja(DimBoard, 1.0)
cajas = []
ncajas = 50

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def lookat():
    global EYE_X
    global EYE_Z
    global radius
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: carritos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    for i in range(ncarritos):
        carritos.append(Carrito(DimBoard, 1))
        
    for i in range(ncajas):
        cajas.append(Caja(DimBoard, 1))

    for carrito in carritos:
            for caja in cajas:
                caja.detCol(carrito.Position[0], carrito.Position[2], carrito.radius)

def display():  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    #Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    
    for caja in cajas:
        caja.draw()

    #Se dibuja carritos
    for obj in carritos:
        obj.draw()
        obj.update()

    for carrito in carritos:
        for caja in cajas:
            caja.detCol(carrito.Position[0], carrito.Position[2], carrito.radius)
    
def handle_keys():
    global CENTER_X, CENTER_Y, CENTER_Z, EYE_Y, theta

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if theta < 1.0:
            theta = 360.0
        else:
            theta += -1.0
        lookat()
    if keys[pygame.K_RIGHT]:
        if theta > 359.0:
            theta = 0
        else:
            theta += 1.0
        lookat()

'''Aqui tendriamos que poner toda la logica del agente junto con su comportamiento
   igual tenemos que actualizar los valores de cada agente para que se pueda
   mostrar en el motor grafico'''
class CarritoAgent(ap.Agent):
    def __init__(self, position, loaded):
        self.position = position
        self.loaded = loaded #0 = empty, 1 = full

    def step(self):
        #Poner el next y action
        p = self.see() #cajas 
        self.next(p)
        self.action()
        pass

    def update(self):
        pass

    def see(self):
        #Logica para buscar caja cercana
        #Deteccion de colisiones
        pass

    def next(self):
        #Si se detecto colision cambiar variable o sino que siga igual
        pass

    def action(self):
        #Depende si se detecto colision, si no hubo, que siga igual 
        #Aqui va move()
        #Aqui se elimina las cajas del suelo 
        pass

    def move(self):
        #Definir el movimiento del carrito, incluido cuando encuentra una caja
        pass

done = False
Init()
while not done:
    handle_keys()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    for obj in agCarritos:
        obj.step()

    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()