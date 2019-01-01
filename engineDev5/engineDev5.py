"""
Designer:       Justin Benson
Version:        5.0
Description:    Version 5.0 better compartmentalizes its classes to allow for
                better versatality across all games
"""


import pygame, sys
from pygame.locals import *
import time
import math
pygame.init()

Debugging = True

class color(object):
    def __init__(self, name, color_code):
        self.color_name = name
        self.color_code = color_code

    def ret_code(self):
        return self.color_code

    def code(self):
        return self.color_code

    def get(self):
        return self.color_code

    def name(self):
        return self.color_name

#Variables for different color codes
white = color("white", (255, 255, 255))
black = color("black", (0, 0, 0))
red = color("red", (255, 0, 0))
dim_red = color("dim red", (125, 0, 0))
orange = color("orange", (255, 125, 0))
yellow = color("yellow", (255, 255, 0))
spring_green = color("spring green", (125, 255, 0))
green = color("green", (0, 255, 0))
turquoise = color("turquoise", (0, 255, 125))
cyan = color("cyan", (0, 255, 255))
ocean = color("ocean", (0, 125, 255))
blue = color("blue", (0, 0, 255))
violet = color("violet", (125, 0, 255))
magenta = color("magenta", (255, 0, 255))
dull_magenta = color("dull magenta", (125, 0, 125))
raspberry = color("raspberry", (255, 0, 125))
brown = color("brown", (126, 46, 31))
gray = color("gray", (125, 125, 125))

#Function to convert a value from degrees to radians
def rad(degrees):
    return ((degrees * math.pi)/180)

#Function to convert a value form radians to degrees
def deg(radians):
    return ((180 * radians)/math.pi)

#Rounds angle to nearest 45 degree; rounds to closest 90 if in between
"""
For the sake of simplicity, the pieces will only move in 45-degree
directions. The finction just finds that closest angle
"""
def angleRound(Val):
    if Val < 0:
        Val = 360 + Val
    if Val > 0 and Val <= 22.5:
        angle = 0
    elif Val > 22.5 and Val < 67.5:
        angle = 45
    elif Val >= 67.5 and Val <= 112.5:
        angle = 90
    elif Val > 112.5 and Val < 157.5:
        angle = 135
    elif Val >= 157.5 and Val <= 202.5:
        angle = 180
    elif Val > 202.5 and Val < 247.5:
        angle = 225
    elif Val >= 247.5 and Val <= 292.5:
        angle = 270
    elif Val > 292.5 and Val < 337.5:
        angle = 315
    elif Val >= 337.5 and Val <= 360:
        angle = 0
    else:
        angle = 0
    return angle

#game_Window class deals with all aspects of displaying things on-screen
class game_Window(object):
    def __init__(self):
        self.height = 100
        self.width = 100
        self.display = pygame.display.set_mode((self.width, self.height))
        self.caption = ""
        self.frameCount = 0
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.fps_cap = 90
        self.use_background_image = False
        self.background_color = white
        self.fullscreen = True

    def display(self):
        return self.display

    def set_res(self, width, height):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))

    def set_caption(self, caption):
        self.caption = caption
        pygame.display.set_caption(caption)

    def set_background_image(self, image):
        self.use_background_image = True
        self.background = pygame.image.load(image)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def set_background_color(self, color):
        self.background_color = color.get()

    def set_fps_cap(self, fps_cap):
        self.fps_cap = fps_cap

    def set_fullscreen(self):
        self.display = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN) 

    def gameExit(self):
        print("exiting game")
        pygame.quit()
        sys.exit()

    def frameUpdate(self):
        self.clock.tick()
        self.fps = int(self.clock.get_fps() + 1)
        fps_message = str("FPS: %s" % self.fps)
        fps_display.set_text(fps_message)
        pygame.display.update()

#game_Action class manages all game logic. ALL events are managed by this class
class game_Action(object):
    def __init__(self):
        self.exit = False
        self.current_scene = "start"
        self.scenes = []

    def add_scene(self, scene):
        self.scenes.append(scene)
        
        if Debugging:
            sceneNames = ""
            print("New scene added:", scene.name)
            for addedScene in self.scenes:
                sceneNames = sceneNames + addedScene.name + " "
            print("Complete List:", sceneNames)

    def change_scene(self, scene):
        self.current_scene = scene
        for scene in self.scenes:
            if scene.name == self.current_scene:
                scene.start()

    def exit(self):
        self.exit = True

    def gameLoop(self):
        while self.exit == False:
            for scene in self.scenes:
                if scene.name == self.current_scene:
                    scene.run()
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameWindow.gameExit()
            gameWindow.frameUpdate()
        gameWindow.gameExit()

def ret_order(pic):
    return pic.order

class scene(object):
    def __init__(self, name):
        self.name = name
        self.background_color = black.get()
        self.background_image = ""
        self.pieces = []
        self.collidables = []
        self.function = 0
        self.function_use = False
        self.function_start = 0
        self.function_start_use = False
        self.playerInput = False
        self.sceneStay = True

    def set_background_color(self, color):
        if Debugging:
            print(self.name, "scene background color set to:", color.name())
            
        self.background_color = color.get()

    def set_function(self, function):
        self.function = function
        self.function_use = True

    def set_function_start(self, func):
        self.function_start = func
        self.function_start_use = True

    def add_piece(self, pic):
        found = False
        for piece in self.pieces:
            if piece == pic:
                found = True
        if not found:
            self.pieces.append(pic)
            self.pieces.sort(key=ret_order)

            if Debugging:
                print("%s added to %s scene" % (pic.name, self.name))
            
            for base in pic.__class__.__bases__:
                if base.__name__ == "gamePiece":
                    if pic.get_collidable():
                        self.collidables.append(pic)
                        
                        if Debugging:
                            print(pic.name, '\t', "set to collidable in ", self.name, '\t', "scene.") 

    def add_pieces(self, pics):
        for pic in pics:
            self.add_piece(pic)
        self.pieces.sort(key=ret_order)
    def del_piece(self, pic):
        self.pieces.remove(pic)
        self.pieces.sort(key=ret_order)

    def set_playerInput(self, value):
        self.playerInput = value

    def run(self):
        """
        for collider in self.collidables:
            if collider.__class__.__name__ == "npc":
                player.collision(collider)
        
        for i in range(len(self.collidables)):
            for j in range((i+1), len(self.collidables)):
                self.collidables[i].collision(self.collidables[j])
        
        keys = pygame.key.get_pressed()
        if self.playerInput:
            player.input(keys)
        if self.function_use:
            self.function()
        """
        #Display section
        if self.background_image != "":
            gameWindow.display.blit(self.background, (0, 0))
        else:
            pygame.draw.rect(gameWindow.display, self.background_color, (0, 0, gameWindow.width, gameWindow.height))
        for piece in self.pieces:
            piece.display()

    def start(self):
        for piece in self.pieces:
            piece.reset()
        if self.function_start_use:
            self.function_start()


class physObject(object):
    def __init__(self):
        #Universal Properties
        self.name = self.__class__.__name__ + " object"
        
        #Physical Properties
        self.length = 1
        self.height = 1
        self.position = (0, 0)

        #Display Properties
        self.use_image = False
        self.sprites = []
        self.order = 1

        #Logic Properties
        self.triggered = False
        
        #Dictionary for setting functions
        self.stat_dic = {
                        "pos"       : self.set_pos,
                        "position"  : self.set_pos,
                        "length"    : self.set_length,
                        "height"    : self.set_height,
                        "size"      : self.set_size,
                        "sprite"    : self.add_sprite,
                        "sprites"   : self.set_sprites,
                        "order"     : self.set_order,
                        "name"      : self.set_name
                        }
        
    def set_pos(self, pos):
        self.position = pos

    def set_length(self, length):
        self.length = length

    def set_height(self, height):
        self.height = height

    def set_size(self, size):
        self.set_length(size[0])
        self.set_height(size[1])

    def add_sprite(self, image):
        self.use_image = True
        self.sprites.append(pygame.image.load(image))
        self.sprite = self.sprites[0]

    def set_sprites(self, images):
        for image in images:
            self.add_sprite(image)

    def set_order(self, order):
        self.order = order

    def set_name(self, name):
        self.name = name

    def set_stats(self, stats):
        if Debugging:
            print("====+ Setting stats for %s +====" % self.name)
            
        for stat in stats:
            for element in self.stat_dic:
                if element == stat:
                    #if element == "normal_color" or element == "trigger_color" or element == "click_color":
                    #    print(self.text, "button", element, "set to color", stats[stat].name())
                    #else:
                    #    print(self.text, "button", element, "set to", stats[stat])
                    self.stat_dic[element](stats[stat])
                    if Debugging:
                        print("%s set to: %s" % (element, str(stats[stat])))
        if Debugging:
            print("====+ Done with %s +====" % self.name)

class gamePiece(physObject):
    def __init__(self):

        #Parameters from  physObject
        physObject.__init__(self)

        #Movement Properties
        self.angle = 0
        self.speed = 1

        #Dictionary for setting functions
        stat_dic =      {
                        "angle"     : self.set_angle,
                        "speed"     : self.set_speed
                        }
        self.stat_dic = {**self.stat_dic, **stat_dic}

    def set_angle(self, angle):
        self.angle = angle

    def set_speed(self, speed):
        self.speed = speed

class button(physObject):
    def __init__(self):

        #Parameters from physObject
        physObject.__init__(self)

        #Interaction Properties
        self.interactable = True
        
        #Display Properties
        self.box = True
        self.text = ""
        self.font_type = "arial.ttf"
        self.font_size = 22
        self.font = pygame.font.Font(self.font_type, self.font_size)
        self.normal_color = dull_magenta.get()
        self.trigger_color = magenta.get()
        self.click_color = violet.get()
        self.use_color = dull_magenta.get()

        #Dictionary for setting functions
        stat_dic =      {
                        "interactable"  : self.set_interactable,
                        "box"           : self.set_box,
                        "text"          : self.set_text,
                        "font"          : self.set_font_type,
                        "font_size"     : self.set_font_size,
                        "normal_color"  : self.set_normal_color,
                        "trigger_color" : self.set_trigger_color,
                        "click_color"   : self.set_click_color
                        }
        self.stat_dic = {**self.stat_dic, **stat_dic}
        
    def set_interactable(self, value):
        self.interactable = value
    
    def set_box(self, value):
        self.box = value

    def set_text(self, text):
        self.text = text
        if self.name == self.__class__.__name__ + " object":
            newName = text + " button"
            if Debugging:
                print("%s name changed to: %s" % (self.name, newName))
            self.name = newName

    def set_font(self):
        self.font = pygame.font.Font(self.font_type, self.font_size)
    
    def set_font_type(self, font_type):
        self.font_type = font_type
        self.set_font()

    def set_font_size(self, font_size):
        self.font_size = font_size
        self.set_font()

    def set_normal_color(self, color):
        self.normal_color = color.get()

    def set_trigger_color(self, color):
        self.trigger_color = color.get()

    def set_click_color(self, color):
        self.click_color = color.get()

    def display(self):
        xPos = self.position[0]
        yPos = self.position[1]

        #print(self.position)
        
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        click = pygame.mouse.get_pressed()[0]
        
        #Positions relative to upper left corner. 
        #                       X Position                  Y Position              dimensions of button
        disp_specs = ((xPos - (self.length/2)), (yPos - (self.height/2)), self.length, self.height)
        if self.box and self.interact:
            if mouse_x > (xPos - length/2) and mouse_x < (xPos + length/2):
                if mouse_y > (yPos - self.height/2) and mouse_y < (yPos + self.height/2):
                    self.use_color = self.trigger_color
                    self.triggered = True
                else:
                    self.use_color = self.normal_color
                    self.triggered = False
            else:
                self.use_color = self.normal_color
                self.triggered = False
        else:
            self.use_color = self.normal_color
            self.triggered = False
        
        if self.triggered:
            if click:
                self.use_color = self.click_color
                self.clicked = True
            else:
                self.use_color = self.trigger_color
                self.clicked = False

        
        #Surface that text will be displayed on
        textSurface = self.font.render(self.text, True, black.get())

        """
        #Code to rotate text on the button
        if self.angle != 0:
            textSurface = pygame.transform.rotate(textSurface, self.angle)
        """

        #Makes a rectangle based on the surface of the text amd then centers to text surface
        textBox = textSurface.get_rect()
        textBox.center = self.position

        #Draws box behind text if user indicates if this not simply a text object
        if self.box:
            pygame.draw.rect(gameWindow.display, self.use_color, (disp_specs))

        #Sending to display manager that object is to be displayed (display() function still needs to be called)
        gameWindow.display.blit(textSurface, textBox)

#Boot-up message
print("+++Starting up+++")
print("+++Loading Assets+++")


#Always constant variables
gameWindow = game_Window()
gameAction = game_Action()

fps_display = button()
fps_display_stats = {
                    "box"   : False,
                    "pos"   : (70, 20),
                    "text"  : "FPS: "
                    }
fps_display.set_stats(fps_display_stats)
