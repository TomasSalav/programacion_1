from model.Viaje import Viaje
from model.Usuario import Usuario
from typing import List

class ViajeInternacional(Viaje):
    def __init__(self, destino:str, duracion:int, usuario:Usuario, documentosNecesarios: List[str] = list()):
        super().__init__(destino, duracion, usuario)
        self.__documentoNecesarios = documentosNecesarios

    def getDocumentosNecesarios(self):
        return self.__documentoNecesarios
    
    def medioTransporte(self):
        return (f"El viaje se hará en avión")
    
    def costoEstimado(self):
        costo = self.getDuracion() * 300.000
        return costo
    
    def __str__(self):
        return super().__str__() + f", • {" → ".join(self.__documentoNecesarios)}"
    
