"""
Vista para gestión de Pedidos
"""
import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView, BG_COLOR, FRAME_COLOR, FG_COLOR, ACCENT_COLOR
from views.base_view import COLOR_GREEN, COLOR_BLUE, COLOR_ORANGE, COLOR_RED, COLOR_PURPLE


class VistaPedido:
    def __init__(self, parent_frame):
        self.frame = ttk.Frame(parent_frame)
        self.frame.configure(style="TFrame")
        
        # Título
        tk.Label(self.frame, text="Registro de Órdenes", 
                font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)
        
        # Frame del formulario
        self.frame_form = tk.LabelFrame(self.frame, text="Pedido", padx=20, pady=15, 
                                        bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), 
                                        bd=1, relief="groove")
        self.frame_form.pack(anchor="w", padx=12, pady=8, fill="x")
        
        # Campos del formulario
        tk.Label(self.frame_form, text="Cliente ID:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_cliente_id = tk.Entry(self.frame_form, width=20, state="readonly")
        self.entry_cliente_id.grid(row=0, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Fecha (YYYY-MM-DD):", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_fecha = tk.Entry(self.frame_form, width=20, state="readonly")
        self.entry_fecha.grid(row=1, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Estado:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_estado = tk.Entry(self.frame_form, width=20, state="readonly")
        self.entry_estado.grid(row=2, column=1, padx=6, pady=4)
        
        # Botones
        self.frame_btns = tk.Frame(self.frame_form, bg=FRAME_COLOR)
        self.frame_btns.grid(row=3, column=0, columnspan=2, pady=10)
        
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
        cols = ("id", "cliente_id", "fecha", "estado")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings")
        self.tree.tag_configure('oddrow', background="#F7F7F7")
        self.tree.tag_configure('evenrow', background=FRAME_COLOR)
        
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=180 if c != "id" else 60)
        
        self.tree.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")
    
    def get_entries(self):
        """Retorna los valores de los campos del formulario"""
        return {
            'cliente_id': self.entry_cliente_id.get().strip(),
            'fecha': self.entry_fecha.get().strip(),
            'estado': self.entry_estado.get().strip()
        }
    
    def set_entries(self, cliente_id, fecha, estado):
        """Establece los valores en los campos del formulario"""
        for entry, value in zip([self.entry_cliente_id, self.entry_fecha, self.entry_estado], 
                               [cliente_id, fecha, estado]):
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.config(state='readonly')
    
    def limpiar_entries(self):
        """Limpia todos los campos del formulario"""
        for entry in [self.entry_cliente_id, self.entry_fecha, self.entry_estado]:
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

