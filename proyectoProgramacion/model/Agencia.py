from model.Viaje import Viaje
from model.ViajeInternacional import ViajeInternacional
from model.ViajeNacional import ViajeNacional
from model.Usuario import Usuario
from view.View import View
from typing import List

class Agencia():
    def __init__(self, nombre:str, direccion:str, viajes:List[Viaje] = list()):
        self.__nombre = nombre
        self.__direccion = direccion
        self.__viajes = viajes

    def setNombre(self, nombre):
        if nombre is not None:
            self.__nombre = nombre
        else:
            View.imprimirError("No puede ingresar datos vacíos")

    def getNombre(self):
        return self.__nombre

    def setDireccion(self, direccion):
        if direccion is not None:
            self.__direccion = direccion
        else:
            View.imprimirError("No puede ingresar datos vacíos")
        
    def getDireccion(self):
        return self.__direccion

    def getViajes(self):
        return self.__viajes
    
    def añadirViaje(self, viaje):
        self.__viajes.append(viaje)

    def eliminarViaje(self, destino, id):
        for viaje in self.__viajes:
            if viaje.getDestino() == destino:
                if viaje.getUsuario().getId() == id:
                    self.__viajes.remove(viaje)
                    return
        View.imprimirError("No se encontró el viaje")


    def cargarDatos(self):
        viajes = [("Santa Marta", 8, Usuario("1114152598", "Juan David Martínez"), "470001"), 
                  ("Estados Unidos", 12, Usuario("1089932449", "Tomás Salazar"), ["Visa Americana", "Carné de Vacunas"])]
        
        self.añadirViaje(ViajeNacional(viajes[0][0], viajes[0][1], viajes[0][2], viajes[0][3]))
        self.añadirViaje(ViajeInternacional(viajes[1][0], viajes[1][1], viajes[1][2], viajes[1][3]))
 

    

