#!/usr/bin/python
import xmlrpc.client
import argparse
import server
import copy


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
    ip = 'localhost'
    puerto = 9000
    proxy = xmlrpc.client.ServerProxy('http://' + ip + ':' + str(puerto))
    try:
        opcion = 99
        cantidad_desconectados_pasada = 0
        while opcion != 0:

            cantidad_desconectados = proxy.tamaño_desconectados()
            mensaje = proxy.checar_jugadores()

            if cantidad_desconectados_pasada < cantidad_desconectados:
                print(mensaje)
                # esto no hace referencia a otro objeto, sino lo copia
                cantidad_desconectados_pasada = copy.copy(
                    cantidad_desconectados)

            opcion = despliega_menu()
            print("\n")
            if opcion == 0:
                proxy.desconectar_jugador(jugador)
                break
            if opcion == 1:
                j = proxy.agrega_jugador(jugador)
                print(j)
            if opcion == 2:
                n = proxy.numero_jugadores()
                print("Jugadores:", n, "jugadores.")
                # AQUÍ DEBERÁ CALCULAR EL QUE GANÓ
            if opcion == 3:
                d = proxy.deck()
                print(d)

        print("¡Gracias por jugar!\n")

    except ConnectionError:
        print("Error de conexión con el servidor.\n")
    except KeyboardInterrupt:
        print("Usuario: " + jugador + "se ha salido de la partida.\n")


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-j", "--jugador", dest="jugador",
                       required=False, default="Fede")
    args = parse.parse_args()
    jugador = args.jugador
    main(jugador)
