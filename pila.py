class Pila:
    def __init__(self):
        self.elementos = []

    def apilar(self, elemento):
        self.elementos.append(elemento)

    def desapilar(self):
        return self.elementos.pop()

    def ver_tope(self):
        return self.elementos[-1]

    def esta_vacia(self):
        return not self.elementos

    def convertir_a_lista(self):
        lista = self.elementos.copy()
        lista.reverse()
        return lista