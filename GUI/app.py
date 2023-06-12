import tkinter as tk
from tkinter import ttk, messagebox
import colorsys
import time
import SQL.commandes_bd as cbd
from Arduino.custom_arduino_manager import CustomArduinoManager
from Data.data_processing import DataProcessing
import Data.graphique as grp



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

        self.possible_levels = ["Claqué au sol", "Jamais touché de piano", "Débutant", "Intermédiaire", "Confirmé",
                                "Expert", "Frédéric Chopin"]

        self.WIDTH_WHITE_KEYS = 60
        self.HEIGHT_WHITE_KEYS = 200
        self.WIDTH_BLACK_KEYS = 35
        self.HEIGHT_BLACK_KEYS = 125

        self.WIDTH_SIDE_PANEL = 350

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

        self.time_start = None
        self.play_mode = "play"     # play / replay

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
        self.replay_button.grid(row=i, column=0, sticky="n")

        self.del_button = tk.Button(self.side_panel, text="Supprimer", command=self.del_perf,
                                       state=tk.DISABLED, font=(self.theme["font"], "13"), bg=self.theme["button_bg"])
        self.del_button.grid(row=i, column=1, sticky="n")

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
        widget.bind("<<ComboboxSelected>>", self.update_state_stat_button)
        if self.song_title_combo_to_data.keys():
            widget.current(0)

        i += 1

        self.play_stop_button = tk.Button(self.side_panel, text="Jouer !", command=self.play_stop, state=tk.DISABLED,
                                          font=(self.theme["font"], "16"), bg=self.theme["button_bg"])
        self.play_stop_button.grid(row=i, column=0)

        self.stat_button = tk.Button(self.side_panel, text="Statistiques", command=self.stats, state=tk.DISABLED,
                                     font=(self.theme["font"], "12"), bg=self.theme["button_bg"])
        self.stat_button.grid(row=i, column=1)



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

        self.update_state_replay_combo_and_buttons()
        self.update_state_stat_button()

    def update_replay_combo(self, nom_combo, infos):
        self.perf_name_combo_to_data[nom_combo] = infos

        self.update_state_replay_combo_and_buttons()

    def update_state_replay_combo_and_buttons(self):
        self.perf_combo["values"] = list(self.perf_name_combo_to_data.keys())

        if self.perf_name_combo_to_data.keys():
            self.perf_combo.current(len(self.perf_name_combo_to_data) - 1)
            self.replay_button["state"] = tk.NORMAL
            self.del_button["state"] = tk.NORMAL
        else:
            self.replay_button["state"] = tk.DISABLED
            self.del_button["state"] = tk.DISABLED
            self.perf_combo_var.set("")

    def update_state_stat_button(self, event=None):
        if self.musician_combo_var.get() and self.song_combo_var.get() and \
            cbd.get_perf(self.connexion_bd, self.musician_name_combo_to_data[self.musician_combo_var.get()][0],
                         self.song_title_combo_to_data[self.song_combo_var.get()][0]):
            self.stat_button["state"] = tk.NORMAL
        else:
            self.stat_button["state"] = tk.DISABLED

    def stop_and_remove_keys(self):
        """
        Arrête le défilement des tuiles et les efface toutes.
        """
        self.time_start = None
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        while self.tiles:
            self.canvas.delete(self.tiles.pop()[0])

        for i in range(len(self.white_notes) + len(self.black_notes)):
            self.un_highlight_key(i)

    def load_keys(self, touches, color_type):
        """
        Charge les touches données avec les couleurs données sur le canvas.

        Paramètres :
            list touches: Liste des touches dont il faut placer les tuiles
            list(str) color_type: Liste de taille le nombre de notes possibles contenant la couleur que doit prendre chaque touche
        """
        for infos in touches:
            if len(infos) > 3:
                note_index, tps_presse, tps_depuis_debut, doigt = infos
            else:
                note_index, tps_presse, tps_depuis_debut = infos

            if note_index <= len(self.white_notes):
                x0 = note_index * self.WIDTH_WHITE_KEYS
                x1 = (note_index + 1) * self.WIDTH_WHITE_KEYS
            else:
                coords = self.canvas.coords(self.black_keys[note_index - len(self.white_notes)])
                x0, x1 = coords[0], coords[2]

            y0 = - self.PX_PER_SEC * tps_depuis_debut
            y1 = y0 - self.PX_PER_SEC * tps_presse

            if color_type == "rainbow_notes":
                if note_index < len(self.white_notes):
                    if note_index % 2:
                        i = (len(self.white_notes) + note_index) // 2
                    else:
                        i = note_index // 2

                    h, s, v = i / len(self.white_notes), .8, 1.0

                else:
                    note_index -= len(self.white_notes)
                    if note_index % 2:
                        i = (len(self.black_notes) + note_index) // 2
                    else:
                        i = note_index // 2

                    h, s, v = i / len(self.black_notes), .8, 1.0

                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                color = '#%02x%02x%02x' % (round(r * 255), round(g * 255), round(b * 255))

                self.tiles.append((self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=2), tps_depuis_debut, tps_presse))

            elif color_type == "rainbow_finger":
                if len(infos) > 3:
                    h, s, v = (doigt + .8) / 5, .8, 1.0
                    r, g, b = colorsys.hsv_to_rgb(h, s, v)
                    color = '#%02x%02x%02x' % (round(r * 255), round(g * 255), round(b * 255))
                else:
                    color = "red"

                self.tiles.append((self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0), tps_depuis_debut, tps_presse))

            else:
                self.tiles.append((self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_type, width=2), tps_depuis_debut, tps_presse))

            self.canvas.lower(self.tiles[-1][0])

    def replay_selected(self, event=None):
        """
        Place les tuiles du replay sélectionné et efface les précédentes.

        Paramètres :
            event: Événement tkinter
        """
        self.stop_and_remove_keys()

        id_morceau = self.perf_name_combo_to_data[self.perf_combo_var.get()][2]
        touches_ref = cbd.get_touches_morceau_ref(self.connexion_bd, id_morceau)

        self.load_keys(touches_ref, "")

        id_perf = self.perf_name_combo_to_data[self.perf_combo_var.get()][0]
        touches_jouees = cbd.get_touches_perf(self.connexion_bd, id_perf)

        self.load_keys(touches_jouees, "rainbow_finger")

    def song_selected(self, event=None):
        """
        Place les tuiles du morceau sélectionné et efface les précédentes.

        Paramètres :
            event: Événement tkinter
        """
        self.stop_and_remove_keys()

        id_morceau = self.song_title_combo_to_data[self.song_combo_var.get()][0]
        touches_ref = cbd.get_touches_morceau_ref(self.connexion_bd, id_morceau)

        self.load_keys(touches_ref, "rainbow_notes")

    def move_tiles(self):
        """
        Déplace les tuiles vers le bas en fonction du temps écoulé depuis last_frame_time.

        Paramètres :
            float last_frame_time: temps (en secondes) au moment du dernier déplacement.
        """
        t = time.time()

        for tile, tps_depuis_debut, tps_presse in self.tiles:
            x0, y0, x1, y1 = self.canvas.coords(tile)
            y0 = self.PX_PER_SEC * (3.0 - float(tps_depuis_debut) + (t - self.time_start))
            y1 = y0 - float(self.PX_PER_SEC * tps_presse)

            self.canvas.coords(tile, x0, y0, x1, y1)

        if self.canvas.coords(self.tiles[0][0])[1] >= self.HEIGHT - self.HEIGHT_WHITE_KEYS + 1.0 * self.PX_PER_SEC:
            if self.play_mode == "play":
                self.play_stop(end_of_song=True)
            else:
                self.launch_replay_stop()
        else:
            self.after_id = self.after(10, self.move_tiles)

    def launch_replay_stop(self):
        """
        Change le texte du bouton replay/stop et appelle la fonction correspondante en fonction de son texte actuel.
        """
        if self.replay_button["text"] == "Replay":
            self.replay_button["text"] = "Stop"
            if self.play_stop_button["text"] == "Stop":
                self.play_stop()

            self.replay_selected()
            self.time_start = time.time() + (self.HEIGHT - self.HEIGHT_WHITE_KEYS) / self.PX_PER_SEC
            self.play_mode = "replay"
            self.after_id = self.after(10, self.move_tiles)

        else:
            self.replay_button["text"] = "Replay"

            self.stop_and_remove_keys()

    def play_stop(self, end_of_song=False):
        """
        Change le texte du bouton jouer/stop et appelle la fonction correspondante en fonction de son texte actuel.
        """
        if self.play_stop_button["text"] == "Jouer !":
            self.play_stop_button["text"] = "Stop"
            self.replay_button["text"] = "Replay"
            self.song_selected()
            self.time_start = time.time() + (self.HEIGHT - self.HEIGHT_WHITE_KEYS) / self.PX_PER_SEC
            self.play_mode = "play"
            self.after_id = self.after(10, self.move_tiles)
            self.data_processing.initialisation()
            self.custom_arduino_manager.recording = True

        else:
            self.play_stop_button["text"] = "Jouer !"
            self.custom_arduino_manager.recording = False
            if end_of_song:
                id_musicien = self.musician_name_combo_to_data[self.musician_combo_var.get()][0]
                id_morceau = self.song_title_combo_to_data[self.song_combo_var.get()][0]
                self.data_processing.put_data_in_database(self.connexion_bd, id_musicien, id_morceau)

                self.update_state_stat_button()
                self.fen_perf()

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

    def del_perf(self):
        if messagebox.askyesno("Supprimer ?", "Êtes-vous sûr de vouloir supprimer la performance ?"):
            id_perf = self.perf_name_combo_to_data[self.perf_combo_var.get()][0]
            cbd.del_performance(self.connexion_bd, id_perf)
            del self.perf_name_combo_to_data[self.perf_combo_var.get()]
            self.update_state_replay_combo_and_buttons()

    def fen_perf(self):
        id_perf = cbd.get_last_id_perf(self.connexion_bd)
        fen_last = tk.Toplevel()
        fen_last.resizable(False, False)
        id_morceau = self.song_title_combo_to_data[self.song_combo_var.get()][0]
        id_musicien = self.musician_name_combo_to_data[self.musician_combo_var.get()][0]
        grp.tableau_last(self.connexion_bd, id_musicien,id_morceau, fen_last)
        grp.graphique_BPM(self.connexion_bd, id_perf, fen_last)
        grp.graphique_accelero(self.connexion_bd, id_perf, fen_last)

    def stats(self):
        fen_stat = tk.Toplevel()
        fen_stat.resizable(False, False)
        id_morceau = self.song_title_combo_to_data[self.song_combo_var.get()][0]
        id_musicien = self.musician_name_combo_to_data[self.musician_combo_var.get()][0]
        grp.graphique_niveau(self.connexion_bd, id_musicien, id_morceau, fen_stat,self.possible_levels)
        grp.graphique_BPM_moyen(self.connexion_bd, id_musicien, id_morceau, fen_stat)
        grp.graphique_nb_fausses_notes(self.connexion_bd, id_musicien, id_morceau, fen_stat)
        grp.graphique_precision(self.connexion_bd, id_musicien, id_morceau, fen_stat)



