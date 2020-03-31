# Juego-de-Piedra-Papel-o-Tijera
Instrucciones
En esta tarea, deben lograr que funcione correctamente el siguiente juego interactivo de "Piedra, Papel o Tijera", el cual consta de dos programas, uno Servidor y otro Cliente. El Servidor lleva registro de todos los jugadores y cual es la opción que tomó (piedra, papel o tijera, al azar) y el Cliente sirve para interactuar con el Servidor, ya sea pidiendo una nueva jugada, mostrando cuantos jugadores hay en línea, y cuál es el status del juego.

 

Lo que ustedes tienen que hacer es editar el programa client.py y calcular quién es el ganador. Las reglas para Piedra, Papel o Tijera para dos jugadores son:

Piedra vence a Tijera
Tijera vence a Papel
Papel vence a Piedra
Si hay empate, recomendar hacer una nueva partida. 

 

Si hay tres jugadores, y por ejemplo, dos empatan (2 tijeras y 1 papel), decir que empataron y recomendar una nueva jugada para ellos. Si es posible, eliminar el jugador perdedor en el Servidor.

 

Muy importante: necesitan ejecutar primero el programa server.py, dejarlo ejecutando y en otra terminal abrir el programa de client.py.

 

Como pueden ver en el código, estamos haciendo uso de 'localhost', o la dirección IP 127.0.0.1 ... si quieren hacer una conexión remota desde una computadora fuera de su red local, tienen que redirigir el puerto 9000 a la computadora que tenga el programar server.py

 

Pueden modificar el programa server.py si lo creen necesario.
