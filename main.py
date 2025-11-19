import g2d
from actor import Actor, Point, Arena

#dim background: 3588x327
global contaTick
global scala1, scala2, scala3
global lago1
global fineScala
global c, c1, i #contatori
scala1=715
scala2=912
scala3=1070
c = 1
c1 = 1 
i=0
lago1=1164
fineScala=1131
contaTick=0
#Classe arthur
class Arthur(Actor):


sheet = "ghosts-goblins.png"

# coordinate della corsa (x, y, w, h)
frames_run = [
    (39, 43, 23, 30),
    (63, 41, 23, 33),
    (86, 41, 22, 34),
    (108, 42, 27, 31)
]

class Arthur(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w = 29
        self._h = 31
        self._speed = 2
        self._vy = 0
        self._direction = 1
        self._click = False
        self._jumping = False
        self._touch = False
        self._arrow = 1
        self._valY = 180
        self._saltato = False
        ####
        self._frame = 0
        self._animation_speed = 4
        self._animation_counter = 0

    def move(self, arena):
        global scala1, scala2, scala3, fineScala, lago1, backX

        for other in arena.collisions():
            if isinstance(other, Zombie):
                if self._touch == False:
                    self._touch = True
                else:
                    self._touch = False

        keys = g2d.current_keys()

        
        moved = False
        
        if "ArrowRight" in keys:  # freccia destra
            self._x += self._speed
            self._arrow = 1
            self._click = True
            moved = True
            if self._x > 50 and backX > -2900:
                backX -= 2

        elif "ArrowLeft" in keys:  # freccia sinistra
            self._x -= self._speed
            self._arrow = 2
            self._click = True
            moved = True
            if self._x < 50 and backX < 0:
                backX += 2
        else:
            self._click = False

       #corsa 
        if moved:
            self._animation_counter += 1
            if self._animation_counter >= self._animation_speed:
                self._frame = (self._frame + 1) % len(frames_run)
                self._animation_counter = 0

        # salto
        if "ArrowUp" in keys and not self._jumping:
            self._vy = -10
            self._jumping = True
            self._arrow = 3
            self._saltato = True

        # Gravità 
        self._vy += 0.5
        self._y += self._vy

        # scale
        if self._saltato:
            if (scala1 <= self._x - backX <= scala1+10 or 
                scala2 <= self._x - backX <= scala2+10 or 
                scala3 <= self._x - backX <= scala3 + 10):
                self._valY = 100
                self.saltato = True
            else:
                if self._x - backX <= 605 or self._x - backX >= fineScala:
                    self._valY = 180
                    self._saltato = False
        else:
            self._saltato = False
            self._valY = 180

        # collisione con terreno
        if self._y > self._valY:
            self._y = self._valY
            self._vy = 0
            self._jumping = False

        # controllo bordi
        if self._x < 0:
            self._x = 0
        if self._x > 600 - self._w:
            self._x = 600 - self._w

    def pos(self):
        return (self._x, self._y)

    def size(self):
        if self._touch == False:
            return self._w, self._h
        else:
            return 23,32

    def sprite(self):
        # se non ha toccato nemici
        if self._touch == False:
            # se si muove
            if self._click and not self._jumping:
                sx, sy, w, h = frames_run[self._frame]
                # aggiorno dim 
                self._w, self._h = w, h
                return sx, sy
            # salto
            elif self._jumping:
                self._w, self._h = 32, 32   #da cambiare 
                return 148, 131  #da cambiare 
            # se è fermo
            else:
                if self._arrow == 1:  # destra
                    self._w, self._h = 29, 31 
                    return 4, 39  
                else:  # sinistra
                    self._w, self._h = 29, 31 
                    return 482, 43
        else:
            # se ha toccato nemici
            return 64, 75

class Zombie(Actor):
    
    global contaTick
    def __init__(self, pos, ct): #ct è il contatick in cui è stato generato
        self._x, self._y = pos
        self._w, self._h = 22, 36
        self._speed = 4
        self._dx =self._speed
        self._ct=ct
        self._die =False #quando muore (ogni 150 sec) sprite cambia e si vede lo combie andarsene 
        
    def move(self, arena):
        for other in arena.collisions():
            if not isinstance(other, Arthur):
                x, y = other.pos()
                if x < self._x:
                    self._dx = self._speed
                else:
                    self._dx = -self._speed
             

        arena_w, arena_h = arena.size()
        if self._x + self._dx < 0:
            self._dx = self._speed
        elif self._x + self._dx > arena_w - self._w:
            self._dx = -self._speed
     
        self._x += self._dx
       
    #farlo morire 
    
        if (self._ct+contaTick) % 120 == 0: 
            arena.kill(self)
            self._die =True
       

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        if self._die: 
            self._h=15
            self._w=31
            return 529,83
        else:
            return 653, 62

#TICK FUNZIONE
backX=0
def tick():
    global contaTick
    global backX, i

    contaTick += 1 #secondi
    k = g2d.current_keys() #array di tasti dalla keynoard
    g2d.clear_canvas()
    g2d.draw_image("ghosts-goblins-bg.png", (backX,0), (0,0)) #sfondo 
    g2d.draw_text(str(contaTick), (50,30), 30) #timer
    for a in arena.actors():
        if a.sprite() != None:
            g2d.draw_image("ghosts-goblins.png", a.pos(), a.sprite(), a.size())
            
    #spawn zoombie ogni 50 tick
    z= [(400,180), (200,180), (500,180), (100,180), (10,180)]
    if contaTick%20==0:
        arena.spawn(Zombie(z[i], contaTick)) #spawn zombie che vanno da destra a sinistra
        if i<len(z)-1 : 
            i+=1
        else: 
            i=0

    
    arena.tick(k)       


    
def main():
    global arena
    global contaTick, i 
    arena = Arena((600, 260)) #dim arena
    g2d.init_canvas(arena.size()) #creo canvas
    
    #ARTHUR
    arena.spawn(Arthur((0, 150)))

    #ZOMBIE spawn nel tick
        
     
    
    
    g2d.main_loop(tick)

main()