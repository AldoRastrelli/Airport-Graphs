from caminos_minimos import dijkstra
from grafo import *
from heapq import *

"""""""""""""""""""""""""""
    Comandos pedidos
"""""""""""""""""""""""""""

def listar_operaciones(operaciones):

    for operacion in operaciones:
        print(f"{operacion}\n")

def betweeness_centrality(grafo, n):

    centralidad = centralidad(grafo)
    heap = ordenar_vertices(centralidad)
    imprimir_heap(heap,n)

def betweeness_centrality_aproximada(grafo, n):             # O(V+E) total

    dic_centralidad = recorrido_dfs_grado(grafo)            # O(V+E)
    lista_centralidad = pasar_dic_a_lista(dic_centralidad)  # O(V)
    lista_centralidad.sort(reverse = True)                  # O(V)
    imprimir_lista(lista_centralidad)                   # O(V)


"""""""""""""""""""""""""""
    Funciones auxiliares
"""""""""""""""""""""""""""

def centralidad(grafo):
    cent = {}
    vertices_grafo = grafo.obtener_vertices()
    for v in vertices_grafo: cent[v] = 0     """O(v)"""
    for v in vertices_grafo:
        distancia, padre = dijkstra(grafo, v)  # Son diccionarios
        cent_aux = {}
        for w in vertices_grafo: cent_aux[w] = 0

        vertices_ordenados = ordenar_vertices(distancia) 
        for dist_w, w in vertices_ordenados:
            cent_aux[padre[w]] += 1 + cent_aux[w]

        for w in vertices_grafo:
            if w == v: continue
            cent[w] += cent_aux[w]
    return cent

def ordenar_vertices(diccionario):
    lista = []
    for tupla in diccionario.items():
        if tupla[1] == float('inf'): continue
        tupla_invertida = (tupla[1],tupla[0])
        lista.append(tupla_invertida)
    
    heapify(lista)
    return lista

def imprimir_heap(heap,n=None):

    if n == None:   n = len(heap)
    sep = ', '
    for i in range(n):
        if i == n-1:
            sep = '\n'
        print(heappop(lista)[1],end = sep)

def recorrido_dfs_grado(grafo):

    visitados = set()
    centralidad = {}

    for v in grafo.obtener_vertices():
        if v not in visitados:
            dfs_grados(grafo, v, visitados, centralidad)
    
    return centralidad

def dfs_grados(grafo, v, visitados, centralidad):
    visitados.add(v)
    centralidad[v] = grafo.obtener_grado(v)

    for w in grafo.obtener_adyacentes(v):
        if w not in visitados:
            dfs_grados(grafo,w,visitados,orden,padre)

def pasar_dic_a_lista(diccionario):

    lista = []
    for clave,valor in diccionario:
        lista.append((valor,clave))
    
    return lista

def imprimir_lista(lista,n=None):
    if n == None:   n = len(lista)
    sep = ', '
    for i in range(n):
        if i == n-1:
            sep = '\n'
        print(lista[i],end = sep)
