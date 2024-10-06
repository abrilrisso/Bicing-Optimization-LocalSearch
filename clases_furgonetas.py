
class Furgoneta(object):
    """
    Clase que representa una furgoneta
    """

    def __init__(self, est_inicial: int = None, est1: int = None, est2: int = None):
        self.est_inicial = est_inicial
        self.est1 = est1
        self.est2 = est2
        """
        * coordX y coordY son atributos públicos que representan las
          coordenadas X e Y iniciales de la furgoneta, mismas de la
          estación donde recojerá las bicicletas
        * bicis_transporte es un atributo público que guarda el número
          de bicicletas que coge la furgoneta en la estación de inicio
          del trayecto
        """
        self.bicis_cogidas: int = 0
        self.bicis_dejadas_est1: int = 0
        self.id_furgo: int = 0

    def __repr__(self):
      if self.est_inicial != None:
        if self.est2 == None:
          return f"\n Furgo {self.id_furgo:2d} \n"\
                 f"Est.inicial: {self.est_inicial:2d} Est1: {self.est1:2d} \n"\
                 f"Bic.cogidas: {self.bicis_cogidas:2d} Bic1:{self.bicis_dejadas_est1:2d}"
        else:
          return f"\n Furgo {self.id_furgo:2d} \n"\
                f"Est.inicial: {self.est_inicial:2d} Est1: {self.est1:2d} Est2: {self.est2:2d} \n"\
                f"Bic.cogidas: {self.bicis_cogidas:2d} Bic1:{self.bicis_dejadas_est1:2d} Bic2:{self.bicis_cogidas - self.bicis_dejadas_est1:2d}"
