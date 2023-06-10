import SQL.commandes_bd as cbd
import time
from datetime import datetime


class DataProcessing:

    def __init__(self, app):
        self.app = app

        self.initialisation()

    def initialisation(self):
        self.mesure_touche_without_id_perf = []
        self.mic_values = []
        self.glove_values = []

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
        temps_depuis_debut = round(time.time() - self.app.time_start, 3)
        self.mic_values.append((temps_depuis_debut, id_notes_with_amplitudes))

        for i_doigt in self.data:
            if self.data[i_doigt]:
                if self.data[i_doigt]["id_note"] is None:
                    if temps_depuis_debut - self.data[i_doigt]["temps_depuis_debut"] >= .5:
                        self.data[i_doigt] = {}
                    else:
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
        temps_depuis_debut = round(time.time() - self.app.time_start, 3)
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

        date_perf = datetime.fromtimestamp(self.app.time_start)
        infos = (id_musicien, id_morceau, date_perf)
        id_perf = cbd.insert_performance(connexion_bd, *infos)
        infos = (id_perf, *infos)

        freqs_cardiaque = []

        nb_iterations = 0
        for temps_depuis_debut, pression_doigts, frequence_cardiaque, accelero_x, accelero_y in self.glove_values:
            if nb_iterations % 20 == 0:
                cbd.insert_accelero(connexion_bd, id_perf, accelero_x, accelero_y, temps_depuis_debut)

            if nb_iterations % 150 == 0 and nb_iterations != 0:
                cbd.insert_BPM(connexion_bd, id_perf, frequence_cardiaque, temps_depuis_debut)
                freqs_cardiaque.append(frequence_cardiaque)

            nb_iterations += 1

        for id_note, i_doigt, temps_depuis_debut, temps_presse in self.mesure_touche_without_id_perf:
            cbd.insert_touche_mesure(connexion_bd, id_perf, id_note, i_doigt, temps_presse, temps_depuis_debut)

        nb_fausses_notes = self.nb_fausses_notes(cbd.get_touches_morceau_ref(connexion_bd, id_morceau), self.mesure_touche_without_id_perf)
        avg_freq = sum(freqs_cardiaque) / len(freqs_cardiaque) if len(freqs_cardiaque) != 0 else 0
        cbd.update_performance(connexion_bd, id_perf, nb_fausses_notes, len(self.mesure_touche_without_id_perf), avg_freq, None)

        nom_combo = cbd.get_titre_morceau(connexion_bd, infos[2]) + " - " + infos[3].strftime("%d/%m/%Y %H:%M:%S")
        self.app.update_replay_combo(nom_combo, infos)

        self.app.update_state_stat_button()

        self.app.fen_perf()

        print("done")
        print()

    @staticmethod
    def nb_fausses_notes(touches_ref, touches_jouees):
        """
        Cette fontion calcule le nombre de fausses notes jouées dans le morceau.

        Paramètres :
            list touches_ref : les informations de référence du morceau
            lits touches_jouees : les informations des notes jouées par le musicien.

        Renvoi :
            int : le nombre de fausses notes
        """
        tolerance_temps = .5
        nb_bonnes_notes = 0

        for note_ref, temps_presse_ref, temps_depuis_debut_ref in touches_ref:
            for note_jouee, i_doigt, temps_depuis_debut_jouee, temps_presse_jouee in touches_jouees:
                if note_ref == note_jouee and abs(float(temps_depuis_debut_ref) - temps_depuis_debut_jouee) < tolerance_temps \
                        and abs(float(temps_depuis_debut_ref + temps_presse_ref) - (temps_depuis_debut_jouee + temps_presse_jouee)) < tolerance_temps:
                    nb_bonnes_notes += 1

        return len(touches_jouees) - nb_bonnes_notes
