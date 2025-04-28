import yaml


class Settings:
    def load_yaml(self):
        with open('Bendercontrol/Model/settings.yaml') as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)

    def get_setting(self, axis, data):
        """
        get the Motorsettings
        :param axis: x_axis, y_axis, z_axis, p_axis
        :param data: attribut example: angle_max...
        :return: value
        """
        # print(self.data[axis][data])
        return self.data[axis][data]

    def get_port(self):
        return self.data['port']

    def set_port(self, new_port):
        self.data['port'] = new_port
        with open('Bendercontrol/Model/settings.yaml', "w") as f:
            yaml.dump(self.data, f)

    def set_position(self, position):
        """
        store new position to settings
        :param position: list [x,y,z,p]
        :return: position as list [x,y,z,p]
        """
        self.data['position']['x'] = position[0]
        self.data['position']['y'] = position[1]
        self.data['position']['z'] = position[2]
        self.data['position']['p'] = position[3]
        with open('Bendercontrol/Model/settings.yaml', "w") as f:
            yaml.dump(self.data, f)

        position = [self.data['position']['x'], self.data['position']['y'], self.data['position']['z'], self.data['position']['p']]
        return position

    def get_position(self):
        """
        return position from settings
        :return: Position as list [x,y,z,p]
        """
        position = [self.data['position']['x'], self.data['position']['y'], self.data['position']['z'], self.data['position']['p']]
        return position
