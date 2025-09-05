from model.Agencia import Agencia
from controller.AppConsole import AppConsole

if __name__ == "__main__":
    agencia = Agencia("Conecta Al Mundo", "Mukava Del Valle", [])
    agencia.cargarDatos()

    appConsole = AppConsole(agencia)
    appConsole.aplicacion()