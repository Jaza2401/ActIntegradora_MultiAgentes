#Autor: Ivan Olmos Pineda


import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

class Carrito:
    
    def __init__(self, dim, vel):
        #vertices del cubo
        self.base = np.array([[-1.0, 0.0, 1.0], [1.0, 0.0, 1.0], [1.0, 0.0,-1.0], [-1.0, 0.0,-1.0],
                                [-1.0, 0.5, 1.0], [1.0, 0.5, 1.0], [1.0, 0.5,-1.0], [-1.0, 0.5,-1.0]])

        self.pillar1 = np.array([[-0.8, 0.5, 0.8], [-0.8, 0.5, 1.0], [-1.0, 0.5, 1.0], [-1.0, 0.5, 0.8],
                               [-0.8, 3.0, 0.8], [-0.8, 3.0, 1.0], [-1.0, 3.0, 1.0], [-1.0, 3.0, 0.8]])
        
        self.pillar2 = np.array([[1.0, 0.5, 0.8], [1.0, 0.5, 1.0], [0.8, 0.5, 1.0], [0.8, 0.5, 0.8],
                               [1.0, 3.0, 0.8], [1.0, 3.0, 1.0], [0.8, 3.0, 1.0], [0.8, 3.0, 0.8]])
        
        self.pillar3 = np.array([[1.0, 0.5, -1.0], [1.0, 0.5, -0.8], [0.8, 0.5, -0.8], [0.8, 0.5, -1.0],
                               [1.0, 3.0, -1.0], [1.0, 3.0, -0.8], [0.8, 3.0, -0.8], [0.8, 3.0, -1.0]])
        
        self.pillar4 = np.array([[-0.8, 0.5, -1.0], [-0.8, 0.5, -0.8], [-1.0, 0.5, -0.8], [-1.0, 0.5, -1.0],
                               [-0.8, 3.0, -1.0], [-0.8, 3.0, -0.8], [-1.0, 3.0, -0.8], [-1.0, 3.0, -1.0]])
        
        self.roof = np.array([[-1.0, 3.0, 1.0], [1.0, 3.0, 1.0], [1.0, 3.0,-1.0], [-1.0, 3.0,-1.0],
                                [-1.0, 3.3, 1.0], [1.0, 3.3, 1.0], [1.0, 3.3,-1.0], [-1.0, 3.3,-1.0]])
        
        self.front = np.array([[1.05, 0.0, 1.5], [1.05, 0.0, -1.5], [1.05, 4.5, -1.5], [1.05, 4.5, 1.5]])
        
        self.scale = 1
        self.radius = math.sqrt(self.scale**2 + self.scale**2)
        self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        self.Position.append(1.0)
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(random.random())
        self.Direction.append(5.0)
        self.Direction.append(random.random())
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        #Colision
        self.cubos = []
        self.dCol = 0
        

    def update(self):
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]

        self.detCol(new_x, new_z)

        if self.dCol == 0:
            # No hay colisión, actualiza la posición
            self.Position[0] = new_x
            self.Position[2] = new_z
            #detecc de que el objeto no se salga del area de navegacion
            if(abs(new_x) <= self.DimBoard):
                self.Position[0] = new_x
            else:
                self.Direction[0] *= -1.0
                #self.Position[0] += self.Direction[0]
            
            if(abs(new_z) <= self.DimBoard):
                self.Position[2] = new_z
            else:
                self.Direction[2] *= -1.0
                #self.Position[2] += self.Direction[2] 
        else:
            # Hay colisión, detiene el cubo
            self.Direction = [0.0, 0.0, 0.0]
        self.dCol = 0
        
        

    def drawFaces(self):
        
        #Base
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.base[0])
        glVertex3fv(self.base[1])
        glVertex3fv(self.base[2])
        glVertex3fv(self.base[3])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.base[4])
        glVertex3fv(self.base[5])
        glVertex3fv(self.base[6])
        glVertex3fv(self.base[7])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.base[0])
        glVertex3fv(self.base[1])
        glVertex3fv(self.base[5])
        glVertex3fv(self.base[4])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.base[1])
        glVertex3fv(self.base[2])
        glVertex3fv(self.base[6])
        glVertex3fv(self.base[5])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.base[2])
        glVertex3fv(self.base[3])
        glVertex3fv(self.base[7])
        glVertex3fv(self.base[6])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.base[3])
        glVertex3fv(self.base[0])
        glVertex3fv(self.base[4])
        glVertex3fv(self.base[7])
        glEnd()
        
        #Pillar 1
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar1[0])
        glVertex3fv(self.pillar1[1])
        glVertex3fv(self.pillar1[2])
        glVertex3fv(self.pillar1[3])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar1[4])
        glVertex3fv(self.pillar1[5])
        glVertex3fv(self.pillar1[6])
        glVertex3fv(self.pillar1[7])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar1[0])
        glVertex3fv(self.pillar1[1])
        glVertex3fv(self.pillar1[5])
        glVertex3fv(self.pillar1[4])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar1[1])
        glVertex3fv(self.pillar1[2])
        glVertex3fv(self.pillar1[6])
        glVertex3fv(self.pillar1[5])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar1[2])
        glVertex3fv(self.pillar1[3])
        glVertex3fv(self.pillar1[7])
        glVertex3fv(self.pillar1[6])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar1[3])
        glVertex3fv(self.pillar1[0])
        glVertex3fv(self.pillar1[4])
        glVertex3fv(self.pillar1[7])
        glEnd()

        #Pillar 2
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar2[0])
        glVertex3fv(self.pillar2[1])
        glVertex3fv(self.pillar2[2])
        glVertex3fv(self.pillar2[3])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar2[4])
        glVertex3fv(self.pillar2[5])
        glVertex3fv(self.pillar2[6])
        glVertex3fv(self.pillar2[7])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar2[0])
        glVertex3fv(self.pillar2[1])
        glVertex3fv(self.pillar2[5])
        glVertex3fv(self.pillar2[4])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar2[1])
        glVertex3fv(self.pillar2[2])
        glVertex3fv(self.pillar2[6])
        glVertex3fv(self.pillar2[5])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar2[2])
        glVertex3fv(self.pillar2[3])
        glVertex3fv(self.pillar2[7])
        glVertex3fv(self.pillar2[6])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar2[3])
        glVertex3fv(self.pillar2[0])
        glVertex3fv(self.pillar2[4])
        glVertex3fv(self.pillar2[7])
        glEnd()

        #Pillar 3
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar3[0])
        glVertex3fv(self.pillar3[1])
        glVertex3fv(self.pillar3[2])
        glVertex3fv(self.pillar3[3])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar3[4])
        glVertex3fv(self.pillar3[5])
        glVertex3fv(self.pillar3[6])
        glVertex3fv(self.pillar3[7])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar3[0])
        glVertex3fv(self.pillar3[1])
        glVertex3fv(self.pillar3[5])
        glVertex3fv(self.pillar3[4])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar3[1])
        glVertex3fv(self.pillar3[2])
        glVertex3fv(self.pillar3[6])
        glVertex3fv(self.pillar3[5])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar3[2])
        glVertex3fv(self.pillar3[3])
        glVertex3fv(self.pillar3[7])
        glVertex3fv(self.pillar3[6])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar3[3])
        glVertex3fv(self.pillar3[0])
        glVertex3fv(self.pillar3[4])
        glVertex3fv(self.pillar3[7])
        glEnd()

        #Pillar 4
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar4[0])
        glVertex3fv(self.pillar4[1])
        glVertex3fv(self.pillar4[2])
        glVertex3fv(self.pillar4[3])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar4[4])
        glVertex3fv(self.pillar4[5])
        glVertex3fv(self.pillar4[6])
        glVertex3fv(self.pillar4[7])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar4[0])
        glVertex3fv(self.pillar4[1])
        glVertex3fv(self.pillar4[5])
        glVertex3fv(self.pillar4[4])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar4[1])
        glVertex3fv(self.pillar4[2])
        glVertex3fv(self.pillar4[6])
        glVertex3fv(self.pillar4[5])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar4[2])
        glVertex3fv(self.pillar4[3])
        glVertex3fv(self.pillar4[7])
        glVertex3fv(self.pillar4[6])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(54/255, 54/255, 54/255)
        glVertex3fv(self.pillar4[3])
        glVertex3fv(self.pillar4[0])
        glVertex3fv(self.pillar4[4])
        glVertex3fv(self.pillar4[7])
        glEnd()

        #Roof
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.roof[0])
        glVertex3fv(self.roof[1])
        glVertex3fv(self.roof[2])
        glVertex3fv(self.roof[3])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.roof[4])
        glVertex3fv(self.roof[5])
        glVertex3fv(self.roof[6])
        glVertex3fv(self.roof[7])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.roof[0])
        glVertex3fv(self.roof[1])
        glVertex3fv(self.roof[5])
        glVertex3fv(self.roof[4])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.roof[1])
        glVertex3fv(self.roof[2])
        glVertex3fv(self.roof[6])
        glVertex3fv(self.roof[5])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.roof[2])
        glVertex3fv(self.roof[3])
        glVertex3fv(self.roof[7])
        glVertex3fv(self.roof[6])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(114/255, 114/255, 114/255)
        glVertex3fv(self.roof[3])
        glVertex3fv(self.roof[0])
        glVertex3fv(self.roof[4])
        glVertex3fv(self.roof[7])
        glEnd()

        #Front
        glBegin(GL_QUADS)
        glColor3f(1.0, 65/255, 65/255)
        glVertex3fv(self.front[0])
        glVertex3fv(self.front[1])
        glVertex3fv(self.front[2])
        glVertex3fv(self.front[3])
        glEnd()
        
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(1,1,1)
        glColor3f(1.0, 1.0, 1.0)
        self.drawFaces()
        glPopMatrix()
        
    def detCol(self, new_x, new_z):
        for cubo in self.cubos:
            if cubo is not self:
                r1 = self.radius
                r2 = cubo.radius
                cx = (cubo.Position[0] - new_x)**2
                cz = (cubo.Position[2] - new_z)**2
                de = math.sqrt(cx + cz)
                if de - (r1 + r2) < 0.0:
                    self.dCol = 1