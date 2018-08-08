import pygame, sys
from pygame.locals import *
import time
import math
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
dim_red = (125, 0, 0)
orange = (255, 125, 0)
yellow = (255, 255, 0)
spring_green = (125, 255, 0)
green = (0, 255, 0)
turquoise = (0, 255, 125)
cyan = (0, 255, 255)
ocean = (0, 125, 255)
blue = (0, 0, 255)
violet = (125, 0, 255)
magenta = (255, 0, 255)
dull_magenta = (125, 0, 125)
raspberry = (255, 0, 125)



def rad(degrees):
    return ((degrees * math.pi)/180)

def deg(radians):
    return ((180 * radians)/math.pi)

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
        self.background_color = color

    def set_fps_cap(self, fps_cap):
        self.fps_cap = fps_cap

    def set_fullscreen(self):
        self.display = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN) 

    def gameExit(self):
        print("exiting game")
        pygame.quit()
        sys.exit()

    def frameUpdate(self, scene):
        self.clock.tick()
        self.fps = self.clock.get_fps()
        pygame.time.delay(int(1000/self.fps_cap))
        fps_message = str("FPS: %s" % (int(self.fps)))
        fps_display.set_text(fps_message)
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
        pygame.display.update()


        
        

class game_Action(object):
    def __init__(self):
        self.exit = False
        self.scene = "Main"

    def exit(self):
        self.exit = True

    def gameLoop(self):
        while self.exit == False:
            if self.scene == "Main":
                mainLoop()
            elif self.scene == "Lose":
                loseLoop()
            elif self.scene == "Win":
                winLoop()
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameWindow.gameExit()
            gameWindow.frameUpdate(self.scene)
        gameWindow.gameExit()
        
"""        while self.scene == "Main" and self.exit == False:
            gameWindow.frameUpdate(self.scene)
            mainLoop()
        while self.scene == "Lose" and self.exit == False:
            gameWindow.frameUpdate(self.scene)
            loseLoop()
        gameWindow.gameExit()
"""

class game_Data(object):
    def __init__(self):
        start_pos = ((gameWindow.width - 100), (gameWindow.height/2))
        self.use = True
        self.playerPositions = []
        for i in range(60):
            self.playerPositions.append(start_pos)
        
    def ret_viewPos(self):
        print (self.playerPositions[59])
        return self.playerPositions[0]
    
    def set_truePos(self, gPos):
        count = 59
        temp = self.playerPositions[count]
        while count > -1:
            self.playerPositions[count] = self.playerPositions[count+1]
            temp = self.playerPositions[count]
#Position code still needs to be worked out

class button(object):
    def __init__(self, text):
        self.text = text
        self.normal_color = dull_magenta
        self.trigger_color = magenta
        self.click_color = violet
        self.font_size = 22
        self.font = pygame.font.Font("arial.ttf", self.font_size)
        self.width = 100
        self.height = 100
        self.xPos = gameWindow.width/2
        self.yPos = gameWindow.height/2
        self.box = True
        self.angle = 0

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_font_size(self, size):
        self.font_size = size
        self.font = pygame.font.Font("arial.ttf", self.font_size)

    def set_normal_color(self, color):
        self.normal_color = color

    def set_trigger_color(self, color):
        self.trigger_color = color

    def set_click_color(self, color):
        self.click_color = color

    def set_text(self, text):
        self.text = text

    def set_pos(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    def no_box(self):
        self.box = False

    def rotate(self, angle):
        self.angle = angle

    def display(self):
        #print ("Displaying", text, "button")
        disp_specs = ((self.xPos - (self.width/2)), (self.yPos - (self.height/2)), self.width, self.height)
        #print (position)
        textSurface = self.font.render(self.text, True, black)
        if self.angle != 0:
            textSurface = pygame.transform.rotate(textSurface, self.angle)
        textBox = textSurface.get_rect()
        textBox.center = (self.xPos, self.yPos)
        if self.box:
            pygame.draw.rect(gameWindow.display, self.normal_color, (disp_specs))
        gameWindow.display.blit(textSurface, textBox)

class gamePiece(object):
    def __init__(self):
        self.gravity = False
        self.collidable = False
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

    def set_pos(self, x, y):
        self.position = (x, y)
        self.orgPosition = (x, y)

    def set_hitbox(self, length, height):
        self.hb_length = length
        self.hb_height = height

    def set_hb(self, length, height):
        self.hb_length = length
        self.hb_height = height

    def set_sprite(self, image):
        self.use_image = True
        self.sprites.append(pygame.image.load(image))
        self.sprite = self.sprites[0]
        
    def set_size(self, length, height):
        self.length = length
        self.height = height
        if self.use_image:
            self.sprite = pygame.transform.scale(self.sprite, (self.length, self.height))

    def set_speed(self, speed):
        self.speed = speed

    def set_hb_type(self, hb_type):
        self.hb_type = hb_type

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

    def input(self, keys):
        move = True
        vert = 0
        hor = 0
        self.angle = 0
        if keys[K_w]:
            vert = 1
        if keys[K_s]:
            vert = -1
        if keys[K_a]:
            hor = -1
        if keys[K_d]:
            hor = 1
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
            move = False
        if move:
            self.move()

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
            else:
                self.triggered = False
                
            if self.triggered == True:
                print ("Collision detected")
                return True
        """
        if self.hb_type == "rectangle":
        xMin = self.position[0] - self.hb_length/2
        xMax = self.position[0] + self.hb_length/2
        yMin = self.position[1] - self.hb_height/2
        yMax = self.position[1] + self.hb_height/2
        collider_hb = collider.get_hb()
        col_xMin = collider_hb[0]
        col_xMax = collider_hb[1]
        col_yMin = collider_hb[2]
        col_yMax = collider_hb[3]
        dim_hb = (xMin, xMax, yMin, yMax)
        #print (dim_hb)
        #print (collider_hb)
        if (xMin <= collider_hb[0] and xMax >= collider_hb[1] and yMin <= collider_hb[2] and yMax >= collider_hb[3]):
            self.triggered = True
            #print ("Collision detected")

        elif (xMin <= collider_hb[1] and xMax >= collider_hb[0] and yMin <= collider_hb[3] and yMax >= collider_hb[2]):
            self.triggered = True
            #print ("Collision detected")
        else:
            self.triggered = False
        """

    def display(self):
        #print ("Displaying gamePiece")
        xPos = self.position[0]
        yPos = self.position[1]
        xMin = xPos - self.length/2
        yMin = yPos - self.height/2
        if self.use_image:
            gameWindow.display.blit(self.sprite, (xMin, yMin))
        else:
            disp_specs = ((xPos - (self.length/2)), (yPos - (self.height/2)), self.length, self.height)
            pygame.draw.rect(gameWindow.display, black, (disp_specs))

    def reset(self):
        self.position = self.orgPosition
        self.angle = 'v'

def mainLoop():
    keys = pygame.key.get_pressed()
    #print (player.position, collider.position)
    player.collision(collider)
    player.input(keys)
    collider.chase(player)
    if player.position[0] >= (gameWindow.width - 100):
        print("You Win!")
        gameAction.scene = "Win"
        player.reset()
        collider.reset()
    if player.triggered:
        gameAction.scene = "Lose"
        player.reset()
        collider.reset()

def mainFrameUpdate():
    gameWindow.background_color = spring_green
    fps_display.display()
    endzone.display()
    collider.display()
    player.display()

def loseLoop():
    keys = pygame.key.get_pressed()
    if keys[K_SPACE]:
        gameAction.scene = "Main"

def loseFrameUpdate():
    title.set_text("YOU LOSE!")
    gameWindow.background_color = dim_red
    fps_display.display()
    title.display()
    subheading.display()

def winLoop():
    keys = pygame.key.get_pressed()
    if keys[K_SPACE]:
        gameAction.scene = "Main"

def winFrameUpdate():
    title.set_text("YOU WIN!")
    gameWindow.background_color = green
    fps_display.display()
    title.display()
    subheading.display()
    

gameWindow = game_Window()
gameAction = game_Action()

gameWindow.set_res(1280, 720)
gameWindow.set_caption("Hello World")
gameWindow.set_background_color(green)
#gameWindow.set_fullscreen()

gameData = game_Data()

player = gamePiece()
player.set_pos(100, gameWindow.height/2)
player.set_sprite("Helm_Blue.png")
player.set_sprite("Helm_Blue_45.png")
player.set_speed(2)

collider = gamePiece()
collider.set_pos((gameWindow.width - 100), (gameWindow.height/2))
collider.set_sprite("Helm_Red.png")
collider.set_sprite("Helm_Red_45.png")
collider.set_speed(1.5)

"""
collider1 = gamePiece()
collider1.set_pos((gameWindow.width - 100), (gameWindow.height/2)-200)
collider1.set_sprite("Helm_Red.png")
collider1.set_sprite("Helm_Red_45.png")
collider1.set_speed(1.5)
"""

fps_display = button("FPS: ")
fps_display.set_pos(50, 50)
fps_display.no_box()

endzone = button("Endzone")
endzone.normal_color = white
endzone.set_size(100, gameWindow.height)
endzone.set_pos((gameWindow.width - 50), gameWindow.height/2) 
endzone.set_font_size(32)
endzone.rotate(-90)

title = button("YOU WIN!")
title.set_pos(gameWindow.width/2, gameWindow.height/2)
title.set_font_size(72)
title.no_box()
title.set_size(400, 300)

subheading = button("Press space to play again")
subheading.set_pos(gameWindow.width/2, gameWindow.height/1.5)
subheading.set_font_size(48)
subheading.no_box()

playerPositions = []
playerPositions.append((0, 0))
playerPositions.append(player.position)
playerPositions.append(player.position)

gameAction.gameLoop()
