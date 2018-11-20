"""
Designer:       Justin Benson
Version:        5
Description:    Version 5 allows for a more organized version for gamePiece physics
"""




import pygame, sys
from pygame.locals import *
import time
import math
pygame.init()


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
            for base in pic.__class__.__bases__:
                if base.__name__ == "gamePiece":
                    if pic.get_collidable():
                        print(pic.name, '\t', "set to collidable in ", self.name, '\t', "scene.") 
                        self.collidables.append(pic)

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
        """
        for i in range(len(self.collidables)):
            for j in range((i+1), len(self.collidables)):
                self.collidables[i].collision(self.collidables[j])
        
        keys = pygame.key.get_pressed()
        if self.playerInput:
            player.input(keys)
        if self.function_use:
            self.function()
        
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

#button class is for use of buttons and/or text with game UI
class button(object):
    def __init__(self, text):
        self.text = text
        self.normal_color = dull_magenta.get()
        self.trigger_color = magenta.get()
        self.click_color = violet.get()
        self.use_color = dull_magenta.get()
        self.font_size = 22
        self.font = pygame.font.Font("arial.ttf", self.font_size)
        self.width = 100
        self.height = 100
        self.xPos = gameWindow.width/2
        self.yPos = gameWindow.height/2
        self.box = True
        self.angle = 0
        self.order = 2
        self.triggered = False
        self.clicked = False
        self.interact = True
        self.stat_dic = {
                         "text"         : self.set_text,
                         "normal_color" : self.set_normal_color,
                         "trigger_color": self.set_trigger_color,
                         "click_color"  : self.set_click_color,
                         "font"         : self.set_font,
                         "font_size"    : self.set_font_size,
                         "size"         : self.set_tup_size,
                         "length"       : self.set_length,
                         "height"       : self.set_height,
                         "pos"          : self.set_tup_pos,
                         "position"     : self.set_pos,
                         "box"          : self.set_box,
                         "order"        : self.set_order,
                         "interact"     : self.set_interact,
                         "interactable" : self.set_interact
                         }
                         

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_tup_size(self, size):
        self.width = size[0]
        self.height = size[1]

    def set_width(self, width):
        self.width = width

    def set_length(self, length):
        self.width = length

    def set_height(self, height):
        self.height = height

    def set_font(self, use_font):
        self.font = pygame.font.Font(use_font, self.font_size)

    def set_font_size(self, size):
        self.font_size = size
        self.font = pygame.font.Font("arial.ttf", self.font_size)

    def set_normal_color(self, color):
        self.normal_color = color.get()

    def set_trigger_color(self, color):
        self.trigger_color = color.get()

    def set_click_color(self, color):
        self.click_color = color.get()

    def set_text(self, text):
        self.text = text

    def set_pos(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    def set_tup_pos(self, pos):
        self.xPos = pos[0]
        self.yPos = pos[1]

    def set_xpos(self, xpos):
        self.xPos = xpos

    def set_ypos(self, ypos):
        self.yPos = ypos

    def set_box(self, value):
        self.box = value

    def set_interact(self, value):
        self.interact = value

    def no_box(self):
        self.box = False

    def rotate(self, angle):
        self.angle = angle

    def set_order(self, order):
        self.order = order

    def set_stats(self, stats):
        print("==============================")
        for stat in stats:
            for element in self.stat_dic:
                if element == stat:
                    if element == "normal_color" or element == "trigger_color" or element == "click_color":
                        print(self.text, "button", element, "set to color", stats[stat].name())
                    else:
                        print(self.text, "button", element, "set to", stats[stat])
                    self.stat_dic[element](stats[stat])
        print("==============================")

    def ret_clicked(self):
        return self.clicked

    def ret_left_side(self):
        return self.xPos - self.width/2

    def reset(self):
        self.triggered = False
        self.clicked = False

    def display(self):
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        click = pygame.mouse.get_pressed()[0]
        
        #Positions relative to upper left corner. 
        #                       X Position                  Y Position              dimensions of button
        disp_specs = ((self.xPos - (self.width/2)), (self.yPos - (self.height/2)), self.width, self.height)
        if self.box and self.interact:
            if mouse_x > (self.xPos - self.width/2) and mouse_x < (self.xPos + self.width/2):
                if mouse_y > (self.yPos - self.height/2) and mouse_y < (self.yPos + self.height/2):
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

        #Code to rotate text on the button
        if self.angle != 0:
            textSurface = pygame.transform.rotate(textSurface, self.angle)

        #Makes a rectangle based on the surface of the text amd then centers to text surface
        textBox = textSurface.get_rect()
        textBox.center = (self.xPos, self.yPos)

        #Draws box behind text if user indicates if this not simply a text object
        if self.box:
            pygame.draw.rect(gameWindow.display, self.use_color, (disp_specs))

        #Sending to display manager that object is to be displayed (display() function still needs to be called)
        gameWindow.display.blit(textSurface, textBox)


#gamePiece is the class used for all elements of the game
class gamePiece(object):
    def __init__(self, name):
        self.name = name
        self.gravity = False
        self.collidable = True
        self.position = (0, 0)
        self.orgPosition = (0, 0)
        self.length = 100
        self.height = 100
        self.hb_length = 100
        self.hb_height = 100
        self.hb_type = "circle"
        self.triggered = False
        self.use_image = False
        self.sprite = ""
        self.sprites = []
        self.spritecount = 0
        self.angle = 0
        self.prevAngle = 0
        self.speed = 1
        self.order = 1
        self.const_daze = 500
        self.daze = 0
        self.stat_dic = {
                        "collidable": self.set_collidable,
                        "pos"       : self.set_pos,
                        "position"  : self.set_pos,
                        "length"    : self.set_length,
                        "height"    : self.set_height,
                        "sprite"    : self.add_sprite,
                        "sprites"   : self.set_sprites,
                        "speed"     : self.set_speed,
                        "order"     : self.set_order
                        }

    def set_collidable(self, value):
        self.collidable = value
    
    def set_pos(self, x, y):
        self.position = (x, y)
        self.orgPosition = (x, y)

    def set_hitbox(self, length, height):
        self.hb_length = length
        self.hb_height = height

    def set_hb(self, length, height):
        self.hb_length = length
        self.hb_height = height

    def add_sprite(self, image):
        self.use_image = True
        self.sprites.append(pygame.image.load(image))
        self.sprite = self.sprites[0]

    def set_sprites(self, images):
        for image in images:
            self.add_sprite(image)

    def set_length(self, length):
        self.length = length

    def set_height(self, height):
        self.height = height
        
    def set_size(self, length, height):
        self.length = length
        self.height = height
        if self.use_image:
            self.sprite = pygame.transform.scale(self.sprite, (self.length, self.height))

    def set_speed(self, speed):
        self.speed = speed

    def set_hb_type(self, hb_type):
        self.hb_type = hb_type

    def set_order(self, order):
        self.order = order

    def set_stats(self, stats):
        print("==============================")
        for stat in stats:
            for element in self.stat_dic:
                if element == stat:
                    print(self.name, element, "set to", stats[stat])
                    self.stat_dic[element](stats[stat])
        print("==============================")

    def get_collidable(self):
        return self.collidable

    def get_hb(self):
        xPos = self.position[0]
        yPos = self.position[1]
        xMin = xPos - self.hb_length/2
        xMax = xPos + self.hb_length/2
        yMin = yPos - self.hb_height/2
        yMax = yPos + self.hb_height/2
        return (xMin, xMax, yMin, yMax)

    def orientUpdate(self):
        if self.angle == 'v' and self.prevAngle != 'v':
            self.sprite = pygame.transform.rotate(self.sprite, 90)
        elif self.angle == 'h' and self.prevAngle != 'h':
            self.sprite = pygame.transform.rotate(self.sprite, -90)
        self.prevAngle = self.angle

    def reset(self):
        self.angle = 0
        self.triggered = False

    def move(self):
        angle = rad(self.angle)
        xPos = self.position[0]
        yPos = self.position[1]
        D_x = self.speed*math.cos(angle)
        D_y = self.speed*math.sin(angle)
        if xPos <= 50 and D_x < 0:
            print("left border hit")
        else:
            xPos = self.position[0] + ((self.speed)*math.cos(angle))
        
        if yPos >= gameWindow.height-50 and D_y < 0:
            print("lower border hit")
        elif yPos <= 50 and D_y > 0:
            print("upper border hit")
        else:
            yPos = self.position[1] - ((self.speed)*math.sin(angle))
            
        self.position = (xPos, yPos)
        if self.angle % 90 == 0:
            self.sprite = pygame.transform.rotate(self.sprites[0], self.angle - 90)
        else:
            self.sprite = pygame.transform.rotate(self.sprites[1], self.angle - 45)
        self.prevAngle = self.angle

    def get_triggered(self):
        return self.triggered

    def chase(self, piece):
        if self.daze <= 0:
            D_x = int(piece.position[0] - self.position[0])
            D_y = int(self.position[1] - piece.position[1])
            if D_x == 0:
                D_x = 1
            self.angle = deg(math.atan(D_y/D_x))
            if D_x < 0:
                self.angle = self.angle + 180
            self.angle = angleRound(self.angle)
        else:
            self.daze -= 1
        self.move()

    def collision(self, collider):
        if self.hb_type == "circle":
            x_dist = math.fabs(self.position[0] - collider.position[0])
            y_dist = math.fabs(self.position[1] - collider.position[1])
            maxRad = self.length/2 + collider.length/2
            distance = math.sqrt(x_dist**2 + y_dist**2)
            #print("maxRad =", maxRad, "  distance =", distance)
            if distance <= maxRad:
                self.triggered = True
                collider.triggered = True
            else:
                self.triggered = False
                collider.triggered = False
                
            if self.triggered == True:
                dummyangle = self.angle
                self.angle = collider.angle
                collider.angle = dummyangle
                self.daze = 100
                collider.daze = 100
                return True

    def logic(self):
        

    def display(self):
        #True positions of player
        xPos = self.position[0]
        yPos = self.position[1]

        #Converted position to be placed
        xMin = xPos - self.length/2
        yMin = yPos - self.height/2
        if self.use_image:
            gameWindow.display.blit(self.sprite, (xMin, yMin))
        else:
            disp_specs = ((xPos - (self.length/2)), (yPos - (self.height/2)), self.length, self.height)
            pygame.draw.rect(gameWindow.display, black, (disp_specs))
            
#player class is a subset of the game piece class for the player character
class _player(gamePiece):
    def __init__(self, name):
        gamePiece.__init__(self, name)
    #Gathers keyboard input, converts it to x/y axis values and then to an angle value
    def input(self, keys):
        move = True     #Determines if the player needs to move
        
        #Vertical and horizontal axies for determining motion
        vert = 0
        hor = 0

        #Direction for player to move
        self.angle = 0

        #Gathering keyboard input and setting to axies
        if keys[K_w]:
            vert = 1
        if keys[K_s]:
            vert = -1
        if keys[K_a]:
            hor = -1
        if keys[K_d]:
            hor = 1

        #Converting axis values into angles
        if vert == 0 and hor != 0:
            self.angle = 90 - (90 * hor)
        elif hor == 0 and vert != 0:
            self.angle = 180 - (90 * vert)
        elif vert != 0 and hor != 0:
            if vert == 1 and hor == -1:
                self.angle = 135
            elif vert == 1 and hor == 1:
                self.angle = 45
            elif vert == -1 and hor == -1:
                self.angle = 225
            elif vert == -1 and hor == 1:
                self.angle = 315
        else:
            move = False    #Triggered if neither axis has a value
        if move:
            self.move()

class npc(gamePiece):
    def __init__(self, name):
        gamePiece.__init__(self, name)

    """
    def chase(self, player):
        D_x = int(player.position[0] - self.position[0])
        D_y = int(self.position[1] - player.position[1])
        if D_x == 0:
            D_x = 1
        self.angle = deg(math.atan(D_y/D_x))
        if D_x < 0:
            self.angle = self.angle + 180
        #print("Change X:", D_x, " Change Y:", D_y, " Angle:", self.angle)
        self.angle = angleRound(self.angle)
        self.move()
    """

class game_Data(object):
    def __init__(self):
        self.level1Complete = False
        self.level2Complete = False
        self.level3Complete = False
        self.currentLevel = 0

    def set_current_level(self, num):
        self.currentLevel = num

    def next_level(self):
        self.currentLevel += 1

    def ret_level(self):
        return self.currentLevel

    def ret_complete(self, num):
        if num == 1 and self.level1Complete:
            return True
        elif num == 2 and self.level2Complete:
            return True
        if num == 3 and self.level3Complete:
            return True

    def level_complete(self):
        if self.currentLevel == 1:
            self.level1Complete = True
            print("Level 1 complete")
        elif self.currentLevel == 2:
            self.level2Complete = True
            print("Level 2 complete")
        elif self.currentLevel == 3:
           self.level3Complete = True
           print("Level 3 complete")

    def disp_levels(self):
        print("========STATS========")
        print_string = "Level 1: "
        if self.level1Complete:
            print_string = print_string + "Complete"
        else:
            print_string = print_string + "Incomplete"
        print(print_string)
        print_string = "Level 2: "
        if self.level2Complete:
            print_string = print_string + "Complete"
        else:
            print_string = print_string + "Incomplete"
        print(print_string)
        print_string = "Level 3: "
        if self.level3Complete:
            print_string = print_string + "Complete"
        else:
            print_string = print_string + "Incomplete"
        print(print_string)
        print("=====================")

#Boot-up message
print("+++Starting up+++")
print("+++Loading Assets+++")


#Always constant variables
gameWindow = game_Window()
gameAction = game_Action()
gameData = game_Data()
player = _player("player")

fps_display = button("FPS: ")
fps_display.set_pos(70, 20)
fps_display.no_box()
