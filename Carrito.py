#Autor: Ivan Olmos Pineda

import math
import agentpy as ap
import numpy as np
import random

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


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

        self.platform = np.array([[3.05, 0.0, 1.0], [1.05, 0.0, 1.0], [1.05, 0.0,-1.0], [3.05, 0.0,-1.0],
                                [3.05, 0.2, 1.0], [1.05, 0.2, 1.0], [1.05, 0.2,-1.0], [3.05, 0.2,-1.0]])

        self.scale = 1
        self.ymin = 0.0
        self.ymax = 4.5
        self.radius = math.sqrt(self.scale**2 + self.scale**2) *2 
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
        #Colision con otros carritos
        self.cubos = []
        self.dCol = 0
        #Estado
        self.estado = 0
        self.rotation = [0.0, 0.0, 0.0]
        
    def drawCircle(self, radius, num_segments):
        glBegin(GL_POLYGON)

        for i in range(num_segments):
            theta = 2.0 * math.pi * float(i) / float(num_segments)

            x = radius * math.cos(theta)
            y = radius * math.sin(theta)

            glVertex3f(x, y, 0.0)

        glEnd()

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

        #Plataforma
        glBegin(GL_QUADS)
        glColor3f(255.0, 233.0, 0.0)
        glVertex3fv(self.platform[0])
        glVertex3fv(self.platform[1])
        glVertex3fv(self.platform[2])
        glVertex3fv(self.platform[3])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(255.0, 233.0, 0.0)
        glVertex3fv(self.platform[4])
        glVertex3fv(self.platform[5])
        glVertex3fv(self.platform[6])
        glVertex3fv(self.platform[7])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(255.0, 233.0, 0.0)
        glVertex3fv(self.platform[0])
        glVertex3fv(self.platform[1])
        glVertex3fv(self.platform[5])
        glVertex3fv(self.platform[4])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(255.0, 233.0, 0.0)
        glVertex3fv(self.platform[1])
        glVertex3fv(self.platform[2])
        glVertex3fv(self.platform[6])
        glVertex3fv(self.platform[5])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(255.0, 233.0, 0.0)
        glVertex3fv(self.platform[2])
        glVertex3fv(self.platform[3])
        glVertex3fv(self.platform[7])
        glVertex3fv(self.platform[6])
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(255.0, 233.0, 0.0)
        glVertex3fv(self.platform[3])
        glVertex3fv(self.platform[0])
        glVertex3fv(self.platform[4])
        glVertex3fv(self.platform[7])
        glEnd()

        #Llantas
        glPushMatrix()
        glTranslatef(-0.8, 0.5, 1.1)
        glColor3f(182.0, 149.0, 192.0)
        self.drawCircle(0.2, 50)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.8, 0.5, 1.1)
        glColor3f(182.0, 149.0, 192.0)
        self.drawCircle(0.2, 50)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.8, 0.5, -1.1)
        glColor3f(182.0, 149.0, 192.0)
        self.drawCircle(0.2, 50)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.8, 0.5, -1.1)
        glColor3f(182.0, 149.0, 192.0)
        self.drawCircle(0.2, 50)
        glPopMatrix()
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        self.rotate([self.Direction[0], 0.0, self.Direction[2]])
        glRotatef(self.rotation[1], 0.0, 1.0, 0.0)
        glScaled(1,1,1)
        glColor3f(1.0, 1.0, 1.0)
        self.drawFaces()
        glPopMatrix()

    def stop(self):
        self.Direction[0] = 0.0
        self.Direction[2] = 0.0

    def pushaway (self):
        self.Direction[0] *= -1.0
        self.Direction[2] *= -1.0

    # resetea al estado 0 despues de haber despositado la caja en el almacen
    def reset(self):
        self.estado = 0
        self.ymin = 0.0
        self.platform[:,1] = 0.0

    # cambia al estado "elevado"
    def elevated(self):
        self.estado = 2

    # incrementa en 0.1 la altura de la plataforma
    def elevate(self):
        self.platform[:,1] += 0.1
        self.ymin += 0.1
        
    def rotate(self, direction):
        # Calcula el ángulo actual de la dirección
        current_angle = math.atan2(direction[2], direction[0])

        # Invierte el ángulo de la dirección
        current_angle *= -1
        
        # Calcula las nuevas componentes x e z de la dirección girada
        new_direction_x = math.cos(current_angle)
        new_direction_z = math.sin(current_angle)

        # Establece la nueva dirección girada
        self.direction = [new_direction_x, 0.0, new_direction_z]

        # Calcula la nueva rotación basada en la nueva dirección
        self.rotation[1] = math.degrees(current_angle)

        self.rotation[1] %= 360.0
        
