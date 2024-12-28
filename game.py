import pygame
from pygame import mixer
from typing import Any
from random import randint

# Initialisiere Module
pygame.init()
mixer.init()

# Spiel Aktiv (Spieler am Spielen)
spiel_aktiv = False

# fenster
BREITE, HÖHE = 1000, 800
WIN = pygame.display.set_mode((BREITE, HÖHE))
pygame.display.set_caption('Rakete: von Abdul')

# Framerate (von der Logik)
FRAMERATE: int = 120

# Spielergröße und Geschwindigkeit
SPIELER_BREITE: int = 60
SPIELER_LÄNGE: int = 100
SPIELER_VELOCITY: float = 4
SPIELER_DIAG_VEL: float = 2.9

# Feuerspur Lebensdauer (in sec.)
FEUERDAUER: int = 20

# Dichte der Feuerpartikel
Dichte = 3

########## Debug Mode ##########
# Regeneriere Koordinaten 'R' (Wurde noch nicht implementiert zum vollem Game)
# Logt die aktuellen Koordinaten der Spieler in die Konsole mit 'K'
DebugMode: bool = True
# Status vom dritten Spieler (Testspieler)
SPIELER_DREI_AKTIV: bool = False
########## Debug Mode ##########

# Pause
PAUSED: bool = False

# Esc out
ESC: bool = False

# Kollision
KOLLISION: bool = False

#  RGB VALUE
FARBE_ROT: tuple[int, int, int] = (255, 0, 0)
FARBE_BLAU: tuple[int, int, int] = (0, 0, 255)
FARBE_SCHWARZ: tuple[int, int, int] = (0, 0, 0)
FARBE_WEISS: tuple[int, int, int] = (255, 255, 255)
FARBE_GRAU: tuple[int, int, int] = (50, 50, 50)

# Lade Assets
HINTERGRUND = pygame.image.load(r'Assets\Images\Space Background.png')
tempRAKETE = pygame.image.load(r'Assets\Images\rakete.png')
RAKETE = pygame.transform.scale(tempRAKETE, (SPIELER_BREITE, SPIELER_LÄNGE))

# Lade Musik
beyond = mixer.Sound(r'Assets/Music/St3phen - Beyond The Twilight.mp3')
full = mixer.Sound(r'Assets/Music/St3phen - Full Power.mp3')
arcade = mixer.Sound(r'Assets/Music/St3phen - Arcade Tokens.mp3')
fanfare = mixer.Sound(r'Assets/Music/St3phen - Victory Fanfare.mp3')

# Liste der Musikdateien
musikliste = [beyond, full, arcade, fanfare]

# Variablen für Musik
music_on = True
volume = 0.5  # Startlautstärke (0.0 bis 1.0)

print('musiklänge in sec.\n')
print('beyond: ' + str(beyond.get_length()))
print('full: ' + str(full.get_length()))
print('arcade: ' + str(arcade.get_length()))
print('fanfare: ' + str(fanfare.get_length()))


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
        Rotiert das Objekt mithilfe der 'rotieren' Funktion und malt diese auf den Fenster (WIN)
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
        return self.richtung                                # Standard rotation

    def collision(self, other: Any):
        """
        Checkt die Kollision von Sich selbst (Objekt) und von einem anderen Objekt mit deren Attribute
        :return:
        """
        self.hitbox = pygame.Rect(self.x, self.y, self.breite, self.höhe)
        other.hitbox = pygame.Rect(other.x, other.y, other.breite, other.höhe)
        return self.hitbox.colliderect(other.hitbox)


class FeuerSpur:
    def __init__(self, x: int, y: int, Lebensdauer: int, farbe: tuple[int, int, int]):
        self.x = x
        self.y = y
        self.Größe = randint(3, 7)
        self.Lebensdauer = Lebensdauer * FRAMERATE
        self.Farbe = farbe

    def update(self):
        if self.Größe >= 0:
            self.Größe -= 0.03 # Nimmt pro Aufrufung Weg von der größe wird jedoch auf int "getrimmt" im Laufe des Spiels
        self.Lebensdauer -= 1 # Nimmt pro Aufrufung einen Frame Weg von der Lebensdauer

    def malen(self, fenster):
        if self.Größe >= 0:
            pygame.draw.circle(fenster, self.Farbe, (self.x, self.y), int(self.Größe))




def refreshWin(tasten) -> None:

    """
    Aktualisiert den Bildschirm |
    Malt die Objekte und checkt für Kollision mithilfe der Spieler-Class
    """

    global KOLLISION

    WIN.blit(HINTERGRUND,(0, 0))

    # Spieler Eins Feuerspur
    for _ in range(Dichte):
        SpielerEinsPartikel.append(
            FeuerSpur(
                SpielerEins.x + SPIELER_BREITE // 2 + randint(-5, 5),
                SpielerEins.y + SPIELER_LÄNGE // 2 + randint(-5, 5),
                90, FARBE_ROT
            )
        )

    for _ in range(Dichte):
        SpielerZweiPartikel.append(
            FeuerSpur(
                SpielerZwei.x + SPIELER_BREITE // 2 + randint(-5, 5),
                SpielerZwei.y + SPIELER_LÄNGE // 2 + randint(-5, 5),
                90, FARBE_BLAU
            )
        )
    # Partikel malen und Lebenszeit Überprüfen / Updaten und Spieler Malen
    for partikel in SpielerEinsPartikel[:]:
        partikel.update()
        partikel.malen(WIN)
        if partikel.Größe <= 0 or partikel.Lebensdauer <= 0:
            SpielerEinsPartikel.remove(partikel)

    SpielerEins.maleSpieler(tasten)

    # Partikel malen und Lebenszeit Überprüfen / Updaten und Spieler Malen
    for partikel in SpielerZweiPartikel[:]:
        partikel.update()
        partikel.malen(WIN)
        if partikel.Größe <= 0 or partikel.Lebensdauer <= 0:
            SpielerZweiPartikel.remove(partikel)

    SpielerZwei.maleSpieler(tasten)

    if SPIELER_DREI_AKTIV:
        SpielerDrei.maleSpieler(tasten)

    if SpielerEins.collision(SpielerZwei):
        WIN.blit(HINTERGRUND, (0, 0))
        KOLLISION = True
        printCol('Verloren!')
        # Ich kann nicht überprüfen welche Rakete in welche hereingeflogen ist aber man könnte es machen, indem man die richtung des Spielers dann benutzt, was etwas schwierig sein kann.

    if SPIELER_DREI_AKTIV and (SpielerDrei.collision(SpielerEins) or SpielerDrei.collision(SpielerZwei)):
        WIN.blit(HINTERGRUND, (0, 0))
        KOLLISION = True
        printCol('ZZ')

    # Kollisionserkennung: Spieler 2 kann nicht in die Spur von Spieler 1 laufen
    for partikel in SpielerEinsPartikel:
        if (
            SpielerZwei.x < partikel.x < SpielerZwei.x + SPIELER_BREITE
            and
            SpielerZwei.y < partikel.y < SpielerZwei.y + SPIELER_BREITE
        ):
            KOLLISION = True
            printCol('Spieler Blau ist in die Spur vom Roten Spieler geflogen!')

    # Kollisionserkennung: Spieler 1 kann nicht in die Spur von Spieler 2 laufen
    for partikel in SpielerZweiPartikel:
        if (
            SpielerEins.x < partikel.x < SpielerEins.x + SPIELER_BREITE
            and
            SpielerEins.y < partikel.y < SpielerEins.y + SPIELER_BREITE
        ):
            KOLLISION = True
            printCol('Spieler Rot ist in die Spur vom Blauen Spieler geflogen!')


    pygame.display.update()

def Pause() -> None:

    """Zeigt den Pausebildschirm"""

    WIN.blit(HINTERGRUND, (0, 0))

    font = pygame.font.Font(None, 74)
    pause = font.render("PAUSIERT", True, "BLACK")
    PausePos = pause.get_rect(center=(BREITE / 2, HÖHE / 2 - 75))

    pygame.draw.rect(WIN, FARBE_WEISS, PausePos.inflate(40, 40))

    WIN.blit(pause, PausePos)

    pygame.display.update()

def draw_slider(x, y, width, height, value):
    """
    Zeichnet einen Lautstärkeregler (Slider).
    """
    # Hintergrundleiste
    pygame.draw.rect(WIN, FARBE_SCHWARZ, (x, y, width, height))
    # Bewegliche Leiste basierend auf der Lautstärke
    pygame.draw.rect(WIN, FARBE_BLAU, (x, y, width * value, height))


def options_menu():
    """
    Zeigt das Optionsmenü an.
    """
    global music_on, volume

    clock = pygame.time.Clock()
    slider_rect = pygame.Rect(BREITE // 4, HÖHE // 2, BREITE // 2, 20)
    back_button = pygame.Rect(BREITE // 2 - 100, HÖHE - 100, 200, 50)
    toggle_button = pygame.Rect(BREITE // 2 - 150, HÖHE // 3, 300, 50)

    while True:
        WIN.fill(FARBE_WEISS)
        mouse_pos = pygame.mouse.get_pos()

        # Titeltext
        font = pygame.font.Font(None, 74)
        options_text = font.render("Optionen", True, FARBE_BLAU)
        options_rect = options_text.get_rect(center=(BREITE / 2, 50))
        WIN.blit(options_text, options_rect)

        # Toggle Button für Musik
        pygame.draw.rect(WIN, FARBE_WEISS, toggle_button)
        toggle_text = font.render("Musik: AN" if music_on else "Musik: AUS", True, FARBE_ROT if not music_on else FARBE_BLAU)
        toggle_text_rect = toggle_text.get_rect(center=toggle_button.center)
        if toggle_text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(WIN, FARBE_GRAU, toggle_text_rect.inflate(20, 20))
        WIN.blit(toggle_text, toggle_text_rect)

        # Lautstärkeregler

        slider_text = font.render(f"Lautstärke: {int(volume * 100)}%", True, FARBE_SCHWARZ)
        slider_text_rect = slider_text.get_rect(center=(BREITE / 2, slider_rect.y - 40))
        if slider_rect.collidepoint(mouse_pos):
            pygame.draw.rect(WIN, FARBE_SCHWARZ, slider_rect.inflate(10, 10))
        draw_slider(slider_rect.x, slider_rect.y, slider_rect.width, slider_rect.height, volume)
        WIN.blit(slider_text, slider_text_rect)

        # Zurück-Button
        pygame.draw.rect(WIN, FARBE_WEISS, back_button)
        back_text = font.render("Zurück", True, FARBE_BLAU)
        back_text_rect = back_text.get_rect(center=back_button.center)
        if back_button.collidepoint(mouse_pos):
            pygame.draw.rect(WIN, FARBE_GRAU, back_button.inflate(20, 20))
        WIN.blit(back_text, back_text_rect)


        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return  # Zurück ins Hauptmenü
                elif toggle_button.collidepoint(event.pos):
                    music_on = not music_on  # Musik ein-/ausschalten

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION and event.buttons[0]:
                if slider_rect.collidepoint(event.pos):
                    # Slider-Wert basierend auf Mausposition
                    relative_x = event.pos[0] - slider_rect.x
                    volume = max(0, min(1, relative_x / slider_rect.width))  # Zwischen 0 und 1

        clock.tick(FRAMERATE)


def main_menu():
    """
    Zeigt das Hauptmenü des Spiels an und verarbeitet Benutzerinteraktionen.
    """

    # Framerate (der Logik)
    clock = pygame.time.Clock()
    clock.tick(FRAMERATE)

    menu_font = pygame.font.Font(None, 74)  # Schriftart für das Menü
    options_font = pygame.font.Font(None, 36)  # Kleinere Schrift für die Optionen (Einstellung für Steuerung, Audio etc.) !!! NICHT IMPLEMENTIERT !!!

    # Text für die Menüpunkte
    start_game_text = menu_font.render("Spiel starten", True, FARBE_BLAU)
    options_text = menu_font.render("Optionen", True, FARBE_BLAU)
    quit_text = menu_font.render("Beenden", True, FARBE_BLAU)

    # Position der Menüpunkte
    start_game_rect = start_game_text.get_rect(center=(BREITE / 2, HÖHE / 3))
    options_rect = options_text.get_rect(center=(BREITE / 2, HÖHE / 2))
    quit_rect = quit_text.get_rect(center=(BREITE / 2, HÖHE * 2 / 3))

    # Zeige das Menü
    while True:
        WIN.fill(FARBE_WEISS)

        # Mausposition abfragen
        mouse_pos = pygame.mouse.get_pos()

        # Verdunkelungseffekt durch Färbung der Buttons, wenn die Maus darüber fährt
        if start_game_rect.collidepoint(mouse_pos):
            pygame.draw.rect(WIN, FARBE_GRAU, start_game_rect.inflate(20, 20))  # Verdunkelung (Dunkelgrau)
        if options_rect.collidepoint(mouse_pos):
            pygame.draw.rect(WIN, FARBE_GRAU, options_rect.inflate(20, 20))
        if quit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(WIN, FARBE_GRAU, quit_rect.inflate(20, 20))

        # Buttons und Texte zeichnen
        WIN.blit(start_game_text, start_game_rect)
        WIN.blit(options_text, options_rect)
        WIN.blit(quit_text, quit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_rect.collidepoint(mouse_pos):
                    return  # Spiel starten
                elif options_rect.collidepoint(mouse_pos):
                    options_menu()
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()  # Spiel beenden
                    exit()

def printCol(wer: any, ) -> None:
    """
    Zeigt die Nachricht bei einer Kollision auf den Fenster (WIN)
    :return:
    """

    WIN.blit(HINTERGRUND, (0, 0))

    font = pygame.font.Font(None, 46)
    collision = font.render(f"{wer}", True, "BLACK")
    ColPos = collision.get_rect(center=(BREITE / 2, HÖHE / 2))

    pygame.draw.rect(WIN, "WHITE", ColPos.inflate(20, 20))

    WIN.blit(collision, ColPos)

def SpawnRandX(mal: int, index: int):

    """Debugfunktion"""

    Breite = []
    while mal >= 0:
        value = randint(0, (BREITE - SPIELER_BREITE))
        Breite.append(value)
        mal -= 1
    return Breite[index]

def SpawnRandY(höhe: int):

    """Debugfunktion"""

    höhe = randint(0, höhe)
    return höhe



# Die Spieler, ihre Steuerung, Koordinaten und andere Attribute
SpielerEins = Spieler(270, 350, SPIELER_BREITE, SPIELER_LÄNGE, RAKETE, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, 0)
SpielerZwei = Spieler(670, 350, SPIELER_BREITE, SPIELER_LÄNGE, RAKETE, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, 0)
SpielerDrei = Spieler(SpawnRandX(3, 1), SpawnRandY(HÖHE), SPIELER_BREITE, SPIELER_LÄNGE, RAKETE, pygame.K_z, pygame.K_h, pygame.K_j, pygame.K_g, 0)

# Die Liste um die Feuerpartikel zu speichern
SpielerEinsPartikel = [] # SpielerEins Partikel liste
SpielerZweiPartikel = [] # SpielerZwei Partikel liste

def main() -> None:

    """Main Game Funktion"""

    global PAUSED
    global KOLLISION

    main_menu()

    clock = pygame.time.Clock()
    run = True

    while run:

        # Framerate (der Logik)
        clock.tick(FRAMERATE)

        # fenster schließ funktion
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE and not KOLLISION:
                    PAUSED = not PAUSED

                # Spiel neu starten
                if event.key == pygame.K_ESCAPE and KOLLISION:
                    SpielerEins.x, SpielerEins.y, SpielerEins.richtung = 270, 350, 0
                    SpielerZwei.x, SpielerZwei.y, SpielerZwei.richtung = 670, 350, 0
                    if SPIELER_DREI_AKTIV:
                        SpielerDrei.x, SpielerDrei.y, SpielerDrei.richtung = SpawnRandX(3, 1), SpawnRandY(HÖHE), 0
                    KOLLISION = not KOLLISION

                # Debug Respawn
                if event.key == pygame.K_r and DebugMode:
                    SpielerEins.x, SpielerEins.y, SpielerEins.richtung = SpawnRandX(3, 3), SpawnRandY(HÖHE), 0
                    SpielerZwei.x, SpielerZwei.y, SpielerZwei.richtung = SpawnRandX(3, 2), SpawnRandY(HÖHE), 0
                    if SPIELER_DREI_AKTIV:
                        SpielerDrei.x, SpielerDrei.y, SpielerDrei.richtung = SpawnRandX(3, 1), SpawnRandY(HÖHE), 0

                # Debug Koordinaten in die Konsole ausgeben
                if event.key == pygame.K_k and DebugMode:
                    print('Koordinaten:\n')
                    print(f'Erster Spieler X: {SpielerEins.x}, Y: {SpielerEins.y}')
                    print(f'Zweiter Spieler X: {SpielerZwei.x}, Y: {SpielerZwei.y}')

                    if SPIELER_DREI_AKTIV:
                        print(f'Dritter Spieler X: {SpielerDrei.x}, Y: {SpielerDrei.y}')



        # Überprüft Steuerungsinput, nur wenn keine Kollision vorhanden ist
        if not KOLLISION:
                # Game Logik die Pausiert wird
                if not PAUSED:
                    key = pygame.key.get_pressed()

                    SpielerEins.rotieren(key)
                    SpielerZwei.rotieren(key)
                    if SPIELER_DREI_AKTIV:
                        SpielerDrei.rotieren(key)

                    SpielerEins.bewegungChecken(key)
                    SpielerZwei.bewegungChecken(key)
                    if SPIELER_DREI_AKTIV:
                        SpielerDrei.bewegungChecken(key)

                    refreshWin(key)

                # Handelt den Pause-Event
                else:
                    Pause()
        else:
            SpielerEinsPartikel.clear()
            SpielerZweiPartikel.clear()

    pygame.quit()

# Ausfühern nur bei direkter Dateiausführung / vermeidet das Ausführen durch eine andere Datei (Kann zu Fehlern führen)
if __name__ == '__main__':
    main()