import g2d
import actor 

#ARENA 500,325

g2d.init_canvas((600,250))
g2d.draw_image("ghosts-goblins-bg.png", (0,0), (0,0)) #sfondo
#ciao emma maria perla 
actor.create_hero((50,150))
#ciao emma maria perla
g2d.main_loop()


