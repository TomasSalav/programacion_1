from model.Agencia import Agencia
from model.Usuario import Usuario
from model.ViajeInternacional import ViajeInternacional
from model.ViajeNacional import ViajeNacional
from view.View import View

class AppConsole():
    def __init__(self, agencia:Agencia):
        self.__agencia = agencia

    def aplicacion(self):
        correrAplicacion = True

        while correrAplicacion:
            opcion = View.imprimirMenu()

            match opcion:
                case 1:
                    for viaje in self.__agencia.getViajes():
                        print(viaje)
                case 2:
                    viaje = ViajeInternacional(View.pedirString("Ingrese el destino del viaje"),
                                                                  View.pedirInt("Ingrese la cantidad de días"),
                                                                  Usuario(View.pedirString("Ingrese la identificación del usuario"),
                                                                          View.pedirString("Ingrese el nombre del usuario")),
                                                                  [View.pedirString("Ingrese el nombre del documento") for _ in range(View.pedirInt("Ingrese la cantidad de documentos necesarios"))],  
                                                                )
                    self.__agencia.añadirViaje(viaje)
                    print(f"\n{viaje.descripcion()} - El costo estimado del viaje es {viaje.costoEstimado()} - {viaje.medioTransporte()}")
                case 3:
                    viaje = ViajeNacional(View.pedirString("Ingrese el destino del viaje"),
                                                View.pedirInt("Ingrese la cantidad de días"),
                                                Usuario(View.pedirString("Ingrese la identificación del usuario"),
                                                        View.pedirString("Ingrese el nombre del usuario")),
                                                View.pedirString("Ingrese el código postal"),  
                                            )
                    self.__agencia.añadirViaje(viaje)
                    print(f"\n{viaje.descripcion()} - El costo estimado del viaje es {viaje.costoEstimado()} - {viaje.medioTransporte()}")
                case 4:
                    self.__agencia.eliminarViaje(View.pedirString("Ingrese el destino del viaje"), View.pedirString("Ingrese el id del usuario"))
                case 0:
                    correrAplicacion = False