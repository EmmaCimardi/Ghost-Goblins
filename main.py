import g2d
from actor import Actor, Point, Arena

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

main()