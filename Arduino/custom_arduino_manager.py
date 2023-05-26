from Arduino.arduino_manager import ArduinoManager

from time import time


class CustomArduinoManager:
    """
    Classe permettant de gérer les liaisons séries avec à la fois la carte Arduino du micro et celle réceptionnant et
    transférant les données du gant.
    """

    def __init__(self, app):
        self.app = app

        self.mic_manager = None
        self.glove_manager = None

        self.init_managers()

        self.t = time()

    def init_managers(self):
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
            self.mic_manager = ArduinoManager(port_mic)
            self.glove_manager = ArduinoManager(port_glove)

            self.mic_manager._on_input_line_callback = self.mic_callback
            self.mic_manager.run_listening()

            self.glove_manager._on_input_line_callback = self.glove_callback
            self.glove_manager.run_listening()

    def mic_callback(self, input_line):
        # frequencies_with_amplitudes = []
        #
        # half_length = len(input_line)//2
        #
        # for i in range(0, half_length, 2):
        #     frequencies_with_amplitudes.append((int.from_bytes(input_line[i:i + 2], "little"),
        #                                         int.from_bytes(input_line[half_length + i:half_length + i + 2], "little")))
        #
        # print(frequencies_with_amplitudes)
        # print(time() - self.t)
        # self.t = time()

        pass

    def glove_callback(self, input_line):
        print(f"Trame reçue : {input_line}")
        accelerox = int.from_bytes(input_line[0:2], "little")
        acceleroy = int.from_bytes(input_line[2:4], "little")
        frequence_cardiaque = int.from_bytes(input_line[4:5], "little")
        pression_doigts = int.from_bytes(input_line[5:6], "little")
        print(f"accelrox décodée: {accelerox}")
        print(f"acceleroy décodée: {acceleroy}")
        print(f"frequence_cardiaque décodée: {frequence_cardiaque}")
        print(f"pression_doigts décodée: {pression_doigts}")
        print(time() - self.t)
        self.t = time()
        print()

        # pass

    def close(self):
        if self.mic_manager is not None:
            self.mic_manager.close()

        if self.glove_manager is not None:
            self.glove_manager.close()
