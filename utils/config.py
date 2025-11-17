"""
Configuración de la aplicación
"""
import os

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # <- pon tu contraseña si la tienes. Si no tienes, déjalo vacío.
    "database": "northwind"  # <- Cambia 'mysql' por 'northwind'
}

IMAGES_DIR = "imagenes_empleados"
os.makedirs(IMAGES_DIR, exist_ok=True)

