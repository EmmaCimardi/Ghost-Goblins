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
