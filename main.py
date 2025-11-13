import g2d
from actor import Actor, Point, Arena

#ARENA 500,325

g2d.init_canvas((600,250))
g2d.draw_image("ghosts-goblins-bg.png", (0,0), (0,0)) #sfondo



g2d.main_loop()