#!/usr/bin/python
import xmlrpc.client
import argparse
import server


def despliega_menu():
    print("--------------------------\n")
    print("** MENU **\n")
    print("1.- Iniciar jugada")
    print("2.- Jugadores en la partida")
    print("3.- Mostrar partida")
    print("0.- Salir")
    o = input("\nOpción:> ")
    return int(o)


def main(jugador):
    print("\n== JUEGO DE PIEDRA, PAPEL O TIJERA ==\n")
    print("Iniciando...\n")
    keyboardyes = KeyboardInterrupt
    proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
    try:
        opcion = 99
        while opcion != 0:
            opcion = despliega_menu()
            print("\n")
            if opcion == 0:
                break
            if opcion == 1:
                j = proxy.agrega_jugador(jugador)
                print(j)
            if opcion == 2:
                n = proxy.numero_jugadores()
                print("Jugadores:", n, "jugadores.")
            if opcion == 3:
                d = proxy.deck()
                print(d)
                
        print("¡Gracias por jugar!\n")

    except ConnectionError:
        print("Se desconectó el servidor o bien, nunca se encendió.\n")
    except KeyboardInterrupt:
        print("Usuario: " + jugador +  " ha cancelado la partida.\n")


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-j", "--jugador", dest="jugador",
                       required=False, default="Fede")
    args = parse.parse_args()
    jugador = args.jugador
    main(jugador)
