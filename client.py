import socket

# Configuración del socket TCP/IP
HOST = '127.0.0.1'
PORT = 5000

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print("¡Conectado al servidor! Escribí tus mensajes ('exito' para salir).")
        
        while True:
            msg = input("> ")
            
            if msg.lower() == 'exito':
                print("Saliendo...")
                break
                
            if msg.strip() == '':
                continue
                
            client_socket.send(msg.encode('utf-8'))
            
            # Recibir la respuesta
            response = client_socket.recv(1024)
            print(f"Respuesta del servidor: {response.decode('utf-8')}")
            
    except ConnectionRefusedError:
        print("Error: No se pudo conectar. Revisá que el servidor esté corriendo.")
    finally:
        client_socket.close()

if __name__ == '__main__':
    start_client()
