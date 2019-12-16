from graph import Graph
from aeropuerto import Aeropuerto
from shortest_paths import *
import csv


def generar_grafos(archivo_aeropuertos, archivo_vuelos):
    with open(archivo_aeropuertos) as aeropuertos:
        aeropuertos = csv.reader(aeropuertos)
        grafo_tiempos = Graph()
        grafo_precios = Graph()
        grafo_frecuencias = Graph()

        for ciudad, codigo_aeropuerto, latitud, longitud in aeropuertos:
            aeropuerto = Aeropuerto(
                codigo_aeropuerto, ciudad, latitud, longitud)
            grafo_tiempos.add_vertex(aeropuerto)
            grafo_precios.add_vertex(aeropuerto)
            grafo_frecuencias.add_vertex(aeropuerto)

    with open(archivo_vuelos) as vuelos:
        vuelos = csv.reader(vuelos)

        for origen, destino, tiempo, precio, cant_vuelos in vuelos:
            grafo_tiempos.add_edge(origen, destino, tiempo)
            grafo_precios.add_edge(origen, destino, precio)
            grafo_frecuencias.add_edge(origen, destino, cant_vuelos)

    return grafo_tiempos, grafo_precios, grafo_frecuencias


def imprimir_camino(camino):
    for i in range(len(camino)-1):
        print(camino[i], end=' -> ')
    if camino:
        print(camino[-1])


def listar_operaciones(operaciones):
    for op in operaciones:
        print(op)


def camino_minimo(aeropuertos, origenes, destinos, pesado):  # camino_mas camino_escalas
    distancia_min = float('inf')
    camino_min = []
    algoritmo = dijkstra if pesado else bfs

    for origen in origenes:
        for destino in destinos:
            camino_distancia = algoritmo(aeropuertos, origen, destino, None)[0]

            if pesado:
                camino, distancia = camino_distancia
            else:
                camino, distancia = camino_distancia, len(camino_distancia)-1

            if distancia < distancia_min:
                distancia_min = distancia
                camino_min = camino

    imprimir_camino(camino_min)
