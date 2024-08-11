import random as rnd
import pandas as pd
import numpy as np
import random
from horario import OperacionesHorario
from recocido_simulado import RecocidoSimulado

class GeneradorHorarios:

    def __init__(self, excel_profes, horas_al_dia, cantidad_grupos, semilla):
        self.semilla = semilla
        self.detalles = pd.read_csv(excel_profes, sep = " ", index_col = False)
        self.profes = self.detalles['nombre'].tolist()
        # self.horas = {x: y for x,y in zip(self.profes,self.detalles['horas'])}
        self.horas = self.detalles['horas'].tolist()
        self.horas_servicio = self.detalles['servicio'].tolist()
        self.dimension = (horas_al_dia,5, cantidad_grupos) # renglones son la hora de clase, columna por día y así por cada grupo

    def indices_elementos_repetidos(self, lista, elemento):
        lista = list(lista)
        indice_cercano = -1 
        indices = []
        for _ in range(len(lista)):
            try:
                loc = lista.index(elemento, indice_cercano+1)
            except ValueError:
                break
            else:
                indices.append(loc)
                indice_cercano = loc
        return indices

    def misma_columna(self, indice1, indice2, numero_columnas):
        # print(x,y)
        for n in range(numero_columnas+1):
            # print(6*n,6*n+1)
            if 6*n <= indice1 < 6*n + 6 and  6*n <= indice2 < 6*n + 6: return True
        return False

    def suma_distancia_entre_puntos(self, puntos):
        distancias = []
        # print(puntos)
        for i in puntos:
            distancias.append(np.abs(np.array([i]) - np.array([x for x in puntos if x != i and (self.misma_columna(i,x,5))])).sum())
        return distancias

    # def dias_sin_clases(self,sol):
    #     columnas_ceros = 0
    #     for x in np.split(sol, [6,12,18,24]):
    #         # unique, counts = np.unique(x,return_counts= True)
    #         # print(np.unique(x))
    #         if np.all(x == '0'): 
    #             columnas_ceros += 5
    #             # print("si")
    #     return columnas_ceros

    def funcion_aptitud(self, sol):
        suma = 0
        for profe in self.profes:
            indices = self.indices_elementos_repetidos(sol, profe)
            distancias = self.suma_distancia_entre_puntos(indices)
            # print(profe, distancias)
            suma += np.array(distancias).sum() #+ self.dias_sin_clases(sol)
        return suma

    def optimizacion_recocido_simulado(self, iteraciones_max, repeticiones):
        self.log_aptitudes = []
        self.mejores_horarios = []
        for _ in range(repeticiones):
            recocido = RecocidoSimulado(self.horas, self.profes, self.funcion_aptitud, self.dimension, self.semilla)
            mejor_sol = recocido.solucion_incial()
            sol = recocido.recocido_simulado(iteraciones_max)
            # print(self.funcion_aptitud(sol))
            self.log_aptitudes.append(self.funcion_aptitud(sol))
            if self.funcion_aptitud(mejor_sol) > self.funcion_aptitud(sol): 
                mejor_sol = sol.copy()
                # self.log_aptitudes = recocido.aptitudes.copy()
            if self.funcion_aptitud(sol) == 0.0: self.mejores_horarios.append(sol.copy())

        # return pd.DataFrame(OperacionesHorario.decodificar_horario(mejor_sol, (self.dimension[0],self.dimension[1])), columns = ['L','M','M','J','V'])
        return mejor_sol
        
    # def graficar_evolucion_aptiud(self):

