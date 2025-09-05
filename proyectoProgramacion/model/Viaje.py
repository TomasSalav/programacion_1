from abc import ABC, abstractmethod
from model.Usuario import Usuario
from view.View import View

class Viaje(ABC):
    def __init__(self, destino:str, duracion:int, usuario:Usuario):
        self.__destino = destino
        self.__duracion = duracion
        self.__usuario = usuario

    def setDestino(self, destino):
        if destino is not None:
            self.__destino = destino
        else:
            View.imprimirError("No puede ingresar datos vacíos")

    def getDestino(self):
        return self.__destino
    
    def setDuracion(self, duracion):
        if duracion is not None:
            self.__duracion = duracion
        else:
            View.imprimirError("No puede ingresar datos vacíos")

    def getDuracion(self):
        return self.__duracion 
    
    def getUsuario(self):
        return self.__usuario

    @abstractmethod
    def medioTransporte(self):
        pass

    @abstractmethod
    def costoEstimado(self, duracion):
        pass

    def descripcion(self):
        return f"Viaje a {self.__destino} con duración de {self.__duracion} días"
    
    def __str__(self):
          return f"Destino: {self.__destino}, Duracion: {self.__duracion} días, Usuario: {self.__usuario.getNombre()}"
