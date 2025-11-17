"""
Vista para gestión de Clientes
"""
import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView, BG_COLOR, FRAME_COLOR, FG_COLOR, ACCENT_COLOR
from views.base_view import COLOR_GREEN, COLOR_BLUE, COLOR_ORANGE, COLOR_RED, COLOR_PURPLE


class VistaCliente:
    def __init__(self, parent_frame):
        self.frame = ttk.Frame(parent_frame)
        self.frame.configure(style="TFrame")
        
        # Título
        tk.Label(self.frame, text="Gestión de Clientes Frecuentes", 
                font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)
        
        # Frame del formulario
        self.frame_form = tk.LabelFrame(self.frame, text="Formulario", padx=20, pady=15, 
                                        bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), 
                                        bd=1, relief="groove")
        self.frame_form.pack(anchor="w", padx=12, pady=8, fill="x")
        
        # Campos del formulario
        tk.Label(self.frame_form, text="Nombre:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nombre = tk.Entry(self.frame_form, width=50, state="readonly")
        self.entry_nombre.grid(row=0, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Correo:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_correo = tk.Entry(self.frame_form, width=50, state="readonly")
        self.entry_correo.grid(row=1, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Teléfono:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_telefono = tk.Entry(self.frame_form, width=50, state="readonly")
        self.entry_telefono.grid(row=2, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Dirección:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_direccion = tk.Entry(self.frame_form, width=50, state="readonly")
        self.entry_direccion.grid(row=3, column=1, padx=6, pady=4)
        
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
        cols = ("id", "nombre", "correo", "telefono", "direccion")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings", 
                                selectmode="browse", height=10)
        self.tree.tag_configure('oddrow', background="#F7F7F7")
        self.tree.tag_configure('evenrow', background=FRAME_COLOR)
        
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            width = 60 if c == "id" else 100 if c == "telefono" else 250
            self.tree.column(c, width=width, anchor="w")
        
        self.tree.column("correo", width=250)
        self.tree.column("direccion", width=300)
        self.tree.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")
    
    def get_entries(self):
        """Retorna los valores de los campos del formulario"""
        return {
            'nombre': self.entry_nombre.get().strip(),
            'correo': self.entry_correo.get().strip(),
            'telefono': self.entry_telefono.get().strip(),
            'direccion': self.entry_direccion.get().strip()
        }
    
    def set_entries(self, nombre, correo, telefono, direccion):
        """Establece los valores en los campos del formulario"""
        for entry, value in zip([self.entry_nombre, self.entry_correo, 
                                self.entry_telefono, self.entry_direccion], 
                               [nombre, correo, telefono, direccion]):
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.config(state='readonly')
    
    def limpiar_entries(self):
        """Limpia todos los campos del formulario"""
        for entry in [self.entry_nombre, self.entry_correo, 
                     self.entry_telefono, self.entry_direccion]:
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

