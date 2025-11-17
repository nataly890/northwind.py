"""
Controlador para gestión de Productos
"""
from tkinter import messagebox
from models.producto import Producto


class ControladorProducto:
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
    
    def get_category_map(self):
        """Devuelve un diccionario para mapear nombres de categoría a IDs y viceversa"""
        rows = self.db.fetchall("SELECT id, nombre FROM categorias")
        name_to_id = {name: id for id, name in rows}
        id_to_name = {id: name for id, name in rows}
        return name_to_id, id_to_name
    
    def listar(self):
        """Lista todos los productos"""
        query = """
            SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, 
                   COALESCE(c.nombre, 'N/A'), COALESCE(c.descripcion, 'N/A')
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            ORDER BY p.id
        """
        rows = self.db.fetchall(query)
        self.vista.populate_tree(rows)
        
        # Actualizar combobox
        _, id_to_name = self.get_category_map()
        self.vista.update_categoria_combo(id_to_name)
    
    def guardar(self):
        """Guarda un nuevo producto"""
        datos = self.vista.get_entries()
        name_to_id, _ = self.get_category_map()
        
        cat_name = datos['categoria']
        categoria_id = name_to_id.get(cat_name)
        
        if not datos['nombre'] or not datos['precio'] or not datos['stock']:
            messagebox.showwarning("Validación", "Nombre, precio y stock son obligatorios.")
            return
        
        try:
            precio = float(datos['precio'])
            stock = int(datos['stock'])
        except ValueError:
            messagebox.showerror("Error", "Precio o stock con formato incorrecto")
            return
        
        nuevo_producto = Producto(
            nombre=datos['nombre'],
            descripcion=datos['descripcion'],
            precio=precio,
            stock=stock,
            categoria_id=categoria_id
        )
        
        if nuevo_producto.guardar(self.db):
            messagebox.showinfo("OK", "Producto guardado")
            self.listar()
            self.limpiar()
    
    def seleccionar(self, evt):
        """Selecciona un producto de la tabla"""
        sel = self.vista.tree.selection()
        if not sel:
            return
        
        v = self.vista.tree.item(sel[0], "values")
        self.vista.set_entries(v[0], v[1], v[2], v[3], v[4], v[5])
    
    def actualizar(self):
        """Actualiza un producto existente"""
        producto_id = self.vista.get_selected_id()
        if not producto_id:
            messagebox.showwarning("Seleccionar", "Selecciona un producto")
            return
        
        try:
            idp = int(producto_id)
        except ValueError:
            messagebox.showerror("Error", "ID de producto inválido")
            return
        
        datos = self.vista.get_entries()
        name_to_id, _ = self.get_category_map()
        
        cat_name = datos['categoria']
        categoria_id = name_to_id.get(cat_name)
        
        if not datos['nombre'] or not datos['precio'] or not datos['stock']:
            messagebox.showwarning("Validación", "Nombre, precio y stock son obligatorios.")
            return
        
        try:
            precio = float(datos['precio'])
            stock = int(datos['stock'])
        except ValueError:
            messagebox.showerror("Error", "Precio o stock con formato incorrecto")
            return
        
        producto_actualizado = Producto(
            nombre=datos['nombre'],
            descripcion=datos['descripcion'],
            precio=precio,
            stock=stock,
            categoria_id=categoria_id
        )
        
        if producto_actualizado.actualizar(self.db, idp):
            messagebox.showinfo("OK", "Producto actualizado")
            self.listar()
            self.limpiar()
    
    def eliminar(self):
        """Elimina un producto"""
        producto_id = self.vista.get_selected_id()
        if not producto_id:
            messagebox.showwarning("Seleccionar", "Selecciona un producto")
            return
        
        try:
            idp = int(producto_id)
        except ValueError:
            messagebox.showerror("Error", "ID de producto inválido")
            return
        
        if messagebox.askyesno("Confirmar", "Eliminar producto?"):
            if Producto.eliminar(self.db, idp):
                messagebox.showinfo("OK", "Producto eliminado")
                self.listar()
                self.limpiar()
    
    def limpiar(self):
        """Limpia los campos del formulario"""
        self.vista.limpiar_entries()

