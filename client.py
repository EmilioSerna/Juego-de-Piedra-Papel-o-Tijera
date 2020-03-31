#!/usr/bin/python
import xmlrpc.client
import argparse


def despliega_menu():
    print("MENU")
    print("1.Iniciar jugada")
    print("2.Preguntar si hay más jugadores")
    print("3.Mostrar partida")
    print("0.Salir")
    o = input("Opcion:>")
    return int(o)


def switch(opcion): # memily
    '''
        abre las funciones de acuerdo a la opción que escogiste, por default vuelve a desplegar menu
        recibe: opcion (int)
    '''
    if opcion == 1:
        iniciar_jugada()
    elif opcion == 2:
        hay_jugadores()
    elif opcion == 3:
        mostrar_partida()
    elif opcion == 0:
        salir()
    else:
        print("Escribe una opción")
        print("------------------")
        despliega_menu()


def main(jugador):
    print("Iniciamos!")
    proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
    try:
        opcion = 99
        while opcion != 0:
            opcion = despliega_menu()
            if opcion == 0:
                break
            if opcion == 1:
                j = proxy.agrega_jugador(jugador)
                print(j)
            if opcion == 2:
                n = proxy.numero_jugadores()
                print("Jugadores:", n)
            if opcion == 3:
                d = proxy.deck()
                print(d)
        print("Saliendo")

    except ConnectionError:
        print("Se desconecto el Server")
    except KeyboardInterrupt:
        print("Usuario cancela programa")


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-j", "--jugador", dest="jugador",
                       required=False, default="Fede")
    args = parse.parse_args()
    jugador = args.jugador
    main(jugador)
