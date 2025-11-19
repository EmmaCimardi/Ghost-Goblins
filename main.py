import g2d
from actor import Actor, Point, Arena
import random
#dim background: 3588x327
global contaTick, x_arthur
global scala1, scala2, scala3
global lago1
global fineScala
#inizializzazione variabili globali
#valore x sullo sfondo(.png) delle varie cose:
scala1=715
scala2=912
scala3=1070
lago1=1164 
fineScala=1131
#contatori:
contaTick=0 #timer
x_arthur=0 # valore di x aggiornato  (arthur)
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
        
        self._frame = 0
        self._animation_speed = 4
        self._animation_counter = 0
        

    def move(self, arena):
        global scala1, scala2, scala3, fineScala, lago1, backX, x_arthur
       
        for other in arena.collisions():
            if isinstance(other, Zombie):
                if self._touch == False:
                    self._touch = True
                else:
                    self._touch = False
            if isinstance(other, Platform):
                self._y = 100 #se tocco la platform salendo le scale poi arthur cammina su y=100
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
            
        if "Space" in keys:
            arena.spawn(Torch(self._x+10, self._y))

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
            
        x_arthur=self._x-backX #aggiorno la posizione di arthur
        

    def pos(self):
        return (self._x, self._y)

    def size(self):
        if self._touch == False: #se è un cavagliere
            return self._w, self._h
        else:
            return 23,32 #se è ""spoglio"""

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
    
    global contaTick, backX, x_arthur #var globali
    def __init__(self, pos, ct, direzione): #ct è il contatick in cui è stato generato
        self._x, self._y = pos #y=210
        self._w, self._h = 22, 36
        self._speed = 4
        self._dx =self._speed
        self._ct=ct #secondo in cui è stato generato
        self._die =False #quando muore (ogni 100 sec) sprite cambia e si vede lo combie andarsene 
        self._dir= direzione #lo zombie va a destra o sinistra, #true destra, false sinistra
        
    def move(self, arena):
             
        #sorge dal terreno, 210-180=30/10=3, in 3 tick sale
    
        if self._y> 180:
            self._y -= 10
            
        if self._y <= 180:
            
            if x_arthur > self._x: #se la posizione di arthur>di zombi allora si gira a destra "verso arthr"
                self._dx = self._speed #d
            else:
                self._dx= -self._speed#s
                
            arena_w, arena_h = arena.size()
            self._x += self._dx        
            if self._x < 0:
                self._x = 0
                self._dx = self._speed 
            elif self._x + self._w > arena_w:
                self._x = arena_w - self._w
                self._x = -self._speed
            #farlo morire dopo 100 tick
            #contatick è quello "aggiornato" mentre self._ct è il secondo in cui è stato generato lo zombie
            if contaTick - self._ct >= 50:
                self._die = True #cambio immagine e metto zombie che va a terra
                #self._dx = 0 #fermo
                arena.kill(self)
        

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        
        return 653, 62

class Platform(Actor):

    def __init__(self, pos, w, h):
        self._x, self._y = pos
        self._w, self._h = w, h
                
    def move(self, arena):
        self._x=self._x
    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return None

class Torch(Actor):
    def __init__(self, pos):
        self._x, self._y = pos 
        self._w, self._h = 15, 15
        self._speed = 4
        self._dx, self._dy = self._speed, self._speed

    def move(self, arena: Arena):
        self._x += self._dx #ad ogni tick la fiaccola va
        for other in arena.collisions():
            if isinstance(other, Zombie):
                arena.kill(other) #se tocca uno zombie questo muore 
                arena.kill(self)
        
        
        #if self._y + self._dy > arena_h - self._h:
            #flame spawn
    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 130,334


#class Flame(Actor): 
    
#TICK FUNZIONE
backX=0 #movimento dello sfondo
def tick():
    #funzioni globalo
    global contaTick
    global backX, i, x_arthur

    contaTick += 1 #secondi
    k = g2d.current_keys() #array di tasti dalla keynoard
    g2d.clear_canvas()
    g2d.draw_image("ghosts-goblins-bg.png", (backX,0), (0,0)) #sfondo 
    g2d.draw_text(str(contaTick), (50,30), 30) #timer
    
    for a in arena.actors():  #genero actor
        if a.sprite() != None:
            g2d.draw_image("ghosts-goblins.png", a.pos(), a.sprite(), a.size())
     
    arena.tick(k)        
    #spawn zoombie 
    zX= random.randrange(60,600) #la x di zombie è casuale [60,550[
    d = random.choice([True, False])#destra(true) o sinistra(false)
    prob = random.randrange(0,20) #ho una probabilita su 1500 che nasca uno zombie (metto 1/10 per vederli)
    distanza= x_arthur - zX #devo calcolare la distanza tra arthur e gli zombie, se lo zombie è vicino di 200
    if distanza <=0 : 
        distanza = distanza*(-1) #distanza deve essere positiva, minore o maggiore di 200
   # if distanza <= 500: #se quidi la distanza tra arthur e zombie è <= 200 procedo
    if prob==1: 
        arena.spawn(Zombie((zX,210), contaTick, d)) #spawn zombie che vanno da destra a sinistra    
    #passo per parametro: (x casuale,y), secondo in cui viene generato, destra/sinistra
    
def main():
    #var globali
    global arena
    global contaTick 
    
    #arena
    arena = Arena((600, 260)) #dim arena
    g2d.init_canvas(arena.size()) #creo canvas
    
    #ARTHUR
    arena.spawn(Arthur((0, 180))) #spawn arthur sul terreno

    #ZOMBIE spawn nel tick!!
    
    #Piattaforme
    arena.spawn(Platform((597, 122),121,16 )) #primo spigolo di terra(sinistra della scala1)
    arena.spawn(Platform((738, 121), 173,16))
    arena.spawn(Platform((927, 123), 148,16))
    arena.spawn(Platform((1088, 125), 47,16))
    
     
    
    
    g2d.main_loop(tick)

main()