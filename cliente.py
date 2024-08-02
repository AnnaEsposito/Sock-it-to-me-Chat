import socket
import threading

# Conectar el cliente al servidor
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.connect(('127.0.0.1', 12345))

# Función para recibir mensajes del servidor
def recibir_mensajes():
    while True:
        try:
            mensaje = socket_cliente.recv(1024)
            if not mensaje:
                break
            print(mensaje.decode())
        except:
            break

# Iniciar el hilo para recibir mensajes
threading.Thread(target=recibir_mensajes).start()

# Enviar nombre de usuario al servidor
nombre = input("Introduce tu nombre: ")
socket_cliente.send(nombre.encode())

# Enviar mensajes al servidor
while True:
    mensaje = input()
    socket_cliente.send(mensaje.encode())
