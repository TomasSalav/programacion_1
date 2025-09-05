from model.Viaje import Viaje
from model.Usuario import Usuario
from view.View import View

class ViajeNacional(Viaje):
    def __init__(self, destino:str, duracion:str, usuario:Usuario, codigoPostal:str):
        super().__init__(destino, duracion, usuario)
        self.__codigoPostal = codigoPostal

    def setCodigoPostal(self, codigoPostal):
        if codigoPostal is not None:
            self.__codigoPostal = codigoPostal
        else:
            View.imprimirError("No puede ingresar datos vacíos")

    def getCodigoPostal(self):
        return self.__CodigoPostal
    
    def medioTransporte(self):
        return (f"El viaje se hará en bus")
    
    def costoEstimado(self):
        costo = self.getDuracion() * 100.000
        return costo
    
    def __str__(self):
        return super().__str__() + f", Código Postal: {self.__codigoPostal}"