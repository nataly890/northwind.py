"""
Modelo Pedido
"""
from models.base_model import BaseModel


class Pedido(BaseModel):
    def __init__(self, cliente_id, fecha, estado):
        self.cliente_id = cliente_id
        self.fecha = fecha
        self.estado = estado

    def guardar(self, db_connector):
        query = "INSERT INTO pedidos (cliente_id, fecha, estado) VALUES (%s, %s, %s)"
        params = (self.cliente_id, self.fecha, self.estado)
        return db_connector.execute(query, params)

    def actualizar(self, db_connector, pedido_id):
        query = "UPDATE pedidos SET cliente_id=%s, fecha=%s, estado=%s WHERE id=%s"
        params = (self.cliente_id, self.fecha, self.estado, pedido_id)
        return db_connector.execute(query, params)

    @staticmethod
    def eliminar(db_connector, pedido_id):
        query = "DELETE FROM pedidos WHERE id=%s"
        params = (pedido_id,)
        return db_connector.execute(query, params)

