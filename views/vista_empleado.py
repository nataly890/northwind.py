"""
Vista para gestión de Empleados
"""
import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
from shutil import copyfile
import os
from views.base_view import BaseView, BG_COLOR, FRAME_COLOR, FG_COLOR, ACCENT_COLOR, ACCENT_HOVER_COLOR
from views.base_view import COLOR_GREEN, COLOR_BLUE, COLOR_ORANGE, COLOR_RED, COLOR_PURPLE
from utils.config import IMAGES_DIR


class VistaEmpleado:
    def __init__(self, parent_frame):
        self.frame = ttk.Frame(parent_frame)
        self.frame.configure(style="TFrame")
        
        # Título
        tk.Label(self.frame, text="Administración de Personal", 
                font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)
        
        # Frame del formulario
        self.frame_form = tk.LabelFrame(self.frame, text="Empleado", padx=20, pady=15, 
                                        bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), 
                                        bd=1, relief="groove")
        self.frame_form.pack(anchor="w", padx=12, pady=8, fill="x")
        
        # Campos del formulario
        tk.Label(self.frame_form, text="Apellido:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_apellido = tk.Entry(self.frame_form, width=30, state="readonly")
        self.entry_apellido.grid(row=0, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Nombre:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nombre = tk.Entry(self.frame_form, width=30, state="readonly")
        self.entry_nombre.grid(row=1, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Fecha Nac.:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_fecha = DateEntry(self.frame_form, date_pattern="yyyy-mm-dd", state="readonly")
        self.entry_fecha.grid(row=2, column=1, padx=6, pady=4)
        
        tk.Label(self.frame_form, text="Foto (ruta):", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_foto = tk.Entry(self.frame_form, width=40, state="readonly")
        self.entry_foto.grid(row=3, column=1, padx=6, pady=4)
        
        self.btn_foto = tk.Button(self.frame_form, text="Seleccionar...", width=12)
        self.btn_foto.grid(row=3, column=2, padx=6)
        BaseView.style_button(self.btn_foto, ACCENT_COLOR, ACCENT_HOVER_COLOR, fg_color=FRAME_COLOR)
        
        tk.Label(self.frame_form, text="Notas:", bg=FRAME_COLOR, fg=FG_COLOR, 
                font=("Calibri", 10)).grid(row=4, column=0, sticky="nw", pady=5)
        self.entry_notas = tk.Text(self.frame_form, width=50, height=4, state=tk.DISABLED)
        self.entry_notas.grid(row=4, column=1, padx=6, pady=4)
        
        # Botones
        self.frame_btns = tk.Frame(self.frame_form, bg=FRAME_COLOR)
        self.frame_btns.grid(row=5, column=0, columnspan=3, pady=10)
        
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
        cols = ("id", "last_name", "first_name", "birth_date", "photo", "notes")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings")
        self.tree.tag_configure('oddrow', background="#F7F7F7")
        self.tree.tag_configure('evenrow', background=FRAME_COLOR)
        
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").capitalize())
            self.tree.column(c, width=160 if c != "id" else 60)
        
        self.tree.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")
    
    def seleccionar_foto(self):
        """Abre el diálogo para seleccionar una foto"""
        archivo = filedialog.askopenfilename(
            title="Selecciona imagen", 
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif")]
        )
        if not archivo:
            return
        
        nombre = os.path.basename(archivo)
        destino = os.path.join(IMAGES_DIR, nombre)
        
        try:
            copyfile(archivo, destino)
            self.entry_foto.config(state='normal')
            self.entry_foto.delete(0, tk.END)
            self.entry_foto.insert(0, destino)
            self.entry_foto.config(state='readonly')
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"No se pudo copiar la imagen: {e}")
    
    def get_entries(self):
        """Retorna los valores de los campos del formulario"""
        return {
            'apellido': self.entry_apellido.get().strip(),
            'nombre': self.entry_nombre.get().strip(),
            'fecha': self.entry_fecha.get().strip(),
            'foto': self.entry_foto.get().strip(),
            'notas': self.entry_notas.get("1.0", tk.END).strip()
        }
    
    def set_entries(self, apellido, nombre, fecha, foto, notas):
        """Establece los valores en los campos del formulario"""
        for entry, value in zip([self.entry_apellido, self.entry_nombre], [apellido, nombre]):
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.config(state='readonly')
        
        try:
            self.entry_fecha.config(state='normal')
            self.entry_fecha.set_date(fecha)
            self.entry_fecha.config(state='readonly')
        except Exception:
            self.entry_fecha.config(state='normal')
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.config(state='readonly')
        
        self.entry_foto.config(state='normal')
        self.entry_foto.delete(0, tk.END)
        self.entry_foto.insert(0, foto or "")
        self.entry_foto.config(state='readonly')
        
        self.entry_notas.config(state='normal')
        self.entry_notas.delete("1.0", tk.END)
        self.entry_notas.insert("1.0", notas or "")
        self.entry_notas.config(state=tk.DISABLED)
    
    def limpiar_entries(self):
        """Limpia todos los campos del formulario"""
        for entry in [self.entry_apellido, self.entry_nombre, self.entry_foto]:
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.config(state='readonly')
        
        self.entry_fecha.config(state='normal')
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.config(state='readonly')
        
        self.entry_notas.config(state='normal')
        self.entry_notas.delete("1.0", tk.END)
        self.entry_notas.config(state=tk.DISABLED)
    
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

