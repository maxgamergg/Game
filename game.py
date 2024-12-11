import pygame
from pygame import mixer
from typing import Any


pygame.init()
mixer.init()

# Audio
LAUTSTAERKE = 0.025 # %

# fenster
BREITE, HÖHE = 1000, 800
WIN = pygame.display.set_mode((BREITE, HÖHE))
pygame.display.set_caption('Abduls Spiel')

# spielergröße und geschwindigkeit
SPIELER_BREITE = 60
SPIELER_LÄNGE = 100
SPIELER_VELOCITY = 3
SPIELER_DIAG_VEL = 1.9

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



class Spieler:
    def __init__(self, x:int, y:int, breite:int, höhe:int, textur: Any, oben: Any, unten: Any, rechts: Any, links: Any, richtung: int) -> None:
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
        rotierteRakete = pygame.transform.rotate(self.textur, self.rotieren(tasten))
        WIN.blit(rotierteRakete, (self.x, self.y))

    def bewegungChecken(self, tasten):
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
        self.hitbox = pygame.Rect(self.x, self.y, self.breite, self.höhe)
        other.hitbox = pygame.Rect(other.x, other.y, other.breite, other.höhe)
        return self.hitbox.colliderect(other.hitbox)


def refreshWin(tasten) -> None:

    global KOLLISION

    WIN.blit(HINTERGRUND,(0, 0))
    SpielerEins.maleSpieler(tasten)
    SpielerZwei.maleSpieler(tasten)

    if SpielerEins.collision(SpielerZwei):
        WIN.blit(HINTERGRUND, (0, 0))
        KOLLISION = True
        printCol()

    pygame.display.update()

def Pause():
    WIN.blit(HINTERGRUND, (0, 0))

    font = pygame.font.Font(None, 74)
    pause = font.render("PAUSE", True, "BLACK")
    PauseOrt = pause.get_rect(center=(BREITE / 2, HÖHE / 2))

    WIN.blit(pause, PauseOrt)

    pygame.display.update()


def printCol():
    WIN.blit(HINTERGRUND, (0, 0))

    font = pygame.font.Font(None, 74)
    collision = font.render(f"Verloren!", True, "BLACK")
    ColOrt = collision.get_rect(center=(BREITE / 2, HÖHE / 2))

    WIN.blit(collision, ColOrt)


SpielerEins =  Spieler(400, 500, SPIELER_BREITE, SPIELER_LÄNGE, RAKETE, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, 0)
SpielerZwei = Spieler(600, 300, SPIELER_BREITE, SPIELER_LÄNGE, RAKETE, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, 0)

def main() -> None:

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

                if event.key == pygame.K_ESCAPE and KOLLISION:
                    SpielerEins.x, SpielerEins.y = 400, 500
                    SpielerZwei.x, SpielerZwei.y = 600, 300
                    KOLLISION = not KOLLISION



        if not KOLLISION:
                if not PAUSED:
                    key = pygame.key.get_pressed()

                    SpielerEins.rotieren(key)
                    SpielerZwei.rotieren(key)

                    SpielerEins.bewegungChecken(key)
                    SpielerZwei.bewegungChecken(key)

                    refreshWin(key)

                else:
                    Pause()


    pygame.quit()

if __name__ == '__main__':
    main()