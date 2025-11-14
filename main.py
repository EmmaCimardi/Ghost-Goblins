import g2d
from actor import Actor, Point, Arena
#ciaoooooooo
g2d.init_canvas((600, 250))
g2d.draw_image("ghosts-goblins-bg.png", (0, 0))

class Arthur(Actor):
    def __init__(self, x, y):
        self._x = x     #pos iniziale art
        self._y = y     #pos iniziale art
        self._w = 32    #larghezza art
        self._h = 48    #altezza art
        self._speed = 3 #velocita orizzontale 
        self._vy = 0    #velocita verticale
        self._direction = 1 
        self._jumping = False   #stato del salto
    
    def move(self, arena):
        keys = g2d.current_keys()  #lista tasti premuti 
        
        if "d" in keys:  # "d", muovi art a destra.
            self._x += self._speed
        if "a" in keys:  # "a", muovi art a sinistra.
            self._x -= self._speed
        if "w" in keys and not self._jumping:  # "w", art salta .
            self._vy = -10
            self._jumping = True
        
        # Gravità
        self._vy += 0.5
        self._y += self._vy
        
        # collisione con il terreno 
        if self._y > 200:
            self._y = 200
            self._vy = 0
            self._jumping = False
        
        # controllo dei bordi dello schermo
        if self._x < 0:
            self._x = 0
        if self._x > 600 - self._w:
            self._x = 600 - self._w
    
    def pos(self):
        return (self._x, self._y)
    
    def size(self):
        return (self._w, self._h)
    
    def sprite(self):
        return None

arena = Arena((600, 260))
arthur = Arthur(0, 200)
arena.spawn(arthur)

def main():
    g2d.clear_canvas()
    g2d.draw_image("ghosts-goblins-bg.png", (0, 0))
    
    x, y = arthur.pos()
    w, h = arthur.size()
    g2d.draw_rect((x, y), (w, h))  # quadrato rosso
    
    arena.tick(g2d.current_keys())

g2d.main_loop(main)


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