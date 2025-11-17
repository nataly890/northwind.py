"""
Vista para gestión de Detalles de Pedido
"""
import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView, BG_COLOR, FRAME_COLOR, FG_COLOR, ACCENT_COLOR
from views.base_view import COLOR_GREEN, COLOR_BLUE, COLOR_ORANGE, COLOR_RED, COLOR_PURPLE


class VistaDetallePedido:
    def __init__(self, parent_frame):
        self.frame = ttk.Frame(parent_frame)
        self.frame.configure(style="TFrame")
        
        # Título
        tk.Label(self.frame, text="Detalles de Órdenes", 
                font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)
        
        # Frame del formulario
        self.frame_form = tk.LabelFrame(self.frame, text="Detalle", padx=20, pady=15, 
                                        bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), 
                                        bd=1, relief="groove")
        self.frame_form.pack(anchor="w", padx=12, pady=8, fill="x")
        
        # Campos del formulario
        tk.Label(self.frame_form, text="Pedido ID:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_pedido_id = tk.Entry(self.frame_form, width=12, state="readonly")
        self.entry_pedido_id.grid(row=0, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Producto ID:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_producto_id = tk.Entry(self.frame_form, width=12, state="readonly")
        self.entry_producto_id.grid(row=1, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Cantidad:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_cantidad = tk.Entry(self.frame_form, width=12, state="readonly")
        self.entry_cantidad.grid(row=2, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Precio unit.:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_precio = tk.Entry(self.frame_form, width=12, state="readonly")
        self.entry_precio.grid(row=3, column=1, padx=6, pady=4)
        
        # Botones
        self.frame_btns = tk.Frame(self.frame_form, bg=FRAME_COLOR)
        self.frame_btns.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.btn_guardar = tk.Button(self.frame_btns, text="Guardar")
        BaseView.style_button(self.btn_guardar, COLOR_GREEN, "#55a058")
        
        self.btn_mostrar = tk.Button(self.frame_btns, text="Mostrar")
        BaseView.style_button(self.btn_mostrar, COLOR_BLUE, "#0069D9")
        
        self.btn_actualizar = tk.Button(self.frame_btns, text="Actualizar")
        BaseView.style_button(self.btn_actualizar, COLOR_ORANGE, "#E0A800", fg_color=FG_COLOR)
        
        self.btn_eliminar = tk.Button(self.frame_btns, text="Eliminar")
        BaseView.style_button(self.btn_eliminar, COLOR_RED, "#C82333")
        
        self.btn_limpiar = tk.Button(self.frame_btns, text="Limpiar")
        BaseView.style_button(self.btn_limpiar, COLOR_PURPLE, "#5A32A3")
        
        for b in (self.btn_guardar, self.btn_mostrar, self.btn_actualizar, 
                 self.btn_eliminar, self.btn_limpiar):
            b.pack(side="left", padx=8)
        
        # Treeview
        cols = ("id", "pedido_id", "producto_id", "cantidad", "precio_unitario")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings")
        self.tree.tag_configure('oddrow', background="#F7F7F7")
        self.tree.tag_configure('evenrow', background=FRAME_COLOR)
        
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=150 if c != "id" else 60)
        
        self.tree.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")
    
    def get_entries(self):
        """Retorna los valores de los campos del formulario"""
        return {
            'pedido_id': self.entry_pedido_id.get().strip(),
            'producto_id': self.entry_producto_id.get().strip(),
            'cantidad': self.entry_cantidad.get().strip(),
            'precio': self.entry_precio.get().strip()
        }
    
    def set_entries(self, pedido_id, producto_id, cantidad, precio):
        """Establece los valores en los campos del formulario"""
        for entry, value in zip([self.entry_pedido_id, self.entry_producto_id, 
                                self.entry_cantidad, self.entry_precio], 
                               [pedido_id, producto_id, cantidad, precio]):
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.config(state='readonly')
    
    def limpiar_entries(self):
        """Limpia todos los campos del formulario"""
        for entry in [self.entry_pedido_id, self.entry_producto_id, 
                     self.entry_cantidad, self.entry_precio]:
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.config(state='readonly')
    
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

