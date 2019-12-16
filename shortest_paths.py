from queue import Queue
from heapq import *


def bfs(graph, origin, destination1, destination2):
    """
        Devuelve una tupla de la forma (camino1, camino2) donde camino1 y camino2 son listas de tuplas que
        representan una sucesion de vertices entre destination1 y origin y entre destination2 y origin repectivamente
        en caso de que no exista un camino la lista sera vacia
    """
    to_visit = Queue()
    visited = {}
    parents = {}
    to_visit.put(origin)
    parents[origin] = None
    visited[origin] = True

    while not to_visit.empty() and not (destination1 in visited and destination2 in visited):
        actual = to_visit.get()
        for adjacent in graph.get_adjacents(actual):
            if adjacent not in visited:
                to_visit.put(adjacent)
                parents[adjacent] = actual
                visited[adjacent] = True

    return build_path(parents, destination1), build_path(parents, destination2)


def build_path(parents, destination):
    if destination not in parents:
        return []  # El vertice esta en otra componente, el grafo no es conexo
    actual = destination
    path = [destination]

    while parents[actual] is not None:
        actual = parents[actual]
        path.append(actual)

    return path  # Incluye vertice de origen y de destino


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
