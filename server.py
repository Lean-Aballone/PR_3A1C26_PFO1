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