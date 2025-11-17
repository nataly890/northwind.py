"""
Vista para gestión de Productos
"""
import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView, BG_COLOR, FRAME_COLOR, FG_COLOR, ACCENT_COLOR
from views.base_view import COLOR_GREEN, COLOR_BLUE, COLOR_ORANGE, COLOR_RED, COLOR_PURPLE


class VistaProducto:
    def __init__(self, parent_frame):
        self.frame = ttk.Frame(parent_frame)
        self.frame.configure(style="TFrame")
        
        # Título
        tk.Label(self.frame, text="Control de Inventario", 
                font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)
        
        # Frame del formulario
        self.frame_form = tk.LabelFrame(self.frame, text="Producto", padx=20, pady=15, 
                                        bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), 
                                        bd=1, relief="groove")
        self.frame_form.pack(anchor="w", padx=12, pady=8, fill="x")
        
        # Fila 1: ID y Nombre
        tk.Label(self.frame_form, text="ID:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_id = tk.Entry(self.frame_form, width=10, state='readonly')
        self.entry_id.grid(row=0, column=1, padx=(0, 20), pady=4, sticky="w")
        
        tk.Label(self.frame_form, text="Nombre:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=0, column=2, sticky="w", pady=5)
        self.entry_nombre = tk.Entry(self.frame_form, width=40, state="readonly")
        self.entry_nombre.grid(row=0, column=3, padx=6, pady=4, sticky="w")
        
        # Fila 2: Precio y Stock
        tk.Label(self.frame_form, text="Precio:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_precio = tk.Entry(self.frame_form, width=10, state="readonly")
        self.entry_precio.grid(row=1, column=1, padx=(0, 20), pady=4, sticky="w")
        
        tk.Label(self.frame_form, text="Stock:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=1, column=2, sticky="w", pady=5)
        self.entry_stock = tk.Entry(self.frame_form, width=15, state="readonly")
        self.entry_stock.grid(row=1, column=3, sticky="w", padx=6, pady=4)
        
        # Fila 3: Categoría y Descripción
        tk.Label(self.frame_form, text="Categoría:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.combo_categoria = ttk.Combobox(self.frame_form, width=25, state="readonly")
        self.combo_categoria.grid(row=2, column=1, columnspan=3, sticky="w", padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Descripción:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_desc = tk.Entry(self.frame_form, width=60, state="readonly")
        self.entry_desc.grid(row=3, column=1, columnspan=3, padx=6, pady=4, sticky="w")
        
        # Botones
        self.frame_btns = tk.Frame(self.frame_form, bg=FRAME_COLOR)
        self.frame_btns.grid(row=4, column=0, columnspan=4, pady=10)
        
        self.btn_guardar = tk.Button(self.frame_btns, text="Guardar")
        BaseView.style_button(self.btn_guardar, COLOR_GREEN, "#55a058")
        
        self.btn_mostrar = tk.Button(self.frame_btns, text="Mostrar")
        BaseView.style_button(self.btn_mostrar, COLOR_BLUE, "#0069D9")
        
        self.btn_actualizar = tk.Button(self.frame_btns, text="Actualizar")
        BaseView.style_button(self.btn_actualizar, COLOR_ORANGE, "#E0A800", fg_color=FG_COLOR)
        
        self.btn_eliminar = tk.Button(self.frame_btns, text="Eliminar")
        BaseView.style_button(self.btn_eliminar, COLOR_RED, "#7E22DF")
        
        self.btn_limpiar = tk.Button(self.frame_btns, text="Limpiar")
        BaseView.style_button(self.btn_limpiar, COLOR_PURPLE, "#5A32A3")
        
        for b in (self.btn_guardar, self.btn_mostrar, self.btn_actualizar, 
                 self.btn_eliminar, self.btn_limpiar):
            b.pack(side="left", padx=8)
        
        # Treeview
        cols = ("id", "nombre", "descripcion", "precio", "stock", "categoria", "desc_categoria")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings")
        self.tree.tag_configure('oddrow', background="#F7F7F7")
        self.tree.tag_configure('evenrow', background=FRAME_COLOR)
        
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").capitalize())
            self.tree.column(c, width=140 if c not in ("id", "precio", "stock") else 60)
        
        self.tree.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")
    
    def get_entries(self):
        """Retorna los valores de los campos del formulario"""
        return {
            'id': self.entry_id.get().strip(),
            'nombre': self.entry_nombre.get().strip(),
            'descripcion': self.entry_desc.get().strip(),
            'precio': self.entry_precio.get().strip(),
            'stock': self.entry_stock.get().strip(),
            'categoria': self.combo_categoria.get()
        }
    
    def set_entries(self, id_val, nombre, descripcion, precio, stock, categoria):
        """Establece los valores en los campos del formulario"""
        for entry, value in zip([self.entry_id, self.entry_nombre, self.entry_desc, 
                                self.entry_precio, self.entry_stock], 
                               [id_val, nombre, descripcion, precio, stock]):
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.config(state='readonly')
        self.combo_categoria.set(categoria if categoria != "N/A" else "")
    
    def limpiar_entries(self):
        """Limpia todos los campos del formulario"""
        for entry in [self.entry_id, self.entry_nombre, self.entry_desc, 
                     self.entry_precio, self.entry_stock]:
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.config(state='readonly')
        self.combo_categoria.set('')
    
    def get_selected_id(self):
        """Retorna el ID del elemento seleccionado en el tree"""
        sel = self.tree.selection()
        if sel:
            return self.tree.item(sel[0], "values")[0]
        return None
    
    def populate_tree(self, data):
        """Llena el treeview con los datos"""
        for r in self.tree.get_children():
            self.tree.delete(r)
        for i, row in enumerate(data):
            tag = 'evenrow' if i % 2 != 0 else 'oddrow'
            self.tree.insert("", "end", values=row, tags=(tag,))
    
    def update_categoria_combo(self, categorias):
        """Actualiza el combobox de categorías"""
        self.combo_categoria['values'] = sorted(list(categorias.values()))

