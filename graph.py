from collections import defaultdict


class Graph:
    def __init__(self, vertex_list=[]):
        self.vertex = defaultdict(dict)
        for v in vertex_list:
            self.add_vertex(v)

    def add_vertex(self, v):
        if v in self.vertex:
            print("El vertice ya ha sido agregado")
        else:
            self.vertex[v] = {}

    def add_edge(self, v1, v2, weight=0):
        self.vertex[v1][v2] = weight
        self.vertex[v2][v1] = weight

    def get_vertex(self):
        return list(self.vertex)

    def get_adjacents(self, v):
        if v not in self.vertex:
            print("El vertice no existe")
            return []
        else:
            return list(self.vertex[v])

    def get_weight(self, v1, v2):
        if (v1 not in self.vertex) or (v2 not in self.vertex):
            print("Al menos uno de los vertices no existe")
        else:
            return self.vertex[v1][v2]

    def __contains__(self, v):
        return v in self.vertex

    def __str__(self):
        return str(self.vertex)

    def __iter__(self):
        return iter(self.vertex)

    def __len__(self):
        return len(self.vertex)
