"""
Controlador para gestión de Empleados
"""
from tkinter import messagebox
from models.empleado import Empleado


class ControladorEmpleado:
    def __init__(self, vista, db):
        self.vista = vista
        self.db = db
        self._bind_events()
        self.listar()
    
    def _bind_events(self):
        """Vincula los eventos de la vista con los métodos del controlador"""
        self.vista.btn_foto.config(command=self.vista.seleccionar_foto)
        self.vista.btn_guardar.config(command=self.guardar)
        self.vista.btn_mostrar.config(command=self.listar)
        self.vista.btn_actualizar.config(command=self.actualizar)
        self.vista.btn_eliminar.config(command=self.eliminar)
        self.vista.btn_limpiar.config(command=self.limpiar)
        self.vista.tree.bind("<<TreeviewSelect>>", self.seleccionar)
    
    def listar(self):
        """Lista todos los empleados"""
        rows = self.db.fetchall("SELECT id,last_name,first_name,birth_date,photo,notes FROM empleados ORDER BY id")
        self.vista.populate_tree(rows)
    
    def guardar(self):
        """Guarda un nuevo empleado"""
        datos = self.vista.get_entries()
        
        if not datos['apellido'] or not datos['nombre']:
            messagebox.showwarning("Validación", "Apellido y nombre son obligatorios.")
            return
        
        nuevo_empleado = Empleado(
            last_name=datos['apellido'],
            first_name=datos['nombre'],
            birth_date=datos['fecha'],
            photo=datos['foto'],
            notes=datos['notas']
        )
        
        if nuevo_empleado.guardar(self.db):
            messagebox.showinfo("OK", "Empleado guardado")
            self.listar()
            self.limpiar()
    
    def seleccionar(self, evt):
        """Selecciona un empleado de la tabla"""
        sel = self.vista.tree.selection()
        if not sel:
            return
        
        v = self.vista.tree.item(sel[0], "values")
        self.vista.set_entries(v[1], v[2], v[3], v[4], v[5])
    
    def actualizar(self):
        """Actualiza un empleado existente"""
        empleado_id = self.vista.get_selected_id()
        if not empleado_id:
            messagebox.showwarning("Seleccionar", "Selecciona un empleado")
            return
        
        datos = self.vista.get_entries()
        
        empleado_actualizado = Empleado(
            last_name=datos['apellido'],
            first_name=datos['nombre'],
            birth_date=datos['fecha'],
            photo=datos['foto'],
            notes=datos['notas']
        )
        
        if empleado_actualizado.actualizar(self.db, empleado_id):
            messagebox.showinfo("OK", "Empleado actualizado")
            self.listar()
    
    def eliminar(self):
        """Elimina un empleado"""
        empleado_id = self.vista.get_selected_id()
        if not empleado_id:
            messagebox.showwarning("Seleccionar", "Selecciona un empleado")
            return
        
        if messagebox.askyesno("Confirmar", "Eliminar empleado?"):
            if Empleado.eliminar(self.db, empleado_id):
                messagebox.showinfo("OK", "Empleado eliminado")
                self.listar()
                self.limpiar()
    
    def limpiar(self):
        """Limpia los campos del formulario"""
        self.vista.limpiar_entries()

