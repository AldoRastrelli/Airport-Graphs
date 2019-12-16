class Aeropuerto:    
    def __init__(self,codigo,ciudad,latitud,longitud):
        self.codigo = codigo
        self.ciudad = ciudad
        self.latitud = latitud
        self.longitud = longitud

    def __eq__(self, other):
        return self.codigo == str(other)

    def __str__(self):
        return self.codigo

    def __repr__(self):
        return self.codigo

    def __hash__(self):
        return hash(self.codigo)