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
