"""
Modelo Cliente
"""
from models.base_model import BaseModel


class Cliente(BaseModel):
    def __init__(self, nombre, correo, telefono, direccion):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion

    def guardar(self, db_connector):
        query = "INSERT INTO clientes (nombre, correo, telefono, direccion) VALUES (%s, %s, %s, %s)"
        params = (self.nombre, self.correo, self.telefono, self.direccion)
        return db_connector.execute(query, params)

    def actualizar(self, db_connector, cliente_id):
        query = "UPDATE clientes SET nombre = %s, correo = %s, telefono = %s, direccion = %s WHERE id = %s"
        params = (self.nombre, self.correo, self.telefono, self.direccion, cliente_id)
        return db_connector.execute(query, params)

    @staticmethod
    def eliminar(db_connector, cliente_id):
        query = "DELETE FROM clientes WHERE id = %s"
        params = (cliente_id,)
        return db_connector.execute(query, params)

