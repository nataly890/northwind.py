"""
Modelo Producto
"""
from models.base_model import BaseModel


class Producto(BaseModel):
    def __init__(self, nombre, descripcion, precio, stock, categoria_id):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.categoria_id = categoria_id

    def guardar(self, db_connector):
        query = "INSERT INTO productos (nombre, descripcion, precio, stock, categoria_id) VALUES (%s, %s, %s, %s, %s)"
        params = (self.nombre, self.descripcion, self.precio, self.stock, self.categoria_id)
        return db_connector.execute(query, params)

    def actualizar(self, db_connector, producto_id):
        query = "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s, categoria_id=%s WHERE id=%s"
        params = (self.nombre, self.descripcion, self.precio, self.stock, self.categoria_id, producto_id)
        return db_connector.execute(query, params)

    @staticmethod
    def eliminar(db_connector, producto_id):
        query = "DELETE FROM productos WHERE id=%s"
        params = (producto_id,)
        return db_connector.execute(query, params)

