import sys
import csv
from biblioteca import *

OPERACIONES = {"camino_mas", "camino_escalas", "centralidad_aprox", "pagerank", "centralidad",
               "nueva_aerolinea", "recorrer_mundo", "recorrer_mundo_aprox", "vacaciones", "itinerario", "exportar_kml"}


def main():
    archivo_aeropuertos = sys.argv[1]
    archivo_vuelos = sys.argv[2]

    caminos_minimos = {"escalas": "cmescalas.json",
                       "precio": "cmprecio.json", "tiempo": "cmtiempo.json"}

    generar_archivos_cm(caminos_minimos) #comentar para pruebas mas rapidas

    aeropuertos = {}
    aeropuertos_por_ciudad = {}
    grafo_aeropuertos = Grafo()

    procesar_archivos(archivo_aeropuertos, archivo_vuelos,
                      grafo_aeropuertos, aeropuertos, aeropuertos_por_ciudad)

    camino_anterior = []

    for comando in sys.stdin:
        comando = comando.rstrip('\n')

        if comando == "listar_operaciones":
            listar_operaciones(OPERACIONES)
        else:
            try:
                operacion, parametros = formatear_comando(comando)

                if operacion not in OPERACIONES:
                    raise Exception

                if operacion == "exportar_kml":
                    parametros.extend([camino_anterior,aeropuertos])

                camino_anterior = ejecutar_comando(
                    operacion, parametros, grafo_aeropuertos, aeropuertos_por_ciudad, caminos_minimos)

            except Exception as e:
                print(f"comando erróneo: '{comando}'")
                raise(e)


main()
