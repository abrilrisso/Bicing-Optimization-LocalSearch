from abia_bicing import Estaciones
from clases_furgonetas import Furgoneta


class Parametros(object):
    def __init__(self, estaciones: Estaciones, num_furgonetas: int, semilla:int):
        self.estaciones = []
        self.furgonetas = []
        self.semilla = semilla  # para randomizar algunos parámetros en la primer funcion generadora del estado inicial
        
        for estacion in estaciones.lista_estaciones:
            self.estaciones.append(estacion)

        for i in range(num_furgonetas):
            furgo = Furgoneta()
            furgo.id_furgo = i
            self.furgonetas.append(furgo)

    def __repr__(self):
        return f"Params(estaciones={self.estaciones}, furgonetas={self.furgonetas}, semilla={self.semilla})"