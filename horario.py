import pandas as pd
import numpy as np

class OperacionesHorario:  

    # def __init__(self, horas, profes_por_dia):
    #     self.horario = pd.DataFrame(profes_por_dia, index = horas)
        
    # def solucion_aleatoria_inicial(self):

    @staticmethod
    def codificar_horario(horario:pd.DataFrame):
        return horario.to_numpy().flatten('F')
    
    @staticmethod
    def decodificar_horario(cod, dim:tuple):
        return cod.reshape((dim[0],dim[1]), order = 'F')