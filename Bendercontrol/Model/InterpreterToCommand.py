import time

from Bendercontrol.Model.Settings import Settings
from Bendercontrol.Model.TerminalToArduino import TerminalToArduino

from copy import deepcopy



class InterpreterToCommand:
    def __init__(self, terminal):
        self.settings = Settings()
        self.settings.load_yaml()

        self.dict_gcode = {}

        self.terminal = terminal

    def get_command_from_gcode(self, gcode):
        # Cut String to important Char
        print("***************************************************************************")
        print("Interpreter G-Code 1: " + gcode)
        try:
            gcode = gcode.split('[')
            gcode = gcode[1]
            gcode = gcode.split(']')
            gcode = str(gcode[0])
            list_gcode = gcode.split(',')  # Cut string to list
        except IndexError:
            print("Error Gcode can't read")
            return -1

        # Change List to Dictionary
        self.dict_gcode['row'] = list_gcode[0][1:10]
        self.dict_gcode['command'] = list_gcode[1][1:10]

        for x in range(2, len(list_gcode[2:]) + 2):
            self.dict_gcode[list_gcode[x][1]] = list_gcode[x][2:10]

        print(self.dict_gcode)

        # Open method with command https://data-flair.training/blogs/python-switch-case/
        method_name = self.dict_gcode['command']
        method = getattr(self, method_name, lambda: 'Invalid')
        method()

    # -------------G-Codes----------------------

    def G01(self):
        """
        Run Command G01 "Step driving Position"
        :return: 0 if done
        """
        print("G01")

        # ---Z-Axis--- ( And Moving Pin to the side)
        if self.dict_gcode.get('Z', 0):
            old_position = self.settings.get_position()
            print("Last Position              ", old_position)
            new_position = deepcopy(old_position)  # Copy the hole List

            new_position[2] = int(self.dict_gcode['Z'])
            print("New Position               ", new_position)

            new_position = self.pin_free_for_driving(old_position, new_position)
            print("New Position with free Pin ", new_position)

            str_command = self.calc_axis_abs(old_position, new_position, 'z_axis', int(self.dict_gcode['K']))
            if str_command != -1:
                self.terminal.send_command(str_command)
            self.settings.set_position(new_position)

        # ---Y-Axis---
        if self.dict_gcode.get('Y', 0):
            old_position = self.settings.get_position()
            print("Last Position              ", old_position)
            new_position = deepcopy(old_position)

            new_position[1] = int(self.dict_gcode['Y'])
            print("New Position               ", new_position)

            str_command = self.calc_axis_abs(old_position, new_position, 'y_axis', int(self.dict_gcode['J']))
            if str_command != -1:
                self.terminal.send_command(str_command)
            self.settings.set_position(new_position)

        # ---X-Axis---
        if self.dict_gcode.get('X', 0):
            old_position = self.settings.get_position()
            print("Last Position              ", old_position)
            new_position = deepcopy(old_position)

            new_position[0] = float(self.dict_gcode['X'])
            print("New Position               ", new_position)

            str_command = self.calc_axis_abs(old_position, new_position, 'x_axis', int(self.dict_gcode['I']))
            if str_command != -1:
                self.terminal.send_command(str_command)
            self.settings.set_position(new_position)

        return 0

    def G02(self):  # Multi-Achsen-Steuerung
        return 0

    def G03(self):
        print("G03")
        return 0

    def G04(self):  # Wait in seconds
        print("G04: Wait in seconds")
        time.sleep(int(self.dict_gcode['H']))
        return 0

    def G28(self):  # Nullpunkt anfahren
        print("G28")
        old_position = self.settings.get_position()
        new_position = [0.0, 0, 0, 0]
        all_axis = ['x_axis', 'y_axis', 'z_axis', 'p_axis']

        for c, axis in enumerate(all_axis):
            str_command = self.calc_axis_abs(old_position, new_position, axis, self.settings.get_setting(axis, 'work_speed'))
            print("Command send to Arduino: " + str_command)

            if str_command != -1:
                pass
                # self.terminal.send_command(str_command)

        self.settings.set_position(new_position)

    def G92(self):  # All positions NULL
        print("G92")
        new_position = [0.0, 0, 0, 0]
        self.settings.set_position(new_position)

    def M10(self):  # Drive wire for insert new wire in start position
        print("M10 Draht vorfahren in Nullposition")
        self.set_pin(str(self.dict_gcode['row']), 0)  # Pin down
        self.terminal.send_command("<0, 3, 2000, 1500>")
        print("Command send to Arduino: " + "<0, 3, 2000, 1500>")
        # self.G28() # TODO: G28 Debugen und testen dann wieder einschalten
        return 1

    def M11(self):  # Drive wire for cutting
        print("M11 Drahr vorfahren zum abschneiden")
        self.set_pin(str(self.dict_gcode['row']), 0)  # Pin down
        self.terminal.send_command("<0, 3, 200, 1500>")
        print("Command send to Arduino: " + "<0, 3, 200, 1500>")
        self.G28()
        return 1

    def M20(self):  # Pin down
        self.terminal.send_command(str("<" + str(self.dict_gcode['row']) + ", " + str(self.settings.get_setting("p_axis", 'number')) + ", " + str(self.settings.get_setting("p_axis", 'pin_down')) + ", 0>"))
        return 1

    def M21(self):  # Pin up
        self.terminal.send_command(str("<" + str(self.dict_gcode['row']) + ", " + str(self.settings.get_setting("p_axis", 'number')) + ", " + str(self.settings.get_setting("p_axis", 'pin_up')) + ", 0>"))
        return 1

    def M30(self):  # Programm ende beendet Automatik
        print("M30")
        #self.G28() # TODO: G28 Debugen und testen dann wieder einschalten
        return 1

    # -------------Calculations----------------------

    def calc_axis_abs(self, old_position, new_position, axis, speed):
        if new_position[0] < self.settings.get_setting(axis, 'angle_min') or new_position[0] > self.settings.get_setting(axis, 'angle_max'):
            print("Error value out of Range row: " + self.dict_gcode['row'])
            pass

        # Switch Case for different Motors
        if axis == 'x_axis' or 'y_axis' == axis:  # x_axis or y_axis turn is absolute
            steps_per_round = self.settings.get_setting(axis, 'steps_per_round')
            steps = int((steps_per_round / 360) * (new_position[int(self.settings.get_setting(axis, 'number'))-1] - old_position[int(self.settings.get_setting(axis, 'number'))-1]))
        elif axis == 'z_axis':  # z_axis feed is relative
            steps_per_mm = self.settings.get_setting(axis, 'steps_per_mm')
            steps = int(steps_per_mm * (new_position[int(self.settings.get_setting(axis, 'number')) - 1]))
        elif axis == 'p_axis':  # p_axis feed is absolute 0 or 1
            steps = int(new_position[int(self.settings.get_setting(axis, 'number')) - 1])
        else:
            return -1

        if steps != 0:
            return str("<" + str(self.dict_gcode['row']) + ", " + str(self.settings.get_setting(axis, 'number')) + ", " + str(steps) + ", " + str(speed) + ">")
        else:
            return -1

    def set_pin(self, row, pin):
        """
        Moves Pin
        :param row: 0 or a row as int
        :param pin: 0 or 1 as int; 0 = down, 1 = up
        """
        self.terminal.send_command("< " + str(row) + ", 4, " + str(pin) + ", 0 >")
        print("Command send to Arduino: < " + str(row) + ", 4, " + str(pin) + ", 0 >")

    def pin_free_for_driving(self, old_position, new_position):
        """
        to avoid collision between pin and wire
        :param old_position: list [x, y, z, p]
        :param new_position: list [x, y, z, p]
        :return: new_position: list [x, y, z, p]
        """
        feed_distance = abs(old_position[2] - new_position[2])
        speed = self.settings.get_setting('x_axis', 'work_speed')

        # Complied free way for the wire at MORE than 15 mm Z-Driving
        if feed_distance > 15:
            if old_position[0] < 0:  # if the pin stands right at drive to the left
                new_position[0] = self.settings.get_setting('home_position', 'left')
                str_command = self.calc_axis_abs(old_position, new_position, 'x_axis', speed)
                self.terminal.send_command(str_command)

                return new_position

            else:  # if the pin stands left at drive to the right
                new_position[0] = self.settings.get_setting('home_position', 'right')
                str_command = self.calc_axis_abs(old_position, new_position, 'x_axis', speed)
                self.terminal.send_command(str_command)

                return new_position

        elif feed_distance == 0:
            return old_position

        # free the wire a bit to feed forward
        else:
            if old_position[0] < 0:
                new_position[0] = old_position[0] + self.settings.get_setting('home_position', 'pin_free_angle')
            else:
                new_position[0] = old_position[0] - self.settings.get_setting('home_position', 'pin_free_angle')

            str_command = self.calc_axis_abs(old_position, new_position, 'x_axis', speed)
            self.terminal.send_command(str_command)

            return new_position
