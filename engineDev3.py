"""
Designer:      Justin Benson
Version:       3
Description:   Version 3 adds abilities to set object variables via dictionary instead of using
               individual functions to set each variable. In version 3 colors are now objects 
               instead of individual variables.
"""
print("+++Starting up+++")
print("+++Loading Assets+++")




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
        self.fps = int(self.clock.get_fps())
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
        keys = pygame.key.get_pressed()
        if self.function != 0:
            self.function
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

    def chase(self, player):
        D_x = int(player.position[0] - self.position[0])
        D_y = int(self.position[1] - player.position[1])
        gameData.set_truePos((D_x, D_y))
        D_x = gameData.ret_viewPos()[0]
        D_y = gameData.ret_viewPos()[1]
        if D_x == 0:
            D_x = 1
        self.angle = deg(math.atan(D_y/D_x))
        if D_x < 0:
            self.angle = self.angle + 180
        #print("Change X:", D_x, " Change Y:", D_y, " Angle:", self.angle)
        self.angle = angleRound(self.angle)
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
                
            if self.triggered == True:
                print (self.name, "Collision detected with", collider.name)
                return True

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

#Following code needs to be revised and replaced somewhere more modular so all scenes can access it
"""
        if scene == "Main":
            if self.use_background_image:
                self.display.blit(self.background, (0, 0))
            else:
                pygame.draw.rect(self.display, self.background_color, (0, 0, self.width, self.height))
            mainFrameUpdate()
        elif scene == "Lose":
            pygame.draw.rect(self.display, self.background_color, (0, 0, self.width, self.height))
            loseFrameUpdate()
        elif scene == "Win":
            pygame.draw.rect(self.display, self.background_color, (0, 0, self.width, self.height))
            winFrameUpdate()
"""
#Always constant variables
gameWindow = game_Window()
gameAction = game_Action()
gameData = game_Data()
player = _player("player")

fps_display = button("FPS: ")
fps_display.set_pos(70, 20)
fps_display.no_box()

#Main game variables
gameWindow.set_res(1600, 900)
player.add_sprite("Helm_Blue.png")
player.add_sprite("Helm_Blue_45.png")

#Declare scenes here (recommend starting with start_scene)

start_scene = scene("start")
gameAction.add_scene(start_scene)

game_scene = scene("game")
gameAction.add_scene(game_scene)

level1 = scene("level1")
gameAction.add_scene(level1)

level2 = scene("level2")
gameAction.add_scene(level2)

level3 = scene("level3")
gameAction.add_scene(level3)

win_scene = scene("win")
gameAction.add_scene(win_scene)

lose_scene = scene("lose")
gameAction.add_scene(lose_scene)

options_scene = scene("options")
gameAction.add_scene(options_scene)

#Put non-essential/modifiable code here

bot1 = npc("bot1")
bot2 = npc("bot2")
bot3 = npc("bot3")
bots = [bot1, bot2, bot3]
bot_stats = {
            "sprites"   : ["Helm_Red.png", "Helm_Red_45.png"],
            "speed"     : 0.5
            }
for bot in bots:
    bot.set_stats(bot_stats)

start_button = button("Start")
start_button_stats = {
                    "text"          : "Start",
                    "pos"           : (gameWindow.width/2, gameWindow.height/1.5),
                    "normal_color"  : green,
                    "trigger_color" : spring_green,
                    "click_color"   : brown
                    }
start_button.set_stats(start_button_stats)


menu_button = button("Back to start")
menu_button_stats = {
                    "size"          : (gameWindow.width/10, gameWindow.height/10),
                    "pos"           : (gameWindow.width/3, gameWindow.height/1.5),
                    "normal_color"  : green,
                    "trigger_color" : spring_green,
                    "click_color"   : brown
                    }
menu_button.set_stats(menu_button_stats)


next_button = button("Next Level")
next_button_stats = {
                    "size"          : (gameWindow.width/10, gameWindow.height/10),
                    "pos"           : (gameWindow.width/1.5, gameWindow.height/1.5),
                    "normal_color"  : green,
                    "trigger_color" : spring_green,
                    "click_color"   : brown
                    }
next_button.set_stats(next_button_stats)


start_message = button("Football Arcade")
start_message_stats = {
                    "size"          : (gameWindow.width/1.5, gameWindow.height/5),
                    "pos"           : (gameWindow.width/2, gameWindow.height/3),
                    "font_size"     : 96,
                    "box"           : False
                    }
start_message.set_stats(start_message_stats)


endzone = button("Endzone")
endzone_stats = {
                "size"          : (gameWindow.width/16, gameWindow.height),
                "pos"           : (gameWindow.width - gameWindow.width/32, gameWindow.height/2),
                "interact"      : False,
                "normal_color"  : white,
                "order"         : 0
                }
endzone.set_stats(endzone_stats)

top_text = button("top text type")
top_text_stats = {
                "size"          : (gameWindow.width/2, gameWindow.height/16),
                "pos"           : (gameWindow.width/2, gameWindow.height/32),
                "interact"      : False,
                "box"           : False
                }
top_text.set_stats(top_text_stats)


options_button = button("options")
options_button_stats = {
                        "size"          : (gameWindow.width/16, gameWindow.height/9),
                        "pos"           : (gameWindow.width/16, gameWindow.height/9),
                        "normal_color"  : ocean,
                        "trigger_color" : cyan,
                        "click_color"   : turquoise
                        }
options_button.set_stats(options_button_stats)

com_button1 = button("Level 1")
com_button2 = button("Level 2")
com_button3 = button("Level 3")
com_button_stats = {
                    "size"          : (gameWindow.width/10, gameWindow.height/10),
                    "normal_color"  : red,
                    "interactable"  : False
                    }

com_buttons = [com_button1, com_button2, com_button3]
for button in com_buttons:
    button.set_stats(com_button_stats)
com_button1.set_pos(gameWindow.width/6, gameWindow.height/3)
com_button2.set_pos(gameWindow.width/6, gameWindow.height/2)
com_button3.set_pos(gameWindow.width/6, gameWindow.height/1.5)




#Scene functions

#===Start Scene===
start_scene.set_background_color(white)

start_scene.add_pieces([fps_display, start_message, start_button, options_button])

start_scene.add_pieces([com_button1, com_button2, com_button3])

def start_scene_main():
    if start_button.ret_clicked():
        print("Button clicked")
        gameAction.change_scene("level1")
    if options_button.ret_clicked():
        gameAction.change_scene("options")
start_scene.set_function(start_scene_main)

def start_scene_start():
    start_button.set_text("Start")
    start_message.set_text("Football Arcade")
    start_button.reset()
    gameData.disp_levels()
    count = 0
    for num in range(len(com_buttons)):
        if gameData.ret_complete(num + 1):
            com_buttons[num].set_normal_color(green)
            com_buttons[num].set_trigger_color(green)
            com_buttons[num].set_click_color(green)
start_scene.set_function_start(start_scene_start)
"""game_scene"""
game_scene.set_background_color(spring_green)
game_scene.set_playerInput(True)


player.set_pos(100, 300)

game_scene.add_piece(fps_display)
game_scene.add_piece(endzone)
game_scene.add_piece(bot1)

def game_scene_main():
    if player.position[0] > endzone.ret_left_side():
        gameAction.change_scene("win")
        gameData.level_complete()
    bot1.chase(player)
    player.collision(bot1)
    if player.get_triggered():
        gameAction.change_scene("lose")
    
game_scene.set_function(game_scene_main)

def game_scene_start():
    player.set_pos(gameWindow.width/10, gameWindow.height/2)
    bot1.set_pos(gameWindow.width/1.5, gameWindow.height/2)
    gameData.set_current_level(1)
game_scene.set_function_start(game_scene_start)

#===Level 1===
level1.set_background_color(spring_green)
level1.set_playerInput(True)

level1.add_piece(player)
player.set_pos(100, 300)

level1.add_pieces([fps_display, endzone, bot1])

def level1_scene_main():
    if player.position[0] > endzone.ret_left_side():
        gameAction.change_scene("win")
        gameData.level_complete()
    bot1.chase(player)
    player.collision(bot1)
    if player.get_triggered():
        gameAction.change_scene("lose")
level1.set_function(level1_scene_main)

def level1_scene_start():
    print("starting level 1")
    player.set_pos(gameWindow.width/10, gameWindow.height/2)
    bot1.set_pos(gameWindow.width/1.5, gameWindow.height/2)
    gameData.set_current_level(1)
level1.set_function_start(level1_scene_start)
#===Level 2===
level2.set_background_color(spring_green)
level2.set_playerInput(True)

level2.add_piece(player)
player.set_pos(100, 300)

level2.add_pieces([fps_display, endzone, bot1, bot2])

def level2_scene_main():
    if player.position[0] > endzone.ret_left_side():
        gameAction.change_scene("win")
        gameData.level_complete()
    bot1.chase(player)
    bot2.chase(player)
    player.collision(bot1)
    player.collision(bot2)
    if player.get_triggered():
        gameAction.change_scene("lose")
level2.set_function(level2_scene_main)

def level2_scene_start():
    print("starting level 2")
    player.set_pos(gameWindow.width/10, gameWindow.height/2)
    bot1.set_pos(gameWindow.width/1.5, gameWindow.height/1.5)
    bot2.set_pos(gameWindow.width/1.5, gameWindow.height/3)
    gameData.set_current_level(2)
level2.set_function_start(level2_scene_start)
#===Level3===
level3.set_background_color(spring_green)
level3.set_playerInput(True)

level3.add_piece(player)
player.set_pos(100, 300)

level3.add_pieces([fps_display, endzone, bot1, bot2, bot3])

def level3_scene_main():
    if player.position[0] > endzone.ret_left_side():
        gameAction.change_scene("win")
        gameData.level_complete()
    bot1.chase(player)
    bot2.chase(player)
    bot3.chase(player)
    player.collision(bot1)
    player.collision(bot2)
    player.collision(bot3)
    if player.get_triggered():
        gameAction.change_scene("lose")
level3.set_function(level3_scene_main)

def level3_scene_start():
    player.set_pos(gameWindow.width/10, gameWindow.height/2)
    bot1.set_pos(gameWindow.width/1.5, gameWindow.height/2)
    bot2.set_pos(gameWindow.width/1.5, gameWindow.height/1.5)
    bot3.set_pos(gameWindow.width/1.5, gameWindow.height/3)
    gameData.set_current_level(3)
level3.set_function_start(level3_scene_start)

#===Win Scene===
win_scene.set_background_color(yellow)

win_scene.add_pieces([start_message, menu_button, next_button])

def win_scene_main():
    if menu_button.ret_clicked():
        gameAction.change_scene("start")
    if next_button.ret_clicked():
        print(gameData.ret_level())
        if gameData.ret_level() == 1:
            gameAction.change_scene("level2")
        elif gameData.ret_level() == 2:
            gameAction.change_scene("level3")
        else:
            print("Error: Next button active where it shouldn't be")
win_scene.set_function(win_scene_main)

def win_scene_start():
    gameData.level_complete()
    start_message.set_text("You Won this level!")
    if gameData.ret_level() >= 3:
        start_message.set_text("You have completed all Levels")
        win_scene.del_piece(next_button)
    else:
        win_scene.add_piece(next_button)
win_scene.set_function_start(win_scene_start)
#===Lose Scene===
lose_scene.set_background_color(cyan)

lose_scene.add_pieces([start_message, menu_button])

def lose_scene_main():
    if menu_button.ret_clicked():
        gameAction.change_scene("start")
lose_scene.set_function(lose_scene_main)

def lose_scene_start():
    start_message.set_text("You Lost this level try again")
    menu_button.set_text("Back to start")
    start_button.reset()
lose_scene.set_function_start(lose_scene_start)

#==Options Menu===
options_scene.set_background_color(gray)

options_scene.add_pieces([menu_button])

def options_scene_main():
    if menu_button.ret_clicked():
        gameAction.change_scene("start")
options_scene.set_function(options_scene_main)

def options_scene_start():
    top_text.set_text("Options")
    menu_button.reset()
options_scene.set_function_start(options_scene_start)

#Always last line of program
print("+++Game starting+++")
gameAction.gameLoop()
