import pygame

SCREEN = WIDTH, HEIGHT = 15*50, 600

class tile:
    def __int__(self, largeur, hauteur_pour_un_temps, couleur, note):
        self.largeur = largeur
        self.hauteur_pour_un_temps = hauteur_pour_un_temps
        self.couleur = couleur
        self.note = note

    def calculer_position(self):
        """Calcule les coordonnées d'affichage de le tuile en fonction de la note à laquelle elle correspond"""
        self.y = 2

class partition:
    def __init__(self):
        self.liste_notes = []


C4 = tile(50, 100, "red", 0)
partition_test = partition()
partition_test.liste_notes.append((C4, 6))

class Notes_qui_defilent:
    def __int__(self, largeur_touche, fenetre, partition, hauteur_fenetre):
        self.largeur_touche = largeur_touche
        self.fenetre = fenetre
        self.partition = partition
        self.timer = 0
        self.hauteur_fenetre = hauteur_fenetre

    def dessiner_notes_qui_défilent(self):
        for duo in partition:
            if duo[1] - self.timer <= 4:
                tile = duo[0]
                pygame.draw.rect(tile.fenetre, tile.couleur, (self.hauteur_fenetre - tile.hauteur_pour_un_temps*(duo[1]-self.timer), b, tile.largeur, tile.hauteur)


