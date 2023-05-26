import os
import csv
import commandes_bd as cbd

white_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6']
black_notes = ['Db4', 'Eb4', 'Gb4', 'Ab4', 'Bb4', 'Db5', 'Eb5', 'Gb5', 'Ab5', 'Bb5']


def inserer_morceau_ref(connexion_bd, titre, bpm_morceau, chemin_csv_touches):
    """
    Insère un morceau de référence dans la base de données.

    Paramètres :
        str titre: Titre du morceau
        str chemin_csv_touches: Chemin du fichier csv contenant les touches à rentrer dans la bd
    """
    id_morceau = cbd.insert_morceau(connexion_bd, titre, bpm_morceau)

    with open(chemin_csv_touches, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')

        for row in csv_reader:
            note = row[0]
            if note in white_notes:
                note_index = white_notes.index(note)
            elif note in black_notes:
                note_index = len(white_notes) + black_notes.index(note)
            else:
                raise Exception("Note non disponible sur le piano !")

            tps_presse = round(float(row[2]), 3)
            tps_depuit_debut = round(float(row[3]), 3)

            cbd.insert_touche_ref(connexion_bd, id_morceau, note_index, tps_presse, tps_depuit_debut)


chemin_dossier_morceaux = "Morceaux/"

connexion_bd = cbd.ouvrir_connexion_bd()

if connexion_bd is not None:
    cbd.clear_touche_ref(connexion_bd)
    cbd.clear_morceau(connexion_bd)

    for file_name in os.listdir(chemin_dossier_morceaux):

        if file_name.split(".")[-1] == "csv":

            titre_morceau, bpm_morceau = file_name[:-4].split("_")
            chemin_csv_touches = chemin_dossier_morceaux + file_name

            inserer_morceau_ref(connexion_bd, titre_morceau, bpm_morceau, chemin_csv_touches)

    cbd.fermer_connexion_bd(connexion_bd)
