"""
Modelo Categoria
"""
from models.base_model import BaseModel


class Categoria(BaseModel):
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def guardar(self, db_connector):
        query = "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)"
        params = (self.nombre, self.descripcion)
        return db_connector.execute(query, params)

    def actualizar(self, db_connector, categoria_id):
        query = "UPDATE categorias SET nombre = %s, descripcion = %s WHERE categorias.id = %s"
        params = (self.nombre, self.descripcion, categoria_id)
        return db_connector.execute(query, params)

    @staticmethod
    def eliminar(db_connector, categoria_id):
        query = "DELETE FROM categorias WHERE categorias.id = %s"
        params = (categoria_id,)
        return db_connector.execute(query, params)

