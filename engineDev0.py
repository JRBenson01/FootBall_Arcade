import pygame, sys
from pygame.locals import *
pygame.init()

class gameWindow(object):
    def __init__(self, length, height, caption):
        self.length = length
        self.height = height
        self.caption = caption
        self.clock = pygame.clock()
        self.display = pygame.display.set_mode((length, height))
        self.exit = False

    def set_background(self, background):
        background = pygame.transform.scale(background, (length, height))
        self.display.blit(background, (0, 0))

    def frame():
        

    def exitCheck(self):
        if self.exit == False:
            pygame.quit()
            sys.exit()

class gameAction(object):
    def __init__(self):
        

    def setAction(self, action, key_bind, action_function):
        self.action = action 
