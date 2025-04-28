#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####################################################
#                                                   #
#        Version V6.0 Realesed                      #
#                                                   #
#####################################################

# Realesed:
# V1.0 Übernahme der Vorlage und Aufräumen
# V1.1 Aufteilen und strukturieren in Programmstruktur
# V2.0 Erstes Einbinden der GUI für "einrichten"
# V2.1 COM-Port Einstellungen verbessern Verbindung automatisch aufbauen
# V3.0 Erstellen G-Code interpreter
# V4.0 Manueller Modus aufbauen
# V5.0 Einarbeiten der Fehler aus den tests an der Maschine(Y/Z Achse richtig ansteuern...)
# V6.0 Neuer Benderkopf mit Servosteuerung

# Realeseplanung:


# Vorbereitunge:
# Installation PYCharm
# Installation Python 3.9
# Installation aller Packages (Pandas, PYQt5, PyYAML, numpy, pyserial)


import sys

from PyQt5 import QtWidgets

from Bendercontrol.Model.Settings import Settings
from Bendercontrol.Model.GCode import GCode
from Bendercontrol.View.GUI import GUI
from Bendercontrol.Model.TerminalToArduino import TerminalToArduino


def main():

    app = QtWidgets.QApplication(sys.argv)
    dialog = GUI()
    dialog.show()

    # --------------------------

    sys.exit(app.exec_())  # Close Window


if __name__ == "__main__": main()
