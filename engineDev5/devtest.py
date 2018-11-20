from engineDev5 import *


#Main game variables
gameWindow.set_res(800, 800)

main_scene = scene("main")
gameAction.add_scene(main_scene)
main_scene.set_background_color(white)

gameAction.change_scene("main")

#Always last line of program
print("+++Game starting+++")
gameAction.gameLoop()
