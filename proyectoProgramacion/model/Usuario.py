from view.View import View

class Usuario:
    def __init__(self, id:str, nombre:str):
        self.__id = id
        self.__nombre = nombre

    def setNombre(self, nombre):
        if nombre is not None:
            self.__nombre = nombre
        else:
            View.imprimirError("No puede ingresar datos vacíos")

    def getNombre(self):
        return self.__nombre
    
    def setId(self, id):
        if id is not None:
            self.__id = id
        else:
            View.imprimirError("No puede ingresar datos vacíos")

    def getId(self):
        return self.__id
    
    def __str__(self):
          return f"Nombre: {self.__nombre()}, ID: {self.__id()}"
