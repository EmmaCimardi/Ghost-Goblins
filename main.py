import g2d
from actor import Actor, Point, Arena
img=False
global backX #dichiaro bg in tutti metodi dove la uso

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

    def __init__(self, pos):
            
        self._x, self._y = pos    #pos iniziale art
        self._w = 29    #larghezza art
        self._h = 31    #altezza art
        self._speed = 2 #velocita orizzontale 
        self._vy = 0    #velocita verticale
        self._direction = 1 
        self._click=False #se a,w o d sono stati cliccati
        
        
        self._jumping = False   #stato del salto
        self._touch= False #se è nudo
        self._arrow= 1 #1 destra, 2 sinistra, 3 saltare
        self._valY=180 #distanza da terra (y=180)
        self._saltato=False #ha saltato?
    
    def move(self, arena):
        global scala1, scala2, scala3, fineScala
        global lago1, backX #richiamo le global 
    
        #se tocca lo zombie
        for other in arena.collisions():
            if isinstance(other, Zombie):
                if self._touch == False:
                    self._touch=True
                else:
                    self._touch=False
                    #arena.kill(self)
                   
        keys = g2d.current_keys()  #lista tasti premuti 
        
        #se premo un tasto:
        
        if "d" in keys:  # "d", muovi art a destra.
            self._x += self._speed
            self._arrow= 1 # verso destra
            self._click=True
            if self._x > 50 and backX > -2900:
                backX -= 2
        else:
            self._click=False

        if "a" in keys:  # "a", muovi art a sinistra.
            self._x -= self._speed 
            self._arrow= 2  #verso sinistra
            self._click=True
            if self._x < 50 and backX < 0:
                backX += 2
        else:
            self._click = False
            
        if "w" in keys and not self._jumping:  # "w", arthur salta
            self._vy = -10
            self._jumping = True
            self._arrow= 3 # verso alto
            self._saltato=True
       
            
        # Gravità
        self._vy += 0.5
        self._y += self._vy
        
        if self._saltato: #se ha fatto un salto (schiacciato w) entro
            
            if ( scala1<= self._x - backX  <= scala1+10 or scala2<= self._x - backX  <= scala2+10 or 
                scala3<= self._x - backX  <= scala3 +10 ): # se sono dalle scale salgo

                self._valY = 100
                self._saltato=True #rimane ad altezza 100  
            else:
                
                if self._x - backX <= 605 or self._x - backX >= fineScala: #se ha superato il pezzo di terra, o è sesco vado ad altezza 180
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
                if self._click:  # SOLO se stai premendo "a"
                    global c1
                    match c1:
                        case 1:
                            c1 += 1
                            self._w = 25
                            self._h = 30
                            return 38, 42
                        case 2:
                            c1 += 1
                            self._w = 23
                            self._h = 33
                            return 86, 42
                        case 3:
                            c1 = 1
                            self._w = 30
                            self._h = 30
                            return 107, 42
                else: 
                    return 4,39  # Immagine statica
                    
            
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
                    return 482, 43 
            if self._arrow == 3:
                return 148,131       
        else: 
            return 64,75

#Classe zombie

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
    #ARENA
    global arena
    global contaTick, i 
    arena = Arena((600, 260)) #dim arena
    g2d.init_canvas(arena.size()) #creo canvas
    
    #ARTHUR
    arena.spawn(Arthur((0, 150)))

    #ZOMBIE spawn nel tick
        
     
    
    
    g2d.main_loop(tick)

main()