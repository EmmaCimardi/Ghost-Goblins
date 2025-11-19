import g2d
from actor import Actor, Point, Arena

img=False
global backX
global scala1, scala2, scala3, lago1, fineScala, c, c1
scala1=715
scala2=912
scala3=1078
c = 1 
scala3=10
c1 = 1 
lago1=1164
fineScala=1131


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
                scala3 <= self._x - backX <= fineScala):
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
            return 32, 23

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
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 22, 36
        self._speed = 2
        self._dx, self._dy = self._speed, self._speed
        
    def move(self, arena: Arena):
        arena_w, arena_h = arena.size()
        
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


backX=0
def tick():
    global backX
    g2d.clear_canvas()
    g2d.draw_image("ghosts-goblins-bg.png", (backX,0), (0,0))
    
    for a in arena.actors():
        if a.sprite() != None:
            sprite_pos = a.sprite()
            
            if len(sprite_pos) == 2:
                g2d.draw_image("ghosts-goblins.png", a.pos(), a.sprite(), a.size())
            
            elif len(sprite_pos) == 4:
                sx, sy, w, h = sprite_pos
                g2d.draw_image("ghosts-goblins.png", a.pos(), (sx, sy), (w, h))
    
    if img == True: 
        g2d.draw_image("ending.webp", (0,0), (600,600))
    
    #da cambiare 
    art = None
    for actor in arena.actors():
        if isinstance(actor, Arthur):
            art = actor
            break
    #da cambiare 
    if art:
        g2d.draw_text(f"x={art._x}", (10, 10), 20)
        g2d.draw_text(f"frame={art._frame}", (10, 40), 20)
    
    arena.tick(g2d.current_keys())
    
def main():
    global arena
    arena = Arena((600, 260))
    g2d.init_canvas(arena.size())
    
    arena.spawn(Zombie((60,180)))
    arena.spawn(Arthur((0, 150)))
    
    g2d.main_loop(tick)

main()