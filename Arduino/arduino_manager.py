# Python built-in Packages
import threading

import serial
import serial.tools.list_ports


class ArduinoManager:

    def __init__(self, port, on_input_line_callback=None, baudrate=115200, timeout=.1):
        self.port = port
        self._serial_connection = None
        self._on_input_line_callback = on_input_line_callback
        self.baudrate = baudrate
        self.timeout = timeout
        self._listening_thread = None

        self._serial_connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def run_listening(self):
        self._listening_thread = threading.Thread(target=self._listening_method, args=(self,))
        self._listening_thread.start()

    def close(self):
        print('CLOSING Arduino connection')

        if self._serial_connection is not None:
            self._serial_connection.close()
            self._serial_connection = None

        if self._listening_thread is not None:
            self._listening_thread.join(1000)
            self._listening_thread = None

    def write_line(self, output_line):
        if self._serial_connection is not None:
            self._serial_connection.write(bytes(output_line + '\n', 'utf-8'))

    def read_one_line(self):
        return self._serial_connection.readline().decode("utf-8").strip()

    def _listening_method(self):
        try:
            while True:
                # input_line = self._serial_connection.readline().decode("utf-8").strip()
                input_line = self._serial_connection.readline()
                if input_line:
                    # print('ARDUINO >>> ', end='')
                    # print(input_line)
                    if self._on_input_line_callback is not None:
                        try:
                            self._on_input_line_callback(input_line)
                        except Exception as ex:
                            print('Exception with on_input_line Callback: ' + str(ex))

        except serial.SerialException as e:
            print('ARDUINO [ERROR] on listening')
            print(e)

        print('Listening Thread stopping')

    @staticmethod
    def trouver_ports_arduino():
        """
        Trouve les ports sur lesquels sont connecté des cartes Arduino.

        Renvoi:
            list arduino_ports: Liste des ports sur lesquels sont connecté des cartes Arduino
        """

        arduino_ports = []

        ports = list(serial.tools.list_ports.comports())
        print('* List of Serial Ports:')
        for p in ports:
            print(p.device, '[', p.product, '] /', p.description, '@', p.manufacturer)
            if not (p.product is None) and 'Arduino' in p.product or not (p.description is None) and 'Arduino' in p.description:
                arduino_ports.append((p.device, p.description))
        print()

        for port, description in arduino_ports:
            print(f'=> Found Arduino device on port : {port}, description : {description}')
        print()

        return arduino_ports
