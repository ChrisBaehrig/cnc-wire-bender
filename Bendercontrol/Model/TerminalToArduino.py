import serial


class TerminalToArduino:
    startMarker = 60
    endMarker = 62
    waitingForReply = False

    def connection_built(self, ser_port, baud_rate):
        try:
            self.ser = serial.Serial(ser_port, baud_rate)

        except serial.SerialException:
            # There is no new data from serial port
            print("Port ist't Used find correct Port")
            return None

        except TypeError:
            # Disconnect of USB->UART occured
            print("Port occurred, will be closed")
            ser_port.close()
            return None
        else:
            print("Serial port " + ser_port + " opened Baudrate " + str(baud_rate))

            msg = ""
            while msg.find("Arduino is ready") == -1:

                while self.ser.inWaiting() == 0:
                    pass

                msg = self.recv_from_arduino()
                print(msg)  # python3 requires parenthesis
                print()

            return 1

    def send_to_arduino(self, send_str):
        try:
            self.ser.write(send_str.encode('utf-8'))  # change for Python3

        except AttributeError:
            print("No Connection")
            return None

        else:
            print("Command send to Arduino:    " + send_str)
            print("------------------------------------------------")
            return send_str

    def recv_from_arduino(self):
        ck = ""
        x = "z"  # any value that is not an end- or startMarker
        byte_count = -1  # to allow for the fact that the last increment will be one too many

        # wait for the start character
        while ord(x) != self.startMarker:
            x = self.ser.read()

        # save data until the end marker is found
        while ord(x) != self.endMarker:
            if ord(x) != self.startMarker:
                ck = ck + x.decode("utf-8")  # change for Python3
                byte_count += 1
            x = self.ser.read()

        return "<" + ck + ">"

    def send_command(self, command):
        """
        send Command to Arduino
        :param command: str example: "<1, 1, -4000, 1000 ,0 ,0.0 >"
        :return: command as string
        """
        self.send_to_arduino(command)
        recv_command = self.recv_from_arduino()
        if command != recv_command:
            print("--------")
            print("Error: send failure")
            print(command)
            print(recv_command)
            print("--------")
            return "Error: send failure"
        else:
            return recv_command
