import numpy as np
import random as rnd

class RecocidoSimulado:
    
    def __init__(self, horas, profes, funcion_aptitud, dim, semilla = 0):
        self.horas = horas
        self.profes = profes
        self.funcion_aptitud = funcion_aptitud
        self.temperatura_inicial = 100
        self.dimension = dim
        self.tamaño_sol = dim[0]*dim[1]

    def solucion_incial(self):
        elementos = []
        for i in range(len(self.horas)):
            elementos += self.horas[i] * [self.profes[i]]
        cantidad_ceros = (self.dimension[0] * self.dimension[1]) - len(elementos)
        elementos += cantidad_ceros * [0] 
        ejemplo = rnd.sample(elementos, len(elementos))
        return np.array(ejemplo)

    def esquema_temperatura(self, iteracion):
        # return 
        # return self.temperatura_inicial / ( 1 + np.log(iteracion))
        return self.temperatura_inicial / ( 1 + iteracion)

    def generar_vecino(self, sol):
        sol_nueva = sol.copy()
        indice1 = rnd.randint(0,self.tamaño_sol-1)
        indice2 = rnd.randint(0,self.tamaño_sol-1)
        elemento = sol_nueva[indice1]
        sol_nueva[indice1] = sol_nueva[indice2]
        sol_nueva[indice2] = elemento
        return sol_nueva

    def recocido_simulado(self, iteraciones_max):
        sol = self.solucion_incial()
        self.aptitudes = [self.funcion_aptitud(sol)]
        for i in range(iteraciones_max):
            temperatura = self.temperatura_inicial
            sol_vecino = self.generar_vecino(sol)
            diff = self.funcion_aptitud(sol_vecino) - self.funcion_aptitud(sol)
            if diff < 0: sol = sol_vecino.copy()
            else: 
                proba = rnd.uniform(0,1)
                if proba < np.exp(-diff / temperatura): sol = sol_vecino.copy()
            self.aptitudes.append(self.funcion_aptitud(sol))
            temperatura = self.esquema_temperatura(i)
        return sol





