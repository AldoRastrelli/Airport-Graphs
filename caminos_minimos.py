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

<<<<<<< HEAD
    visitados.add(orden)
    padre[origen] = None
    orden[origen] = 0
=======
    while not to_visit.empty() and not (destination1 in visited and destination2 in visited):
        actual = to_visit.get()
        for adjacent in graph.get_adjacents(actual):
            if adjacent not in visited:
                to_visit.put(adjacent)
                parents[adjacent] = actual
                visited[adjacent] = True
>>>>>>> 5de0d1166cfb2d1c7b6202190b497beeaab5e797

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

<<<<<<< HEAD
    while len(q) > 0:
        v = heappop(q)
        for w in grafo.obtener_adyacentes(v):
            if distancia[v] + grafo.obtener_peso(v, w) < distancia[w]:
                distancia[w] = distancia[v] + grafo.obtener_peso(v, w)
                padre[w] = v
                heappush(q, (distancia[w], w))
    
    return padre, distancia
=======
def dijkstra(graph, start, destination1, destination2):
    """ Recibe un vertice de origen y dos vertices de destino y devuelve una tupla de tuplas del estilo:
    ((camino_hasta_destino1, distancia1), (camino_hasta_destino2, distancia2))"""

    parents = {start: None}
    visited = {}
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    to_visit = []
    heappush(to_visit, (0, start))
    # Las tuplas se comparan por su primer elemento, entonces si guardo en el heap tuplas del estilo:
    # (distancia_hasta_el_vertice, vertice) como es de minimos mantendra al tope el vertice con distancia minima

    while len(to_visit) > 0 and not (destination1 in visited and destination2 in visited):
        actual = heappop(to_visit)
        if actual[1] in visited:
            continue
        visited[actual[1]] = True

        for adjacent in graph.get_adjacents(actual[1]):
            if (distances[actual[1]] + graph.get_weight(actual[1], adjacent)) < distances[adjacent]:
                distances[adjacent] = distances[actual[1]] + \
                    graph.get_weight(actual[1], adjacent)
                parents[adjacent] = actual[1]
            heappush(to_visit, (distances[adjacent], adjacent))

    return (build_path(parents, destination1), distances[destination1]), \
           (build_path(parents, destination2), distances[destination2])
>>>>>>> 5de0d1166cfb2d1c7b6202190b497beeaab5e797
