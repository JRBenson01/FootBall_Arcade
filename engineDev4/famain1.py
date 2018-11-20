from engineDev4 import *


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
player_stats = {
                "speed" : 0.75
                }
player.set_stats(player_stats)



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
    #player.collision(bot1)
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
    #player.collision(bot1)
    #player.collision(bot2)
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
    #player.collision(bot1)
    #player.collision(bot2)
    #player.collision(bot3)
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
