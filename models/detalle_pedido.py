"""
Modelo DetallePedido
"""
from models.base_model import BaseModel


class DetallePedido(BaseModel):
    def __init__(self, pedido_id, producto_id, cantidad, precio_unitario):
        self.pedido_id = pedido_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def guardar(self, db_connector):
        query = "INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
        params = (self.pedido_id, self.producto_id, self.cantidad, self.precio_unitario)
        return db_connector.execute(query, params)

    def actualizar(self, db_connector, detalle_id):
        query = "UPDATE detalle_pedido SET pedido_id=%s, producto_id=%s, cantidad=%s, precio_unitario=%s WHERE id=%s"
        params = (self.pedido_id, self.producto_id, self.cantidad, self.precio_unitario, detalle_id)
        return db_connector.execute(query, params)

    @staticmethod
    def eliminar(db_connector, detalle_id):
        query = "DELETE FROM detalle_pedido WHERE id=%s"
        params = (detalle_id,)
        return db_connector.execute(query, params)

