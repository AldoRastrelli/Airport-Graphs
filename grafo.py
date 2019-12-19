from random import choice
from collections import defaultdict


class Grafo:
    def __init__(self, dirigido=False, lista_vertices=[]):
        self.vertices = defaultdict(dict)
        self.dirigido = dirigido
        for v in lista_vertices:
            self.agregar_vertice(v)

    def agregar_vertice(self, v):
        if v in self.vertices:
            return
        else:
            self.vertices[v] = {}

    def agregar_arista(self, v1, v2, peso=(0)):
        self.vertices[v1][v2] = peso
        if not self.dirigido:
            self.vertices[v2][v1] = peso

    def obtener_vertices(self):
        return list(self.vertices)

    def obtener_adyacentes(self, v):
        if v not in self.vertices:
            return []
        else:
            return list(self.vertices[v])

    def obtener_peso(self, v1, v2):
        if (v1 not in self.vertices) or (v2 not in self.vertices):
            return None
        if (v2 not in self.obtener_adyacentes(v1)):
            return None
        if (not self.dirigido) and (v1 not in self.obtener_adyacentes(v2)):
            return None
        else:
            return self.vertices[v1][v2]

    def vertice_aleatorio(self):
        return choice(self.obtener_vertices())

    def __contains__(self, v):
        return v in self.vertices

    def __str__(self):
        return str(self.vertices)

    def __iter__(self):
        return iter(self.vertices)

    def __len__(self):
        return len(self.vertices)
