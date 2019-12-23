import csv
import random
import sys
from caminos_minimos import *
from biblioteca_grafo import *
from heapq import *
from grafo import Grafo
from aeropuerto import Aeropuerto
MAX_ITER_PR = 10
D = 0.85
SEP_CAMINO = ' -> '

"""""""""""""""""""""""""""
    Funciones auxiliares
"""""""""""""""""""""""""""


def centralidad(grafo):
    """Calcula la centralidad de los vértices de un grafo de manera exacta y
    devuelve un diccionario con los valores. Recibe un grafo por parámetro.
    Precondiciones: el grafo no debe ser vacío. """
    cent = {}
    vertices_grafo = grafo.obtener_vertices()
    for v in vertices_grafo:
        cent[v] = 0  # O(v)
    for v in vertices_grafo:
        padre, distancia = dijkstra(grafo, v, funcion=lambda x: 1/x)
        cent_aux = {}
        for w in vertices_grafo:
            cent_aux[w] = 0

        vertices_ordenados = ordenar_vertices(distancia)
        for dist_w, w in vertices_ordenados:
            if padre[w] is None:
                continue
            cent_aux[padre[w]] += 1 + cent_aux[w]

        for w in vertices_grafo:
            if w == v:
                continue
            cent[w] += cent_aux[w]
    return cent


def ordenar_vertices(diccionario):
    """ Recibe un diccionario de tuplas en el formato (vertice, número real).
    Invierte el sentido de la tupla (número real, vertice) y los appendea en una lista.
    Se devuelve la lista en forma de heap de mínimos. """
    lista = []
    for tupla in diccionario.items():
        if tupla[1] == float('inf'):
            continue
        tupla_invertida = (-tupla[1], tupla[0])
        lista.append(tupla_invertida)
    heapify(lista)
    return lista


def imprimir_heap(heap, n=None):
    """ Imprime n cantidad de elementos de un heap en orden de menor
    a mayor. Se recibe el heap por parámetro.
    N es opcional. De no pasarse, se imprime todo el heap. """
    if n == None:
        n = len(heap)
    sep = ', '
    for i in range(n):
        if i == n-1:
            sep = '\n'
        print(heappop(heap)[1], end=sep)


def recorrido_dfs_grado(grafo):
    """ Recorrido dfs para calcular centralidad aproximada d
    un grafo (grados de vértices).
    Precondiciones: el grafo no debe estar vacío. """
    visitados = set()
    centralidad = {}

    for v in grafo.obtener_vertices():
        if v not in visitados:
            dfs_grados(grafo, v, visitados, centralidad)

    return centralidad


def dfs_grados(grafo, v, visitados, centralidad):
    """ Función recursiva de recorrido_dfs_grado."""
    visitados.add(v)
    centralidad[v] = grafo.obtener_grado(v)

    for w in grafo.obtener_adyacentes(v):
        if w not in visitados:
            dfs_grados(grafo, w, visitados, centralidad)


def pasar_dic_a_lista(diccionario):
    """ convierte un diccionario recibido por parámetro
    en un lista de tuplas del formato (valor,clave) """
    lista = []
    for clave in diccionario:
        valor = diccionario[clave]
        lista.append((valor, clave))

    return lista


def imprimir_lista(lista, n=None):
    """ Recibe una lista y, opcionalmente, un número n
    de elementos a imprimir de la lista, desde la posición 0.
    De no recibirse n, se imprime toda al lista. """
    if n == None or n > len(lista):
        n = len(lista)
    sep = ', '
    for i in range(n):
        if i == n-1:
            sep = '\n'
        print(lista[i][1], end=sep)


def generar_orden_aleatorio_vertices(grafo):
    """ Genera un orden aleatorio de vértices del grafo.
    Devuelve una lista. """
    vertices = grafo.obtener_vertices()
    random.shuffle(vertices)
    return vertices


def _pagerank(grafo, vertices_aleatorios, cant_vertices, iteraciones, pr_dic):
    """ Función recursiva del cálculo de centralidad por medio de PageRank.
    Recibe un grafo, una lista de vertices_aleatorios del grafo que contiene todos
    los vértices ordenados de manera aleatoria sin obligación de relación de adyacencias,
    la cantidad de vértices que tiene el grafo, la cantidad de iteraciones que desean realizarse
    y un diccionario del pagerank de los vertices. """
    if iteraciones >= MAX_ITER_PR:
        return pr_dic

    pr_aux = {}
    for v in vertices_aleatorios:
        sumatoria = 0
        for w in grafo.obtener_adyacentes(v):
            sumatoria += pr_dic[w] / len(grafo.obtener_adyacentes(w))

        pr_aux[v] = (1 - D) / cant_vertices + D * sumatoria

    for v in vertices_aleatorios:
        pr_dic[v] = pr_aux[v]

    return _pagerank(grafo, vertices_aleatorios, cant_vertices, iteraciones + 1, pr_dic)


def _n_lugares(grafo, aerop_ciudad_origen, origen, n, hijo, visitados, no_sirven, actual):
    """ Función auxiliar de n_lugares.
    Recibe un grafo, un vértice origen pertenenciente al grafo, un número n de máximo de vértices
    a recorrer, un diccionario de hijos, un set de visitados y un vértice actual"""

    if actual in visitados:
        return False
    #print("no sirven: ",no_sirven)
    # Si mi lista de visitados tiene n-1 elementos, analizo el elemento actual
    # que aún no fue guardado a ver si me sirve. Si no, returneo False y elijo otro
    if len(visitados) == n-1:

        adyacentes_act = grafo.obtener_adyacentes(actual)
        if origen in adyacentes_act and actual not in visitados:
            visitados.add(actual)
            hijo[actual] = None
            return True
        else:
            if actual not in no_sirven:
                no_sirven[actual] = set()
            no_sirven[actual].add(len(visitados))
            #print("no sirven: ",no_sirven)
            return False

    visitados.add(actual)
    for w in grafo.obtener_adyacentes(actual):
        if w in visitados or len(grafo.obtener_adyacentes(w)) == 1:
            continue
        if w in no_sirven:
            if len(visitados) in no_sirven[w]:
                continue
        hijo[actual] = w
        if _n_lugares(grafo, aerop_ciudad_origen, origen, n, hijo, visitados, no_sirven, w):
            return True

    visitados.remove(actual)
    hijo.pop(actual, None)
    if actual not in no_sirven:
        no_sirven[actual] = set()
    no_sirven[actual].add(len(visitados))
    #print("no sirven: ",no_sirven)
    return False


def generar_camino_circular(hijo, origen):
    """ A partir de un diccionario de hijos que marca un camino entre vértices
    y un vértice de origen, genera el camino total y lo guarda en una lista
    que luego devuelve.
    Postcond: la lista será circular: el primer y el último elemento serán el mismo. """
    camino = []
    actual = origen
    while actual != None:
        camino.append(actual)
        actual = hijo[actual]
    camino.append(origen)
    return camino


def ejecutar_comando(operacion, parametros, grafo_tiempo, grafo_precio, grafo_vuelos, grafo_vuelos_dirigidos, aeropuertos_por_ciudad):
    camino = []

    if operacion == "camino_mas":
        modo = parametros[0]
        if modo == "rapido":
            camino = camino_minimo(
                grafo_tiempo, aeropuertos_por_ciudad, parametros[1], parametros[2])

        elif modo == "barato":
            camino = camino_minimo(
                grafo_precio, aeropuertos_por_ciudad, parametros[1], parametros[2])
        imprimir_camino(camino, SEP_CAMINO)

    elif operacion == "camino_escalas":
        camino = camino_minimo(
            grafo_vuelos, aeropuertos_por_ciudad, parametros[0], parametros[1], False)
        imprimir_camino(camino, SEP_CAMINO)

    elif operacion == "centralidad":
        betweeness_centrality(grafo_vuelos, int(float(parametros[0])))

    elif operacion == "centralidad_aprox":
        betweeness_centrality_aproximada(
            grafo_vuelos, int(float(parametros[0])))

    elif operacion == "pagerank":
        pagerank(grafo_vuelos_dirigidos, int(float(parametros[0])))

    elif operacion == "nueva_aerolinea":
        camino = nueva_aerolinea(
            parametros[0], grafo_precio, grafo_tiempo, grafo_vuelos)
        print("OK")

    elif operacion == "vacaciones":
        camino = n_lugares(grafo_vuelos, aeropuertos_por_ciudad,
                           parametros[0], int(float(parametros[1])))
        if len(camino) > 0:
            imprimir_camino(camino, SEP_CAMINO)

    elif operacion == "itinerario":
        camino = itinerario_cultural(
            parametros[0], grafo_tiempo, aeropuertos_por_ciudad)

    elif operacion == "exportar_kml":
        exportar_kml(parametros[0], parametros[1], parametros[2])
        print("OK")
    return camino


def formatear_comando(comando):
    '''Dado el comando recibido por parámetro, una cadena sin salto de línea,
    devuelve una tupla con la operación a realizar,
    y una lista con los parámetros que debe recibir dicha operación.
    Lanza una excepción en caso de que el comando sea inválido.
    '''
    comandos = comando.split(',')
    long = len(comandos)
    operacion = comandos[0]
    parametros = []

    if long == 3:
        if operacion in {"camino_mas rapido", "camino_mas barato"}:
            operacion, modo = operacion.split()
            return operacion, [modo, comandos[1], comandos[2]]

    elif long == 2:
        segundo_parametro = comandos[1]
        comandos = operacion.split()
        operacion = comandos[0]
        primer_parametro = " ".join(comandos[1:])

        return operacion, [primer_parametro, segundo_parametro]

    elif long == 1:
        comandos = comandos[0].split()
        operacion = comandos[0]

        if operacion in {"itinerario", "exportar_kml", "centralidad", "centralidad_aprox", "pagerank", "nueva_aerolinea"}:
            return operacion, [comandos[1]]

    raise Exception


def procesar_archivos(archivo_aeropuertos, archivo_vuelos, dic_aeropuertos, aeropuertos_por_ciudad):
    '''Recibe un archivo con información sobre aeropuertos y otro sobre vuelos,
    ambos en formato csv y dos diccionarios de aeropuertos.
    Guarda información sobre los aeropuertos en los diccionarios recibidos,
    y devuelve además tres grafos donde cada vértice es un aeropuerto y
    las aristas los vuelos entre ellos, con el peso correspondiente.
    '''
    with open(archivo_aeropuertos) as aeropuertos:
        aeropuertos = csv.reader(aeropuertos)
        grafo_tiempo = Grafo()
        grafo_precio = Grafo()
        grafo_vuelos = Grafo()
        grafo_vuelos_dirigidos = Grafo()

        for ciudad, codigo_aeropuerto, latitud, longitud in aeropuertos:
            if ciudad in aeropuertos_por_ciudad:
                aeropuertos_por_ciudad[ciudad].add(codigo_aeropuerto)
            else:
                aeropuertos_por_ciudad[ciudad] = {codigo_aeropuerto}

            aeropuerto = Aeropuerto(
                codigo_aeropuerto, ciudad, float(latitud), float(longitud))
            dic_aeropuertos[codigo_aeropuerto] = aeropuerto
            grafo_tiempo.agregar_vertice(aeropuerto)
            grafo_precio.agregar_vertice(aeropuerto)
            grafo_vuelos.agregar_vertice(aeropuerto)
            grafo_vuelos_dirigidos.agregar_vertice(aeropuerto)

    with open(archivo_vuelos) as vuelos:
        vuelos = csv.reader(vuelos)

        for origen, destino, tiempo, precio, cant_vuelos in vuelos:
            grafo_tiempo.agregar_arista(origen, destino, int(float(tiempo)))
            grafo_precio.agregar_arista(origen, destino, int(float(precio)))
            grafo_vuelos.agregar_arista(
                origen, destino, int(float(cant_vuelos)))
            grafo_vuelos_dirigidos.agregar_arista(
                origen, destino, int(float(cant_vuelos)))

    return grafo_tiempo, grafo_precio, grafo_vuelos, grafo_vuelos_dirigidos


def imprimir_camino(camino, separador=" "):
    '''Imprime por salida estandar los elementos de camino, con el separador de por medio.'''
    for i in range(len(camino)-1):
        print(camino[i], end=separador)
    if camino:
        print(camino[-1])


def camino_minimo(grafo, aeropuertos, origen, destino, pesado=True):
    '''Dado un grafo, una ciudad de origen y otra de destino
    calcula y devuelve en forma de lista el camino mínimo entre esas ciudades.
    Si el grafo es pesado, utiliza el algoritmo de Dijkstra.
    Sino, utiliza un recorrido bfs.
    '''

    distancia_min = float('inf')
    camino_min = []

    for ae_origen in aeropuertos[origen]:
        for ae_destino in aeropuertos[destino]:
            if pesado:
                padres, orden = dijkstra(grafo, ae_origen, destino=ae_destino)
            else:
                padres, orden = bfs(grafo, ae_origen, ae_destino)

            camino, distancia = construir_camino(padres, orden, ae_destino)
            if distancia < distancia_min:
                distancia_min = distancia
                camino_min = camino

    return camino_min


"""""""""""""""""""""""""""
    Comandos pedidos
"""""""""""""""""""""""""""


def listar_operaciones(operaciones):
    """ Recibe una lista de operaciones disponibles y las
    imprime una por renglón """
    for operacion in operaciones:
        print(f"{operacion}")


def betweeness_centrality(grafo, n):
    """ Calcula la centralidad exacta de los vértices del grafo e
    imprime los n más importantes de orden mayor a menor.
    Precond: el grafo no debe estar vacío, n debe ser un número entero."""
    centr = centralidad(grafo)        # O(V*ElogV)
    heap = ordenar_vertices(centr)    # O(V)
    imprimir_heap(heap, n)         # O(V)


def betweeness_centrality_aproximada(grafo, n):             # O(V+E) total
    """ Calcula la Centralidad aproximada de los vértices del grafo e
    imprime los n más importantes de orden mayor a menor.
    Precond: el grafo no debe estar vacío, n debe ser un número entero."""
    dic_centralidad = recorrido_dfs_grado(grafo)            # O(V+E)
    lista_centralidad = pasar_dic_a_lista(dic_centralidad)  # O(V)
    lista_centralidad.sort(reverse=True)                  # O(V)
    imprimir_lista(lista_centralidad, n)                   # O(V)


def pagerank(grafo, n):
    """ Calcula la centralidad por medio de PageRank e imprime los n
    más importantes de orden mayor a menor.
    Recibe un grafo y un número n de vértices del grafo a imprimir con
    la mayor centralidad. """
    vertices_aleatorios = generar_orden_aleatorio_vertices(grafo)
    pr_dic = {}

    iteraciones = 0
    cant_vertices = len(vertices_aleatorios)
    for v in vertices_aleatorios:
        pr_dic[v] = 0

    dic_pagerank = _pagerank(grafo, vertices_aleatorios,
                             cant_vertices, iteraciones, pr_dic)
    lista_pagerank = pasar_dic_a_lista(dic_pagerank)
    lista_pagerank.sort(reverse=True)
    imprimir_lista(lista_pagerank, n)


def n_lugares(grafo, aeropuertos, origen, n):
    """ Encuentra un camino circular de n vértices dentro de un grafo comenzando desde
    el origen pasado por parámetro.
    Recibe un grafo, diccionario de sus aeropuertos, un origen, un número n de máximo de vértices
    a recorrer"""
    if n == 1:
        return [origen]

    if n < 3:
        print("No se encontro recorrido")
        return []

    if origen not in aeropuertos:
        print("No se encontro recorrido")
        return []

    # Considero que a mayor cant de adyacentes, más probable es encontrar un camino y que tarde menos.
    # Entonces se ordena por cantidad de adyacentes y se le da prioridad a los que tiene más.
    lista_aerop = [(len(grafo.obtener_adyacentes(aerop)),aerop) for aerop in aeropuertos[origen] ]    
    lista_aerop.sort(reverse = True)
    
    for grado_aerop, aeropuerto_origen in lista_aerop:
        no_sirven = {}
        hijo = {}
        visitados = set()
        if _n_lugares(grafo, aeropuertos[origen], aeropuerto_origen, n, hijo, visitados, no_sirven, aeropuerto_origen):
            return generar_camino_circular(hijo, aeropuerto_origen)

    print("No se encontro recorrido")
    return []


def itinerario_cultural(archivo_itinerario, grafo_aeropuertos, aeropuertos):
    '''Recibe un archivo existente con formato csv,
    donde la primera linea incluye las ciudades que se desea visitar,
    y las subsiguientes lineas indican qué ciudades deben ser visitadas antes de qué otras.
    Imprime por salida estandar el orden en que deben ser visitadas y el recorrido que se debe realizar,
    para que la cantidad de escalas sea mínima.
    '''
    with open(archivo_itinerario) as itinerario:
        itinerario = csv.reader(itinerario)

        ciudades = next(itinerario)
        grafo_ciudades = Grafo(True, ciudades)

        for ciudad_a, ciudad_b in itinerario:
            grafo_ciudades.agregar_arista(ciudad_a, ciudad_b)

    orden = orden_topologico_dfs(grafo_ciudades)
    imprimir_camino(orden, ', ')
    camino_total = []

    for i in range(len(orden)-1):
        origen, destino = orden[i], orden[i+1]
        camino_min = camino_minimo(
            grafo_aeropuertos, aeropuertos, origen, destino, True)
        camino_total.extend(camino_min)
        if i != len(orden)-2:
            camino_total.pop()
        imprimir_camino(camino_min, SEP_CAMINO)
    return camino_total


def exportar_kml(archivo, camino, aeropuertos):
    '''Recibe un recorrido de aeropuertos, en forma de lista o tupla,
    y genera a partir de este un archivo con formato kml con el nombre recibido por parámetro.'''
    inicio = '''<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>KML TP3</name>'''
    fin = '''
    <Document>\n</kml>'''

    with open(archivo, 'w') as kml:
        kml.write(inicio)

        for aeropuerto in camino:
            aeropuerto = aeropuertos[aeropuerto]

            lugar = f'''
        <Placemark>
            <name>{aeropuerto}</name>
            <Point>
                <coordinates>{aeropuerto.get_longitud()}, {aeropuerto.get_latitud()}</coordinates>
            </Point>
        </Placemark>
        '''
            kml.write(lugar)

        for i in range(len(camino)-1):
            origen = aeropuertos[camino[i]]
            destino = aeropuertos[camino[i+1]]
            recorrido = f'''
        <Placemark>
            <LineString>
                <coordinates>{origen.get_longitud()}, {origen.get_latitud()} {destino.get_longitud()}, {destino.get_latitud()}</coordinates>
            </LineString>
        </Placemark>
        '''
            kml.write(recorrido)

        kml.write(fin)


def nueva_aerolinea(archivo, grafo_precio, grafo_tiempo, grafo_vuelos):
    '''Dado los grafos recibidos por parámetro, genera un archivo con formato csv
    con las rutas aéreas a seguir para que el costo total en dinero sea mínimo.'''

    mst = prim(grafo_precio)

    visitados = set()
    camino = []

    with open(archivo, 'w') as ruta:
        ruta = csv.writer(ruta)

        for origen in mst:
            camino.append(origen)
            for destino in mst.obtener_adyacentes(origen):
                if (origen, destino) in visitados or (destino, origen) in visitados:
                    continue
                tiempo = grafo_tiempo.obtener_peso(origen, destino)
                precio = grafo_precio.obtener_peso(origen, destino)
                vuelos = grafo_vuelos.obtener_peso(origen, destino)
                visitados.add((origen, destino))
                camino.append(destino)
                ruta.writerow([origen, destino, tiempo, precio, vuelos])
    return camino
