
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

        while True:

            # Esperar mensaje
            datos = conexion.recv(1024)

            # Si no llegan datos, el cliente se desconectó
            if not datos:
                break

            mensaje = datos.decode()

            # Agregar el nombre al mensaje
            mensaje_completo = f"{nombre}: {mensaje}"

            print(mensaje_completo)

            # Enviar a todos los demás clientes
            broadcast(mensaje_completo, conexion)

    except ConnectionResetError:
        print(f"{nombre} se desconectó abruptamente")

    except Exception as error:
        print(f"Error con {direccion}: {error}")

    finally:

        # Eliminar al cliente
        if conexion in clientes_conectados:
            clientes_conectados.pop(conexion)

        conexion.close()

        # Avisar a los demás que salió
        if 'nombre' in locals():
            broadcast(f"{nombre} salió del chat.", conexion)

        print(f"Conexión cerrada: {direccion}")


# Crear servidor TCP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((HOST, PUERTO))
servidor.listen()

print(f"Servidor escuchando en el puerto {PUERTO}...")


# Aceptar clientes continuamente
while True:

    conexion, direccion = servidor.accept()

    print(f"Nuevo cliente conectado: {direccion}")

    # Crear un hilo para cada cliente
    hilo = threading.Thread(
        target=atender_cliente,
        args=(conexion, direccion)
    )

    hilo.start()