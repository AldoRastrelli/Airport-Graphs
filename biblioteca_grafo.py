from grafo import Grafo
from heapq import *
from queue import Queue


def orden_topologico(grafo):
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


def prim(grafo):
    v = grafo.vertice_aleatorio()
    visitados = {v}
    q = []

    for w in grafo.obtener_adyacentes(v):
        peso = grafo.obtener_peso(v, w)
        heappush(q, (peso, v, w))

    arbol = Grafo(grafo.obtener_vertices())

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
