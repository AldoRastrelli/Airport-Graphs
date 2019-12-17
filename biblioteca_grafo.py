from grafo import Grafo
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
