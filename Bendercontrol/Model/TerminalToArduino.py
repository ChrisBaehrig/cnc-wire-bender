import serial
import time


class TerminalToArduino:
    startMarker = 60
    endMarker = 62
    waitingForReply = False
    timeout = 35  # seconds - increased to accommodate motor movement

    def connection_built(self, ser_port, baud_rate):
        try:
            self.ser = serial.Serial(ser_port, baud_rate, timeout=1)
            self.ser.reset_input_buffer()  # Clear any old data
            self.ser.reset_output_buffer()  # Clear output buffer

        except serial.SerialException as e:
            print(f"Serial port error: {str(e)}")
            return None

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None
        else:
            print(f"Serial port {ser_port} opened Baudrate {baud_rate}")

            start_time = time.time()
            while time.time() - start_time < self.timeout:
                if self.ser.in_waiting > 0:
                    msg = self.recv_from_arduino()
                    print(f"Received during connection: {msg}")
                    if msg and "Arduino is ready" in msg:
                        return 1
                time.sleep(0.1)

            print("Timeout waiting for Arduino ready message")
            self.ser.close()
            return None

    def send_to_arduino(self, send_str):
        try:
            if not self.ser or not self.ser.is_open:
                print("No active serial connection")
                return None
                
            self.ser.reset_input_buffer()  # Clear any old data
            self.ser.write(send_str.encode('utf-8'))
            self.ser.flush()  # Wait until all data is written

        except AttributeError:
            print("No Connection")
            return None
        except Exception as e:
            print(f"Error sending data: {str(e)}")
            return None
        else:
            print(f"Command send to Arduino: {send_str}")
            return send_str

    def recv_from_arduino(self):
        try:
            if not self.ser or not self.ser.is_open:
                print("No active serial connection")
                return None

            ck = ""
            x = "z"
            byte_count = -1
            start_time = time.time()

            # Wait for start marker with timeout
            while ord(x) != self.startMarker:
                if time.time() - start_time > self.timeout:
                    print("Timeout waiting for start marker")
                    return None
                if self.ser.in_waiting > 0:
                    x = self.ser.read()

            # Save data until end marker is found
            while ord(x) != self.endMarker:
                if time.time() - start_time > self.timeout:
                    print("Timeout waiting for end marker")
                    return None
                if self.ser.in_waiting > 0:
                    x = self.ser.read()
                    if ord(x) != self.startMarker:
                        ck = ck + x.decode("utf-8")
                        byte_count += 1

            result = "<" + ck + ">"
            print(f"Received message: {result}")
            return result

        except Exception as e:
            print(f"Error receiving data: {str(e)}")
            return None

    def send_command(self, command):
        """
        send Command to Arduino
        :param command: str example: "<1, 1, -4000, 1000, 0, 0>"
        :return: command as string
        """
        self.send_to_arduino(command)
        recv_command = self.recv_from_arduino()
        
        # Extract the core command parameters (first 4 values) for comparison
        def extract_core_cmd(cmd):
            if not cmd:
                return None
            try:
                # Remove < and > and split by commas
                values = cmd.strip('<>').split(',')
                # Take first 4 values and recombine
                return '<' + ','.join(values[:4]) + '>'
            except:
                return None

        core_sent = extract_core_cmd(command)
        core_recv = extract_core_cmd(recv_command)
        
        if core_sent != core_recv:
            print("--------")
            print("Error: send failure")
            print(f"Sent: {command}")
            print(f"Received: {recv_command}")
            print("--------")
            return "Error: send failure"
        else:
            print("------------------------------------------------")
            return recv_command
