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
