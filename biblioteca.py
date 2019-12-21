import csv
import json
import random
from caminos_minimos import *
from biblioteca_grafo import *
from heapq import *
from grafo import Grafo
from aeropuerto import Aeropuerto
MAX_ITER_PR = 100
D = 0.85
SEP_CAMINO = ' -> '

"""""""""""""""""""""""""""
    Funciones auxiliares
"""""""""""""""""""""""""""


def centralidad(grafo):
    cent = {}
    vertices_grafo = grafo.obtener_vertices()
    for v in vertices_grafo:
        cent[v] = 0  # O(v)
    for v in vertices_grafo:
        padre, distancia = dijkstra(grafo, v)  # Son diccionarios
        cent_aux = {}
        for w in vertices_grafo:
            cent_aux[w] = 0

        vertices_ordenados = ordenar_vertices(distancia)
        for dist_w, w in vertices_ordenados:
            if padre[w] is None:
                continue
            cent_aux[padre[w]] += 1 + cent_aux[w]

        for w in vertices_grafo:
            if w == v:
                continue
            cent[w] += cent_aux[w]
    return cent


def ordenar_vertices(diccionario):
    lista = []
    for tupla in diccionario.items():
        if tupla[1] == float('inf'):
            continue
        tupla_invertida = (tupla[1], tupla[0])
        lista.append(tupla_invertida)
    heapify(lista)
    return lista


def imprimir_heap(heap, n=None):
    if n == None:
        n = len(heap)
    sep = ', '
    for i in range(n):
        if i == n-1:
            sep = '\n'
        print(heappop(heap)[1], end=sep)


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
            dfs_grados(grafo, w, visitados, centralidad)


def pasar_dic_a_lista(diccionario):
    lista = []
    for clave in diccionario:
        valor = diccionario[clave]
        lista.append((valor, clave))

    return lista


def imprimir_lista(lista, n=None):
    if n == None or n > len(lista):
        n = len(lista)
    sep = ', '
    for i in range(n):
        if i == n-1:
            sep = '\n'
        print(lista[i][1], end=sep)


def generar_orden_aleatorio(grafo):
    vertices = grafo.obtener_vertices()
    random.shuffle(vertices)
    return vertices


def _pagerank(grafo, vertices_aleatorios, cant_vertices, iteraciones, pr_dic):
    if iteraciones >= MAX_ITER_PR:
        return pr_dic

    pr_aux = {}
    for v in vertices_aleatorios:
        sumatoria = 0
        for w in grafo.obtener_adyacentes(v):
            sumatoria += pr_dic[w] / grafo.obtener_grado(w)

        pr_aux[v] = (1 - D) / cant_vertices + D * sumatoria

    for v in vertices_aleatorios:
        pr_dic[v] = pr_aux[v]

    return _pagerank(grafo, vertices_aleatorios, cant_vertices, iteraciones + 1, pr_dic)


def _n_lugares(grafo, origen, n, hijo, visitados, actual):
    if len(visitados) == n:
        return (origen in grafo.obtener_adyacentes(actual))

    # if w in visitados and w != origen: continue
    for w in grafo.obtener_adyacentes(actual):
        visitados.add(w)
        hijo[actual] = w
        if _n_lugares(grafo, origen, n, hijo, visitados, w):
            hijo[w] = None
            return True
        visitados.remove(w)
    return False


def generar_camino_circular(hijo, origen):
    camino = []
    actual = origen
    while actual != None:
        camino.append(actual)
        actual = hijo[actual]
    camino.append(origen)
    return camino


def ejecutar_comando(operacion, parametros, grafo_tiempo, grafo_precio, grafo_vuelos, aeropuertos, caminos):
    camino = []

    if operacion == "camino_mas":
        modo = parametros[0]
        if modo == "rapido":
            camino = camino_minimo(
                grafo_tiempo, aeropuertos, caminos["tiempo"], parametros[1], parametros[2])

        elif modo == "barato":
            camino = camino_minimo(
                grafo_precio, aeropuertos, caminos["precio"], parametros[1], parametros[2])
        imprimir_camino(camino, SEP_CAMINO)

    elif operacion == "camino_escalas":
        camino = camino_minimo(
            grafo_vuelos, aeropuertos, caminos["escalas"], parametros[0], parametros[1], False)
        imprimir_camino(camino, SEP_CAMINO)

    elif operacion == "centralidad":
        betweeness_centrality(grafo_vuelos, int(parametros[0]))

    elif operacion == "centralidad_aprox":
        betweeness_centrality_aproximada(grafo_vuelos, int(parametros[0]))

    elif operacion == "pagerank":
        pagerank(grafo_vuelos, int(parametros[0]))

    elif operacion == "nueva_aerolinea":
        camino = nueva_aerolinea(
            parametros[0], grafo_precio, grafo_tiempo, grafo_vuelos)  # modificar
        print("OK")

    elif operacion == "recorrer_mundo":
        return camino

    elif operacion == "recorrer_mundo_aprox":
        return camino

    elif operacion == "vacaciones":
        camino = n_lugares(grafo_vuelos, aeropuertos,
                           parametros[0], int(parametros[1]))
        imprimir_camino(camino, SEP_CAMINO)

    elif operacion == "itinerario":
        camino = itinerario_cultural(
            parametros[0], grafo_vuelos, aeropuertos, caminos["escalas"])
        print("OK")

    elif operacion == "exportar_kml":
        exportar_kml(parametros[0], parametros[1], parametros[2])
        print("OK")

    return camino


def formatear_comando(comando):
    comandos = comando.split(',')
    long = len(comandos)
    operacion = comandos[0]
    parametros = []

    if long == 3:
        if operacion in {"camino_mas rapido", "camino_mas barato"}:
            operacion, modo = operacion.split()
            return operacion, [modo, comandos[1], comandos[2]]

    elif long == 2:
        segundo_parametro = comandos[1]
        comandos = operacion.split()
        operacion = comandos[0]
        primer_parametro = " ".join(comandos[1:])

        return operacion, [primer_parametro, segundo_parametro]

    elif long == 1:
        comandos = comandos[0].split()
        operacion = comandos[0]

        if operacion in {"itinerario", "exportar_kml", "centralidad", "centralidad_aprox", "pagerank", "nueva_aerolinea"}:
            return operacion, [comandos[1]]

        elif operacion in {"recorrer_mundo", "recorrer_mundo_aprox"}:
            ciudad = " ".join(comandos[1:])
            return operacion, [ciudad]

    raise Exception


def procesar_archivos(archivo_aeropuertos, archivo_vuelos, dic_aeropuertos, aeropuertos_por_ciudad):
    with open(archivo_aeropuertos) as aeropuertos:
        aeropuertos = csv.reader(aeropuertos)
        grafo_tiempo = Grafo()
        grafo_precio = Grafo()
        grafo_vuelos = Grafo()

        for ciudad, codigo_aeropuerto, latitud, longitud in aeropuertos:
            if ciudad in aeropuertos_por_ciudad:
                aeropuertos_por_ciudad[ciudad].add(codigo_aeropuerto)
            else:
                aeropuertos_por_ciudad[ciudad] = {codigo_aeropuerto}

            aeropuerto = Aeropuerto(
                codigo_aeropuerto, ciudad, float(latitud), float(longitud))
            dic_aeropuertos[codigo_aeropuerto] = aeropuerto
            grafo_tiempo.agregar_vertice(aeropuerto)
            grafo_precio.agregar_vertice(aeropuerto)
            grafo_vuelos.agregar_vertice(aeropuerto)

    with open(archivo_vuelos) as vuelos:
        vuelos = csv.reader(vuelos)

        for origen, destino, tiempo, precio, cant_vuelos in vuelos:
            grafo_tiempo.agregar_arista(origen, destino, float(tiempo))
            grafo_precio.agregar_arista(origen, destino, float(precio))
            grafo_vuelos.agregar_arista(origen, destino, 1/float(cant_vuelos))

    return grafo_tiempo, grafo_precio, grafo_vuelos


def generar_archivos_cm(caminos_minimos):
    for camino in caminos_minimos:
        with open(caminos_minimos[camino], 'w') as archivo:
            archivo.write("{}")


def imprimir_camino(camino, separador=" "):
    for i in range(len(camino)-1):
        print(camino[i], end=separador)
    if camino:
        print(camino[-1])


def camino_minimo(grafo, aeropuertos, archivo_caminos, origen, destino, pesado=True):
    distancia_min = float('inf')
    camino_min = []

    with open(archivo_caminos) as caminos:
        try:
            caminos_calculados = json.load(caminos)
        except:
            caminos_calculados = {}

    if origen in caminos_calculados and destino in caminos_calculados[origen]:
        return caminos_calculados[origen][destino]

    for ae_origen in aeropuertos[origen]:
        for ae_destino in aeropuertos[destino]:
            if pesado:
                padres, orden = dijkstra(grafo, ae_origen, ae_destino)
            else:
                padres, orden = bfs(grafo, ae_origen, ae_destino)

            camino, distancia = construir_camino(padres, orden, ae_destino)
            if distancia < distancia_min:
                distancia_min = distancia
                camino_min = camino

    caminos_calculados[origen] = caminos_calculados.get(origen, {})
    caminos_calculados[origen][destino] = camino_min

    with open(archivo_caminos, 'w') as caminos:
        json.dump(caminos_calculados, caminos)

    return camino_min


"""""""""""""""""""""""""""
    Comandos pedidos
"""""""""""""""""""""""""""


def listar_operaciones(operaciones):
    for operacion in operaciones:
        print(f"{operacion}")


def betweeness_centrality(grafo, n):
    centr = centralidad(grafo)        # O(V*ElogV)
    heap = ordenar_vertices(centr)    # O(V)
    imprimir_heap(heap, n)         # O(V)


def betweeness_centrality_aproximada(grafo, n):             # O(V+E) total
    dic_centralidad = recorrido_dfs_grado(grafo)            # O(V+E)
    lista_centralidad = pasar_dic_a_lista(dic_centralidad)  # O(V)
    lista_centralidad.sort(reverse=True)                  # O(V)
    imprimir_lista(lista_centralidad, n)                   # O(V)


def pagerank(grafo, n):
    vertices_aleatorios = generar_orden_aleatorio(grafo)
    pr_dic = {}

    for v in vertices_aleatorios:
        pr_dic[v] = 0
    iteraciones = 0
    cant_vertices = len(vertices_aleatorios)

    dic_pagerank = _pagerank(grafo, vertices_aleatorios,
                             cant_vertices, iteraciones, pr_dic)
    lista_pagerank = pasar_dic_a_lista(dic_pagerank)
    lista_pagerank.sort(reverse=True)
    imprimir_lista(lista_pagerank, n)


def n_lugares(grafo, aeropuertos, origen, n):
    if n < 3 and n != 1:
        print("No se encontro recorrido")
        return []
    if n == 1:
        return [origen]

    for aeropuerto_origen in aeropuertos[origen]:
        hijo = {}
        visitados = set()
        visitados.add(aeropuerto_origen)
        if _n_lugares(grafo, aeropuerto_origen, n, hijo, visitados, aeropuerto_origen):
            print("hijo", hijo)
            return generar_camino_circular(hijo, aeropuerto_origen)

    print("No se encontro recorrido")
    return []


def itinerario_cultural(archivo_itinerario, grafo_aeropuertos, aeropuertos, caminos_minimos):
    with open(archivo_itinerario) as itinerario:
        itinerario = csv.reader(itinerario)

        ciudades = next(itinerario)
        grafo_ciudades = Grafo(True, ciudades)

        for ciudad_a, ciudad_b in itinerario:
            grafo_ciudades.agregar_arista(ciudad_a, ciudad_b)

    orden = orden_topologico_dfs(grafo_ciudades)
    imprimir_camino(orden, ', ')
    camino_total = []

    for i in range(len(orden)-1):
        origen, destino = orden[i], orden[i+1]
        camino_min = camino_minimo(
            grafo_aeropuertos, aeropuertos, caminos_minimos, origen, destino, False)

        imprimir_camino(camino_min, SEP_CAMINO)
    return camino_total


def exportar_kml(archivo, camino, aeropuertos):
    inicio = '''<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>KML TP3</name>'''
    fin = '''
    <Document>\n</kml>'''

    with open(archivo, 'w') as kml:
        kml.write(inicio)

        for aeropuerto in camino:
            aeropuerto = aeropuertos[aeropuerto]

            lugar = f'''
        <Placemark>
            <name>{aeropuerto}</name>
            <Point>
                <coordinates>{aeropuerto.get_longitud()}, {aeropuerto.get_latitud()}</coordinates>
            </Point>
        </Placemark>
        '''
            kml.write(lugar)

        for i in range(len(camino)-1):
            origen = aeropuertos[camino[i]]
            destino = aeropuertos[camino[i+1]]
            recorrido = f'''
        <Placemark>
            <LineString>
                <coordinates>{origen.get_longitud()}, {origen.get_latitud()} {destino.get_longitud()}, {destino.get_latitud()}</coordinates>
            </LineString>
        </Placemark>
        '''
            kml.write(recorrido)

        kml.write(fin)


def nueva_aerolinea(archivo, grafo_precio, grafo_tiempo, grafo_vuelos):
    mst = prim(grafo_precio)

    visitados = set()
    camino = []

    with open(archivo, 'w') as ruta:
        ruta = csv.writer(ruta)

        for origen in mst:
            camino.append(origen)
            for destino in mst.obtener_adyacentes(origen):
                if (origen, destino) in visitados or (destino, origen) in visitados:
                    continue
                tiempo = grafo_tiempo.obtener_peso(origen, destino)
                precio = grafo_precio.obtener_peso(origen, destino)
                vuelos = 1/grafo_vuelos.obtener_peso(origen, destino)
                visitados.add((origen, destino))
                camino.append(destino)
                ruta.writerow([origen, destino, tiempo, precio, vuelos])
    return camino
