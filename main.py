import g2d
from actor import Actor, Point, Arena

class Arthur(Actor):
    def __init__(self, pos):
             #pos iniziale art
        self._x, self._y = pos    #pos iniziale art
        self._w = 29    #larghezza art
        self._h = 31    #altezza art
        self._speed = 3 #velocita orizzontale 
        self._vy = 0    #velocita verticale
        self._direction = 1 
        self._jumping = False   #stato del salto
        self._touch= False #num collision
    
    def move(self, arena):
        
        #se tocca lo zombie
        for other in arena.collisions():
            if isinstance(other, Zombie):
                if self._touch == False:
                    self._touch=True
                else:
                    self._touch==False
                    arena.kill(self)
                
                    
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
        if self._y > 180: #uguale a self._y
            self._y = 180 #modifica altezza di arthur nel canva
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
        if self._touch == False:
            return self._h , self._w
        else:
            return 23,32
    
    def sprite(self):
        if self._touch == False:
            return 128,610 # x_sprite,y_sprite
        else:
            return 64,75

#Classe zombie

class Zombie(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 22, 36
        self._speed = 2
        self._dx, self._dy = self._speed, self._speed
        
    def move(self, arena: Arena):
       
       #for other in arena.collisions():
            #if not isinstance(other, ):
             #   x, y = other.pos()
              #  if self._x + self._dx < 0:
               #     self._dx = self._speed
                #else:
                 #   self._dx = -self._speed""
                

        arena_w, arena_h = arena.size()
        
        #sposto lo zombie da destra a sinistra
        if self._x + self._dx < 0:
            self._dx = self._speed
        elif self._x + self._dx > arena_w - self._w:
            self._dx = -self._speed
        self._x += self._dx
       
    #draw image
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
    #ARENA
    global arena
    
    arena = Arena((600, 260)) #dim arena
    g2d.init_canvas(arena.size()) #creo canvas
    
    #ZOMBIE
    arena.spawn(Zombie((60,180))) #spawn zombie che vanno da destra a sinistra
     
    #ARTHUR
    arena.spawn(Arthur((0, 150)))

    arena.tick(g2d.current_keys())
    
    #CANVAS
    
    g2d.main_loop(tick)
    

main()