from graph import *
from shortest_paths import *
import csv

def imprimir_camino(camino):
    for i in range(len(camino)-1):
        print(camino[i], end=' -> ')
    if camino: print(camino[-1])

def listar_operaciones(operaciones):
    for op in operaciones:
        print(op)

def camino_minimo(aeropuertos,origenes,destinos,pesado): #camino_mas camino_escalas
    distancia_min = float('inf')
    camino_min = []
    algoritmo = dijkstra if pesado else bfs

    for origen in origenes:
        for destino in destinos:
            camino_distancia = algoritmo(aeropuertos,origen,destino,None)[0]
            
            if pesado:
                camino, distancia = camino_distancia
            else:
                camino, distancia = camino_distancia, len(camino_distancia)-1

            if distancia < distancia_min:
                distancia_min = distancia
                camino_min = camino

    imprimir_camino(camino_min)