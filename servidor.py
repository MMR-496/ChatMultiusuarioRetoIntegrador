
import socket
import threading

HOST = "localhost"
PUERTO = 5000

# Diccionario para guardar conexión y nombre
clientes_conectados = {}


# Enviar mensaje a todos los clientes excepto al que lo envió
def broadcast(mensaje, conexion_actual):
    for cliente in list(clientes_conectados):
        if cliente != conexion_actual:
            try:
                cliente.send(mensaje.encode())
            except:
                # Si un cliente tiene problemas, lo eliminamos
                cliente.close()
                if cliente in clientes_conectados:
                    del clientes_conectados[cliente]


# Atender a cada cliente en su propio hilo
def atender_cliente(conexion, direccion):

    try:
        # El cliente envía su nombre al conectarse
        nombre = conexion.recv(1024).decode()

        # Guardar cliente y nombre
        clientes_conectados[conexion] = nombre

        print(f"{nombre} se conectó desde {direccion}")

        # Avisar a los demás
        broadcast(f"{nombre} se conectó al chat.", conexion)
