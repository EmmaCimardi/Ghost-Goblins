Point = tuple[float, float]

class Actor:
    """Interfaccia da implementare per ciascun personaggio del gioco.
    """
    def move(self, arena: "Arena"):
        """Chiamato dall’arena, nel turno dell’attore.
        """
        raise NotImplementedError("Metodo astratto")

    def pos(self) -> Point:
        """Restituisce la posizione (x, y) dell’attore (angolo in alto a sinistra).
        """
        raise NotImplementedError("Metodo astratto")

    def size(self) -> Point:
        """Restituisce la dimensione (larghezza, altezza) dell’attore.
        """
        raise NotImplementedError("Metodo astratto")

    def sprite(self) -> Point | None:
        """Restituisce la posizione (x, y) dello sprite corrente,
        se è contenuto in un’immagine più grande con altri sprite;
        altrimenti restituisce None.
        """
        raise NotImplementedError("Metodo astratto")


def check_collision(a1: Actor, a2: Actor) -> bool:
    """Controlla se due attori (argomenti) sono in collisione o a contatto,
    usando la rilevazione tramite bounding-box.
    Restituisce True se gli attori si toccano o si sovrappongono, False altrimenti.
    """
    x1, y1, w1, h1 = a1.pos() + a1.size()
    x2, y2, w2, h2 = a2.pos() + a2.size()
    return (y2 <= y1 + h1 and y1 <= y2 + h2 and
            x2 <= x1 + w1 and x1 <= x2 + w2)



class Arena():
    """Gioco 2D generico, con una data dimensione in pixel e una lista di attori.
    """
    def __init__(self, size: Point):
        """Crea un’arena, con dimensioni date in pixel.
        """
        self._w, self._h = size
        self._count = 0
        self._turn = -1
        self._actors = []
        self._curr_keys = self._prev_keys = tuple()
        self._collisions = []

    def spawn(self, a: Actor):
        """Registra un attore in questa arena.
        Gli attori vengono disegnati nell’ordine di registrazione.
        """
        if a not in self._actors:
            self._actors.append(a)

    def kill(self, a: Actor):
        """Rimuove un attore da questa arena.
        """
        if a in self._actors:
            self._actors.remove(a)

    def tick(self, keys=[]):
        """Muove tutti gli attori (tramite il loro metodo move).
        """
        actors = list(reversed(self._actors))
        self._detect_collisions(actors)
        self._prev_keys = self._curr_keys
        self._curr_keys = keys
        for self._turn, a in enumerate(actors):
            a.move(self)
        self._count += 1

    def _naive_collisions(self, actors):
        # Metodo semplice per calcolare tutte le collisioni tra attori
        self._collisions.clear()
        for a1 in actors:
            colls1 = []
            for a2 in actors:
                if a1 is not a2 and check_collision(a1, a2):
                    colls1.append(a2)
            self._collisions.append(colls1)

    def _detect_collisions(self, actors):
        self._collisions.clear()
        # Divide l’arena in celle (tile), per un rilevamento delle collisioni più efficiente
        tile = 40
        nx, ny = -(-self._w // tile),  -(-self._h // tile)  # divisione arrotondata per eccesso
        cells = [set() for _ in range(nx * ny)]  # ogni cella è un insieme
        for i, a in enumerate(actors):
            x, y, w, h = (round(v) for v in a.pos() + a.size())
            for tx in range((x - 1) // tile, 1 + (x + w + 1) // tile):
                for ty in range((y - 1) // tile, 1 + (y + h + 1) // tile):
                    if 0 <= tx < nx and 0 <= ty < ny:
                        # aggiungi l’attore `a` alla cella (tx, ty)
                        cells[ty * nx + tx].add(i)
        for i, a in enumerate(actors):
            neighs = set()
            x, y, w, h = (round(v) for v in a.pos() + a.size())
            for tx in range((x - 1) // tile, 1 + (x + w + 1) // tile):
                for ty in range((y - 1) // tile, 1 + (y + h + 1) // tile):
                    if 0 <= tx < nx and 0 <= ty < ny:
                        # tutti gli attori che condividono una cella con `a`
                        neighs |= cells[ty * nx + tx]
            colls = [actors[j] for j in sorted(neighs, reverse=True)
                     if i != j and check_collision(a, actors[j])]
            self._collisions.append(colls)

    def collisions(self) -> list[Actor]:
        """Restituisce la lista degli attori in collisione con l’attore corrente.
        """
        t, colls = self._turn, self._collisions
        return colls[t] if 0 <= t < len(colls) else []

    def actors(self) -> list:
        """Restituisce una copia della lista degli attori.
        """
        return list(self._actors)

    def size(self) -> Point:
        """Restituisce la dimensione (larghezza, altezza) dell’arena.
        """
        return (self._w, self._h)

    def count(self) -> int:
        """Restituisce il numero totale di tick (o frame).
        """
        return self._count

    def current_keys(self) -> list[str]:
        """Restituisce i tasti attualmente premuti.
        """
        return self._curr_keys

    def previous_keys(self) -> list[str]:
        """Restituisce i tasti premuti al tick precedente.
        """
        return self._prev_keys
