"""
Modelo Empleado
"""
from models.base_model import BaseModel


class Empleado(BaseModel):
    def __init__(self, last_name, first_name, birth_date, photo, notes):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.photo = photo
        self.notes = notes

    def guardar(self, db_connector):
        query = "INSERT INTO empleados (last_name, first_name, birth_date, photo, notes) VALUES (%s, %s, %s, %s, %s)"
        params = (self.last_name, self.first_name, self.birth_date, self.photo, self.notes)
        return db_connector.execute(query, params)

    def actualizar(self, db_connector, empleado_id):
        query = "UPDATE empleados SET last_name=%s, first_name=%s, birth_date=%s, photo=%s, notes=%s WHERE id=%s"
        params = (self.last_name, self.first_name, self.birth_date, self.photo, self.notes, empleado_id)
        return db_connector.execute(query, params)

    @staticmethod
    def eliminar(db_connector, empleado_id):
        query = "DELETE FROM empleados WHERE id=%s"
        params = (empleado_id,)
        return db_connector.execute(query, params)

