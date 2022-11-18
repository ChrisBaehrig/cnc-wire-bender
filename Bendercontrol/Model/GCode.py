import pandas as pd


class GCode:
    def __init__(self, file_path):
        # Load excel as dataframe
        self.df = pd.read_excel(open(file_path, 'rb'), sheet_name='GCODE', index_col=None, names=['g_code'])
        self.df = self.df["g_code"].str.split(r" ")  # Achtung anzahl nicht dynamisch

    def get_gcode_row_string(self, row):
        """
        give the row of the dataframe
        :param row: int
        :return: row of dataframe as string
        """
        if self.df.count() <= row:
            return '---'

        elif row < 0:
            return '---'

        else:
            df_row = self.df[[row]]
            return df_row.to_string()  # aktuelle Zeile

    def get_gcode_row_count(self):
        return int(self.df.count())

