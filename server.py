#!/usr/bin/python

# Equipo: Mustafar
# Fecha: 03 de abril de 2020
# Integrantes:
#
#   Félix López Juan Pablo
#   López Velásquez Octavio
#   Serna Navarro Ángel Emilio
""" Juego de piedra, papel o tijera (versión online 100Gbps 4k 60fps 144Hz Dolby Atmos 32:9 1 link (literalmente)) 
    Programa: Servidor.
"""
from xmlrpc.server import SimpleXMLRPCServer
import logging
import random


class Juego:
    jugadores = None
    opciones = None
    jugadores_desconectados = None

    def __init__(self):
        self.jugadores = {}  # diccionario
        self.jugadores_desconectados = []  # lista
        self.opciones = ["Piedra", "Papel", "Tijera"]

    def mano(self, jugador):
        i = random.randint(0, 2)
        self.jugadores[jugador] = self.opciones[i]
        return [jugador, self.opciones[i]]


# Set up logging
logging.basicConfig(level=logging.DEBUG)
ip = "localhost"
puerto = 9000
server = SimpleXMLRPCServer((ip, puerto), logRequests=True,)
j = Juego()


def agrega_jugador(jugador):
    resultado = j.mano(jugador)
    print(resultado)
    return resultado


def numero_jugadores():
    print(j.jugadores)
    return len(j.jugadores)


def deck():
    return j.jugadores


def desconectar_jugador(jugador):
    """
        agrega a la lista de jugadores_desconectados del objeto jugador
        recibe: nombre del jugador
    """
    j.jugadores_desconectados.append(jugador)
    try:
        del j.jugadores[jugador]  # elimina el jugador del diccionario
    except:
        pass
    return 0


def checar_jugadores():
    """
        despliega el último jugador desconectado
    """
    if len(j.jugadores_desconectados) > 0:
        ultimo_desconectado = j.jugadores_desconectados[-1]
        mensaje = (
            "\n¡El jugador "
            + ultimo_desconectado
            + " se ha desconectado!\n"
            + "Profesor, pónganos un 💯"
        )
        return mensaje
    else:
        return "Esto es un bug, línea 72, llame al administrador, AYUDAAAAA"


def tamaño_desconectados():
    """
        regresa el tamaño de jugadores desconectados de un objeto Jugador
    """
    if len(j.jugadores_desconectados) > 0:
        n = len(j.jugadores_desconectados)
        return n
    else:
        return 0


def definir_ganador():
    manos = dict()
    for i in set(j.jugadores.values()):
        lista = [nombre for nombre in j.jugadores.keys() if j.jugadores[nombre] == i]
        manos[i] = lista
        # lista.clear()
    if len(manos) != 2:
        return "empate"
    else:
        # Un diccionario que indica que le gana a todas las opciones
        rules = {"Piedra": "Papel", "Tijera": "Piedra", "Papel": "Tijera"}
        opciones_partida = list(manos.keys())
        if rules[opciones_partida[0]] in opciones_partida:
            i = 0
            for key, val in manos.items():
                if i == 1:
                    print(val)
                    return val
                else:
                    i += 1
        else:
            for key, val in manos.items():
                print(val)
                return val


def main():
    server.register_function(agrega_jugador)
    server.register_function(numero_jugadores)
    server.register_function(deck)
    server.register_function(desconectar_jugador)
    server.register_function(checar_jugadores)
    server.register_function(tamaño_desconectados)
    server.register_function(definir_ganador)
    # Start the server
    print("\nIniciando servidor...\n")
    try:
        print("===========================\n")
        print("Información del servidor: ")
        print("- Servidor iniciado")
        print("- Dirección IP:", ip)
        print("- Puerto:", puerto)
        print("\n===========================")
        print("\nUsa Control-C para salir.")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSaliendo...\n")


if __name__ == "__main__":
    main()
