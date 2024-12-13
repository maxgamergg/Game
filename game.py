import pygame
from pygame import mixer
from typing import Any
from random import randint


pygame.init()
mixer.init()

# Audio
LAUTSTAERKE = 0.025 # %

# fenster
BREITE, HÖHE = 1000, 800
WIN = pygame.display.set_mode((BREITE, HÖHE))
pygame.display.set_caption('Rakete: von Abdul')

# Spielergröße und geschwindigkeit
SPIELER_BREITE = 60
SPIELER_LÄNGE = 100
SPIELER_VELOCITY = 4
SPIELER_DIAG_VEL = 2.1

# Pause
PAUSED = False

# Esc out
ESC = False

# Kollision
KOLLISION = False

#  RGB VALUE
FARBE_ROT = (255, 0, 0)
FARBE_BLAU = (0, 0, 255)
FARBE_SCHWARZ = (0, 0, 0)

# Lade Assets
HINTERGRUND = pygame.image.load(r'Assets\Images\Space Background.png')
tempRAKETE = pygame.image.load(r'Assets\Images\rakete.png')
RAKETE = pygame.transform.scale(tempRAKETE, (SPIELER_BREITE, SPIELER_LÄNGE))

# Lade Musik
beyond = mixer.Sound(r'Assets/Music/St3phen - Beyond The Twilight.mp3')
full = mixer.Sound(r'Assets/Music/St3phen - Full Power.mp3')
arcade = mixer.Sound(r'Assets/Music/St3phen - Arcade Tokens.mp3')
fanfare = mixer.Sound(r'Assets/Music/St3phen - Victory Fanfare.mp3')

print('beyond:' + str(beyond.get_length()))
print('full:' + str(full.get_length()))
print('arcade:' + str(arcade.get_length()))
print('fanfare:' + str(fanfare.get_length()))


class Spieler:
    def __init__(self, x:int, y:int, breite:int, höhe:int, textur: Any, oben: Any, unten: Any, rechts: Any, links: Any, richtung: int) -> None:
        """
        Die Attribute eines Spielers
        :param x:
        :param y:
        :param breite:
        :param höhe:
        :param textur:
        :param oben:
        :param unten:
        :param rechts:
        :param links:
        :param richtung:
        """
        self.x = x
        self.y = y
        self.breite = breite
        self.höhe = höhe
        self.textur = textur
        self.oben = oben
        self.unten = unten
        self.rechts = rechts
        self.links = links
        self.richtung = richtung
        self.hitbox = (self.x, self.y, self.höhe, self.breite)

    def maleSpieler(self, tasten) -> None:
        """
        Rotiert das Objekt mithilfe der 'rotieren' Funktion und Drawt diese auf den Fenster (WIN)
        :param tasten:
        :return:
        """
        rotierteRakete = pygame.transform.rotate(self.textur, self.rotieren(tasten))
        WIN.blit(rotierteRakete, (self.x, self.y))

    def bewegungChecken(self, tasten):

        """
        Die Steuerung des eigenen Objektes |
        Wird in einer temporären Variable gespeichert, was die bewegung in der X und Y Achse in einen Frame ermöglicht, womit man flüssige diagonale Bewegungen erreichen kann.
        :param tasten:
        :return:
        """

        x_veränderung = 0
        y_veränderung = 0
        if tasten[self.oben] and self.y >= 0:
            y_veränderung -= SPIELER_VELOCITY
        if tasten[self.unten] and self.y <= (HÖHE - SPIELER_LÄNGE):
            y_veränderung += SPIELER_VELOCITY
        if tasten[self.rechts] and self.x <= (BREITE - SPIELER_BREITE):
            x_veränderung += SPIELER_VELOCITY
        if tasten[self.links] and self.x >= 0:
            x_veränderung -= SPIELER_VELOCITY

        if x_veränderung != 0 and y_veränderung != 0:
            x_veränderung *= SPIELER_DIAG_VEL / SPIELER_VELOCITY
            y_veränderung *= SPIELER_DIAG_VEL / SPIELER_VELOCITY

        self.x += x_veränderung
        self.y += y_veränderung


    def rotieren(self, tasten):

        """
        Rotiert die Textur des eigenen Objektes anhand der eigenen Steuerungstasten
        :param tasten:
        :return:
        """

        if tasten[self.oben] and not (tasten[self.rechts] or tasten[self.links]):       # Nach oben
            self.richtung = 0
            return self.richtung
        elif tasten[self.unten] and not (tasten[self.rechts] or tasten[self.links]):    # Nach unten
            self.richtung = 180
            return self.richtung
        elif tasten[self.rechts] and not (tasten[self.oben] or tasten[self.unten]):     # Nach rechts
            self.richtung = -90
            return self.richtung
        elif tasten[self.links] and not (tasten[self.oben] or tasten[self.unten]):      # Nach links
            self.richtung = 90
            return self.richtung
        elif tasten[self.oben] and tasten[self.rechts]:     # Diagonal oben rechts
            self.richtung = -45
            return self.richtung
        elif tasten[self.oben] and tasten[self.links]:      # Diagonal oben links
            self.richtung = 45
            return self.richtung
        elif tasten[self.unten] and tasten[self.rechts]:    # Diagonal unten rechts
            self.richtung = -135
            return self.richtung
        elif tasten[self.unten] and tasten[self.links]:     # Diagonal unten links
            self.richtung = 135
            return self.richtung
        return self.richtung                                # Standart rotation

    def collision(self, other: Any):
        """
        Checkt die Kollision von Sich selbst (Objekt) und von einen anderen Objekt mit deren Attribute
        :return:
        """
        self.hitbox = pygame.Rect(self.x, self.y, self.breite, self.höhe)
        other.hitbox = pygame.Rect(other.x, other.y, other.breite, other.höhe)
        return self.hitbox.colliderect(other.hitbox)


def refreshWin(tasten) -> None:

    """
    Aktuallisiert den Bildschirm |
    Drawt die Objekte und Chekt für Kollision mithulfe der Spielerclass
    """

    global KOLLISION

    WIN.blit(HINTERGRUND,(0, 0))
    SpielerEins.maleSpieler(tasten)
    SpielerZwei.maleSpieler(tasten)
    SpielerDrei.maleSpieler(tasten)

    if SpielerEins.collision(SpielerZwei):
        WIN.blit(HINTERGRUND, (0, 0))
        KOLLISION = True
        printCol()

    if SpielerDrei.collision(SpielerEins):
        WIN.blit(HINTERGRUND, (0,0))
        KOLLISION = True
        printCol()

    if SpielerDrei.collision(SpielerZwei):
        WIN.blit(HINTERGRUND, (0,0))
        KOLLISION = True
        printCol()

    pygame.display.update()

def Pause() -> None:

    """Zeigt den Pausebildschirm an"""

    WIN.blit(HINTERGRUND, (0, 0))

    font = pygame.font.Font(None, 74)
    pause = font.render("PAUSE", True, "BLACK")
    PauseOrt = pause.get_rect(center=(BREITE / 2, HÖHE / 2))

    WIN.blit(pause, PauseOrt)

    pygame.display.update()


def printCol() -> None:
    """
    Zeigt die Nachricht bei einer Kollision auf den Fenster (WIN)
    :return:
    """

    WIN.blit(HINTERGRUND, (0, 0))

    font = pygame.font.Font(None, 74)
    collision = font.render(f"Verloren!", True, "BLACK")
    ColOrt = collision.get_rect(center=(BREITE / 2, HÖHE / 2))

    WIN.blit(collision, ColOrt)

def SpawnRandX(breite: int):
    breite = randint(0, breite)
    return breite

def SpawnRandY(höhe: int):
    höhe = randint(0, höhe)
    return höhe

# Die Spieler, ihre Steuerung, Koordinaten und andere Attribute
SpielerEins =  Spieler(SpawnRandX(BREITE), SpawnRandY(HÖHE), SPIELER_BREITE, SPIELER_LÄNGE, RAKETE, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, 0)
SpielerZwei = Spieler(SpawnRandX(BREITE), SpawnRandY(HÖHE), SPIELER_BREITE, SPIELER_LÄNGE, RAKETE, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, 0)
SpielerDrei = Spieler(SpawnRandX(BREITE), SpawnRandY(HÖHE), SPIELER_BREITE, SPIELER_LÄNGE, RAKETE, pygame.K_z, pygame.K_h, pygame.K_j, pygame.K_g, 0)

def main() -> None:

    """Main Game Funktion"""

    global PAUSED
    global KOLLISION

    clock = pygame.time.Clock()
    run = True

    while run:

        # framerate (der Logik)
        clock.tick(120)

        # fenster schließ funktion
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE and not KOLLISION:
                    PAUSED = not PAUSED

                # Spiel neu starten
                if event.key == pygame.K_ESCAPE and KOLLISION:
                    SpielerEins.x, SpielerEins.y, SpielerEins.richtung = SpawnRandX(BREITE), SpawnRandY(HÖHE), 0
                    SpielerZwei.x, SpielerZwei.y, SpielerZwei.richtung = SpawnRandX(BREITE), SpawnRandY(HÖHE), 0
                    SpielerDrei.x, SpielerDrei.y, SpielerDrei.richtung = SpawnRandX(BREITE), SpawnRandY(HÖHE), 0
                    KOLLISION = not KOLLISION


        # Überprüft Steuerungsinput, nur wenn keine Kollision vorhanden ist
        if not KOLLISION:
                # Game Logik die Pausiert wird
                if not PAUSED:
                    key = pygame.key.get_pressed()

                    SpielerEins.rotieren(key)
                    SpielerZwei.rotieren(key)
                    SpielerDrei.rotieren(key)

                    SpielerEins.bewegungChecken(key)
                    SpielerZwei.bewegungChecken(key)
                    SpielerDrei.bewegungChecken(key)

                    refreshWin(key)

                # Handelt einen Pause Event
                else:
                    Pause()


    pygame.quit()

# Ausfühern nur bei direkter Dateiausführung/ vermeidet das Ausführen durch eine andere Datei  (Kann zu Fehlern führen)
if __name__ == '__main__':
    main()