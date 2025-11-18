import g2d
from actor import Actor, Point, Arena
img=False
global backX #dichiaro bg in tutti metodi dove la uso

#dim background: 3588x327
global scala1 
global scala2
global scala3
global lago1
global fineScala
global c
scala1=715
scala2=912
scala3=10
c = 1 
lago1=1164
fineScala=1131
#Classe arthur
class Arthur(Actor):

    def __init__(self, pos):
            
        self._x, self._y = pos    #pos iniziale art
        self._w = 29    #larghezza art
        self._h = 31    #altezza art
        self._speed = 2 #velocita orizzontale 
        self._vy = 0    #velocita verticale
        self._direction = 1 
        self._click=False
        
        
        self._jumping = False   #stato del salto
        self._touch= False #num collision
        self._arrow= 1 #1 destra, 2 sinistra, 3 saltare
        self._valY=180
        self._saltato=False
    
    def move(self, arena):
        global scala1, scala2, scala3, fineScala
        global lago1, backX
    
        #se tocca lo zombie
        for other in arena.collisions():
            if isinstance(other, Zombie):
                if self._touch == False:
                    self._touch=True
                else:
                    self._touch=False
                    #arena.kill(self)
                    img=True
                    
        keys = g2d.current_keys()  #lista tasti premuti 
        
        if "d" in keys:  # "d", muovi art a destra.
            self._x += self._speed
            self._arrow= 1 # verso destra
            
            if self._x > 50 and backX > -2900:
                backX -= 2
        if "a" in keys:  # "a", muovi art a sinistra.
            self._x -= self._speed 
            self._arrow= 2  #verso sinistra
            self._click=True
            if self._x < 50 and backX < 0:
                backX += 2
        else:
            self._click = False
        if "w" in keys and not self._jumping:  # "w", art salta .
            self._vy = -10
            self._jumping = True
            self._arrow= 3 # verso alto
            self._saltato=True
       
            
        # Gravità
        self._vy += 0.5
        self._y += self._vy
        
        if self._saltato:
            if (scala1<= self._x - backX  <= scala1+10 or \
            scala2<= self._x - backX  <= scala2+10 or \
                scala3<= self._x - backX  <= fineScala): # tratto speciale
                self._valY = 100
                self.saltato=True
            else:
                if self._x - backX < 605 or self._x - backX >= fineScala:
                    self._valY = 180
                    self._saltato=False
        else:
            self._saltato=False
            self._valY = 180


        # collisione con il terreno 
        if self._y > self._valY: #uguale a self._y
            self._y = self._valY #modifica altezza di arthur nel canva
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
            if self._arrow == 1:  
                return 128,610 
            
            if self._arrow == 2: 
                if self._click:  # SOLO se stai premendo "a"
                    global c
                    match c:
                        case 1:
                            c += 1
                            self._w = 22
                            self._h = 34
                            return 447, 42
                        case 2:
                            c += 1
                            self._w = 24
                            self._h = 34
                            return 404, 42
                        case 3:
                            c = 1
                            self._w = 28
                            self._h = 34
                            return 378, 42
                else:  # arrow=2 ma NON stai premendo "a"
                    return 482, 43  # Immagine statica!
                    
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
backX=0
def tick():
    global backX
    g2d.clear_canvas() #pulisco sfondo
    g2d.draw_image("ghosts-goblins-bg.png", (backX,0), (0,0)) #creo sfondo
    for a in arena.actors():
        if a.sprite() != None:
            g2d.draw_image("ghosts-goblins.png", a.pos(), a.sprite(), a.size())
        else:
            pass  # g2d.draw_rect(a.pos(), a.size())
 
    if img ==True: 
        g2d.draw_image("ending.webp", (0,0), (600,600))
    
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
    
    #background
    
    g2d.main_loop(tick)

main()