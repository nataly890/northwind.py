"""
DatabaseConnector - Utilidad para manejar conexiones a MySQL
"""
import mysql.connector
from tkinter import messagebox


class DatabaseConnector:
    def __init__(self, cfg):
        self.cfg = cfg
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.cfg)
        except mysql.connector.Error as e:
            print(f"Error de conexión a la DB: {e}")
            self.conn = None  # Aseguramos que la conexión es None si falla

    def execute(self, query, params=None):
        if not self.conn or not self.conn.is_connected():
            self.connect()  # Intenta reconectar
            if not self.conn:
                messagebox.showerror("DB Error", "No hay conexión a la base de datos.")
                return None
        cur = None  # Inicializar cur a None
        try:
            cur = self.conn.cursor()
            cur.execute(query, params or ())
            self.conn.commit()
            return cur
        except mysql.connector.Error as e:
            if self.conn:
                self.conn.rollback()
            messagebox.showerror("SQL Error", f"{e}")
            return None
        finally:
            if cur:
                cur.close()

    def fetchall(self, query, params=None):
        if not self.conn or not self.conn.is_connected():
            self.connect()  # Intenta reconectar
            if not self.conn:
                messagebox.showerror("DB Error", "No hay conexión a la base de datos.")
                return []
        try:
            cur = self.conn.cursor()
            cur.execute(query, params or ())
            rows = cur.fetchall()
            return rows
        except mysql.connector.Error as e:
            messagebox.showerror("SQL Error", f"{e}")
            return []
        finally:
            if 'cur' in locals() and cur:
                cur.close()

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()

