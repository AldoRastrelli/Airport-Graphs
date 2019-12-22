#!/usr/bin/python3
import sys
import csv
from biblioteca import *

OPERACIONES = {"camino_mas", "camino_escalas", "centralidad_aprox", "pagerank",
               "centralidad", "nueva_aerolinea", "vacaciones", "itinerario", "exportar_kml"}


def main():
    archivo_aeropuertos = sys.argv[1]
    archivo_vuelos = sys.argv[2]

    aeropuertos = {}
    aeropuertos_por_ciudad = {}
    grafo_tiempo, grafo_precio, grafo_vuelos, grafo_vuelos_dirigidos = procesar_archivos(
        archivo_aeropuertos, archivo_vuelos, aeropuertos, aeropuertos_por_ciudad)

    camino_anterior = []

    for comando in sys.stdin:
        comando = comando.rstrip('\n')

        if comando == "listar_operaciones":
            listar_operaciones(OPERACIONES)
            continue
        try:
            operacion, parametros = formatear_comando(comando)

            if operacion not in OPERACIONES:
                raise Exception

            if operacion == "exportar_kml":
                parametros.extend([camino_anterior, aeropuertos])

            camino_anterior = ejecutar_comando(
                operacion, parametros, grafo_tiempo, grafo_precio, grafo_vuelos, grafo_vuelos_dirigidos, aeropuertos_por_ciudad)

        except Exception as e:
            print(f"comando erróneo: '{comando}'")
            raise e


main()
