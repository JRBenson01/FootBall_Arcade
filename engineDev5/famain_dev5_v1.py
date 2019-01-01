from engineDev5 import *

#Main gmae variables
gameWindow.set_res(800, 800)

start_scene = scene("start")
gameAction.add_scene(start_scene)
start_scene.set_background_color(white)

insult_button = button()
insult_button_stats = {
                        "text"  : "GO FUCK YOURSELF",
                        "pos"   : (gameWindow.width/2, gameWindow.height/2),
                        "box"   : False
                        }
insult_button.set_stats(insult_button_stats)

start_scene.add_piece(insult_button)

#Always last line of program
print("+++Game starting+++")
gameAction.gameLoop()
