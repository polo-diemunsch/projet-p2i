import tkinter as tk
import colorsys
from tkinter import ttk
import SQL.commandes_bd as cbd
# import R.r as r
import time
from Arduino.custom_arduino_manager import CustomArduinoManager
from Data.data_processing import DataProcessing


class App(tk.Tk):
    """
    Class gérant l'affichage graphique de l'application
    """

    def __init__(self):
        """
        Initialise l'application, défini le titre, l'icône, la taille de la fenêtre et la position.
        """
        super().__init__()
        self.title("GBAP")
        self.wm_iconphoto(True, tk.PhotoImage(file="GUI/images/icon.png"))

        self.white_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6']
        self.black_notes = ['Db4', 'Eb4', 'Gb4', 'Ab4', 'Bb4', 'Db5', 'Eb5', 'Gb5', 'Ab5', 'Bb5']

        self.possible_levels = ["Claqué au sol", "N'a jamais touché de piano", "Débutant", "Intermédiaire", "Confirmé",
                                "Expert", "Frédéric Chopin"]

        self.WIDTH_WHITE_KEYS = 60
        self.HEIGHT_WHITE_KEYS = 200
        self.WIDTH_BLACK_KEYS = 35
        self.HEIGHT_BLACK_KEYS = 125

        self.WIDTH_SIDE_PANEL = 300

        self.PX_PER_SEC = 200

        self.WIDTH = len(self.white_notes) * self.WIDTH_WHITE_KEYS + self.WIDTH_SIDE_PANEL
        self.HEIGHT = self.HEIGHT_WHITE_KEYS + 3 * self.PX_PER_SEC

        # Pour centrer la fenêtre sur l'écran
        pos_right = int(self.winfo_screenwidth() / 2 - self.WIDTH / 2)
        pos_down = int(self.winfo_screenheight() / 2.25 - self.HEIGHT / 2)

        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{pos_right}+{pos_down}")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.connexion_bd = cbd.ouvrir_connexion_bd()

        self.song_title_combo_to_data = {}
        self.musician_name_combo_to_data = {}
        self.perf_name_combo_to_data = {}

        self.tiles = []

        self.mic_values = []
        self.glove_values = []

        self.musician_selected = False
        self.mic_connected = False
        self.glove_connected = False

        self.top_level_add_musician = None

        self.create_widgets()

        self.after_id = None

        self.data_processing = DataProcessing(self)
        self.custom_arduino_manager = CustomArduinoManager(self, self.data_processing)

    def create_widgets(self):
        """
        Créé les différents widgets de l'application.
        """
        self.theme = {
            "font": "Comic Sans MS",
            "bg": "#BE93E4",
            "button_bg": "#DDA0DD"
        }

        ################################# SIDE PANEL #################################

        self.side_panel = tk.Frame(self, width=self.WIDTH_SIDE_PANEL, bg=self.theme["bg"])
        self.side_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.side_panel.grid_propagate(False)

        for i in range(16):
            self.side_panel.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.side_panel.grid_columnconfigure(i, weight=1)

        i = 0

        widget = tk.Label(self.side_panel, text="GET BETTER\nAT PIANO !", font=(self.theme["font"], "24"), bg=self.theme["bg"])
        widget.grid(row=i, column=0, columnspan=2)

        i += 1

        self.connection_mic_state_label = tk.Label(self.side_panel, text="Le micro est déconnecté", font=(self.theme["font"], "11"),
                                                   fg="red", bg=self.theme["bg"])
        self.connection_mic_state_label.grid(row=i, column=0, columnspan=2)

        i += 1

        self.connection_glove_state_label = tk.Label(self.side_panel, text="Le gant est déconnecté", font=(self.theme["font"], "11"),
                                                     fg="red", bg=self.theme["bg"])
        self.connection_glove_state_label.grid(row=i, column=0, columnspan=2, sticky="n")

        i += 1

        self.connect_arduino_button = tk.Button(self.side_panel, text="Vérifier connection", command=lambda: self.custom_arduino_manager.init_managers(),
                                                font=(self.theme["font"], "12"), bg=self.theme["button_bg"])
        self.connect_arduino_button.grid(row=i, column=0, columnspan=2, sticky="n")

        i += 1

        widget = tk.Label(self.side_panel, text="Sélectionner un musicien :", font=(self.theme["font"], "13"), bg=self.theme["bg"])
        widget.grid(row=i, column=0, columnspan=2, sticky="s")

        i += 1

        for id_musicien, nom, niveau in cbd.get_musiciens(self.connexion_bd):
            nom_combo = str(id_musicien) + " - " + nom
            self.musician_name_combo_to_data[nom_combo] = (id_musicien, nom, niveau)

        self.musician_combo_var = tk.StringVar()
        self.musician_combo = ttk.Combobox(self.side_panel, values=list(self.musician_name_combo_to_data.keys()),
                              width=20, state="readonly", textvariable=self.musician_combo_var)
        self.musician_combo.grid(row=i, column=0, columnspan=2)
        self.musician_combo.bind("<<ComboboxSelected>>", self.load_musician)

        i += 1

        widget = tk.Button(self.side_panel, text="Ajouter un musicien", command=self.pop_add_musician_top_level,
                           font=(self.theme["font"], "12"), bg=self.theme["button_bg"])
        widget.grid(row=i, column=0, columnspan=2, sticky="s")

        i += 1

        widget = tk.Label(self.side_panel, text="Musicien :", font=(self.theme["font"], "14"), bg=self.theme["bg"])
        widget.grid(row=i, column=0, columnspan=2, sticky="s")

        i += 1

        widget = tk.Label(self.side_panel, text="Nom : ", font=(self.theme["font"], "11"), bg=self.theme["bg"])
        widget.grid(row=i, column=0)

        self.musician_name_var = tk.StringVar(value="TBD")
        widget = tk.Label(self.side_panel, textvariable=self.musician_name_var, font=(self.theme["font"], "11"), bg=self.theme["bg"])
        widget.grid(row=i, column=1, sticky="w")

        i += 1

        widget = tk.Label(self.side_panel, text="Niveau estimé : ", font=(self.theme["font"], "11"), bg=self.theme["bg"])
        widget.grid(row=i, column=0)

        self.musician_level_var = tk.StringVar(value="TBD")
        widget = tk.Label(self.side_panel, textvariable=self.musician_level_var, font=(self.theme["font"], "11"), bg=self.theme["bg"])
        widget.grid(row=i, column=1, sticky="w")

        i += 1

        widget = tk.Label(self.side_panel, text="Replay d'un morceau joué :", font=(self.theme["font"], "14"), bg=self.theme["bg"])
        widget.grid(row=i, column=0, columnspan=2, sticky="s")

        i += 1

        self.perf_combo_var = tk.StringVar()
        self.perf_combo = ttk.Combobox(self.side_panel, values=list(self.perf_name_combo_to_data.keys()),
                                       width=30, state="readonly", textvariable=self.perf_combo_var)
        self.perf_combo.grid(row=i, column=0, columnspan=2)

        i += 1

        self.replay_button = tk.Button(self.side_panel, text="Replay", command=self.launch_replay_stop,
                                       state=tk.DISABLED, font=(self.theme["font"], "13"), bg=self.theme["button_bg"])
        self.replay_button.grid(row=i, column=0, columnspan=2, sticky="n")

        i += 1

        widget = tk.Label(self.side_panel, text="Morceau :", font=(self.theme["font"], "14"), bg=self.theme["bg"])
        widget.grid(row=i, column=0, columnspan=2, sticky="s")

        i += 1

        for id_morceau, titre in cbd.get_morceaux(self.connexion_bd):
            titre_combo = str(id_morceau) + " - " + titre
            self.song_title_combo_to_data[titre_combo] = (id_morceau, titre)

        self.song_combo_var = tk.StringVar()
        widget = ttk.Combobox(self.side_panel, values=list(self.song_title_combo_to_data.keys()),
                              width=20, state="readonly", textvariable=self.song_combo_var)
        widget.grid(row=i, column=0, columnspan=2)
        if self.song_title_combo_to_data.keys():
            widget.current(0)

        i += 1

        self.play_stop_button = tk.Button(self.side_panel, text="Jouer !", command=self.play_stop, state=tk.DISABLED,
                                          font=(self.theme["font"], "16"), bg=self.theme["button_bg"])
        self.play_stop_button.grid(row=i, column=0, columnspan=2)

        ################################# CANVAS #################################

        self.canvas = tk.Canvas(self, width=self.WIDTH - self.WIDTH_SIDE_PANEL, height=self.HEIGHT, bg="white")
        self.canvas.pack()

        self.white_keys = []

        for i in range(len(self.white_notes)):
            x0 = i * self.WIDTH_WHITE_KEYS
            y0 = self.HEIGHT - self.HEIGHT_WHITE_KEYS
            x1 = (i + 1) * self.WIDTH_WHITE_KEYS
            y1 = self.HEIGHT
            self.white_keys.append(self.canvas.create_rectangle(x0, y0, x1, y1, fill='white', width=3))

            x = (i + 1/2) * self.WIDTH_WHITE_KEYS
            y = self.HEIGHT - (self.HEIGHT_WHITE_KEYS - self.HEIGHT_BLACK_KEYS) / 2
            self.canvas.create_text(x, y, text=self.white_notes[i], fill="black")

        self.black_keys = []

        skip_count = 0
        last_skip = 3
        skip_track = 0
        for i in range(len(self.black_notes)):
            x0 = (i + 1 + skip_count) * self.WIDTH_WHITE_KEYS - self.WIDTH_BLACK_KEYS / 2
            y0 = self.HEIGHT - self.HEIGHT_WHITE_KEYS
            x1 = (i + 1 + skip_count) * self.WIDTH_WHITE_KEYS + self.WIDTH_BLACK_KEYS / 2
            y1 = self.HEIGHT - self.HEIGHT_WHITE_KEYS + self.HEIGHT_BLACK_KEYS
            self.black_keys.append(self.canvas.create_rectangle(x0, y0,x1, y1, fill='black', width=0))

            x = (i + 1 + skip_count) * self.WIDTH_WHITE_KEYS
            y = self.HEIGHT - self.HEIGHT_WHITE_KEYS + self.HEIGHT_BLACK_KEYS * 2 / 3
            self.canvas.create_text(x, y, text=self.black_notes[i], fill="white")

            skip_track += 1
            if last_skip == 2 and skip_track == 3:
                last_skip = 3
                skip_track = 0
                skip_count += 1
            elif last_skip == 3 and skip_track == 2:
                last_skip = 2
                skip_track = 0
                skip_count += 1

    def close_app(self):
        """
        Se déconnecte de la base de données et ferme l'application.
        """
        cbd.fermer_connexion_bd(self.connexion_bd)
        self.custom_arduino_manager.close()
        self.destroy()

    # def get_mic_values(self, id_notes_with_amplitudes):
    #     """
    #     Stocke les données du micro envoyées depuis le manager Arduino en ajoutant le temps depuis le début du morceau.
    #
    #     Paramètres :
    #         dict id_notes_with_amplitudes: index notes et amplitudes calculées sur l'Arduino du micro
    #     """
    #     for i in range(len(self.white_keys)):
    #         if i in id_notes_with_amplitudes and id_notes_with_amplitudes[i] > 10 + i*7:
    #             self.canvas.itemconfig(self.white_keys[i], fill=self.theme["button_bg"])
    #         else:
    #             self.canvas.itemconfig(self.white_keys[i], fill="white")
    #
    #     for i in range(len(self.black_keys)):
    #         if i + len(self.white_keys) in id_notes_with_amplitudes and id_notes_with_amplitudes[i + len(self.white_keys)] > 10 + i*7:
    #             self.canvas.itemconfig(self.black_keys[i], fill=self.theme["bg"])
    #         else:
    #             self.canvas.itemconfig(self.black_keys[i], fill="black")
    #
    #     self.mic_values.append((round(time.time() - self.time_start, 3), id_notes_with_amplitudes))
    #
    # def get_glove_values(self, accelero_x, accelero_y, frequence_cardiaque, pression_doigts):
    #     """
    #     Stocke les données du gant envoyées depuis le manager Arduino en ajoutant le temps depuis le début du morceau.
    #
    #     Paramètres :
    #         int accelero_x: Valeur en X de l'accéléromètre
    #         int accelero_y: Valeur en Y de l'accéléromètre
    #         int frequence_cardiaque: Valeur de fréquence cardiaque
    #         bytes pression_doigts: Valeurs d'appui de chaque doigt
    #     """
    #     self.glove_values.append((round(time.time() - self.time_start, 3), pression_doigts, frequence_cardiaque,
    #                               accelero_x, accelero_y))
    #
    # def process_data_end_song(self):
    #     """
    #     Traite les données à la fin d'un morceau.
    #     """
    #     self.mic_values.reverse()
    #     self.glove_values.reverse()
    #     print()
    #     print(self.mic_values)
    #     print(self.glove_values)
    #
    #     date_perf = datetime.fromtimestamp(self.time_start)
    #     infos = (self.musician_name_combo_to_data[self.musician_combo_var.get()][0],
    #              self.song_title_combo_to_data[self.song_combo_var.get()][0], date_perf)
    #     id_perf = cbd.insert_performance(self.connexion_bd, *infos)
    #     infos = (id_perf, *infos)
    #
    #     with open(f"Data/{id_perf}.py", "w") as file:
    #         file.write(f"mic_values = {str(self.mic_values)}\n\nglove_values = {str(self.glove_values)}\n")
    #
    #     mesure_touches = []
    #     Data = [{}, {}, {}, {}, {}]
    #
    #     nb_iterations = 0
    #     data_mic = self.mic_values.pop()
    #
    #     while self.glove_values:
    #         data_glove = self.glove_values.pop()
    #         if self.mic_values and self.mic_values[-1][0] >= data_glove[0]:
    #             data_mic = self.mic_values.pop()
    #
    #         cbd.insert_accelero(self.connexion_bd, id_perf, data_glove[3], data_glove[4], data_glove[0])
    #         if nb_iterations % 75 == 0 and nb_iterations != 0:
    #             cbd.insert_BPM(self.connexion_bd, id_perf, data_glove[2], data_glove[0])
    #
    #         to_compare = []
    #         nb_finished_to_do = 0
    #
    #         for i in range(5):
    #             if (data_glove[1] >> i) & 1:
    #                 if not Data[i]:
    #                     Data[i]["doigt"] = i
    #                     Data[i]["temps_depuis_debut"] = data_glove[0]
    #                     Data[i]["notes_possibles"] = []
    #
    #                 if data_mic[0] >= Data[i]["temps_depuis_debut"]:
    #                     Data[i]["notes_possibles"].append(data_mic[1])
    #
    #             elif Data[i]:
    #                 Data[i]["temps_presse"] = data_glove[0] - Data[i]["temps_depuis_debut"]
    #
    #                 if not to_compare:
    #                     for j in range(5):
    #                         if Data[j]:
    #                             for id_note, avg_amp in self.avg_amplitudes_notes(Data[j]["notes_possibles"]):
    #                                 to_compare.append((avg_amp, id_note, j))
    #
    #                             if "temps_presse" in Data[j]:
    #                                 nb_finished_to_do += 1
    #
    #         to_compare.sort(reverse=True)
    #         id_note_done = set()
    #         finger_done = set()
    #
    #         processing_done = False
    #         i = 0
    #
    #         while not processing_done and i < len(to_compare):
    #             avg_amp, id_note, i_finger = to_compare[i]
    #             if id_note not in id_note_done and i_finger not in finger_done:
    #                 id_note_done.add(id_note)
    #                 finger_done.add(i_finger)
    #                 if "temps_presse" in Data[i_finger]:
    #                     values = (id_perf, id_note, i_finger, Data[i_finger]["temps_presse"], Data[i_finger]["temps_depuis_debut"])
    #                     mesure_touches.append(values)
    #                     cbd.insert_touche_mesure(self.connexion_bd, *values)
    #
    #                     Data[i_finger] = {}
    #                     nb_finished_to_do -= 1
    #
    #                     if nb_finished_to_do == 0:
    #                         processing_done = True
    #
    #             i += 1
    #
    #         nb_iterations += 1
    #
    #     print(mesure_touches)
    #
    #     nom_combo = cbd.get_titre_morceau(self.connexion_bd, infos[2]) + " - " + infos[3].strftime("%d/%m/%Y %H:%M:%S")
    #     self.perf_name_combo_to_data[nom_combo] = infos
    #
    #     self.perf_combo["values"] = list(self.perf_name_combo_to_data.keys())
    #     if self.perf_name_combo_to_data.keys():
    #         self.perf_combo.current(len(self.perf_name_combo_to_data) - 1)
    #         self.replay_button["state"] = tk.NORMAL
    #     else:
    #         self.replay_button["state"] = tk.DISABLED
    #
    # @staticmethod
    # def avg_amplitudes_notes(list_id_notes_with_amplitudes):
    #     result = {}
    #     # nb_id_note = {}
    #     for five_id_notes_with_amplitudes in list_id_notes_with_amplitudes:
    #         for id_note, amp in five_id_notes_with_amplitudes.items():
    #             result[id_note] = result.get(id_note, 0) + amp
    #             # nb_id_note[id_note] = nb_id_note.get(id_note, 0) + 1
    #
    #     # for id_note in result:
    #     #     result[id_note] /= nb_id_note[id_note]
    #
    #     list_result = sorted(result.items(), reverse=True, key=lambda x: x[1])
    #
    #     return list_result[:5]

    def highlight_key(self, id_note):
        if id_note < len(self.white_keys):
            self.canvas.itemconfig(self.white_keys[id_note], fill=self.theme["button_bg"])
        else:
            self.canvas.itemconfig(self.black_keys[id_note - len(self.white_keys)], fill=self.theme["bg"])

    def un_highlight_key(self, id_note):
        if id_note < len(self.white_keys):
            self.canvas.itemconfig(self.white_keys[id_note], fill="white")
        else:
            self.canvas.itemconfig(self.black_keys[id_note - len(self.white_keys)], fill="black")

    def update_arduino_connection_state(self, mic_connected, glove_connected):
        """
        Met à jour les textes indiquant l'état de connection des cartes du micro et du gant.

        Paramètres :
            bool mic_connected: État de connection de la carte du micro
            bool glove_connected: État de connection de la carte de transmission du gant
        """
        self.mic_connected = mic_connected
        if mic_connected:
            self.connection_mic_state_label["text"] = "Le micro est connecté"
            self.connection_mic_state_label["fg"] = "green"
        else:
            self.connection_mic_state_label["text"] = "Le micro est déconnecté"
            self.connection_mic_state_label["fg"] = "red"

        self.glove_connected = glove_connected
        if glove_connected:
            self.connection_glove_state_label["text"] = "Le gant est connecté"
            self.connection_glove_state_label["fg"] = "green"
        else:
            self.connection_glove_state_label["text"] = "Le gant est déconnecté"
            self.connection_glove_state_label["fg"] = "red"

        if mic_connected and glove_connected:
            self.connect_arduino_button["state"] = tk.DISABLED

        self.update_play_stop_button_state()

    def pop_add_musician_top_level(self):
        """
        Créé la fenêtre toplevel pour rentrer un nouveau musicien.
        """
        if self.top_level_add_musician is None:
            self.top_level_add_musician = tk.Toplevel(bg=self.theme["bg"])

            width = 500
            height = 400

            # Pour centrer la fenêtre sur l'écran
            pos_right = int(self.winfo_screenwidth() / 2 - width / 2)
            pos_down = int(self.winfo_screenheight() / 2.25 - height / 2)

            self.top_level_add_musician.geometry(f"{width}x{height}+{pos_right}+{pos_down}")
            self.top_level_add_musician.resizable(False, False)

            self.top_level_add_musician.protocol("WM_DELETE_WINDOW", self.close_top_level_add_musician)

            self.top_level_add_musician.grid_propagate(False)

            for i in range(4):
                self.top_level_add_musician.grid_rowconfigure(i, weight=1)
            for i in range(2):
                self.top_level_add_musician.grid_columnconfigure(i, weight=1)

            i = 0

            widget = tk.Label(self.top_level_add_musician, text="Entrez vos infos :",
                              font=(self.theme["font"], "20"), bg=self.theme["bg"])
            widget.grid(row=i, column=0, columnspan=2)

            i += 1

            widget = tk.Label(self.top_level_add_musician, text="Nom :",
                              font=(self.theme["font"], "11"), bg=self.theme["bg"])
            widget.grid(row=i, column=0)

            self.name_entry_var = tk.StringVar()
            widget = tk.Entry(self.top_level_add_musician, width=30, textvariable=self.name_entry_var)
            widget.grid(row=i, column=1)
            widget.bind("<KeyRelease>", self.update_validate_button_state)

            i += 1

            widget = tk.Label(self.top_level_add_musician, text="Niveau estimé :",
                              font=(self.theme["font"], "11"), bg=self.theme["bg"])
            widget.grid(row=i, column=0)

            self.level_combo_var = tk.StringVar()
            widget = ttk.Combobox(self.top_level_add_musician, values=self.possible_levels,
                                  width=30, state="readonly", textvariable=self.level_combo_var)
            widget.grid(row=i, column=1)
            widget.current(1)

            i += 1

            self.validate_button = tk.Button(self.top_level_add_musician, text="Valider", command=self.add_musician, state=tk.DISABLED,
                                             font=(self.theme["font"], "14"), bg=self.theme["button_bg"])
            self.validate_button.grid(row=i, column=0, columnspan=2)

    def close_top_level_add_musician(self):
        """
        Supprime la fenêtre d'ajout de musicien et la met à None.
        """
        self.top_level_add_musician.destroy()
        self.top_level_add_musician = None

    def update_validate_button_state(self, event):
        """
        Met à jour l'état (activé ou non) du bouton pour valider en fonction du contenu des champs renseignés.

        Paramètres :
            event: Événement tkinter
        """
        if self.name_entry_var.get():
            self.validate_button["state"] = tk.NORMAL
        else:
            self.validate_button["state"] = tk.DISABLED

    def add_musician(self):
        """
        Ajoute un musicien à la base de donnée avec les infos des champs nom et niveau estimé.
        Puis sélectionne ce musicien.
        """
        nom = self.name_entry_var.get()
        niveau = self.level_combo_var.get()
        id_musicien = cbd.insert_musicien(self.connexion_bd, nom, niveau)

        name_combo = str(id_musicien) + " - " + nom
        self.musician_name_combo_to_data[name_combo] = (id_musicien, nom, niveau)
        self.musician_combo["values"] = list(self.musician_name_combo_to_data.keys())
        self.musician_combo.current(len(self.musician_name_combo_to_data) - 1)

        self.load_musician()

        self.close_top_level_add_musician()

    def load_musician(self, event=None):
        """
        Charge le musicien choisi avec la combobox.

        Paramètres :
            event: Événement tkinter
        """
        id_musicien, nom, niveau = self.musician_name_combo_to_data[self.musician_combo_var.get()]

        self.musician_name_var.set(nom)
        self.musician_level_var.set(niveau)

        self.musician_selected = True
        self.update_play_stop_button_state()

        titres = {}
        self.perf_name_combo_to_data = {}

        for infos in cbd.get_perfs(self.connexion_bd, id_musicien):
            id_morceau = infos[2]
            if id_morceau not in titres:
                titres[id_morceau] = cbd.get_titre_morceau(self.connexion_bd, id_morceau)
            nom_combo = titres[id_morceau] + " - " + infos[3].strftime("%d/%m/%Y %H:%M:%S")
            self.perf_name_combo_to_data[nom_combo] = infos[:4]

        self.perf_combo["values"] = list(self.perf_name_combo_to_data.keys())
        if self.perf_name_combo_to_data.keys():
            self.perf_combo.current(0)
            self.replay_button["state"] = tk.NORMAL
        else:
            self.replay_button["state"] = tk.DISABLED

    def update_replay_combo(self, nom_combo, infos):
        self.perf_name_combo_to_data[nom_combo] = infos

        self.perf_combo["values"] = list(self.perf_name_combo_to_data.keys())
        if self.perf_name_combo_to_data.keys():
            self.perf_combo.current(len(self.perf_name_combo_to_data) - 1)
            self.replay_button["state"] = tk.NORMAL
        else:
            self.replay_button["state"] = tk.DISABLED

    def stop_and_remove_keys(self):
        """
        Arrête le défilement des tuiles et les efface toutes.
        """
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        while self.tiles:
            self.canvas.delete(self.tiles.pop())

    def load_keys(self, touches, colors):
        """
        Charge les touches données avec les couleurs données sur le canvas.

        Paramètres :
            list touches: Liste des touches dont il faut placer les tuiles
            list(str) colors: Liste de taille le nombre de notes possibles contenant la couleur que doit prendre chaque touche
        """
        for note_index, tps_presse, tps_depuis_debut in touches:
            if note_index <= len(self.white_notes):
                x0 = note_index * self.WIDTH_WHITE_KEYS
                x1 = (note_index + 1) * self.WIDTH_WHITE_KEYS
            else:
                coords = self.canvas.coords(self.black_keys[note_index - len(self.white_notes)])
                x0, x1 = coords[0], coords[2]

            y0 = - self.PX_PER_SEC * tps_depuis_debut
            y1 = y0 - self.PX_PER_SEC * tps_presse

            self.tiles.append(self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[note_index], width=2))
            self.canvas.lower(self.tiles[-1])

    def replay_selected(self, event=None):
        """
        Place les tuiles du replay sélectionné et efface les précédentes.

        Paramètres :
            event: Événement tkinter
        """
        self.stop_and_remove_keys()

        id_morceau = self.perf_name_combo_to_data[self.perf_combo_var.get()][2]
        touches_ref = cbd.get_touches_morceau_ref(self.connexion_bd, id_morceau)

        self.load_keys(touches_ref, ["" for _ in range(len(self.white_notes) + len(self.black_notes))])

        id_perf = self.perf_name_combo_to_data[self.perf_combo_var.get()][0]
        touches_jouees = cbd.get_touches_perf(self.connexion_bd, id_perf)

        self.load_keys(touches_jouees, ["#00FFFF" for _ in range(len(self.white_notes) + len(self.black_notes))])

    def song_selected(self, event=None):
        """
        Place les tuiles du morceau sélectionné et efface les précédentes.

        Paramètres :
            event: Événement tkinter
        """
        self.stop_and_remove_keys()

        id_morceau = self.song_title_combo_to_data[self.song_combo_var.get()][0]
        touches_ref = cbd.get_touches_morceau_ref(self.connexion_bd, id_morceau)

        colors = []
        for note_index in range(len(self.white_notes) + len(self.black_notes)):
            h, l, s = note_index / (len(self.white_notes) + len(self.black_notes)), .7, .5
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            colors.append('#%02x%02x%02x' % (round(r * 255), round(g * 255), round(b * 255)))

        self.load_keys(touches_ref, colors)

    def move_tiles(self, last_frame_time):
        """
        Déplace les tuiles vers le bas en fonction du temps écoulé depuis last_frame_time.

        Paramètres :
            float last_frame_time: temps (en secondes) au moment du dernier déplacement.
        """
        dy = self.PX_PER_SEC * (time.time() - last_frame_time)

        for tile in self.tiles:
            self.canvas.move(tile, 0, dy)

        if self.canvas.coords(self.tiles[0])[1] >= self.HEIGHT - self.HEIGHT_WHITE_KEYS + 1.0 * self.PX_PER_SEC:
            if self.data_processing.time_start is not None:
                self.play_stop(end_of_song=True)
            else:
                self.launch_replay_stop()
        else:
            self.after_id = self.after(10, self.move_tiles, time.time())

    def launch_replay_stop(self):
        """
        Change le texte du bouton replay/stop et appelle la fonction correspondante en fonction de son texte actuel.
        """
        if self.replay_button["text"] == "Replay":
            self.replay_selected()
            self.replay_button["text"] = "Stop"
            self.after_id = self.after(10, self.move_tiles, time.time())

        else:
            self.replay_button["text"] = "Replay"

            self.stop_and_remove_keys()

    def play_stop(self, end_of_song=False):
        """
        Change le texte du bouton jouer/stop et appelle la fonction correspondante en fonction de son texte actuel.
        """
        if self.play_stop_button["text"] == "Jouer !":
            self.song_selected()
            self.play_stop_button["text"] = "Stop"
            self.after_id = self.after(10, self.move_tiles, time.time())
            self.data_processing.initialisation(time.time() + (self.HEIGHT - self.HEIGHT_WHITE_KEYS) / self.PX_PER_SEC)
            self.custom_arduino_manager.recording = True

        else:
            self.play_stop_button["text"] = "Jouer !"
            self.custom_arduino_manager.recording = False
            if end_of_song:
                id_musicien = self.musician_name_combo_to_data[self.musician_combo_var.get()][0]
                id_morceau = self.song_title_combo_to_data[self.song_combo_var.get()][0]
                self.data_processing.put_data_in_database(self.connexion_bd, id_musicien, id_morceau)

            self.stop_and_remove_keys()

    def update_play_stop_button_state(self):
        """
        Met à jour l'état du bouton play / stop en fonction des états de connexion des cartes du micro, du gant et
        de la sélection (du moins de l'absence de sélection) du musicien.
        """
        if self.musician_selected and self.mic_connected and self.glove_connected:
            self.play_stop_button["state"] = tk.NORMAL
        else:
            self.play_stop_button["state"] = tk.DISABLED

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
        tolerance_temps = 0.150
        nb_bonnes_notes = 0

        for note_ref, temps_presse_ref, temps_depuis_debut_ref in touches_ref:
            for note_jouee, temps_presse_jouee, temps_depuis_debut_jouee in touches_jouees:
                if note_ref == note_jouee and abs(temps_depuis_debut_ref - temps_depuis_debut_jouee) < tolerance_temps \
                        and abs(temps_depuis_debut_ref + temps_presse_ref - (temps_depuis_debut_jouee + temps_presse_jouee)) < tolerance_temps:
                    nb_bonnes_notes += 1

        return len(touches_ref) - nb_bonnes_notes
