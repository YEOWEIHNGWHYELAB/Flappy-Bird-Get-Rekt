# Flappy Bird Main Engine

import numpy as np
import math
import random
import matplotlib.pyplot as plt
import pygame
import time
import tkinter as tk
from tkinter import messagebox

class BirdFly(object):
    def __init__(self):
        self.height_bird = 330
        self.bird_X = 60
        self.min_Y = 0
        self.max_Y = 660
        self.bird = pygame.image.load('./Images/bird.png')
        self.delta_Fall = 20
        self.delta_Flap = 90
        self.is_Depressed = False

    def birdHeight(self):
        return self.height_bird

    # Keyboard Control
    def manualMove(self, win):
        # Event Handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] == 1 and (not self.is_Depressed):
            isFlap = True
            self.is_Depressed = True
        elif keys[pygame.K_SPACE] == 0:
            self.is_Depressed = False
            isFlap = False
        else:
            isFlap = False

        # Flap Logic
        if isFlap:
            if self.height_bird <= self.min_Y:
                self.height_bird = self.min_Y
            else:
                self.height_bird -= self.delta_Flap

            win.blit(self.bird, (self.bird_X, self.height_bird))
        else:
            if self.height_bird >= self.max_Y:
                self.height_bird = self.max_Y
            else:
                self.height_bird += self.delta_Fall

            win.blit(self.bird, (self.bird_X, self.height_bird))

class ObstaclesPipe(object):
    def __init__(self, pos):
        self.velocity = 8
        self.listArray_slit_Pos = [1220, 1220, 1220, 1220]
        self.listArray_slit_Pos_Ini = [True, False, False, False]
        self.resolutionX = 1280
        self.resolutionY = 720
        self.slit_height = [500, 500, 500, 500]
        self.slit_size = 200
        self.slit_Pos = pos
        self.isInitialized = False

    def getPosList(self):
        return self.listArray_slit_Pos

    def getHeightList(self):
        return self.slit_height

    def move(self, win):
        for i in range(0, 4):
            if self.listArray_slit_Pos_Ini[i] is True:
                height = self.slit_height[i]

                # Top Part
                pygame.draw.rect(win, (0, 255, 0), pygame.Rect(self.listArray_slit_Pos[i], 0, 60, height - self.slit_size))

                # Bottom Part
                pygame.draw.rect(win, (0, 255, 0), pygame.Rect(self.listArray_slit_Pos[i], height, 60, 720 - height))

                # Initialization Check
                if (self.isInitialized is False and i == 0) and (self.listArray_slit_Pos[i] <= 900) and (self.listArray_slit_Pos[i] >= 580):
                    self.listArray_slit_Pos_Ini[1] = True
                elif (self.isInitialized is False and i == 0) and (self.listArray_slit_Pos[i] <= 580) and (self.listArray_slit_Pos[i] >= 260):
                    self.listArray_slit_Pos_Ini[2] = True
                elif (self.isInitialized is False and i == 0) and (self.listArray_slit_Pos[i] <= 260):
                    self.listArray_slit_Pos_Ini[3] = True
                    self.isInitialized = True

                # Move Pipe
                self.listArray_slit_Pos[i] -= 20

                # Reset Pipe Position
                if self.listArray_slit_Pos[i] <= 0:
                    self.listArray_slit_Pos[i] = 1220
                    self.slit_height[i] = random.randint(200, 660)
