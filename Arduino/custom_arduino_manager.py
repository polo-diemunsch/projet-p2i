from Arduino.arduino_manager import ArduinoManager


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

    def init_managers(self):
        ports = ArduinoManager.trouver_ports_arduino()

        port_mic = None
        port_glove = None

        for port, description in ports:

            if "Uno" in description:
                port_mic = port
            elif "[giyehsjd]" in description:
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
        pass

    def glove_callback(self, input_line):
        pass
