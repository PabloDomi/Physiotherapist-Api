#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import ast


class DataProcessorv2:
    def __init__(self, data, output_path):
        self.data = data
        self.output_path = output_path
        self.pattern = r"x=(-?\d+\.\d+(?:E[-+]?\d+)?), y=(-?\d+\.\d+(?:E[-+]?\d+)?), z=(-?\d+\.\d+(?:E[-+]?\d+)?), visibility=(\d+\.\d+(?:E[-+]?\d+)?)"
        self.data_list = self.read_data(data)
        self.landmarks_df = self.create_dataframe()
        self.save_to_csv()

    def read_data(self, data):
        """
        Lee el archivo y convierte el contenido a una estructura de datos de Python (lista de listas).
        """
        # with open(self.data_path, 'r') as file:
        #     data = file.read()
        return ast.literal_eval(data)

    def extract_values(self, data_string):
        """
        Extrae valores de una cadena utilizando un patrón regex.
        Si encuentra valores en notación científica, los convierte a 0.
        """
        matches = re.match(self.pattern, data_string)
        if matches:
            try:
                x_value = float(matches.group(1))
            except ValueError:
                x_value = 0.0

            try:
                y_value = float(matches.group(2))
            except ValueError:
                y_value = 0.0

            try:
                z_value = float(matches.group(3))
            except ValueError:
                z_value = 0.0

            try:
                visibility_value = float(matches.group(4))
            except ValueError:
                visibility_value = 0.0

            return x_value, y_value, z_value, visibility_value
        else:
            return None

    def create_dataframe(self):
        """
        Crea un DataFrame a partir de la lista de datos.
        """
        data_dict = {
            "frame": [],
            "landmark": [],
            "x": [],
            "y": [],
            "z": [],
            "visibility": []
        }

        for i in range(len(self.data_list)):
            for j in range(len(self.data_list[i])):
                data_dict["frame"].append(i)
                data_dict["landmark"].append(j)
                if self.data_list[i][j] is None:
                    data_dict["x"].append("NaN")
                    data_dict["y"].append("NaN")
                    data_dict["z"].append("NaN")
                    data_dict["visibility"].append("NaN")
                else:
                    values = self.extract_values(self.data_list[i][j])
                    if values:
                        data_dict["x"].append(format(values[0], '.6f'))
                        data_dict["y"].append(format(values[1], '.6f'))
                        data_dict["z"].append(format(values[2], '.6f'))
                        data_dict["visibility"].append(format(values[3], '.6f'))
                    else:
                        data_dict["x"].append("NaN")
                        data_dict["y"].append("NaN")
                        data_dict["z"].append("NaN")
                        data_dict["visibility"].append("NaN")

        return pd.DataFrame.from_dict(data_dict)

    def save_to_csv(self):
        self.landmarks_df.to_csv(self.output_path, index=False)


# In[ ]:


# rutas de los archivos (modificar segun sea necesario)
# data = "Datos de los landmarks en una string"
# output_path = "ruta al archivo limpio de salida (csv)"

# # Uso de la clase
# process = DataProcessorv2(data=data, output_path=output_path)
# process.save_to_csv()
