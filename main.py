from clase_problem import BicingProblem
from clase_estado import generar_estado_inicial1, generar_estado_inicial2, generar_estado_inicial3
from aima.search import hill_climbing, simulated_annealing, exp_schedule
from clase_parametros import Parametros
from abia_bicing import Estaciones
import time
import matplotlib.pyplot as plt

def preguntar_heuristico():
    heur = input("\n 1. Maximización de las ganancias obtenidas por los traslados de bicicletas \
                \n 2. Punto 1 y además minimización de los costes de transporte de las bicicletas \
                \n Selecciona el heurístico deseado (indicando el número 1 o 2): ")
    while (int(heur) != 1) and (int(heur) != 2):
        heur = input("\n 1. Maximización de las ganancias obtenidas por los traslados de bicicletas \
                    \n 2. Punto 1 y además minimización de los costes de transporte de las bicicletas \
                    \n El heurístico debe ser 1 o 2. Selecciona el heurístico deseado: ")
    return(int(heur))

def preguntar_algoritmo():
    alg = input("\n 1. Hill Climbing \n 2. Simulated Annealing \n Selecciona el algorismo deseado (indicando el número 1 o 2): ")
    while (int(alg) != 1) and (int(alg) != 2):
        alg = input("\n 1. Hill Climbing \n 2. Simulated Annealing \n El algorismo debe ser 1 o 2. Selecciona el algorismo deseado: ")
    return(int(alg))

def preguntar_k():
    k = input("\n Selecciona el valor del parámetro k (recomendado 5): ")
    while int(k) < 0:
        k = input("\n El valor de k debe ser mayor que 0. Selecciona el valor de k (recomendado 5): ")
    return(int(k))

def preguntar_lambda():
    lamda = input("\n Selecciona el valor del parámetro lambda (recomendado 0.01): ")
    while float(lamda) < 0 or  float(lamda) > 1:
        lamda = input("\n El valor de lambda debe estar entre 0 y 1. Selecciona el valor de lambda (recomendado 0.01): ")
    return(float(lamda))

def preguntar_num_estacion():
    est = input("\n Selecciona el número de estaciones (recomendado 25): ")
    while int(est)%5 != 0:
        est = input("\n El número de estaciones debe ser divisible entre 5. Selecciona el número de estaciones (recomendado 25): ")
    return(int(est))

def preguntar_num_furgoneta():
    furgo = input("\n Selecciona el número de furgonetas (recomendado 5): ")
    while int(furgo) <= 0:
        furgo = input("\n El número de furgonetas debe ser mayor que 0. Selecciona el número de furgonetas (recomendado 5): ")
    return(int(furgo))

def preguntar_funcion_inicial():
    init = input(" \n Selecciona la función deseada para generar el estado inicial (indicando el número 1, 2 o 3): ")
    while (int(init) != 1) and (int(init) != 2) and (int(init) != 3):
        init = input(" \n La función debe ser la 1, la 2 o la 3. Selecciona la función deseada: ")
    return(int(init))

def preguntar_numero_esperimentos():
    exp = input("\n Cuántos experimentos deseas realizar? (responde con un número del 1 al 10): ")
    while int(exp) not in range(1,11):
        exp = input("\n Debes responder con un número del 1 al 10. Cuántos experimentos deseas realizar?: ")
    return(int(exp))

def preguntar_numero_repeticiones():
    rep = input("\n Cuántas repeticiones del experimento deseas realizar? (responde con un número del 1 al 10): ")
    while int(rep) not in range(1,11):
        rep = input("\n Debes responder con un número del 1 al 10. Cuántas repeticiones del experimento deseas realizar?: ")
    return(int(rep))

experiment = input("\n Que experimento quieres hacer? ")

if int(experiment) == 1:
    num_est = 25
    num_bicis = int(num_est*50)
    num_furgos = int(num_est/5)
    init = preguntar_funcion_inicial()
    exp = 10
    rep = 5
    heur = 1 
    alg = 1 #Hill Climbing

elif int(experiment) == 2:
    num_est = 25
    num_bicis = int(num_est*50)
    num_furgos = int(num_est/5)
    init = preguntar_funcion_inicial()
    exp = 10
    rep = 5
    heur = 1 
    alg = 1 #Hill Climbing

elif int(experiment) == 3:
    num_est = 25
    num_bicis = int(num_est*50)
    num_furgos = int(num_est/5)
    init = 2
    exp = 1
    rep = 5
    heur = 1 
    alg = 2 #Simulated Annealing
    lamda = preguntar_lambda()
    k = preguntar_k()

elif int(experiment) == 4:
    num_est = preguntar_num_estacion()
    num_bicis = int(num_est*50)
    num_furgos = int(num_est/5)
    init = 2
    exp = 1
    rep = 10
    heur = 1 
    alg = 1 #Hill Climbing

elif int(experiment) == 5:
    num_est = 25
    num_bicis = int(num_est*50)
    num_furgos = int(num_est/5)
    init = 2
    exp = 10
    rep = 5
    heur = preguntar_heuristico()
    alg = preguntar_algoritmo()
    lamda = 0.01
    k = 5

elif int(experiment) == (6):
    num_est = 25
    num_bicis = int(num_est*50)
    num_furgos = preguntar_num_furgoneta()
    init = 2
    exp = 10
    rep = 1
    heur = 1
    alg = 1 #Hill Climbing

elif int(experiment) == (7):
    num_est = 25
    num_bicis = int(num_est*50)
    num_furgos = int(num_est/5)
    init = 2
    exp = 1
    rep = 10
    heur = 1
    alg = 1 #Hill Climbing

else:
    num_est = preguntar_num_estacion()
    num_bicis = int(num_est*50)
    num_furgos = int(num_est/5)
    lamda = 0.01
    k = 5
    init = preguntar_funcion_inicial()
    heur = preguntar_heuristico()
    alg = preguntar_algoritmo()
    exp = preguntar_numero_esperimentos()
    rep = preguntar_numero_repeticiones()

semillas = [42,30,17,24,29,33,9,57,61,76]

tiempo_experimentos = []
estado_final_experimentos = []

for i in range(0,int(exp)):
    tiempo_experimentos.append([])
    estado_final_experimentos.append([])

    for _ in range(0,int(rep)): 

        estaciones = Estaciones(num_est, num_bicis, semillas[i])
        params = Parametros(estaciones, num_furgos, 12)


        if int(init) == 1:
            initial_state = generar_estado_inicial1(params)
        elif int(init) == 2:
            initial_state = generar_estado_inicial2(params)
        elif int(init) == 3:
            initial_state = generar_estado_inicial3(params)
        print("\n ESTAT INICIAL", initial_state)

        problemhillclimbing_h1 = BicingProblem(initial_state, True, True)
        problemsimulatedannealing_h1 = BicingProblem(initial_state, False, True)
        problemhillclimbing_h2 = BicingProblem(initial_state, True, False)
        problemsimulatedannealing_h2 = BicingProblem(initial_state, False, False)

        

        tiempo_inicio = time.time()

        if int(alg) == 1:
            if int(heur) == 1:
                n = hill_climbing(problemhillclimbing_h1)
            elif int(heur) == 2:
                n = hill_climbing(problemhillclimbing_h2)
        
        elif int(alg) == 2:
            if int(heur) == 1:
                n = simulated_annealing(problemsimulatedannealing_h1, schedule=exp_schedule(k,lamda, limit=10000))
            elif int(heur) == 2:
                n = simulated_annealing(problemsimulatedannealing_h2, schedule=exp_schedule(k,lamda, limit=10000))

        tiempo_fin = time.time()
        tiempo_total = tiempo_fin - tiempo_inicio
        tiempo_en_ms = round(tiempo_total * 1000,3)
        #print(f"El programa ha tardado {tiempo_en_ms} ms en ejecutarse.")
        #print(n)
        tiempo_experimentos[i].append(tiempo_en_ms)
        estado_final_experimentos[i].append(n)


print("\n\n\nTIEMPO EXPERIMENTOS:")
sum_experimentos = 0
for i in range(len(tiempo_experimentos)):
    sum_réplicas = 0
    for j in range(len(tiempo_experimentos[i])):
        sum_réplicas += int(tiempo_experimentos[i][j])
        #print("\n  Experimento", i, "Réplica", j, ":", tiempo_experimentos[i][j], "ms")
    if len(tiempo_experimentos[i]) > 1:
        print("\n  Tiempo medio de las réplicas del experimento",  i, ":", sum_réplicas/len(tiempo_experimentos[i]), "ms")
    elif len(tiempo_experimentos[i]) == 1:
        print("\n  Tiempo medio de las réplicas del experimento",  i, ":", sum_réplicas/len(tiempo_experimentos[i]), "ms")
    sum_experimentos += int(tiempo_experimentos[i][0])
#if len(tiempo_experimentos) > 1:
    #print("\n  Tiempo medio de los experimentos:", sum_experimentos/len(tiempo_experimentos), "ms")

print("\n\n\nESTADOS FINALES:")
for i in range(len(estado_final_experimentos)):
    sum_réplicas1 = 0
    for j in range(len(estado_final_experimentos[i])):
        #sum_réplicas1 += int(estado_final_experimentos[i][j])
        print("\n  Experimento", i, "Réplica", j, ":", estado_final_experimentos[i][j])
    #if len(estado_final_experimentos[i]) > 1:
        #print("\n  Ganancias medias experimento",  i, ":", sum_réplicas1/len(estado_final_experimentos[i]), "ms")





# FUNCIONES DE VISUALIZACIÓN GRÁFICA DEL ESPACIO DEL PROBLEMA


def dibujar_estado_actual():

    furgonetas,estaciones = n.getstate()
    fig, ax = plt.subplots(figsize=(10, 10))

    # Dibuja la cuadrícula de la ciudad
    for x in range(0, 10100, 100):
        ax.axvline(x, color='grey', linestyle='--', linewidth=0.3)
        ax.axhline(x, color='grey', linestyle='--', linewidth=0.3)

    # Lista para mantener un registro de las estaciones que ya han sido dibujadas
    estaciones_dibujadas = []

    colors = ['red','orange','blue','green','purple']
    # Dibuja los recorridos de las furgonetas
    for i in range(len(furgonetas)):
        furgo = furgonetas[i]
        if furgo.est_inicial != None:
            # Dibuja una cruz negra en la estación furgo.est_inicial
            ax.scatter(estaciones[furgo.est_inicial].coordX, estaciones[furgo.est_inicial].coordY, color='black', s=100, marker='x')

            if furgo.est2 == None:
                x_vals = [estaciones[furgo.est_inicial].coordX, estaciones[furgo.est1].coordX]
                y_vals = [estaciones[furgo.est_inicial].coordY, estaciones[furgo.est1].coordY]
                ax.plot(x_vals, y_vals, color=colors[i])
            else:
                x_vals = [estaciones[furgo.est_inicial].coordX, estaciones[furgo.est1].coordX, estaciones[furgo.est2].coordX]
                y_vals = [estaciones[furgo.est_inicial].coordY, estaciones[furgo.est1].coordY, estaciones[furgo.est2].coordY]
                ax.plot(x_vals, y_vals, color=colors[i])

            # Dibuja las estaciones furgo.est1 y furgo.est2 con el mismo color que el trazado de la furgoneta
            if furgo.est1 not in estaciones_dibujadas:
                ax.scatter(estaciones[furgo.est1].coordX, estaciones[furgo.est1].coordY, color=colors[i], s=40)
                estaciones_dibujadas.append(furgo.est1)
            if furgo.est2 != None and furgo.est2 not in estaciones_dibujadas:
                ax.scatter(estaciones[furgo.est2].coordX, estaciones[furgo.est2].coordY, color=colors[i], s=40)
                estaciones_dibujadas.append(furgo.est2)

    # Dibuja las estaciones restantes en negro
    for i in range(len(estaciones)):
        if i not in estaciones_dibujadas:
            ax.scatter(estaciones[i].coordX, estaciones[i].coordY, color='black', s=30)

    ax.set_xlim(0, 10100)
    ax.set_ylim(0, 10100)
    plt.show()



def dibujar_ciudad():

    diferencias = [est.num_bicicletas_next - est.demanda for est in params.estaciones]
    estaciones = params.estaciones
    fig, ax = plt.subplots(figsize=(10, 10))

    # Dibuja la cuadrícula de la ciudad
    for x in range(0, 10100, 100):
        ax.axvline(x, color='grey', linestyle='--', linewidth=0.3)
        ax.axhline(x, color='grey', linestyle='--', linewidth=0.3)

    # Coordenadas de las estaciones (sustituya esto por sus propias coordenadas)
    coordX = [estacion.coordX for estacion in estaciones]
    coordY = [estacion.coordY for estacion in estaciones]

    # Dibuja las estaciones con colores basados en sus diferencias
    sc = ax.scatter(coordX, coordY, c=diferencias, cmap='plasma', s=35)

    # Añade una barra de colores
    cbar = plt.colorbar(sc)
    cbar.set_label('Diferencias')

    ax.set_xlim(0, 10100)
    ax.set_ylim(0, 10100)
    plt.show()
 

# Visualización del estado final
dibujar_estado_actual()

# Para visualizar el escenario inicial del problema se debe llamar a la función dibujar_ciudad()
# dibujar_ciudad()
