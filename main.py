import g2d
from actor import Actor, Point, Arena


#Classe zombie

class Zombie(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 22, 36
        self._speed = 2
        self._dx, self._dy = self._speed, self._speed
        
    def move(self, arena: Arena):
        for other in arena.collisions():
            if not isinstance(other, ):
                x, y = other.pos()
                if self._x + self._dx < 0:
                    self._dx = self._speed
                else:
                    self._dx = -self._speed
                

        arena_w, arena_h = arena.size()
        
        #sposto lo zombie da destra a sinistra
        if self._x + self._dx < 0:
            self._dx = self._speed
        elif self._x + self._dx > arena_w - self._w:
            self._dx = -self._speed
            
        
        self._x += self._dx
       

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 653, 62
    
#TICK FUNZIONE
def tick():
    g2d.clear_canvas() #pulisco sfondo
    g2d.draw_image("ghosts-goblins-bg.png", (0,0), (0,0)) #creo sfondo
    for a in arena.actors():
        if a.sprite() != None:
            g2d.draw_image("ghosts-goblins.png", a.pos(), a.sprite(), a.size())
        else:
            pass  # g2d.draw_rect(a.pos(), a.size())

    arena.tick(g2d.current_keys()) 

            
def main():
    global arena
    
    arena = Arena((600, 260)) #dim arena
    arena.spawn(Zombie((0,200))) #spawn zombie che vanno da destra a sinistra
     
    g2d.init_canvas(arena.size()) #creo canvas
    g2d.main_loop(tick)
    
main()