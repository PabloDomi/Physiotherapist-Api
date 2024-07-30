#!/usr/bin/env python
# coding: utf-8

# CLASE

# In[1]:


import pandas as pd
import re
import ast


class DataProcessor:
    def __init__(self, data, output_path):
        self.data = data
        self.output_path = output_path
        self.pattern = r"x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+), visibility=(\d+\.\d+)"
        self.data_list = self.read_data()
        self.landmarks_df = self.create_dataframe()

    def read_data(self):
        """
        Lee el archivo y convierte el contenido a una estructura de datos de Python (lista de listas).
        """
        # with open(self.data_path, 'r') as file:
        #     data = file.read()
        return ast.literal_eval(self.data)

    def extract_values(self, data_string):
        """
        Extrae valores de una cadena utilizando un patrón regex.
        """
        matches = re.match(self.pattern, data_string)
        if matches:
            x_value = float(matches.group(1))
            y_value = float(matches.group(2))
            z_value = float(matches.group(3))
            visibility_value = float(matches.group(4))
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


# In[3]:


# # datapath = r"C:\Users\ARMCO\Documents\PROYECTOS\Anaphys\data\landmarks_prueba_2.txt"
# output_path = r"/tmp/landmarks.csv"

# # Uso de la clase
# processor = DataProcessor(data, output_path=output_path)
# landmarks_df = processor.landmarks_df
# processor.save_to_csv()
# # Mostrar el DataFrame
# landmarks_df
