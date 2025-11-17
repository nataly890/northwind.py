"""
Controlador para gestión de Pedidos
"""
from tkinter import messagebox
from models.pedido import Pedido


class ControladorPedido:
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
        """Lista todos los pedidos"""
        rows = self.db.fetchall("SELECT id,cliente_id,fecha,estado FROM pedidos ORDER BY id")
        self.vista.populate_tree(rows)
    
    def guardar(self):
        """Guarda un nuevo pedido"""
        datos = self.vista.get_entries()
        
        try:
            cliente_id = int(datos['cliente_id'])
        except ValueError:
            messagebox.showerror("Error", "Cliente ID debe ser entero")
            return
        
        if not datos['fecha'] or not datos['estado']:
            messagebox.showwarning("Validación", "Fecha y estado son obligatorios.")
            return
        
        nuevo_pedido = Pedido(
            cliente_id=cliente_id,
            fecha=datos['fecha'],
            estado=datos['estado']
        )
        
        if nuevo_pedido.guardar(self.db):
            messagebox.showinfo("OK", "Pedido guardado")
            self.listar()
            self.limpiar()
    
    def seleccionar(self, evt):
        """Selecciona un pedido de la tabla"""
        sel = self.vista.tree.selection()
        if not sel:
            return
        
        v = self.vista.tree.item(sel[0], "values")
        self.vista.set_entries(v[1], v[2], v[3])
    
    def actualizar(self):
        """Actualiza un pedido existente"""
        pedido_id = self.vista.get_selected_id()
        if not pedido_id:
            messagebox.showwarning("Seleccionar", "Selecciona un pedido")
            return
        
        datos = self.vista.get_entries()
        
        try:
            cliente_id = int(datos['cliente_id'])
        except ValueError:
            messagebox.showerror("Error", "Cliente ID debe ser entero")
            return
        
        pedido_actualizado = Pedido(
            cliente_id=cliente_id,
            fecha=datos['fecha'],
            estado=datos['estado']
        )
        
        if pedido_actualizado.actualizar(self.db, pedido_id):
            messagebox.showinfo("OK", "Pedido actualizado")
            self.listar()
            self.limpiar()
    
    def eliminar(self):
        """Elimina un pedido"""
        pedido_id = self.vista.get_selected_id()
        if not pedido_id:
            messagebox.showwarning("Seleccionar", "Selecciona un pedido")
            return
        
        if messagebox.askyesno("Confirmar", "Eliminar pedido?"):
            if Pedido.eliminar(self.db, pedido_id):
                messagebox.showinfo("OK", "Pedido eliminado")
                self.listar()
                self.limpiar()
    
    def limpiar(self):
        """Limpia los campos del formulario"""
        self.vista.limpiar_entries()

