from aeropuerto import Aeropuerto
from caminos_minimos import *
from biblioteca_grafo import *
import csv
import json
from grafo import *
from heapq import *

"""""""""""""""""""""""""""
    Comandos pedidos
"""""""""""""""""""""""""""

def listar_operaciones(operaciones):

    for operacion in operaciones:
        print(f"{operacion}\n")

def betweeness_centrality(grafo, n):

    centralidad = centralidad(grafo)        # O(V*ElogV)
    heap = ordenar_vertices(centralidad)    # O(V)
    imprimir_heap(heap,n)                   # O(V)

def betweeness_centrality_aproximada(grafo, n):             # O(V+E) total

    dic_centralidad = recorrido_dfs_grado(grafo)            # O(V+E)
    lista_centralidad = pasar_dic_a_lista(dic_centralidad)  # O(V)
    lista_centralidad.sort(reverse = True)                  # O(V)
    imprimir_lista(lista_centralidad)                   # O(V)


def itinerario_cultural(archivo_itinerario, aeropuertos, caminos_minimos):
    with open(archivo_itinerario) as itinerario:
        itinerario = csv.reader(itinerario)

        ciudades = next(itinerario)
        grafo_ciudades = Grafo(True, ciudades)

        for ciudad_a, ciudad_b in itinerario:
            grafo_ciudades.agregar_arista(ciudad_a, ciudad_b)

    orden = orden_topologico(grafo_ciudades)
    imprimir_camino(orden, ', ')

    for i in range(len(orden)-1):
        origen, destino = orden[i], orden[i+1]
        camino_min = camino_minimo(
            grafo_ciudades, aeropuertos, caminos_minimos, origen, destino, False)
        imprimir_camino(camino_min, ' -> ')


def exportar_kml(archivo, camino):
    inicio = '''<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>KML TP3</name>'''
    fin = '''
    <Document>\n</kml>'''

    with open(archivo, 'w') as kml:
        kml.write(inicio)

        for aeropuerto in camino:
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
            origen = camino[i]
            destino = camino[i+1]
            recorrido = f'''
        <Placemark>
            <LineString>
                <coordinates>{origen.get_longitud()}, {origen.get_latitud()} {destino.get_longitud()}, {destino.get_latitud()}</coordinates>
            </LineString>
        </Placemark>
        '''
            kml.write(recorrido)

        kml.write(fin)
    print("OK")


def nueva_aerolinea(archivo, grafo):
    mst = prim(grafo, True)

    with open(archivo, 'w') as ruta:
        ruta = csv.writer(ruta)

        for origen in mst:
            for destino in mst.obtener_adyacentes(origen):
                peso = mst.obtener_peso(origen, destino)
                ruta.writerow([origen, destino, peso])

    print("OK")



"""""""""""""""""""""""""""
    Funciones auxiliares
"""""""""""""""""""""""""""

def centralidad(grafo):
    cent = {}
    vertices_grafo = grafo.obtener_vertices()
    for v in vertices_grafo: cent[v] = 0     """O(v)"""
    for v in vertices_grafo:
        distancia, padre = dijkstra(grafo, v)  # Son diccionarios
        cent_aux = {}
        for w in vertices_grafo: cent_aux[w] = 0

        vertices_ordenados = ordenar_vertices(distancia) 
        for dist_w, w in vertices_ordenados:
            cent_aux[padre[w]] += 1 + cent_aux[w]

        for w in vertices_grafo:
            if w == v: continue
            cent[w] += cent_aux[w]
    return cent

def ordenar_vertices(diccionario):
    lista = []
    for tupla in diccionario.items():
        if tupla[1] == float('inf'): continue
        tupla_invertida = (tupla[1],tupla[0])
        lista.append(tupla_invertida)
    
    heapify(lista)
    return lista

def imprimir_heap(heap,n=None):

    if n == None:   n = len(heap)
    sep = ', '
    for i in range(n):
        if i == n-1:
            sep = '\n'
        print(heappop(lista)[1],end = sep)

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
            dfs_grados(grafo,w,visitados,orden,padre)

def pasar_dic_a_lista(diccionario):

    lista = []
    for clave,valor in diccionario:
        lista.append((valor,clave))
    
    return lista

def imprimir_lista(lista,n=None):
    if n == None:   n = len(lista)
    sep = ', '
    for i in range(n):
        if i == n-1:
            sep = '\n'
        print(lista[i],end = sep)


def ejecutar_comando(operacion, parametros, caminos_minimos):
    pass


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

        if operacion in {"itinerario", "exportar_kml", "centralidad", "centralidad_aprox", "nueva_aerolinea"}:
            return operacion, [comandos[1]]

        elif operacion in {"recorrer_mundo", "recorrer_mundo_aprox"}:
            ciudad = " ".join(comandos[1:])
            return operacion, [ciudad]

    raise Exception


def procesar_archivos(archivo_aeropuertos, archivo_vuelos, grafo_aeropuertos, ciudades):
    with open(archivo_aeropuertos) as aeropuertos:
        aeropuertos = csv.reader(aeropuertos)

        for ciudad, codigo_aeropuerto, latitud, longitud in aeropuertos:
            if ciudad in ciudades:
                ciudades[ciudad].add(codigo_aeropuerto)
            else:
                ciudades[ciudad] = {codigo_aeropuerto}
            aeropuerto = Aeropuerto(
                codigo_aeropuerto, ciudad, float(latitud), float(longitud))
            grafo_aeropuertos.agregar_vertice(aeropuerto)

    with open(archivo_vuelos) as vuelos:
        vuelos = csv.reader(vuelos)

        for origen, destino, tiempo, precio, cant_vuelos in vuelos:
            peso = float(tiempo), float(precio), float(cant_vuelos)
            grafo_aeropuertos.agregar_arista(origen, destino, peso)


def imprimir_camino(camino, separador):
    print(separador.join(camino))


def listar_operaciones(operaciones):
    for op in operaciones:
        print(op)


# camino_mas camino_escalas
def camino_minimo(grafo, aeropuertos, caminos, origen, destino, pesado):
    distancia_min = float('inf')
    camino_min = []
    algoritmo = dijkstra if pesado else bfs
    caminos_calculados = {}

    with open(caminos) as caminos:
        caminos_calculados = json.load(caminos)

    if origen in caminos_calculados and destino in caminos_calculados[origen]:
        return caminos_calculados[origen][destino]

    for origen in aeropuertos[origen]:
        for destino in aeropuertos[destino]:
            padres, orden = algoritmo(grafo, origen, destino)
            camino, distancia = construir_camino(padres, orden)

            if distancia < distancia_min:
                distancia_min = distancia
                camino_min = camino

    caminos_calculados[origen] = caminos_calculados.get(origen, {})
    caminos_calculados[origen][destino] = camino_min

    with open(caminos, 'w') as caminos:
        json.dump(caminos_calculados, caminos)

    return camino_min

