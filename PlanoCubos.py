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
ncarritos = 1

#cajas = Caja(DimBoard, 1.0)
cajas = []
ncajas = 40


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
        carrito = Carrito(DimBoard, 1)
        carritos.append(CarritoWrapper(carrito))
        
    for i in range(ncajas):
        cajas.append(Caja(DimBoard, 1))

    # for carrito in carritos:
    #         for caja in cajas:
    #             caja.detCol(carrito.Position[0], carrito.Position[2], carrito.radius)

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

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3d(DimBoard * 1.5, 0, -DimBoard * 0.5)
    glVertex3d(DimBoard * 1.5, 0, DimBoard * 0.5)
    glVertex3d(DimBoard, 0, DimBoard * 0.5)
    glVertex3d(DimBoard, 0, -DimBoard * 0.5)
    glEnd()
    
    for caja in cajas:
        caja.draw()

    for carrito_wrapper in carritos:
        carrito_wrapper.carrito.draw()
        carrito_wrapper.agente.step()

    for carrito_wrapper in carritos:
        carrito = carrito_wrapper.carrito  # Access the Carrito instance within the wrapper
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

class CarritoWrapper:
    def __init__(self, carrito):
        self.carrito = carrito
        self.agente = CarritoAgent(carrito)

'''Aqui tendriamos que poner toda la logica del agente junto con su comportamiento
   igual tenemos que actualizar los valores de cada agente para que se pueda
   mostrar en el motor grafico'''
class CarritoAgent(ap.Agent):
    def __init__(self, carrito):
        self.carrito = carrito
        self.dCol = 0
        self.stop = 0

    def step(self):
        # Poner el next y action
        p = self.see(cajas)
        self.next(p)
        self.action()

    def see(self, c):
        # Logica para buscar caja cercana
        # Deteccion de colisiones
        return c

    def next(self, p):
            # Si se detecto colision cambiar variable o sino que siga igual
        new_x = self.carrito.Position[0] + self.carrito.Direction[0]
        new_z = self.carrito.Position[2] + self.carrito.Direction[2]

        if self.dCol == 0:
            print("buscando colision")
            for caja in p:
                r1 = self.carrito.radius
                r2 = caja.radius
                cx = (caja.Position[0] - new_x)**2
                cz = (caja.Position[2] - new_z)**2
                de = math.sqrt(cx + cz)
                if de - (r1 + r2) < 0.0:
                    p.remove(caja)
                    self.dCol = 1
        else:
            print("colision encontrada")

    def action(self):
        # Dependiendo de si se detecto colision, actualizar el estado del agente
        if self.dCol == 0:
            # No hay colisión, actualiza la posición
            new_x = self.carrito.Position[0] + self.carrito.Direction[0]
            new_z = self.carrito.Position[2] + self.carrito.Direction[2]
            # detección de que el objeto no se salga del área de navegación
            if abs(new_x) <= self.carrito.DimBoard:
                self.carrito.Position[0] = new_x
            else:
                self.carrito.Direction[0] *= -1.0

            if abs(new_z) <= self.carrito.DimBoard:
                self.carrito.Position[2] = new_z
            else:
                self.carrito.Direction[2] *= -1.0
        else:
            #self.dCol = 0
            target_x = self.carrito.DimBoard
            target_z = 0.0
            # Calcular la nueva dirección hacia el punto específico
            delta_x = target_x - self.carrito.Position[0]
            delta_z = target_z - self.carrito.Position[2]
            distance = math.sqrt(delta_x**2 + delta_z**2)
            
            if distance > 0.0:
                # Normalizar la dirección
                new_direction_x = delta_x / distance
                new_direction_z = delta_z / distance
                # Establecer la nueva dirección
                self.carrito.Direction = [new_direction_x, 0.0, new_direction_z]
            else:
                # El carro ya está en el punto específico, no hay necesidad de cambiar la dirección
                self.dCol = 0

        self.dCol = 0

done = False
Init()
while not done:
    handle_keys()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()