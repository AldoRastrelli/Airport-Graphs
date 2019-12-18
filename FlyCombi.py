import sys
import csv
from biblioteca import *

OPERACIONES = {"camino_mas", "camino_escalas", "centralidad_aprox", "pagerank", "centralidad",
               "nueva_aerolinea", "recorrer_mundo", "recorrer_mundo_aprox", "vacaciones", "itinerario", "exportar_kml"}


def main():
    aeropuertos = sys.argv[1]
    vuelos = sys.argv[2]

    caminos_minimos = {"escalas": "cmescalas.json",
                       "precio": "cmprecio.json", "tiempo": "cmtiempo.json"}

    aeropuertos_por_ciudad = {}
    grafo_aeropuertos = Grafo()

    procesar_archivos(aeropuertos, vuelos, grafo_aeropuertos, aeropuertos_por_ciudad)

    for comando in sys.stdin:
        comando = comando.rstrip('\n')

        if comando == "listar_operaciones":
            listar_operaciones(OPERACIONES)
        else:
            try:
                operacion, parametros = formatear_comando(comando)
                ejecutar_comando(operacion, parametros, caminos_minimos)
            except:
                print("comando erróneo")


main()
