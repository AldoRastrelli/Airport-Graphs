from grafo import Grafo
from heapq import *
from queue import Queue
from pila import Pila


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


def _orden_topologico_dfs(grafo, v, pila, visitados):
    visitados.add(v)
    for w in grafo.obtener_adyacentes(v):
        if w not in visitados:
            _orden_topologico_dfs(grafo, w, pila, visitados)
    pila.apilar(v)


def orden_topologico_dfs(grafo):
    visitados = set()
    pila = Pila()
    for v in grafo:
        if v not in visitados:
            _orden_topologico_dfs(grafo, v, pila, visitados)
    return pila.convertir_a_lista()


def orden_topologico_bfs(grafo):
    grados = {}

    for v in grafo:
        grados[v] = 0

    for v in grafo:
        for w in grafo.obtener_adyacentes(v):
            grados[w] += 1

    q = Queue()

    for v in grafo:
        if grados[v] == 0:
            q.put(v)

    orden = []

    while not q.empty():
        v = q.get()

        orden.append(v)

        for w in grafo.obtener_adyacentes(v):
            grados[w] -= 1

            if grados[w] == 0:
                q.put(w)

    return orden if len(orden) == len(grafo) else None


def prim(grafo, dirigido=False):
    v = grafo.vertice_aleatorio()
    visitados = {v}
    q = []

    for w in grafo.obtener_adyacentes(v):
        peso = grafo.obtener_peso(v, w)
        heappush(q, (peso, v, w))

    arbol = Grafo(dirigido, grafo.obtener_vertices())

    while q:
        peso, v, w = heappop(q)
        if w in visitados:
            continue

        arbol.agregar_arista(v, w, peso)
        visitados.add(w)

        for x in grafo.obtener_adyacentes(w):
            if x not in visitados:
                peso = grafo.obtener_peso(w, x)
                heappush(q, (peso, w, x))
    return arbol
