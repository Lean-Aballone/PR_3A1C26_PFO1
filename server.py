import socket
import sqlite3
import datetime
import sys

# Configuración del socket TCP/IP
HOST = '127.0.0.1'
PORT = 5000

def init_db():
    # crea db y tabla si no existe
    try:
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT,
                fecha_envio TEXT,
                ip_cliente TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"No se pudo acceder a la base de datos: {e}")
        sys.exit(1)

def init_socket():
    # Configuración del socket TCP/IP
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # evita el error de puerto ocupado si se cierra mal
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        return server_socket
    except OSError as e:
        print(f"Error al iniciar el servidor, puede que el puerto {PORT} esté ocupado: {e}")
        sys.exit(1)

def save_message(content, client_ip):
    # Guardamos el mensaje en la DB y devolvemos la fecha
    try:
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO messages (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)',
                       (content, now, client_ip))
        conn.commit()
        conn.close()
        return now
    except sqlite3.Error as e:
        print(f"Error al guardar en DB: {e}")
        return None

def handle_connections(server_sock):
    print(f"Servidor escuchando en {HOST}:{PORT}...")
    while True:
        try:
            conn, addr = server_sock.accept()
            print(f"Se conectó un cliente desde {addr}")
            
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                msg = data.decode('utf-8')
                print(f"Recibido: {msg}")
                
                timestamp = save_message(msg, addr[0])
                
                if timestamp:
                    response = f"Mensaje recibido: {timestamp}"
                else:
                    response = "Error al guardar el mensaje"
                    
                conn.send(response.encode('utf-8'))
                
            conn.close()
            print(f"Cliente desconectado: {addr}")
            
        except KeyboardInterrupt:
            print("\nServidor apagado manualmente.")
            break

if __name__ == '__main__':
    init_db()
    s = init_socket()
    handle_connections(s)
    s.close()
