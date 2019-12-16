from queue import Queue
from heapq import heappush
from heapq import heappop
from grafo import obtener_adyacentes
from grafo import obtener_vertices
from grafo import obtener_peso
from grafo import Grafo


def bfs(grafo, origen):
    
    visitados = set()
    padre = {}
    orden = {}
    q = Queue()

    visitados.add(orden)
    padre[origen] = None
    orden[origen] = 0

    q.put(origen)

    
    while not q.empty():
        v = q.get()
        for w in grafo.obtener_adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                q.put(w)
                padre[w] = v
                orden[w] = orden[v] +1
    
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
    for w in grafo.obtener_adyacentes():
        if w not in visitados:
            padre[w] = v
            orden[w] = orden[v] +1
            dfs(grafo,w,visitados,orden,padre)

def dijkstra(grafo, origen):    # .Camino mínimo
    
    distancia = {}
    padre = {}
    for v in grafo.obtener_vertices():
        distancia[v] = float('inf')
    
    distancia[origen] = 0
    padre[origen] = None
    q = []
    heappush(q, (distancia[origen], origen))

    while len(q) > 0:
        v = heappop(q)
        for w in grafo.obtener_adyacentes(v):
            if distancia[v] + grafo.obtener_peso(v, w) < distancia[w]:
                distancia[w] = distancia[v] + grafo.obtener_peso(v, w)
                padre[w] = v
                heappush(q, (distancia[w], w))
    
    return padre, distancia
