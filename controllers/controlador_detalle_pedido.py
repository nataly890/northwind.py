"""
Controlador para gestión de Detalles de Pedido
"""
from tkinter import messagebox
from models.detalle_pedido import DetallePedido


class ControladorDetallePedido:
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
        """Lista todos los detalles de pedido"""
        rows = self.db.fetchall("SELECT id,pedido_id,producto_id,cantidad,precio_unitario FROM detalle_pedido ORDER BY id")
        self.vista.populate_tree(rows)
    
    def guardar(self):
        """Guarda un nuevo detalle de pedido"""
        datos = self.vista.get_entries()
        
        try:
            pedido_id = int(datos['pedido_id'])
            producto_id = int(datos['producto_id'])
            cantidad = int(datos['cantidad'])
            precio = float(datos['precio'])
        except ValueError:
            messagebox.showerror("Error", "IDs y cantidad deben ser enteros; precio debe ser decimal")
            return
        
        nuevo_detalle = DetallePedido(
            pedido_id=pedido_id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio
        )
        
        if nuevo_detalle.guardar(self.db):
            messagebox.showinfo("OK", "Detalle guardado")
            self.listar()
            self.limpiar()
    
    def seleccionar(self, evt):
        """Selecciona un detalle de la tabla"""
        sel = self.vista.tree.selection()
        if not sel:
            return
        
        v = self.vista.tree.item(sel[0], "values")
        self.vista.set_entries(v[1], v[2], v[3], v[4])
    
    def actualizar(self):
        """Actualiza un detalle existente"""
        detalle_id = self.vista.get_selected_id()
        if not detalle_id:
            messagebox.showwarning("Seleccionar", "Selecciona un detalle")
            return
        
        datos = self.vista.get_entries()
        
        try:
            pedido_id = int(datos['pedido_id'])
            producto_id = int(datos['producto_id'])
            cantidad = int(datos['cantidad'])
            precio = float(datos['precio'])
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto")
            return
        
        detalle_actualizado = DetallePedido(
            pedido_id=pedido_id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio
        )
        
        if detalle_actualizado.actualizar(self.db, detalle_id):
            messagebox.showinfo("OK", "Detalle actualizado")
            self.listar()
            self.limpiar()
    
    def eliminar(self):
        """Elimina un detalle"""
        detalle_id = self.vista.get_selected_id()
        if not detalle_id:
            messagebox.showwarning("Seleccionar", "Selecciona un detalle")
            return
        
        if messagebox.askyesno("Confirmar", "Eliminar detalle?"):
            if DetallePedido.eliminar(self.db, detalle_id):
                messagebox.showinfo("OK", "Detalle eliminado")
                self.listar()
                self.limpiar()
    
    def limpiar(self):
        """Limpia los campos del formulario"""
        self.vista.limpiar_entries()

