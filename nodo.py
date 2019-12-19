class Nodo:

    def __init__(self, dato = None, prox = None):
        """constructor de la clase"""

        self.dato = dato
        self.prox = prox

    def __str__(self):
        """devuelve un string del dato del nodo"""

        return str(self.dato)

    def ver_lista(nodo):
        """imprime los elementos de la lista enlazada"""

        while nodo is not None:
            print(nodo)
            nodo = nodo.prox

    