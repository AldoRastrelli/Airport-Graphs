from grafo import Graph
from aeropuerto import Aeropuerto
from caminos_minimos import *
import csv


def ejecutar_comando(operacion, parametros):
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
            grafo_aeropuertos.add_vertex(aeropuerto)

    with open(archivo_vuelos) as vuelos:
        vuelos = csv.reader(vuelos)

        for origen, destino, tiempo, precio, cant_vuelos in vuelos:
            peso = float(tiempo), float(precio), float(cant_vuelos)
            grafo_aeropuertos.add_edge(origen, destino, peso)


def imprimir_camino(camino, separador):
    print(separador.join(camino))


def listar_operaciones(operaciones):
    for op in operaciones:
        print(op)


def camino_minimo(aeropuertos, origenes, destinos, pesado):  # camino_mas camino_escalas
    distancia_min = float('inf')
    camino_min = []
    algoritmo = dijkstra if pesado else bfs

    for origen in origenes:
        for destino in destinos:
            camino_distancia = algoritmo(
                aeropuertos, origen, destino, destino)[0]

            if pesado:
                camino, distancia = camino_distancia
            else:
                camino, distancia = camino_distancia, len(camino_distancia)-1

            if distancia < distancia_min:
                distancia_min = distancia
                camino_min = camino

    imprimir_camino(camino_min, " -> ")
