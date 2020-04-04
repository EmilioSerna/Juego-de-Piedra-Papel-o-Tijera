#!/usr/bin/python

# Equipo: Mustafar
# Fecha: 03 de abril de 2020
# Integrantes:
#
#   Félix López Juan Pablo
#   López Velásquez Octavio
#   Serna Navarro Ángel Emilio
""" Juego de piedra, papel o tijera (versión online 100Gbps 4k 60fps 144Hz Dolby Atmos 32:9 1 link (literalmente)) 
    Programa: Cliente.
"""
import xmlrpc.client
import argparse
import server
import copy
import time


def despliega_menu():
    try:
        print("--------------------------\n")
        print("** MENU **\n")
        print("1.- Cambiar mano")
        print("2.- Jugadores en la partida")
        print("3.- Mostrar partida")
        print("4.- Mostrar mi mano")
        print("5.- FAQ")
        print("0.- Salir")
        o = input("\nOpción:> ")
        return int(o)
    except KeyboardInterrupt:
        print("Has abandonado la partida.\n")
        proxy.desconectar_jugador(jugador)
    except:
        print("¡Elige una opción!")
        return despliega_menu()


def faq():
    print("-¿Es esto realmente un FAQ?")
    print(
        "     No, son preguntas hechas y respondidas por Emilio. Por eso están mal respondidas. "
    )
    print("-¿De qué me sirve esto?")
    print("     No lo sé, sinceramente")
    print("-¿Cómo se juega?")
    print(
        "     Cuando entras al servidor por primera vez, se te asigna una mano automáticamente"
    )
    print(
        "     si aún no tienes jugada tienes que presionar 1 para que se genere una mano"
    )
    print("-¿Cómo veo quién ganó?")
    print("     Selecciona la opción 3")
    print("-¿Por qué no puedo seleccionar mi mano?")
    print("     Es más divertido cuando se lo dejas al azar")
    print("¿Es este acaso un easter egg de Octavio?")
    print("     Profesor, ¿usted ha jugado DOOM?")
    print("-¿El Octavio roba FAQs?")
    print(
        "     Sí, este ni siquiera es tu Easter Egg. Not really, pero mira, bueno, podría ser."
        + " Estas son las mañanitas que cantaba el rey David..."
    )
    print("\n")


def main(jugador):
    print("\n== JUEGO DE PIEDRA, PAPEL O TIJERA ==\n")
    print("Iniciando...\n")
    keyboardyes = KeyboardInterrupt
    ip = "localhost"
    puerto = 9000
    proxy = xmlrpc.client.ServerProxy("http://" + ip + ":" + str(puerto))
    try:
        opcion = 99
        cantidad_desconectados_pasada = 0
        primera_vez = (
            True  # para que no imprima quién se desconectó cuando recién entras
        )

        if jugador in proxy.deck():  # si existe el jugador en el servidor
            print(
                "Ya existe el jugador:",
                jugador,
                "\nPor favor, reingresa con otro usuario",
            )
            opcion = 0
        else:
            # print("Entraste como Observador")
            j = proxy.agrega_jugador(jugador)
            print("Tu mano (" + (jugador) + ") es:", j[1])

        while opcion != 0:

            # verifica el num de jugadores desconectados
            cantidad_desconectados = proxy.tamaño_desconectados()
            # mensaje que regresa server.checar_jugadores()
            mensaje = proxy.checar_jugadores()

            # esto es para que no imprima cada ciclo
            if cantidad_desconectados_pasada < cantidad_desconectados:
                # esto no hace referencia a otro objeto, sino lo copia
                cantidad_desconectados_pasada = copy.copy(cantidad_desconectados)
                if primera_vez == False:
                    print(mensaje)

            opcion = despliega_menu()
            print("\n")
            if opcion == 0:
                proxy.desconectar_jugador(jugador)
                break
            elif opcion == 1:
                j = proxy.agrega_jugador(jugador)
                print("Tu nueva mano es:", j[1])
            elif opcion == 2:
                n = proxy.numero_jugadores()
                print("Jugador(es):", n, "jugador(es).")
            elif opcion == 3:
                d = proxy.deck()
                # print(d)

                winner = ""
                if len(d) != 0 or len(d) != 1:
                    # Aquí va el método/función que determina quien gana.
                    # Hay que meterlo en server.py para que el mensaje de ganador se comunique
                    # a todos los clientes.

                    expected_value = next(
                        iter(d.values())
                    )  # Toma un valor, ejemplo 'Piedra' en los valores del diccionario de jugadores.
                    all_equal = all(
                        value == expected_value for value in d.values()
                    )  # Verifica si es igual a todos los valores dentro del diccionario.

                    if (
                        all_equal == True
                    ):  # Si todos los valores son iguales, significa un empate entre todos.
                        print("Hubo un empate. Recomendamos reiniciar el juego.")

                        for (jugador, jugada) in d.items():
                            # Este for imprime únicamente, con formato, la jugada de los jugadores.
                            print(jugador, "con", jugada)
                            """
                            Ejemplo: 
                                - Octavio con tijeras.
                                - Emilio con tijeras.
                                - JuanPi con piedra.
                                                            """
                        time.sleep(3)
                        # <-- Aquí podemos hacer que abra el menú después de un poco de tiempo.
                        despliega_menu()
                    else:
                        winner = proxy.definir_ganador()
                        if winner == "empate":
                            print("Hubo un empate entre todos los jugadores")
                        else:
                            if len(winner) > 1:
                                print("Hubo un empate entre: ")
                                print(winner)
                                for jugador in winner:
                                    print(jugador)
                            else:
                                mano = proxy.deck()[jugador]
                                print(f"Ganador: {winner[0]}", "con", d[winner[0]])
                                # print(winner)
                                # print("¡Has ganado!")
                                if jugador not in winner:
                                    proxy.desconectar_jugador(jugador)
                                    print(
                                        "Has sido enviado al lobby de los perdedores."
                                        + " DOOM's music starts playing. Tarandarandararararan"
                                    )
                                    mensaje = proxy.checar_jugadores()
                                    break
                else:
                    print(
                        "Sería recomendable hacer una jugada o agregar jugadores antes de jugar "
                        + "o saber quién ganó."
                    )
            elif opcion == 4:
                mano = proxy.deck()[jugador]
                print("Tu mano (" + (jugador) + ") es:", mano)
            elif opcion == 5:
                faq()
            primera_vez = False
        print("¡Gracias por jugar!\n")

    except ConnectionError:
        print("Error de conexión con el servidor.\n")
    except KeyboardInterrupt:
        pass
    except ValueError as error:
        print(error)
        proxy.desconectar_jugador(jugador)
    except:
        proxy.desconectar_jugador(jugador)


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "-j", "--jugador", dest="jugador", required=False, default="Fede"
    )
    args = parse.parse_args()
    jugador = args.jugador
    main(jugador)
