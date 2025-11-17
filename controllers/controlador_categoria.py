"""
Controlador para gestión de Categorías
"""
from tkinter import messagebox
from models.categoria import Categoria


class ControladorCategoria:
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
        """Lista todas las categorías"""
        rows = self.db.fetchall("SELECT id,nombre,descripcion FROM categorias ORDER BY id")
        self.vista.populate_tree(rows)
    
    def guardar(self):
        """Guarda una nueva categoría"""
        datos = self.vista.get_entries()
        if not datos['nombre']:
            messagebox.showwarning("Validación", "Nombre es obligatorio")
            return
        
        nueva_categoria = Categoria(
            nombre=datos['nombre'],
            descripcion=datos['descripcion']
        )
        
        if nueva_categoria.guardar(self.db):
            messagebox.showinfo("OK", "Categoría guardada")
            self.limpiar()
            self.listar()
    
    def seleccionar(self, evt):
        """Selecciona una categoría de la tabla"""
        sel = self.vista.tree.selection()
        if not sel:
            return
        
        v = self.vista.tree.item(sel[0], "values")
        self.vista.set_entries(v[0], v[1], v[2])
    
    def actualizar(self):
        """Actualiza una categoría existente"""
        datos = self.vista.get_entries()
        try:
            idc = int(datos['id'])
        except (ValueError, TypeError):
            messagebox.showerror("Error", "No se pudo obtener un ID válido del formulario.")
            return
        
        if not datos['nombre']:
            messagebox.showwarning("Validación", "Nombre es obligatorio")
            return
        
        categoria_actualizada = Categoria(
            nombre=datos['nombre'],
            descripcion=datos['descripcion']
        )
        
        if categoria_actualizada.actualizar(self.db, idc):
            messagebox.showinfo("OK", "Categoría actualizada")
            self.listar()
            self.limpiar()
    
    def eliminar(self):
        """Elimina una categoría"""
        categoria_id = self.vista.get_selected_id()
        if not categoria_id:
            messagebox.showwarning("Seleccionar", "Selecciona una categoría")
            return
        
        if messagebox.askyesno("Confirmar", "Eliminar categoría?"):
            if Categoria.eliminar(self.db, categoria_id):
                messagebox.showinfo("OK", "Categoría eliminada")
                self.limpiar()
                self.listar()
    
    def limpiar(self):
        """Limpia los campos del formulario"""
        self.vista.limpiar_entries()

