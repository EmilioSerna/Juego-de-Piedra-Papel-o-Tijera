#!/usr/bin/python
from xmlrpc.server import SimpleXMLRPCServer
import logging
import random


class Juego:
    jugadores = None
    opciones = None

    def __init__(self):
        self.jugadores = {}
        self.opciones = ['Piedra', 'Papel', 'Tijera']
    def mano(self, jugador):
        i = random.randint(0, 2)
        self.jugadores[jugador] = self.opciones[i]
        return [jugador, self.opciones[i]]


# Set up logging
logging.basicConfig(level=logging.DEBUG)

server = SimpleXMLRPCServer(
    ('localhost', 9000),
    logRequests=True,
    )
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


def main():
    server.register_function(agrega_jugador)
    server.register_function(numero_jugadores)
    server.register_function(deck)
    # Start the server
    try:
        print('Usa Control-C para salir.')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Saliendo...')


if __name__ == "__main__":
    main()
