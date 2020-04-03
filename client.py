#!/usr/bin/python
import xmlrpc.client
import argparse
import server
import copy


def despliega_menu():
    print("--------------------------\n")
    print("** MENU **\n")
    print("1.- Cambiar mano")
    print("2.- Jugadores en la partida")
    print("3.- Mostrar partida")
    print("4.- FAQ")
    print("0.- Salir")
    o = input("\nOpción:> ")
    return int(o)


def faq():
    print("-¿Es esto realmente un FAQ?")
    print("     No, son preguntas hechas y respondidas por Emilio")
    print("-¿De qué me sirve esto?")
    print("     No lo sé, sinceramente")
    print("-¿Cómo se juega?")
    print("     Cuando entras al servidor por primera vez, eres observador")
    print("     si aún no tienes jugada tienes que presionar 1 para que se genere una mano")
    print("-¿Cómo veo quién ganó?")
    print("     Selecciona la opción 3")
    print("-¿Por qué no puedo seleccionar mi mano?")
    print("     Es más divertido cuando se lo dejas al azar")
    print("\n")


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
        primera_vez = True  # para que no imprima quién se desconectó cuando recién entras

        if jugador in proxy.deck():  # si existe el jugador en el servidor
            print("Ya existe el jugador:", jugador,
                  "\nPor favor, reingresa con otro usuario")
            opcion = 0
        else:
            #print("Entraste como Observador")
            j = proxy.agrega_jugador(jugador)
            print("Tu mano es:", j[1])

        while opcion != 0:

            # verifica el num de jugadores desconectados
            cantidad_desconectados = proxy.tamaño_desconectados()
            # mensaje que regresa server.checar_jugadores()
            mensaje = proxy.checar_jugadores()

            # esto es para que no imprima cada ciclo
            if cantidad_desconectados_pasada < cantidad_desconectados:
                # esto no hace referencia a otro objeto, sino lo copia
                cantidad_desconectados_pasada = copy.copy(
                    cantidad_desconectados)
                if primera_vez == False:
                    print(mensaje)

            opcion = despliega_menu()
            print("\n")
            if opcion == 0:
                proxy.desconectar_jugador(jugador)
                break
            if opcion == 1:
                j = proxy.agrega_jugador(jugador)
                print("Tu mano es:", j[1])
            if opcion == 2:
                n = proxy.numero_jugadores()
                print("Jugadores:", n, "jugadores.")
                mano = proxy.mi_mano(jugador)
            if opcion == 3:
                d = proxy.deck()
                print(d)
                # print(list(d[0], d[1]))

                winner = ""
                if (len(d) != 0 or len(d) != 1):
                    # Aquí va el método/función que determina quien gana.
                    # Hay que meterlo en server.py para que el mensaje de ganador se comunique
                    # a todos los clientes.
                    pass
                else:
                    print(
                        "Sería recomendable hacer una jugada antes de saber quién ganó.")
            if opcion == 4:
                faq()
            primera_vez = False
        print("¡Gracias por jugar!\n")

    except ConnectionError:
        print("Error de conexión con el servidor.\n")
    except KeyboardInterrupt:
        print("Has abandonado la partida.\n")
        proxy.desconectar_jugador(jugador)


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-j", "--jugador", dest="jugador",
                       required=False, default="Fede")
    args = parse.parse_args()
    jugador = args.jugador
    main(jugador)
