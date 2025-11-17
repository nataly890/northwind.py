"""
Controlador para gestión de Clientes
"""
from tkinter import messagebox
from models.cliente import Cliente


class ControladorCliente:
    def __init__(self, vista, db):
        self.vista = vista
        self.db = db
        self._bind_events()
        self.listar()
    
    def _bind_events(self):
        """Vincula los eventos de la vista con los métodos del controlador"""
        self.vista.btn_guardar.config(command=self.guardar)
        self.vista.btn_mostrar.config(command=self.listar)
        self.vista.btn_actualizar.config(command=self.actualizar)
        self.vista.btn_eliminar.config(command=self.eliminar)
        self.vista.btn_limpiar.config(command=self.limpiar)
        self.vista.tree.bind("<<TreeviewSelect>>", self.seleccionar)
    
    def listar(self):
        """Lista todos los clientes"""
        rows = self.db.fetchall("SELECT id,nombre,correo,telefono,direccion FROM clientes ORDER BY id")
        self.vista.populate_tree(rows)
    
    def guardar(self):
        """Guarda un nuevo cliente"""
        datos = self.vista.get_entries()
        if not datos['nombre'] or not datos['correo']:
            messagebox.showwarning("Validación", "Nombre y correo son obligatorios.")
            return
        
        nuevo_cliente = Cliente(
            nombre=datos['nombre'],
            correo=datos['correo'],
            telefono=datos['telefono'],
            direccion=datos['direccion']
        )
        
        if nuevo_cliente.guardar(self.db):
            messagebox.showinfo("OK", "Cliente guardado")
            self.limpiar()
            self.listar()
    
    def seleccionar(self, evt):
        """Selecciona un cliente de la tabla"""
        sel = self.vista.tree.selection()
        if not sel:
            return
        
        v = self.vista.tree.item(sel[0], "values")
        self.vista.set_entries(v[1], v[2], v[3], v[4])
    
    def actualizar(self):
        """Actualiza un cliente existente"""
        cliente_id = self.vista.get_selected_id()
        if not cliente_id:
            messagebox.showwarning("Seleccionar", "Selecciona un cliente en la tabla.")
            return
        
        datos = self.vista.get_entries()
        if not datos['nombre'] or not datos['correo']:
            messagebox.showwarning("Validación", "Nombre y correo son obligatorios.")
            return
        
        cliente_actualizado = Cliente(
            nombre=datos['nombre'],
            correo=datos['correo'],
            telefono=datos['telefono'],
            direccion=datos['direccion']
        )
        
        if cliente_actualizado.actualizar(self.db, cliente_id):
            messagebox.showinfo("OK", "Cliente actualizado")
            self.listar()
    
    def eliminar(self):
        """Elimina un cliente"""
        cliente_id = self.vista.get_selected_id()
        if not cliente_id:
            messagebox.showwarning("Seleccionar", "Selecciona un cliente en la tabla.")
            return
        
        if messagebox.askyesno("Confirmar", "Eliminar cliente seleccionado?"):
            if Cliente.eliminar(self.db, cliente_id):
                messagebox.showinfo("OK", "Cliente eliminado")
                self.listar()
                self.limpiar()
    
    def limpiar(self):
        """Limpia los campos del formulario"""
        self.vista.limpiar_entries()

