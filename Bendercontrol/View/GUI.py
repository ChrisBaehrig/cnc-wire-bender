import time

from PyQt5 import QtWidgets, uic  # uic ist der compiler von ui (xml) zu python

from ..Model.GCode import GCode
from ..Model.InterpreterToCommand import InterpreterToCommand
from ..Model.TerminalToArduino import TerminalToArduino
import Bendercontrol.Model.Settings

import tkinter as tk
from tkinter import filedialog  # Necessary for Program without debug


# ----------------------------------------------------------------------------------------------

class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.terminal = TerminalToArduino()
        self.ui = uic.loadUi("Bendercontrol/View/GUI_Qt.ui", self)

        # SLOTS connection to GUI.ui
        self.ui.button_build_connection.clicked.connect(self.on_connect)
        self.ui.button_end_connection.clicked.connect(self.on_connect_end)
        self.ui.pushButton_COM_save.clicked.connect(self.on_com_save)
        self.ui.pushButton_einrichten_run_xaxis.clicked.connect(self.on_run_xaxis)
        self.ui.pushButton_einrichten_run_yaxis.clicked.connect(self.on_run_yaxis)
        self.ui.pushButton_einrichten_run_zaxis.clicked.connect(self.on_run_zaxis)
        self.ui.pushButton_einrichten_run_paxis.clicked.connect(self.on_run_paxis)
        self.ui.pushButton_automatic_open_gcode.clicked.connect(self.on_open_file)
        self.ui.pushButton_automatic_run.clicked.connect(self.on_run_automatic)
        self.ui.pushButton_next_row.clicked.connect(self.on_next_row)
        self.ui.button_send_manual.clicked.connect(self.on_run_manuel)
        self.ui.pushButton_point_zero.clicked.connect(self.on_point_zero)

        self.act_gcode_row = 0
        self.arduino_connected = 0
        self.g_code_load = 0

        # Initialize settings and load saved port
        self.settings = Bendercontrol.Model.Settings.Settings()
        self.settings.load_yaml()
        self.port = self.settings.get_port()
        
        # Update GUI with saved port
        self.ui.label_port.setText("Aktueller COM-Port: " + self.port)
        # Set the current port in the combo box
        current_index = self.ui.comboBox_com_port.findText(self.port)
        if current_index >= 0:
            self.ui.comboBox_com_port.setCurrentIndex(current_index)

    # --------------Folder "Einrichten"---------------------------------

    def on_connect(self):
        print("Verbindung aufbauen")
        # Build Connection --------------------------------------------------------
        self.port = self.settings.get_port()  # Use the settings instance we already have
        self.ui.label_port.setText("Aktueller COM-Port: " + self.port)
        
        try:
            self.arduino_connected = self.terminal.connection_built(self.port, 9600)
            if self.arduino_connected == 1:
                self.ui.out_status_connection.setText("Verbindung ist aufgebaut")
                self.ui.out_status_connection.setStyleSheet("color: green")
            else:
                self.ui.out_status_connection.setText("Verbindungsaufbau fehlgeschlagen")
                self.ui.out_status_connection.setStyleSheet("color: red")
        except Exception as e:
            print(f"Connection error: {str(e)}")
            self.ui.out_status_connection.setText(f"Fehler: {str(e)}")
            self.ui.out_status_connection.setStyleSheet("color: red")
            self.arduino_connected = 0

    def on_connect_end(self):
        try:
            if self.arduino_connected == 0:
                print("Verbindung ist bereits beendet")
            else:
                self.terminal.ser.close()
                self.ui.out_status_connection.setText("Verbindung ist beendet")
                self.ui.out_status_connection.setStyleSheet("color: black")
                self.arduino_connected = 0
        except Exception as e:
            print(f"Error closing connection: {str(e)}")
            self.ui.out_status_connection.setText("Fehler beim Beenden der Verbindung")
            self.ui.out_status_connection.setStyleSheet("color: red")
            self.arduino_connected = 0

    def on_com_save(self):
        # Use the existing settings instance instead of creating a new one
        new_port = str(self.ui.comboBox_com_port.currentText())
        self.settings.set_port(new_port)
        self.port = new_port  # Update current port
        self.ui.label_port.setText("Aktueller COM-Port: " + self.port)
        print(f"COM-Port gespeichert: {self.port}")  # Debug output

    def on_run_xaxis(self):
        if self.arduino_connected == 0:
            self.on_connect()

        axis = str(1)  # Axis: 1 = XAxis...
        steps = str(self.ui.spinBox_einrichten_xaxis.value())
        speed = str(self.ui.spinBox_einrichten_xaxis_speed.value())
        command_str = "<1, " + axis + ", " + steps + ", " + speed + ", 0, 0>"

        self.terminal.send_command(command_str)
        # Wait for Arduino to finish movement
        time.sleep(1)  # Reduced fixed delay

    def on_run_yaxis(self):
        if self.arduino_connected == 0:
            self.on_connect()

        axis = str(2)  # Axis: 2 = YAxis...
        steps = str(self.ui.spinBox_einrichten_yaxis.value())
        speed = str(self.ui.spinBox_einrichten_yaxis_speed.value())
        command_str = "<1, " + axis + ", " + steps + ", " + speed + ", 0, 0>"
        self.terminal.send_command(command_str)
        time.sleep(1)  # Reduced fixed delay

    def on_run_zaxis(self):
        if self.arduino_connected == 0:
            self.on_connect()

        axis = str(3)  # Axis: 3 = ZAxis...
        steps = str(self.ui.spinBox_einrichten_zaxis.value())
        speed = str(self.ui.spinBox_einrichten_zaxis_speed.value())
        command_str = "<1, " + axis + ", " + steps + ", " + speed + ", 0, 0>"
        self.terminal.send_command(command_str)
        time.sleep(1)  # Reduced fixed delay

    def on_run_paxis(self):
        if self.arduino_connected == 0:
            self.on_connect()

        axis = str(4)  # Axis: 4 = PAxis...
        steps = str(self.ui.spinBox_einrichten_paxis.value())
        speed = str(0)
        command_str = "<1, " + axis + ", " + steps + ", " + speed + ", 0, 0>"
        self.terminal.send_command(command_str)
        time.sleep(1)  # Reduced fixed delay

    def on_point_zero(self):
        command = InterpreterToCommand(self.terminal)
        command.G92()

    # --------------Reiter Manuell---------------------------------

    def on_run_manuel(self):
        command = InterpreterToCommand(self.terminal)

        if self.arduino_connected == 0:
            self.on_connect()

        axis = ['', '', '', '']
        speed = ['', '', '', '']
        axis[0] = str(self.ui.spinBox_xaxis.value())
        axis[1] = str(self.ui.spinBox_yaxis.value())
        axis[2] = str(self.ui.spinBox_zaxis.value())
        axis[3] = str(self.ui.spinBox_paxis.value())
        speed[0] = str(self.settings.get_setting('x_axis', 'work_speed'))
        speed[1] = str(self.settings.get_setting('y_axis', 'work_speed'))
        speed[2] = str(self.settings.get_setting('z_axis', 'work_speed'))

        # Example: 1    [N1, G01, X29, I1500, Y26, J1200, Z90, K1300]
        gcode = "0    [N0, G01, X" + axis[0] + ", I" + speed[0] + ", Y" + axis[1] + ", J" + speed[1] + ", Z" + axis[2] + ", K" + speed[2] + "]"
        print(gcode)
        command.get_command_from_gcode(gcode)

        # Pin heben und senken
        if axis[3] == '0':
            command.M20()
        if axis[3] == '1':
            command.M21()

    # --------------Reiter Automatic---------------------------------

    def on_run_automatic_old(self):
        test_data = []
        test_data.append("<1, 1, -4000, 1000 ,0 ,0.0 >")
        test_data.append("<2, 2, 4000, 200 ,0 ,0.0 >")
        test_data.append("<3, 2, -4000, 600 ,0 ,0.0 >")
        test_data.append("<4, 1, 8000, 2000 ,0 ,0.0 >")
        test_data.append("<5, 1, -4000, 6000 ,0 ,0.0 >")

        num_loops = len(test_data)

        n = 0
        while n < num_loops:  # Alle Zeilen abarbeiten
            teststr = test_data[n]

            self.terminal.send_to_arduino(teststr)

            while self.terminal.ser.inWaiting() == 0:  # "Pass" erst wenn Daten angekommen
                pass

            data_recv = self.terminal.recv_from_arduino()
            print("Reply Received  " + data_recv)
            print("===========")
            n += 1

            time.sleep(5)

    def on_open_file(self):
        root = tk.Tk()
        root.withdraw()

        # self.file_path_gcode = "D:/Hobby_Projekte/Drahtbiegemaschiene/Programmierung/Excel-Berechnung/test2.xlsx"
        # self.file_path_gcode = "C:/Users/Q396791/Desktop/Bender/20-01-09_Ecel_V1/test.xlsx"  # Nur zum Testen
        # self.file_path_gcode = "D:/Hobby_Projekte/Drahtbiegemaschiene/cnc-wire-bender/Examples/GCode/test.xlsx"  # Nur zum Testen
        self.file_path_gcode = tk.filedialog.askopenfilename()  # Debug
        self.ui.out_status_gcode.setText("G Code ist geladen")
        print(self.file_path_gcode)
        print("test")

        self.g_code = GCode(self.file_path_gcode)
        print("GCode ist geladen")
        self.act_gcode_row = 0
        self.__update_text_gcode()
        self.g_code_load = 1

    def on_next_row(self):
        if self.arduino_connected == 0:
            self.on_connect()

        if self.g_code_load == 0:
            self.on_open_file()

        if self.act_gcode_row < self.g_code.get_gcode_row_count():  # Letzte Zeile abfangen

            command = InterpreterToCommand(self.terminal)
            edit_gcode = self.ui.out_in_act_gcode.text()  # Abfrage aus edit feld
            command.get_command_from_gcode(edit_gcode)

            self.act_gcode_row += 1
            self.__update_text_gcode()
        else:
            pass

    def on_run_automatic(self):
        if self.g_code_load == 0:
            self.on_open_file()

        for x in range(0, self.g_code.get_gcode_row_count()):
            self.on_next_row()
            x += 1
            # print(self.act_gcode_row)
            time.sleep(1)

    def __update_text_gcode(self):
        text_last_gcode = ''
        for x in range(0, 5):
            text_last_gcode += str(self.g_code.get_gcode_row_string(self.act_gcode_row + x - 5))
            text_last_gcode += '\n'
            self.ui.out_last_gcode.setText(text_last_gcode)

        gcode = str(self.g_code.get_gcode_row_string(self.act_gcode_row))
        self.ui.out_in_act_gcode.setText(gcode)

        text_next_gcode = ''
        for x in range(0, 5):
            text_next_gcode += str(self.g_code.get_gcode_row_string(self.act_gcode_row + x + 1))
            text_next_gcode += '\n'
            self.ui.out_next_gcode.setText(text_next_gcode)
