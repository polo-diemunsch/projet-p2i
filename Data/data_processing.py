import SQL.commandes_bd as cbd
import time
from datetime import datetime


class DataProcessing:

    def __init__(self, app):
        self.app = app

        self.initialisation()

    def initialisation(self, time_start=None):
        self.mesure_touche_without_id_perf = []
        self.mic_values = []
        self.glove_values = []

        self.time_start = None if (time_start is None) else time_start
        self.id_perf = None

        self.data = {}
        for i in range(5):
            self.data[i] = {}
        self.note_taken = set()

    def get_mic_values(self, id_notes_with_amplitudes):
        """
        Stocke les données du micro envoyées depuis le manager Arduino en ajoutant le temps depuis le début du morceau.

        Paramètres :
            dict id_notes_with_amplitudes: index notes et amplitudes calculées sur l'Arduino du micro
        """
        temps_depuis_debut = round(time.time() - self.time_start, 3) - .1
        self.mic_values.append((temps_depuis_debut, id_notes_with_amplitudes))

        for i_doigt in self.data:
            if self.data[i_doigt]:
                if self.data[i_doigt]["id_note"] is None:
                    self.fill_id_note_max_amp(id_notes_with_amplitudes, i_doigt)

                elif id_notes_with_amplitudes.get(self.data[i_doigt]["id_note"], 0) < 15:
                    self.mesure_touche_without_id_perf.append((self.data[i_doigt]["id_note"], i_doigt, self.data[i_doigt]["temps_depuis_debut"],
                                                               temps_depuis_debut - self.data[i_doigt]["temps_depuis_debut"]))

                    self.app.un_highlight_key(self.data[i_doigt]["id_note"])
                    self.note_taken.remove(self.data[i_doigt]["id_note"])
                    self.data[i_doigt] = {}

    def get_glove_values(self, accelero_x, accelero_y, frequence_cardiaque, pression_doigts):
        """
        Stocke les données du gant envoyées depuis le manager Arduino en ajoutant le temps depuis le début du morceau.

        Paramètres :
            int accelero_x: Valeur en X de l'accéléromètre
            int accelero_y: Valeur en Y de l'accéléromètre
            int frequence_cardiaque: Valeur de fréquence cardiaque
            bytes pression_doigts: Valeurs d'appui de chaque doigt
        """
        temps_depuis_debut = round(time.time() - self.time_start, 3) - .5
        self.glove_values.append((temps_depuis_debut, pression_doigts, frequence_cardiaque, accelero_x, accelero_y))

        for i in range(5):
            if (pression_doigts >> i) & 1 and not self.data[i]:
                self.data[i]["id_note"] = None
                if self.mic_values and self.mic_values[-1][0] < temps_depuis_debut:
                    self.fill_id_note_max_amp(self.mic_values[-1][1], i)

                self.data[i]["temps_depuis_debut"] = temps_depuis_debut

    def fill_id_note_max_amp(self, id_notes_with_amplitudes, i_doigt):
        id_note_max_amp = -1
        max_amp = -1
        for id_note, amp in id_notes_with_amplitudes.items():
            if amp > max_amp and amp > 15 and id_note not in self.note_taken:
                max_amp = amp
                id_note_max_amp = id_note

        if id_note_max_amp != -1:
            self.data[i_doigt]["id_note"] = id_note_max_amp
            self.note_taken.add(self.data[i_doigt]["id_note"])
            self.app.highlight_key(self.data[i_doigt]["id_note"])

    def put_data_in_database(self, connexion_bd, id_musicien, id_morceau):

        print()
        print(self.mic_values)
        print(self.glove_values)
        print(self.mesure_touche_without_id_perf)

        date_perf = datetime.fromtimestamp(self.time_start)
        infos = (id_musicien, id_morceau, date_perf)
        id_perf = cbd.insert_performance(connexion_bd, *infos)
        infos = (id_perf, *infos)

        # nb_iterations = 0
        # for temps_depuis_debut, pression_doigts, frequence_cardiaque, accelero_x, accelero_y in self.glove_values:
        #     cbd.insert_accelero(connexion_bd, id_perf, accelero_x, accelero_y, temps_depuis_debut)
        #     if nb_iterations % 75 == 0 and nb_iterations != 0:
        #         cbd.insert_BPM(connexion_bd, id_perf, frequence_cardiaque, temps_depuis_debut)
        #
        #     nb_iterations += 1

        for id_note, i_doigt, temps_depuis_debut, temps_presse in self.mesure_touche_without_id_perf:
            cbd.insert_touche_mesure(connexion_bd, id_perf, id_note, i_doigt, temps_presse, temps_depuis_debut)

        self.time_start = None

        nom_combo = cbd.get_titre_morceau(connexion_bd, infos[2]) + " - " + infos[3].strftime("%d/%m/%Y %H:%M:%S")
        self.app.update_replay_combo(nom_combo, infos)

        print("done")
        print()
