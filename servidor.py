import socket
import select

# Configuración del socket del servidor
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se crea el objeto socket, especificando que aceptara direcciones IP y que implementara para la comunicacion el protocolo TCP
socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Este metodo permite que se pueda reutilizar la dirección IP y el puerto.
socket_servidor.bind(('0.0.0.0', 12345))#Se enlaza el socket a todas las interfaces de red en la máquina (0.0.0.0) y al puerto 12345.
socket_servidor.listen(10)#Se coloca el socket en modo de escucha para aceptar conexiones entrantes de clientes.

print("Servidor de chat iniciado en el puerto 12345")

# Listas para seguimiento de conexiones
lista_sockets = [socket_servidor]
clientes = {}

# Función para manejar mensajes entrantes
def recibir_mensaje(socket_cliente):
    try:
        mensaje = socket_cliente.recv(1024)
        if not mensaje:
            return False
        return mensaje.decode()
    except:
        return False

# Bucle principal del servidor
while True:
    sockets_lectura, _, sockets_excepcion = select.select(lista_sockets, [], lista_sockets)
    
    for socket_notificado in sockets_lectura:
        if socket_notificado == socket_servidor:
            socket_cliente, direccion_cliente = socket_servidor.accept()
            socket_cliente.send("NOMBRE".encode())
            usuario = recibir_mensaje(socket_cliente)
            if usuario is False:
                continue
            lista_sockets.append(socket_cliente)
            clientes[socket_cliente] = usuario
            print(f"Conexión aceptada de {direccion_cliente} con nombre {usuario}")
        else:
            mensaje = recibir_mensaje(socket_notificado)
            if mensaje is False:
                print(f"Conexión cerrada de {clientes[socket_notificado]}")
                lista_sockets.remove(socket_notificado)
                del clientes[socket_notificado]
                continue
            usuario = clientes[socket_notificado]
            print(f"Mensaje recibido de {usuario}: {mensaje}")
            for socket_cliente in clientes:
                if socket_cliente != socket_notificado:
                    socket_cliente.send(f"{usuario}: {mensaje}".encode())
    
    for socket_notificado in sockets_excepcion:
        lista_sockets.remove(socket_notificado)
        del clientes[socket_notificado]
