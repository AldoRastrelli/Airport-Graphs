from queue import Queue
from heapq import heappush
from heapq import heappop
from grafo import Grafo


def construir_camino(padres, orden, destino):
    if destino not in padres:
        return []
    actual = destino
    camino = [destino]

    while padres[actual] is not None:
        actual = padres[actual]
        camino.append(actual)

    camino.reverse()
    return camino, orden[destino]


def bfs(grafo, origen, destino):
    visitados = set()
    padre = {}
    orden = {}
    q = Queue()

    visitados.add(origen)
    padre[origen] = None
    orden[origen] = 0

    q.put(origen)

    while not q.empty() and destino not in visitados:
        v = q.get()
        for w in grafo.obtener_adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                q.put(w)
                padre[w] = v
                orden[w] = orden[v] + 1
    return padre, orden


def recorrido_dfs(grafo):
    visitados = set()
    padre = {}
    orden = {}

    for v in grafo.obtener_vertices():
        if v not in visitados:
            orden[v] = 0
            padre[v] = None
            dfs(grafo, v, visitados, padre, orden)

    return padre, orden


def dfs(grafo, v, visitados, padre, orden):
    visitados.add(v)
    for w in grafo.obtener_adyacentes(v):
        if w not in visitados:
            padre[w] = v
            orden[w] = orden[v] + 1
            dfs(grafo, w, visitados, orden, padre)


def dijkstra(grafo, origen, destino, peso=0):    # .Camino mínimo
    distancia = {}
    padre = {}
    for v in grafo.obtener_vertices():
        distancia[v] = float('inf')

    distancia[origen] = 0
    padre[origen] = None
    q = []
    heappush(q, (distancia[origen], origen))

    while len(q) > 0:
        v = heappop(q)[1]
        if v == destino:
            break
        for w in grafo.obtener_adyacentes(v):
            if distancia[v] + grafo.obtener_peso(v, w)[peso] < distancia[w]:
                distancia[w] = distancia[v] + grafo.obtener_peso(v, w)[peso]
                padre[w] = v
                heappush(q, (distancia[w], w))

    return padre, distancia
