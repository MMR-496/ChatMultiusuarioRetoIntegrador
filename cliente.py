import socket
import threading

HOST = "localhost"
PUERTO = 5000

# Crear socket TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarse al servidor
cliente.connect((HOST, PUERTO))

# Pedir nombre
nombre = input("Escribe tu nombre: ")

# Enviar nombre al servidor
cliente.send(nombre.encode())


# Recibir mensajes del servidor
def recibir_mensajes():

    while True:
        try:

            mensaje = cliente.recv(1024).decode()

            if not mensaje:
                break

            print("\n" + mensaje)

        except ConnectionResetError:
            print("El servidor cerró la conexión.")
            break

        except:
            print("Se perdió la conexión con el servidor.")
            break


# Crear hilo para recibir mensajes
hilo = threading.Thread(target=recibir_mensajes)

# El hilo termina cuando termina el programa
hilo.daemon = True

hilo.start()


# Enviar mensajes
while True:

    mensaje = input(">")

    # Comando para salir
    if mensaje.lower() == "/salir":
        break

    try:
        cliente.send(mensaje.encode())

    except:
        print("No se pudo enviar el mensaje.")
        break


# Cerrar conexión
cliente.close()

print("Desconectado del chat.")