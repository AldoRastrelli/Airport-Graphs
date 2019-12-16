import sys
import csv
from biblioteca import *

OPERACIONES = {"camino_mas", "camino_escalas", "centralidad_aprox", "pagerank", "centralidad",
               "nueva_aerolinea", "recorrer_mundo", "recorrer_mundo_aprox", "vacaciones", "itinerario", "exportar_kml"}


def main():
    aeropuertos = sys.argv[1]
    vuelos = sys.argv[2]

    grafo_tiempos, grafo_precios, grafo_frecuencias = generar_grafos(
        aeropuertos, vuelos)

    for comando in sys.stdin:

        comando = comando.rstrip('\n')

        if comando == "listar_operaciones":
            listar_operaciones(OPERACIONES)

        elif comando not in OPERACIONES:
            print("comando inválido")


main()
