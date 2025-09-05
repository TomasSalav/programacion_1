class View:
    @classmethod
    def imprimirError(cls, texto):
        print(f"X - {texto}.")

    @classmethod
    def pedirString(cls, texto):
        while True:
            try:
                return str(input(f"{texto} -> "))
            except:
                cls.imprimirError("Ingrese un tipo de dato válido")

    @classmethod
    def pedirInt(cls, texto):
        while True:
            try:
                return int(input(f"{texto} -> "))
            except:
                cls.imprimirError("Ingrese un tipo de dato válido")

    @classmethod
    def imprimirMenu(cls):
        print("""
----- CONECTA AL MUNDO - VIAJES ------
1. Imprimir Viajes
2. Añadir Viaje Internacional
3. Añadir Viaje Nacional
4. Eliminar Viaje
              
0. Salir
              """)

        return cls.pedirInt("Ingrese la opción deseada")
    

