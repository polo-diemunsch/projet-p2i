from Arduino.arduino_manager import ArduinoManager
from Arduino.notes_frequences import id_note_from_frequency
import time


class CustomArduinoManager:
    """
    Classe permettant de gérer les liaisons séries avec à la fois la carte Arduino du micro et celle réceptionnant et
    transférant les données du gant.
    """

    def __init__(self, app, data_processing):
        self.app = app
        self.data_processing = data_processing

        self.mic_manager = None
        self.glove_manager = None

        self.recording = False

        self.init_managers()

        self.t1 = time.time()
        self.t2 = time.time()

    def init_managers(self):
        """
        Reconnait les cartes (Uno pour le micro et MKR WAN pour le gant) et initialise les deux managers.
        Si les deux cartes sont reconnues, lance l'écoute des données reçues.
        """
        ports = ArduinoManager.trouver_ports_arduino()

        port_mic = None
        port_glove = None

        for port, description in ports:

            if "Uno" in description:
                port_mic = port
            elif "MKR WAN 1310" in description:
                port_glove = port

        if port_mic is None or port_glove is None:
            self.app.update_arduino_connection_state(port_mic is not None, port_glove is not None)
        else:
            self.app.update_arduino_connection_state(True, True)
            self.mic_manager = ArduinoManager(port_mic, 5*2*2)
            self.glove_manager = ArduinoManager(port_glove, 6)

            self.mic_manager._on_input_line_callback = self.mic_callback
            self.mic_manager.run_listening()

            self.glove_manager._on_input_line_callback = self.glove_callback
            self.glove_manager.run_listening()

    def mic_callback(self, input_line):
        """
        Traite les données reçues du micro puis les envois à l'application.

        Paramètres :
            bytes input_line: données brutes reçues de l'Arduino du micro
        """
        if self.recording:
            id_notes_with_amplitudes = {}

            half_length = len(input_line)//2

            for i in range(0, half_length, 2):
                freq = int.from_bytes(input_line[i:i + 2], "little")
                amp = int.from_bytes(input_line[half_length + i:half_length + i + 2], "little")
                id_note = id_note_from_frequency(freq)

                id_notes_with_amplitudes[id_note] = max(id_notes_with_amplitudes.get(id_note, 0), amp)

            # print(id_notes_with_amplitudes)
            # print(time.time() - self.t1)
            # self.t1 = time.time()
            # print()

            print(id_notes_with_amplitudes)

            self.data_processing.get_mic_values(id_notes_with_amplitudes)

    def glove_callback(self, input_line):
        """
        Traite les données reçues du gant puis les envois à l'application.

        Paramètres :
            bytes input_line: données brutes reçues de l'Arduino de transmission du gant
        """
        if self.recording:
            accelero_x = int.from_bytes(input_line[0:2], "little", signed=True)
            accelero_y = int.from_bytes(input_line[2:4], "little", signed=True)
            frequence_cardiaque = int.from_bytes(input_line[4:5], "little")
            pression_doigts = int.from_bytes(input_line[5:6], "little")

            # pression_doigts_individuels = []
            # for i in range(5):
            #     pression_doigts_individuels.append(bool((pression_doigts >> i) & 1))

            # print(f"Trame reçue : {input_line}")
            # print(f"accelro_x décodée: {accelero_x}")
            # print(f"accelero_y décodée: {accelero_y}")
            # print(f"frequence_cardiaque décodée: {frequence_cardiaque}")
            print(f"pression_doigts décodée: {pression_doigts}")
            # # print(f"pression_doigts_individuels: {pression_doigts_individuels}")
            # print(time.time() - self.t2)
            # self.t2 = time.time()
            # print()

            self.data_processing.get_glove_values(accelero_x, accelero_y, frequence_cardiaque, pression_doigts)

    def close(self):
        """
        Ferme les connexions aux Arduino en vue de fermer l'application.
        """
        if self.mic_manager is not None:
            self.mic_manager.close()

        if self.glove_manager is not None:
            self.glove_manager.close()
