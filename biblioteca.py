import csv
import json
import random
from caminos_minimos import *
from biblioteca_grafo import *
from heapq import *
from grafo import Grafo
from aeropuerto import Aeropuerto
MAX_ITER_PR = 100
D = 0.85
SEP_CAMINO = ' -> '

"""""""""""""""""""""""""""
    Comandos pedidos
"""""""""""""""""""""""""""


def listar_operaciones(operaciones):
    for operacion in operaciones:
        print(f"{operacion}")


def betweeness_centrality(grafo, n):
    centralidad = centralidad(grafo)        # O(V*ElogV)
    heap = ordenar_vertices(centralidad)    # O(V)
    imprimir_heap(heap, n)                   # O(V)


def betweeness_centrality_aproximada(grafo, n):             # O(V+E) total
    dic_centralidad = recorrido_dfs_grado(grafo)            # O(V+E)
    lista_centralidad = pasar_dic_a_lista(dic_centralidad)  # O(V)
    lista_centralidad.sort(reverse=True)                  # O(V)
    imprimir_lista(lista_centralidad)                   # O(V)


def pagerank(grafo):
    vertices_aleatorios = generar_orden_aleatorio(grafo)
    pr_dic = {}

    for v in vertices_aleatorios:
        pr_dic[v] = 0
    iteraciones = 0
    cant_vertices = len(vertices_aleatorios)

    return _pagerank(grafo, vertices_aleatorios, cant_vertices, iteraciones, pr_dic)


def n_lugares(grafo,origen,n):
    if n < 3 and n != 1:
        print("No se encontro recorrido")
        return
    if n == 1:
        print(origen)
        return
    
    hijo = {}
    visitados = set()

    visitados.add(origen)
    if not _n_lugares(grafo, origen, n, hijo, visitados, origen):
        print("No se encontro recorrido")
        return
    camino = generar_camino_circular(hijo,origen)
    return imprimir_camino(camino,SEP_CAMINO)


def itinerario_cultural(archivo_itinerario, grafo_aeropuertos, aeropuertos, caminos_minimos):
    with open(archivo_itinerario) as itinerario:
        itinerario = csv.reader(itinerario)

        ciudades = next(itinerario)
        grafo_ciudades = Grafo(True, ciudades)

        for ciudad_a, ciudad_b in itinerario:
            grafo_ciudades.agregar_arista(ciudad_a, ciudad_b)

    orden = orden_topologico(grafo_ciudades)
    imprimir_camino(orden, ', ')
    camino_total = []

    for i in range(len(orden)-1):
        origen, destino = orden[i], orden[i+1]
        camino_min = camino_minimo(
            grafo_aeropuertos, aeropuertos, caminos_minimos, origen, destino)

        imprimir_camino(camino_min, 'SEP_CAMINO')
    return camino_total


def exportar_kml(archivo, camino, aeropuertos):
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


def nueva_aerolinea(archivo, grafo):
    mst = prim(grafo, True)
    camino_total = []

    with open(archivo, 'w') as ruta:
        ruta = csv.writer(ruta)

        for origen in mst:
            for destino in mst.obtener_adyacentes(origen):
                tiempo, precio, frecuencia = mst.obtener_peso(origen, destino)
                ruta.writerow([origen, destino, tiempo, precio, frecuencia])

    print("OK")


"""""""""""""""""""""""""""
    Funciones auxiliares
"""""""""""""""""""""""""""


def centralidad(grafo):
    cent = {}
    vertices_grafo = grafo.obtener_vertices()
    for v in vertices_grafo:
        cent[v] = 0  # O(v)
    for v in vertices_grafo:
        distancia, padre = dijkstra(grafo, v)  # Son diccionarios
        cent_aux = {}
        for w in vertices_grafo:
            cent_aux[w] = 0

        vertices_ordenados = ordenar_vertices(distancia)
        for dist_w, w in vertices_ordenados:
            cent_aux[padre[w]] += 1 + cent_aux[w]

        for w in vertices_grafo:
            if w == v:
                continue
            cent[w] += cent_aux[w]
    return cent


def ordenar_vertices(diccionario):
    lista = []
    for tupla in diccionario.items():
        if tupla[1] == float('inf'):
            continue
        tupla_invertida = (tupla[1], tupla[0])
        lista.append(tupla_invertida)

    heapify(lista)
    return lista


def imprimir_heap(heap, n=None):

    if n == None:
        n = len(heap)
    sep = ', '
    for i in range(n):
        if i == n-1:
            sep = '\n'
        print(heappop(lista)[1], end=sep)


def recorrido_dfs_grado(grafo):

    visitados = set()
    centralidad = {}

    for v in grafo.obtener_vertices():
        if v not in visitados:
            dfs_grados(grafo, v, visitados, centralidad)

    return centralidad


def dfs_grados(grafo, v, visitados, centralidad):
    visitados.add(v)
    centralidad[v] = grafo.obtener_grado(v)

    for w in grafo.obtener_adyacentes(v):
        if w not in visitados:
            dfs_grados(grafo, w, visitados, orden, padre)


def pasar_dic_a_lista(diccionario):

    lista = []
    for clave, valor in diccionario:
        lista.append((valor, clave))

    return lista


def imprimir_lista(lista, n=None):
    if n == None:
        n = len(lista)
    sep = ', '
    for i in range(n):
        if i == n-1:
            sep = '\n'
        print(lista[i], end=sep)


def generar_orden_aleatorio(grafo):

    vertices = grafo.obtener_vertices()
    random.shuffle(vertices)
    return vertices


def _pagerank(grafo, vertices_aleatorios, cant_vertices, iteraciones, pr_dic):

    if iteraciones >= MAX_ITER_PR:
        return pr_dic

    pr_aux = {}
    for v in vertices_aleatorios:
        sumatoria = 0
        for w in grafo.obtener_adyacentes(v):
            sumatoria += pr_dic[w] / grafo.obtener_grado(w)

        pr_aux[v] = (1 - D) / cant_vertices + D * sumatoria

    for v in vertices_aleatorios:
        pr_dic[v] = pr_aux[v]

    return _pagerank(grafo, vertices_aleatorios, cant_vertices, iteraciones + 1, pr_dic)


def _n_lugares(grafo, origen, n, hijo, visitados, actual):
    if len(visitados) == n:
        return (origen in grafo.obtener_adyacentes(actual))
    
    for w in grafo.obtener_adyacentes(actual):
        visitados.add(w)
        hijo[actual] = w
        if _n_lugares(grafo, origen, n, hijo, visitados, w):
            hijo[w] = None
            return True
        visitados.remove(w)
    return false


def generar_camino_circular(hijo,origen):
    camino = []
    actual = origen
    while actual != None:
        camino.append(actual)
        actual = hijo[actual]
    camino.append(origen)
    return camino

def ejecutar_comando(operacion, parametros, grafo, aeropuertos, caminos):
    camino = []

    if operacion == "camino_mas":
        modo = parametros[0]
        if modo == "rapido":
            camino = camino_minimo(
                grafo, aeropuertos, caminos["tiempo"], parametros[1], parametros[2], 0)  # 0 == tiempo

        elif modo == "barato":
            camino = camino_minimo(
                grafo, aeropuertos, caminos["precio"], parametros[1], parametros[2], 1)  # 1 == precio
        imprimir_camino(camino, "SEP_CAMINO")

    elif operacion == "camino_escalas":
        camino = camino_minimo(
            grafo, aeropuertos, caminos["escalas"], parametros[0], parametros[1])
        imprimir_camino(camino, "SEP_CAMINO")

    elif operacion == "centralidad":
        betweeness_centrality(grafo, parametros[0])

    elif operacion == "centralidad_aprox":
        betweeness_centrality_aproximada(grafo, parametros[0])

    elif operacion == "pagerank":
        pagerank(grafo)

    elif operacion == "nueva_aerolinea":
        camino = nueva_aerolinea(parametros[0], grafo)

    elif operacion == "recorrer_mundo":
        return camino

    elif operacion == "recorrer_mundo_aprox":
        return camino

    elif operacion == "vacaciones":
        return camino

    elif operacion == "itinerario":
        camino = itinerario_cultural(
            parametros[0], grafo, aeropuertos, caminos["escalas"])
        print("OK")

    elif operacion == "exportar_kml":
        exportar_kml(parametros[0], parametros[1], parametros[2])
        print("OK")

    return camino


def formatear_comando(comando):
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

        elif operacion in {"recorrer_mundo", "recorrer_mundo_aprox"}:
            ciudad = " ".join(comandos[1:])
            return operacion, [ciudad]

    raise Exception


def procesar_archivos(archivo_aeropuertos, archivo_vuelos, grafo_aeropuertos, dic_aeropuertos, aeropuertos_por_ciudad):
    with open(archivo_aeropuertos) as aeropuertos:
        aeropuertos = csv.reader(aeropuertos)

        for ciudad, codigo_aeropuerto, latitud, longitud in aeropuertos:
            if ciudad in aeropuertos_por_ciudad:
                aeropuertos_por_ciudad[ciudad].add(codigo_aeropuerto)
            else:
                aeropuertos_por_ciudad[ciudad] = {codigo_aeropuerto}

            aeropuerto = Aeropuerto(
                codigo_aeropuerto, ciudad, float(latitud), float(longitud))
            grafo_aeropuertos.agregar_vertice(aeropuerto)
            dic_aeropuertos[codigo_aeropuerto] = aeropuerto

    with open(archivo_vuelos) as vuelos:
        vuelos = csv.reader(vuelos)

        for origen, destino, tiempo, precio, cant_vuelos in vuelos:
            peso = float(tiempo), float(precio), float(cant_vuelos)
            grafo_aeropuertos.agregar_arista(origen, destino, peso)


def generar_archivos_cm(caminos_minimos):
    for camino in caminos_minimos:
        with open(caminos_minimos[camino], 'w') as archivo:
            archivo.write("{}")


def imprimir_camino(camino, separador = " "):
    for i in range(len(camino)-1):
        print(camino[i], end=separador)
    if camino:
        print(camino[-1])


# camino_mas camino_escalas
def camino_minimo(grafo, aeropuertos, archivo_caminos, origen, destino, peso=None):
    distancia_min = float('inf')
    camino_min = []
    caminos_calculados = {}

    with open(archivo_caminos) as caminos:
        caminos_calculados = json.load(caminos)

    if origen in caminos_calculados and destino in caminos_calculados[origen]:
        return caminos_calculados[origen][destino]

    for ae_origen in aeropuertos[origen]:
        for ae_destino in aeropuertos[destino]:
            if peso is None:
                padres, orden = bfs(grafo, ae_origen, ae_destino)
            else:
                padres, orden = dijkstra(grafo, ae_origen, ae_destino, peso)

            camino, distancia = construir_camino(padres, orden, ae_destino)
            if distancia < distancia_min:
                distancia_min = distancia
                camino_min = camino

    caminos_calculados[origen] = caminos_calculados.get(origen, {})
    caminos_calculados[origen][destino] = camino_min

    with open(archivo_caminos, 'w') as caminos:
        json.dump(caminos_calculados, caminos)

    return camino_min
