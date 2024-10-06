from clases_furgonetas import Furgoneta


class OperadorProblemaBicing(object):
    pass

class IntercambiarDestinoFurgos(OperadorProblemaBicing):
    """
    Intercambia las estaciones destino de dos furgonetas
    """
    def __init__(self,furgoneta1: Furgoneta, furgoneta2: Furgoneta, estacion1: int, estacion2: int):
        self.furgo1 = furgoneta1
        self.furgo2 = furgoneta2
        self.est1 = estacion1
        self.est2 = estacion2
    
    def __repr__(self) -> str:
        return f"Se intercambia la destinación {self.est1} de la furgoneta {(self.furgo1).id_furgo}" \
               f"por la destinación {self.est2} de la furgoneta {self.furgo2.id_furgo}"


class ReasignarFurgoAEstacion(OperadorProblemaBicing):
    """
    Cambia la estación a la que va una furgoneta, igual va a una estación con
    más excedente para optimizar
    """
    def __init__(self, furgoneta: Furgoneta, estacion1: int, estacion2: int):
        self.furgo = furgoneta
        self.est1 = estacion1
        self.est2 = estacion2
    
    def __repr__(self) -> str:
        return f"Furgoneta {self.furgo.id_furgo} pasa de ir a la estacion {self.est1} a la estacion {self.est2}"


class ReorganizacionEntregas(OperadorProblemaBicing):
    """
    Cambia orden en el que furgoneta entrega las bicis en las estaciones destino
    """
    def __init__(self, furgoneta: Furgoneta):
        self.furgo = furgoneta
        self.est1 = furgoneta.est1
        self.est2 = furgoneta.est2
    
    def __repr__(self) -> str:
        return f"Furgoneta {self.furgo.id_furgo} ahora va primero a estacion {self.est2} y luego a {self.est1}"

class AjusteCantidadBicisOrigen(OperadorProblemaBicing):
    """
    Cambia el número de bicis que coge de la estacion origen
    para coincidir con necesidades de estaciones destino
    """
    def __init__(self, furgoneta: Furgoneta, nuevo_numero_bicis: int):
        self.furgo = furgoneta
        self.numero_bicis_anterior = furgoneta.bicis_cogidas
        self.numero_bicis_nuevo = nuevo_numero_bicis
    
    def __repr__(self) -> str:
        return f"Furgoneta {self.furgo.id_furgo} pasa de recoger {self.numero_bicis_anterior} bicis a recoger {self.numero_bicis_nuevo} bicis"

class ReasignacionBicis(OperadorProblemaBicing):
    """ 
    Cambia el número de bicis a entregar de cada estación
    """
    def __init__(self, furgoneta: Furgoneta, nuevo_numero_bicis_est1: int, nuevo_numero_bicis_est2: int):
        self.furgo = furgoneta
        self.bicis_dejadas_est1 = furgoneta.bicis_dejadas_est1
        self.bicis_dejadas_est2 = furgoneta.bicis_cogidas - furgoneta.bicis_dejadas_est1
        self.nuevo_numero_bicis_est1 = nuevo_numero_bicis_est1
        self.nuevo_numero_bicis_est2 = nuevo_numero_bicis_est2
        
    def __repr__(self) -> str:
        return f"Furgoneta {self.furgo.id_furgo} pasa de dejar {self.bicis_dejadas_est1} bicis en la estación 1 a dejar {self.nuevo_numero_bicis_est1} bicis \n " \
               f"y pasa de dejar {self.bicis_dejadas_est2} bicis en la estación 2 a dejar {self.nuevo_numero_bicis_est2} bicis"

class AñadirSegundaEstacion(OperadorProblemaBicing):
    """
    Afegeix una segona estació a una furgoneta per poder fer una entrega més
    """
    def __init__(self, furgoneta: Furgoneta, estacion2: int, num_bicis: int):
        self.furgo = furgoneta
        self.est1 = furgoneta.est1
        self.est2 = estacion2
        self.bicis_dejadas_est1 = num_bicis
        self.bicis_dejadas_est2 = self.furgo.bicis_cogidas - num_bicis
    
    def __repr__(self) -> str:
        return f"Furgoneta {self.furgo.id_furgo} ahora va también a la estación {self.est2} donde deja {self.bicis_dejadas_est2}"
#Altres operadors que no sé si són necessaris: eliminació i creació de furgo, optimització de ruta d'una furgo(per on va a les estacions destí)