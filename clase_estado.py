from __future__ import annotations
import copy, random
from clases_operadores import OperadorProblemaBicing, AjusteCantidadBicisOrigen, ReasignarFurgoAEstacion, ReorganizacionEntregas, ReasignacionBicis, IntercambiarDestinoFurgos, AñadirSegundaEstacion
from clase_parametros import Parametros
from typing import Generator


class Estado(object):
    
    def __init__(self, furgonetas, estaciones):
        self.furgonetas = furgonetas
        self.estaciones = estaciones
    

    def getstate(self):
        return (self.furgonetas,self.estaciones)
        

    def copy(self) -> Estado:
        # Copiar furgonetas
        nueva_lista_furgonetas = [copy.copy(furgo) for furgo in self.furgonetas]
        # Copiar estaciones
        nueva_lista_estaciones = [copy.copy(est) for est in self.estaciones]
        # Copiar diferencias
        #nuevas_diferencias = [copy.copy(diferencia) for diferencia in self.diferencias]

        # nuevas_estaciones al return!
        return Estado(nueva_lista_furgonetas, nueva_lista_estaciones)

    
    def __repr__(self) -> str:
    
        print("\nESTADO ACTUAL:")
        distancia_total = 0
        
        for i in range(len(self.furgonetas)):
            furgo = self.furgonetas[i]
            
            if furgo.est_inicial != None:
                origen = self.estaciones[furgo.est_inicial]
                destino1 = self.estaciones[furgo.est1]
                distancia_total += abs(destino1.coordX - origen.coordX) + abs(destino1.coordY - origen.coordY)
                
                if furgo.est2 == None:
                    print(f"\nFurgo {i:2d} \n"\
                          f"Est.inicial: {furgo.est_inicial:2d}  Est1: {furgo.est1:2d} \n"\
                          f"Bic.cogidas: {furgo.bicis_cogidas:2d}  Bic1: {furgo.bicis_dejadas_est1:2d}")

                else:
                    destino2 = self.estaciones[furgo.est2]
                    distancia_total += abs(destino2.coordX - destino1.coordX) + abs(destino2.coordY - destino1.coordY)
                    print(f"\nFurgo {i:2d} \n"\
                          f"Est.inicial: {furgo.est_inicial:2d}  Est1: {furgo.est1:2d}  Est2: {furgo.est2:2d} \n"\
                          f"Bic.cogidas: {furgo.bicis_cogidas:2d}  Bic1: {furgo.bicis_dejadas_est1:2d}  Bic2: {furgo.bicis_cogidas - furgo.bicis_dejadas_est1:2d}")
        return f"\n Ganancias según el heurístico 1: {self.heuristico1()}"\
               f"\n Ganancias según el heurístico 2: {self.heuristico2()}"\
               f"\n Distancia total = {distancia_total}m"


    def generar_acciones(self) -> Generator[OperadorProblemaBicing, None, None]:
        
        # IntercambiarDestinoFurgos
        
        for furgo1 in self.furgonetas:
            for furgo2 in self.furgonetas:
                if (furgo1.est1 != None)  and (furgo2.est1 != None) and (furgo2 != furgo1):
                    yield IntercambiarDestinoFurgos(furgo1, furgo2, furgo1.est1, furgo2.est1)
                    
                    if furgo1.est2 != None:
                        yield IntercambiarDestinoFurgos(furgo1, furgo2, furgo1.est2, furgo2.est1)
                    if furgo2.est2 != None:
                        yield IntercambiarDestinoFurgos(furgo1, furgo2, furgo1.est1, furgo2.est2)
                    if furgo1.est2 != None and furgo2.est2 != None:
                        yield IntercambiarDestinoFurgos(furgo1, furgo2, furgo1.est2, furgo2.est2)
        

        # ReasignarFurgoAEstacion

        for furgo in self.furgonetas:
            if furgo.est1 != None:
                for i in range(len(self.estaciones)):
                    if (i != furgo.est1) and (i != furgo.est2):  
                        yield ReasignarFurgoAEstacion(furgo,furgo.est1,i)
                        if furgo.est2 != None:
                            yield ReasignarFurgoAEstacion(furgo,furgo.est2, i)
                        
   
        # ReorganizacionEntregas
        for furgo in self.furgonetas:
            if furgo.est2 != None:
                yield ReorganizacionEntregas(furgo)           
        
        
        # AjusteCantidadBicisOrigen
        for furgo in self.furgonetas:
            if furgo.est1 != None:
                diferencia = self.estaciones[furgo.est_inicial].num_bicicletas_next - self.estaciones[furgo.est_inicial].demanda
                
                if diferencia > 0:
                    excedente = min(diferencia, self.estaciones[furgo.est_inicial].num_bicicletas_no_usadas)
                    if excedente > 30:
                        excedente = 30
                    
                    for i in range(1,excedente+1):
                        if i != furgo.bicis_cogidas:
                            yield AjusteCantidadBicisOrigen(furgo, i)
        

        #ReasignacionBicis
        for furgo in self.furgonetas:
            if furgo.est1 != None and furgo.est2 != None:
                j = 0
                for i in range(1,furgo.bicis_cogidas+1):
                    if i != furgo.bicis_cogidas and i != furgo.bicis_dejadas_est1:
                        j = furgo.bicis_cogidas - i
                        yield ReasignacionBicis(furgo, i, j)
        

        #AñadirSegundaEstacion
        for furgo in self.furgonetas:
            if furgo.est1 != None and furgo.est2 == None:
                for i in range(len(self.estaciones)):
                    if (i != furgo.est_inicial) and (i != furgo.est1):
                        for n in range(1,furgo.bicis_cogidas):
                            yield AñadirSegundaEstacion(furgo, i, n)


        
    def generar_una_accion(self) -> Generator[OperadorProblemaBicing, None, None]:
        
        # IntercambiarDestinoFurgos
        combinaciones_intercambiar_destinos_furgos = set()
        for furgo1 in self.furgonetas:
            for furgo2 in self.furgonetas:
                if (furgo1.est1 != None)  and (furgo2.est1 != None) and (furgo2 != furgo1):
                    combinaciones_intercambiar_destinos_furgos.add((furgo1, furgo2, furgo1.est1, furgo2.est1))
                    if furgo1.est2 != None:
                        combinaciones_intercambiar_destinos_furgos.add((furgo1, furgo2, furgo1.est2, furgo2.est1))
                    if furgo2.est2 != None:
                        combinaciones_intercambiar_destinos_furgos.add((furgo1, furgo2, furgo1.est1, furgo2.est2))
                    if furgo1.est2 != None and furgo2.est2 != None:
                        combinaciones_intercambiar_destinos_furgos.add((furgo1, furgo2, furgo1.est2, furgo2.est2))
        
        # ReasignarFurgoAEstacion
        combinaciones_reasignar_furgo_a_estacion = set()
        for furgo in self.furgonetas:
            if furgo.est1 != None:
                for i in range(len(self.estaciones)):
                    if (i != furgo.est_inicial) and (i != furgo.est1) and (i != furgo.est2):
                        combinaciones_reasignar_furgo_a_estacion.add((furgo,furgo.est1,i))
                            
                        if furgo.est2 != None:
                            combinaciones_reasignar_furgo_a_estacion.add((furgo,furgo.est2, i))

        # ReorganizacionEntregas
        combianciones_reorganizacion_entregas = set()
        for furgo in self.furgonetas:
            if furgo.est2 != None:
                combianciones_reorganizacion_entregas.add((furgo))           

        # AjusteCantidadBicisOrigen
        combinaciones_ajuste_cantidad_bicis_origen = set()
        for furgo in self.furgonetas:
            if furgo.est1 != None:
                diferencia = self.estaciones[furgo.est_inicial].num_bicicletas_next - self.estaciones[furgo.est_inicial].demanda
                
                if diferencia > 0:
                    excedente = min(diferencia, self.estaciones[furgo.est_inicial].num_bicicletas_no_usadas)
                    if excedente > 30:
                        excedente = 30
                    
                    for i in range(1,excedente+1):
                        if i != furgo.bicis_cogidas:
                            combinaciones_ajuste_cantidad_bicis_origen.add((furgo, i))

        #ReasignacionBicis
        combinaciones_reasignacion_bicis = set()
        for furgo in self.furgonetas:
            if furgo.est1 != None and furgo.est2 != None:
                j = 0
                for i in range(1,furgo.bicis_cogidas+1):
                    if i != furgo.bicis_cogidas and i != furgo.bicis_dejadas_est1:
                        j = furgo.bicis_cogidas - i
                        combinaciones_reasignacion_bicis.add((furgo, i, j))

        #AñadirSegundaEstacion
        combinaciones_añadir_segunda_estacion = set()
        for furgo in self.furgonetas:
            if furgo.est1 != None and furgo.est2 == None:
                for i in range(len(self.estaciones)):
                    if (i != furgo.est_inicial) and (i != furgo.est1):
                         for n in range(1,furgo.bicis_cogidas):
                            combinaciones_añadir_segunda_estacion.add((furgo, i, n))
        
        a=len(combinaciones_intercambiar_destinos_furgos)
        b=len(combinaciones_reasignar_furgo_a_estacion)
        c=len(combianciones_reorganizacion_entregas)
        d=len(combinaciones_ajuste_cantidad_bicis_origen)
        e=len(combinaciones_reasignacion_bicis)
        f=len(combinaciones_añadir_segunda_estacion)
        suma=a+b+c+d+e+f
        
        valor_random = random.random()#li hauriem de posar una semilla perquè sempre generés el mateix
        if valor_random < (a/suma):
            combinacion = random.choice(list(combinaciones_intercambiar_destinos_furgos))
            yield IntercambiarDestinoFurgos(combinacion[0], combinacion[1], combinacion[2], combinacion[3])
        elif (a/suma) <= valor_random < (a+b/suma):
            combinacion = random.choice(list(combinaciones_reasignar_furgo_a_estacion))
            yield ReasignarFurgoAEstacion(combinacion[0], combinacion[1], combinacion[2])
        elif (a+b/suma) <= valor_random < (a+b+c/suma):
            combinacion = random.choice(list(combianciones_reorganizacion_entregas))
            yield ReorganizacionEntregas(combinacion[0])
        elif (a+b+c/suma) <= valor_random < (a+b+c+d/suma):
            combinacion = random.choice(list(combinaciones_ajuste_cantidad_bicis_origen))
            yield AjusteCantidadBicisOrigen(combinacion[0], combinacion[1])
        elif (a+b+c+b/suma) <= valor_random < (a+b+c+d+e/suma):
            combinacion = random.choice(list(combinaciones_reasignacion_bicis))
            yield ReasignacionBicis(combinacion[0],combinacion[1],combinacion[2])
        else:
            combinacion = random.choice(list(combinaciones_añadir_segunda_estacion))
            yield AñadirSegundaEstacion(combinacion[0],combinacion[1])



    def aplicar_acciones(self, accion: OperadorProblemaBicing) -> Estado:
        new_state = self.copy()

        if isinstance(accion, IntercambiarDestinoFurgos):
            """
            print(accion)
            print("before furgo1:", accion.furgo1)
            print("before furgo2:", accion.furgo2)
            """
            id_estf1 = accion.est1
            id_estf2 = accion.est2

            id_furgo1 = (accion.furgo1).id_furgo
            id_furgo2 = (accion.furgo2).id_furgo
            furgo1_new = new_state.furgonetas[id_furgo1]
            furgo2_new = new_state.furgonetas[id_furgo2]

            if id_estf1 == furgo1_new.est1:   # de la f1 hem agafat est1
                (new_state.furgonetas[id_furgo1]).est1 = id_estf2

                if id_estf2 == furgo2_new.est1:  # de la f2 hem agafat est 1
                    (new_state.furgonetas[id_furgo2]).est1 = id_estf1

                else:  # de la f2 hem agafat est2
                    (new_state.furgonetas[id_furgo2]).est2 = id_estf1
                
            elif id_estf2 == furgo1_new.est1:   # de la f1 hem agafat est2
                (new_state.furgonetas[id_furgo1]).est2 = id_estf2

                if id_estf2 == furgo2_new.est1:  # de la f2 hem agafat est 1
                    (new_state.furgonetas[id_furgo2]).est1 = id_estf1

                else:  # de la f2 hem agafat est2
                    (new_state.furgonetas[id_furgo2]).est2 = id_estf1
                    
            """
            print("after furgo1:", new_state.furgonetas[id_furgo1])
            print("after furgo2:", new_state.furgonetas[id_furgo2])
            """
            

        elif isinstance(accion, ReasignarFurgoAEstacion):
            """
            print(accion)
            print("before furgo:", accion.furgo)
            """
            est1_antes = accion.est1
            est2_despues = accion.est2

            id_furgo = (accion.furgo).id_furgo
            new_furgo = new_state.furgonetas[id_furgo]

            if est1_antes == new_furgo.est_inicial:
                (new_state.furgonetas[id_furgo]).est_inicial = est2_despues

            elif est1_antes == new_furgo.est1:
                (new_state.furgonetas[id_furgo]).est1 = est2_despues

            elif est1_antes == new_furgo.est2:
                (new_state.furgonetas[id_furgo]).est2 = est2_despues

            """
            print("after furgo:", new_state.furgonetas[id_furgo])
            """
            

        elif isinstance(accion, ReorganizacionEntregas):
            """
            print(accion)
            print("before furgo:",accion.furgo)
            """
            est1 = accion.est1
            est2 = accion.est2

            id_furgo = (accion.furgo).id_furgo
            new_state.furgonetas[id_furgo].est1, new_state.furgonetas[id_furgo].est2 = est2, est1
            new_state.furgonetas[id_furgo].bicis_dejadas_est1 = (accion.furgo).bicis_cogidas - (accion.furgo).bicis_dejadas_est1
            """
            print("after furgo:", new_state.furgonetas[id_furgo])
            """


        elif isinstance(accion, AjusteCantidadBicisOrigen):
            """
            print(accion)
            print("before furgo:", accion.furgo)
            """
            id_furgo = (accion.furgo).id_furgo
            bicis_anteriores = accion.numero_bicis_anterior
            bicis_nuevas = accion.numero_bicis_nuevo
            diferencia_bicis = bicis_nuevas - bicis_anteriores

            new_state.furgonetas[id_furgo].bicis_cogidas = bicis_nuevas

            if (accion.furgo).est2 == None:
                new_state.furgonetas[id_furgo].bicis_dejadas_est1 = bicis_nuevas
            
            else:
                bicis_dejadas_est2 = (accion.furgo).bicis_cogidas - (accion.furgo).bicis_dejadas_est1
                
                if diferencia_bicis + bicis_dejadas_est2 >= 0:

                    if diferencia_bicis + bicis_dejadas_est2 == 0:
                        new_state.furgonetas[id_furgo].est2 = None
                
                else:
                    new_state.furgonetas[id_furgo].bicis_dejadas_est1 = bicis_nuevas
                    new_state.furgonetas[id_furgo].est2 = None
            """
            print("after furgo:", new_state.furgonetas[id_furgo])
            """
        
        elif isinstance(accion, ReasignacionBicis):
            """
            print(accion)
            print("before furgo:", accion.furgo)
            """
            id_furgo = (accion.furgo).id_furgo
            bicis_nuevas_est1 = accion.nuevo_numero_bicis_est1

            new_state.furgonetas[id_furgo].bicis_dejadas_est1 = bicis_nuevas_est1
            """
            print("after furgo:", new_state.furgonetas[id_furgo])
            """
        
        elif isinstance(accion, AñadirSegundaEstacion):
            est1 = accion.est1
            est2 = accion.est2
            bicis_est1 = accion.bicis_dejadas_est1

            id_furgo = (accion.furgo).id_furgo
            new_furgo = new_state.furgonetas[id_furgo]

            (new_state.furgonetas[id_furgo]).est2 = est2
            (new_state.furgonetas[id_furgo]).bicis_dejadas_est1 = bicis_est1

        return new_state


    def heuristico1(self):
        self.diferencias_inicial = [est.num_bicicletas_next - est.demanda for est in self.estaciones]
        self.diferencias = [est.num_bicicletas_next - est.demanda for est in self.estaciones]
        self.actualizar_diferencias()
        total = self.calculo_coste_diferencias()
        #print("Ganancias según el heurístico 1: " + str(total))
        return total

    def heuristico2(self) -> int:
        '''
        Éste heurístico a parte de las ganancias calcula el coste de los
        kilómetros gastados por las furgonetas. 
        '''
        self.diferencias_inicial = [est.num_bicicletas_next - est.demanda for est in self.estaciones]
        self.diferencias = [est.num_bicicletas_next - est.demanda for est in self.estaciones]
        self.actualizar_diferencias()
        costo_kilometros = self.calculo_coste_kilometros()
        diferencias = self.calculo_coste_diferencias()
        ganancia_neta = diferencias - costo_kilometros
        #print("Ganancias según el heurístico 2: " + str(ganancia_neta))
        return ganancia_neta
    
    def actualizar_diferencias(self):
        for furgoneta in self.furgonetas:
            
            if furgoneta.est_inicial != None:
                self.diferencias[furgoneta.est_inicial] -= furgoneta.bicis_cogidas
            if furgoneta.est1 != None:
                self.diferencias[furgoneta.est1] += (furgoneta.bicis_dejadas_est1)
            if furgoneta.est2 != None:
                self.diferencias[furgoneta.est2] += (furgoneta.bicis_cogidas - furgoneta.bicis_dejadas_est1)
            
    def calculo_coste_kilometros(self):
        costo_kilometros = 0

        for furgoneta in self.furgonetas:
            
            if furgoneta.est_inicial != None:
                origen = self.estaciones[furgoneta.est_inicial]
                destino1 = self.estaciones[furgoneta.est1]

                distancia1 = abs(destino1.coordX - origen.coordX) + abs(destino1.coordY - origen.coordY)
                costo1 = ((furgoneta.bicis_cogidas + 9) // 10) * distancia1
                costo_kilometros += costo1

            if furgoneta.est2 != None:
                destino2 = self.estaciones[furgoneta.est2]
                bicis_dejadas_est2 = furgoneta.bicis_cogidas - furgoneta.bicis_dejadas_est1
                distancia2 = abs(destino2.coordX - destino1.coordX) + abs(destino2.coordY - destino1.coordY)
                costo2 = ((bicis_dejadas_est2 + 9) // 10) * distancia2
                costo_kilometros += costo2
        return costo_kilometros/1000

    
    def calculo_coste_diferencias(self):
        total = 0
        assert len(self.diferencias) == len(self.diferencias_inicial)

        for i in range(len(self.diferencias)):
            if self.diferencias_inicial[i] >= 0:
                if self.diferencias[i] <= 0:
                    total += (self.diferencias[i])
            else:
                if self.diferencias[i] >= 0:
                    total += (abs(self.diferencias_inicial[i]))
                else:
                    total += (abs(self.diferencias_inicial[i])-abs(self.diferencias[i]))
            
        return total



def generar_estado_inicial1(params: Parametros) -> Estado:
        
    rng: random.Random = random.Random(params.semilla)  #usar semilla para el rng
    furgos_usadas = 0

    for i in range(len(params.estaciones)):
        
        if furgos_usadas < len(params.furgonetas):
            diferencia = params.estaciones[i].num_bicicletas_next - params.estaciones[i].demanda

            if diferencia > 0:
                excedente = min(diferencia, params.estaciones[i].num_bicicletas_no_usadas, 30)
                
                # asignamos furgoneta de recogida en la primera estacion con diferencia negativa que encontramos
                furgo = params.furgonetas[furgos_usadas]
                furgo.est_inicial = i
                furgo.bicis_cogidas = excedente
                furgos_usadas += 1

                # asignamos estación destino 1 de la furgoneta aleatoriamente
                id_est1 = furgo.est_inicial
                while id_est1 == furgo.est_inicial:   # comprobamos que no coincida con la inicial
                    id_est1 = rng.randint(0, len(params.estaciones)-1)
                furgo.est1 = id_est1

                # decidimos aleatoriamente si la furgoneta tendrá 1 o 2 estaciones destino
                cuantas_estaciones = rng.randint(1, 2)

                if cuantas_estaciones == 1:
                    furgo.bicis_dejadas_est1 = furgo.bicis_cogidas

                else:
                    # decidimos aleatoriamente cuantas bicicletas se dejan en la estacion destino 1
                    num_bicis_est1 = rng.randint(0, furgo.bicis_cogidas-1)
                    furgo.bicis_dejadas_est1 = num_bicis_est1
                    
                    # asignamos estación destino 2 de la furgoneta aleatoriamente
                    id_est2 = id_est1
                    while id_est2 == id_est1 or id_est2 == furgo.est_inicial: # comprobamos que no coincida la inicial o la 1
                        id_est2 = rng.randint(0, len(params.estaciones)-1)
                    furgo.est2 = id_est2 

    return Estado(params.furgonetas, params.estaciones)



def generar_estado_inicial2(params: Parametros) -> Estado:

    est_y_ex_ordenadas = []   # lista de tuplas (id_estacion, excedente o demanda estacion)
    recuento_exc_demanda =[]  # lista del excedente o demanda de cada estación, la iremos modificando
    
    for i in range(len(params.estaciones)):
        diferencia = params.estaciones[i].num_bicicletas_next - params.estaciones[i].demanda
        excedente_o_demanda = min(diferencia, params.estaciones[i].num_bicicletas_no_usadas)
        est_y_ex_ordenadas.append((i,excedente_o_demanda))
        recuento_exc_demanda.append(excedente_o_demanda)
    
    est_y_ex_ordenadas.sort(key=lambda x: x[1])  # ordenación de la lista de tuplas de menor a mayor demanda o excedente


    for furgo in params.furgonetas:
        id_furgo = furgo.id_furgo

        # asignamos estación de salida de las furgonetas
        id_est_inicial = est_y_ex_ordenadas[len(params.estaciones) - 1 - furgo.id_furgo][0]
        params.furgonetas[id_furgo].est_inicial = id_est_inicial
        
        bicis_cogidas = min(recuento_exc_demanda[id_est_inicial], 30)

        params.furgonetas[id_furgo].bicis_cogidas = bicis_cogidas
        recuento_exc_demanda[id_est_inicial] -= bicis_cogidas
        
        # asignamos estación una destino aleatoria a las furgonetas
        id_est = 0
        while bicis_cogidas > 0:
            if recuento_exc_demanda[id_est] < 0:
                params.furgonetas[id_furgo].est1 = id_est
                params.furgonetas[id_furgo].bicis_dejadas_est1 = bicis_cogidas
                recuento_exc_demanda[id_est] += bicis_cogidas
                bicis_cogidas = 0
            id_est += 1
            
    return Estado(params.furgonetas, params.estaciones)



def generar_estado_inicial3(params: Parametros) -> Estado:

    est_y_ex_ordenadas = []   # lista de tuplas (id_estacion, excedente o demanda estacion)
    recuento_exc_demanda =[]  # lista del excedente o demanda de cada estación, la iremos modificando
    
    for i in range(len(params.estaciones)):
        diferencia = params.estaciones[i].num_bicicletas_next - params.estaciones[i].demanda
        excedente_o_demanda = min(diferencia, params.estaciones[i].num_bicicletas_no_usadas)
        est_y_ex_ordenadas.append((i,excedente_o_demanda))
        recuento_exc_demanda.append(excedente_o_demanda)
    
    est_y_ex_ordenadas.sort(key=lambda x: x[1])  # ordenación de la lista de tuplas de menor a mayor demanda o excedente


    for furgo in params.furgonetas:
        id_furgo = furgo.id_furgo

        # asignamos estación de salida de las furgonetas
        id_est_inicial = est_y_ex_ordenadas[len(params.estaciones) - 1 - furgo.id_furgo][0]
        params.furgonetas[id_furgo].est_inicial = id_est_inicial
        
        bicis_cogidas = min(recuento_exc_demanda[id_est_inicial], 30)

        params.furgonetas[id_furgo].bicis_cogidas = bicis_cogidas
        recuento_exc_demanda[id_est_inicial] -= bicis_cogidas
        
        # asignamos estación 1 de las furgonetas
        id_est1 = est_y_ex_ordenadas[furgo.id_furgo][0]
        params.furgonetas[id_furgo].est1 = id_est1
        
        falten_est1 = abs(recuento_exc_demanda[id_est1])
        if falten_est1 > furgo.bicis_cogidas:
            falten_est1 = furgo.bicis_cogidas

        params.furgonetas[id_furgo].bicis_dejadas_est1 = falten_est1
        recuento_exc_demanda[id_est1] += furgo.bicis_dejadas_est1

        # asignamos estación 2 de las furgonetas
        if furgo.bicis_cogidas > falten_est1:
            id_est2 = est_y_ex_ordenadas[furgo.id_furgo + 1][0]
            bicis_est2 = bicis_cogidas - falten_est1

            params.furgonetas[id_furgo].est2 = id_est2
            recuento_exc_demanda[id_est2] += bicis_est2


    return Estado(params.furgonetas, params.estaciones)