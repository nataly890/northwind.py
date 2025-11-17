# northwind_app.py

import tkinter as tk

from tkinter import ttk, messagebox, filedialog

import mysql.connector

import os

from shutil import copyfile

from tkcalendar import DateEntry

import sys

# ---------------------------

# CONFIG - AJUSTA SI HACE FALTA

# ---------------------------

DB_CONFIG = {

    "host": "localhost",

    "user": "root",

    "password": "",         # <- pon tu contraseña si la tienes. Si no tienes, déjalo vacío.

    "database": "northwind" # <- Cambia 'mysql' por 'northwind'

}

IMAGES_DIR = "imagenes_empleados"

os.makedirs(IMAGES_DIR, exist_ok=True)



# ---------------------------

# MODELOS (INTEGRADOS)

# ---------------------------

class Cliente:

    def __init__(self, nombre, correo, telefono, direccion):

        self.nombre = nombre

        self.correo = correo

        self.telefono = telefono

        self.direccion = direccion



    def guardar(self, db_connector):

        query = "INSERT INTO clientes (nombre, correo, telefono, direccion) VALUES (%s, %s, %s, %s)"

        params = (self.nombre, self.correo, self.telefono, self.direccion)

        return db_connector.execute(query, params)



    def actualizar(self, db_connector, cliente_id):

        query = "UPDATE clientes SET nombre = %s, correo = %s, telefono = %s, direccion = %s WHERE id = %s"

        params = (self.nombre, self.correo, self.telefono, self.direccion, cliente_id)

        return db_connector.execute(query, params)



    @staticmethod

    def eliminar(db_connector, cliente_id):

        query = "DELETE FROM clientes WHERE id = %s"

        params = (cliente_id,)

        return db_connector.execute(query, params)



class Categoria:

    def __init__(self, nombre, descripcion):

        self.nombre = nombre

        self.descripcion = descripcion



    def guardar(self, db_connector):

        query = "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)"

        params = (self.nombre, self.descripcion)

        return db_connector.execute(query, params)



    def actualizar(self, db_connector, categoria_id):

        query = "UPDATE categorias SET nombre = %s, descripcion = %s WHERE categorias.id = %s"

        params = (self.nombre, self.descripcion, categoria_id)

        return db_connector.execute(query, params)



    @staticmethod

    def eliminar(db_connector, categoria_id):

        query = "DELETE FROM categorias WHERE categorias.id = %s"

        params = (categoria_id,)

        return db_connector.execute(query, params)



class Producto:

    def __init__(self, nombre, descripcion, precio, stock, categoria_id):

        self.nombre = nombre

        self.descripcion = descripcion

        self.precio = precio

        self.stock = stock

        self.categoria_id = categoria_id



    def guardar(self, db_connector):

        query = "INSERT INTO productos (nombre, descripcion, precio, stock, categoria_id) VALUES (%s, %s, %s, %s, %s)"

        params = (self.nombre, self.descripcion, self.precio, self.stock, self.categoria_id)

        return db_connector.execute(query, params)



    def actualizar(self, db_connector, producto_id):

        query = "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s, categoria_id=%s WHERE id=%s"

        params = (self.nombre, self.descripcion, self.precio, self.stock, self.categoria_id, producto_id)

        return db_connector.execute(query, params)



    @staticmethod

    def eliminar(db_connector, producto_id):

        query = "DELETE FROM productos WHERE id=%s"

        params = (producto_id,)

        return db_connector.execute(query, params)



class Pedido:

    def __init__(self, cliente_id, fecha, estado):

        self.cliente_id = cliente_id

        self.fecha = fecha

        self.estado = estado



    def guardar(self, db_connector):

        query = "INSERT INTO pedidos (cliente_id, fecha, estado) VALUES (%s, %s, %s)"

        params = (self.cliente_id, self.fecha, self.estado)

        return db_connector.execute(query, params)



    def actualizar(self, db_connector, pedido_id):

        query = "UPDATE pedidos SET cliente_id=%s, fecha=%s, estado=%s WHERE id=%s"

        params = (self.cliente_id, self.fecha, self.estado, pedido_id)

        return db_connector.execute(query, params)



    @staticmethod

    def eliminar(db_connector, pedido_id):

        query = "DELETE FROM pedidos WHERE id=%s"

        params = (pedido_id,)

        return db_connector.execute(query, params)





class Empleado:

    def __init__(self, last_name, first_name, birth_date, photo, notes):

        self.last_name = last_name

        self.first_name = first_name

        self.birth_date = birth_date

        self.photo = photo

        self.notes = notes



    def guardar(self, db_connector):

        query = "INSERT INTO empleados (last_name, first_name, birth_date, photo, notes) VALUES (%s, %s, %s, %s, %s)"

        params = (self.last_name, self.first_name, self.birth_date, self.photo, self.notes)

        return db_connector.execute(query, params)



    def actualizar(self, db_connector, empleado_id):

        query = "UPDATE empleados SET last_name=%s, first_name=%s, birth_date=%s, photo=%s, notes=%s WHERE id=%s"

        params = (self.last_name, self.first_name, self.birth_date, self.photo, self.notes, empleado_id)

        return db_connector.execute(query, params)



    @staticmethod

    def eliminar(db_connector, empleado_id):

        query = "DELETE FROM empleados WHERE id=%s"

        params = (empleado_id,)

        return db_connector.execute(query, params)



class DetallePedido:

    def __init__(self, pedido_id, producto_id, cantidad, precio_unitario):

        self.pedido_id = pedido_id

        self.producto_id = producto_id

        self.cantidad = cantidad

        self.precio_unitario = precio_unitario



    def guardar(self, db_connector):

        query = "INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"

        params = (self.pedido_id, self.producto_id, self.cantidad, self.precio_unitario)

        return db_connector.execute(query, params)



    def actualizar(self, db_connector, detalle_id):

        query = "UPDATE detalle_pedido SET pedido_id=%s, producto_id=%s, cantidad=%s, precio_unitario=%s WHERE id=%s"

        params = (self.pedido_id, self.producto_id, self.cantidad, self.precio_unitario, detalle_id)

        return db_connector.execute(query, params)



    @staticmethod

    def eliminar(db_connector, detalle_id):

        query = "DELETE FROM detalle_pedido WHERE id=%s"

        params = (detalle_id,)

        return db_connector.execute(query, params)



# ---------------------------

# DB HELPER

# ---------------------------

class DatabaseConnector:

    def __init__(self, cfg):

        self.cfg = cfg

        self.conn = None

        self.connect()



    def connect(self):

        try:

            self.conn = mysql.connector.connect(**self.cfg)

        except mysql.connector.Error as e:

            print(f"Error de conexión a la DB: {e}")

            self.conn = None # Aseguramos que la conexión es None si falla



    def execute(self, query, params=None):

        if not self.conn or not self.conn.is_connected():

            self.connect() # Intenta reconectar

            if not self.conn:

                messagebox.showerror("DB Error", "No hay conexión a la base de datos.")

                return None

        cur = None # Inicializar cur a None

        try:

            cur = self.conn.cursor()

            cur.execute(query, params or ())

            self.conn.commit()

            return cur

        except mysql.connector.Error as e:

            if self.conn:

                self.conn.rollback()

            messagebox.showerror("SQL Error", f"{e}")

            return None

        finally:

            if cur:

                cur.close()



    def fetchall(self, query, params=None):

        if not self.conn or not self.conn.is_connected():

            self.connect() # Intenta reconectar

            if not self.conn:

                messagebox.showerror("DB Error", "No hay conexión a la base de datos.")

                return []

        try:

            cur = self.conn.cursor()

            cur.execute(query, params or ())

            rows = cur.fetchall()

            return rows

        except mysql.connector.Error as e:

            messagebox.showerror("SQL Error", f"{e}")

            return []

        finally:

            if 'cur' in locals() and cur:

                cur.close()



    def close(self):

        if self.conn and self.conn.is_connected():

            self.conn.close()



# --- UI principal (Creación temprana para messageboxes) ---

root = tk.Tk()

root.withdraw() # Ocultar la ventana principal temporalmente



# conectar

db = DatabaseConnector(DB_CONFIG)



if not db.conn:

    # Si la conexión falla, mostramos el error y salimos.

    messagebox.showerror("DB Error", "No se pudo conectar a la base de datos.\nLa aplicación se cerrará.")

    root.destroy()

    sys.exit()



root.deiconify() # Hacemos visible la ventana principal de nuevo

# ---------------------------

# CREAR TABLAS SI NO EXISTEN (simplificadas)

# ---------------------------

def ensure_tables():

    db.execute("""

    CREATE TABLE IF NOT EXISTS clientes (

        id INT AUTO_INCREMENT PRIMARY KEY,

        nombre VARCHAR(150) NOT NULL,

        correo VARCHAR(150),

        telefono VARCHAR(50),

        direccion VARCHAR(200)

    )""")

    db.execute("""

    CREATE TABLE IF NOT EXISTS categorias (

        id INT AUTO_INCREMENT PRIMARY KEY,

        nombre VARCHAR(100) NOT NULL,

        descripcion TEXT

    )""")

    db.execute("""

    CREATE TABLE IF NOT EXISTS productos (

        id INT AUTO_INCREMENT PRIMARY KEY,

        nombre VARCHAR(150) NOT NULL,

        descripcion TEXT,

        precio DECIMAL(10,2),

        stock INT,

        categoria_id INT,

        FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL

    )""")

    db.execute("""

    CREATE TABLE IF NOT EXISTS pedidos (

        id INT AUTO_INCREMENT PRIMARY KEY,

        cliente_id INT,

        fecha DATE,

        estado VARCHAR(50),

        FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL

    )""")

    db.execute("""

    CREATE TABLE IF NOT EXISTS detalle_pedido (

        id INT AUTO_INCREMENT PRIMARY KEY,

        pedido_id INT,

        producto_id INT,

        cantidad INT,

        precio_unitario DECIMAL(10,2),

        FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,

        FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE SET NULL

    )""")

    db.execute("""

    CREATE TABLE IF NOT EXISTS empleados (

        id INT AUTO_INCREMENT PRIMARY KEY,

        last_name VARCHAR(100) NOT NULL,

        first_name VARCHAR(100) NOT NULL,

        birth_date DATE,

        photo VARCHAR(255),

        notes TEXT

    )""")



ensure_tables()



# ---------------------------

# UI principal

# ---------------------------



# --- Estilo de la UI ---

BG_COLOR = "#F0F8F7"       # Mint Cream

FG_COLOR = "#4A4A4A"       # Gris oscuro para texto

FRAME_COLOR = "#FFFFFF"    # Blanco para los marcos

ACCENT_COLOR = "#79B4A9"   # Verde menta suave

ACCENT_HOVER_COLOR = "#8AC4B9" # Menta más claro para hover



COLOR_GREEN = "#66BB6A"    # Verde suave

COLOR_BLUE = "#42A5F5"     # Azul suave

COLOR_ORANGE = "#FFA726"   # Naranja suave

COLOR_RED = "#EF5350"      # Rojo coral suave

COLOR_PURPLE = "#AB47BC"   # Púrpura suave



root.title("Northwind - Gestión")

root.geometry("1200x750")

root.configure(bg=BG_COLOR)



# --- Configuración de Estilos TTK ---

style = ttk.Style(root)

style.theme_use("clam")



# Estilo del Notebook (pestañas)

style.configure("TNotebook", background=BG_COLOR, borderwidth=0)

style.configure("TNotebook.Tab", background=BG_COLOR, foreground="#6c757d", padding=[15, 8], font=("Calibri", 11, "bold"), borderwidth=0)

style.map("TNotebook.Tab", background=[("selected", FRAME_COLOR)], foreground=[("selected", ACCENT_COLOR)])



# Estilo del Treeview (tablas)

style.configure("Treeview", background=FRAME_COLOR, foreground=FG_COLOR, fieldbackground=FRAME_COLOR, rowheight=28, font=("Calibri", 11))

style.configure("Treeview.Heading", background=ACCENT_COLOR, foreground=FRAME_COLOR, font=("Calibri", 11, "bold"), relief="flat", padding=[0, 5])

style.map("Treeview.Heading", background=[('active', ACCENT_HOVER_COLOR)])

style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Eliminar bordes

style.map('Treeview', background=[('selected', '#DDF0EC')], foreground=[('selected', FG_COLOR)])



notebook = ttk.Notebook(root)

notebook.pack(fill="both", expand=True, padx=12, pady=12)



# helper estilo botones

def style_button(btn, color, hover_color, fg_color="white"):

    btn.configure(bg=color, fg=fg_color, activebackground=hover_color, relief="flat", bd=0, font=("Calibri", 10, "bold"), width=14,

                  borderwidth=0, pady=5)

    btn.bind("<Enter>", lambda e, c=hover_color: e.widget.config(bg=c))

    btn.bind("<Leave>", lambda e, c=color: e.widget.config(bg=c))



# ---------------------------

# TAB: CLIENTES

# ---------------------------

tab_cli = ttk.Frame(notebook); notebook.add(tab_cli, text="Clientes Frecuentes")

tab_cli.configure(style="TFrame") # Aplicar estilo si es necesario



tk.Label(tab_cli, text="Gestión de Clientes Frecuentes", font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)

frame_cli = tk.LabelFrame(tab_cli, text="Formulario", padx=20, pady=15, bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), bd=1, relief="groove"); frame_cli.pack(anchor="w", padx=12, pady=8, fill="x")



tk.Label(frame_cli, text="Nombre:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=0, column=0, sticky="w", pady=5)

entry_cli_nombre = tk.Entry(frame_cli, width=50, state="readonly"); entry_cli_nombre.grid(row=0, column=1, padx=6, pady=4)

tk.Label(frame_cli, text="Correo:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=1, column=0, sticky="w", pady=5)

entry_cli_correo = tk.Entry(frame_cli, width=50, state="readonly"); entry_cli_correo.grid(row=1, column=1, padx=6, pady=4)

tk.Label(frame_cli, text="Teléfono:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=2, column=0, sticky="w", pady=5)

entry_cli_telefono = tk.Entry(frame_cli, width=50, state="readonly"); entry_cli_telefono.grid(row=2, column=1, padx=6, pady=4)

tk.Label(frame_cli, text="Dirección:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=3, column=0, sticky="w", pady=5)

entry_cli_direccion = tk.Entry(frame_cli, width=50, state="readonly"); entry_cli_direccion.grid(row=3, column=1, padx=6, pady=4)



frame_cli_btns = tk.Frame(frame_cli, bg=FRAME_COLOR); frame_cli_btns.grid(row=4, column=0, columnspan=2, pady=10)

btn_cli_guardar = tk.Button(frame_cli_btns, text="Guardar"); style_button(btn_cli_guardar, COLOR_GREEN, "#55a058")

btn_cli_mostrar = tk.Button(frame_cli_btns, text="Mostrar"); style_button(btn_cli_mostrar, COLOR_BLUE, "#0069D9")

btn_cli_update = tk.Button(frame_cli_btns, text="Actualizar"); style_button(btn_cli_update, COLOR_ORANGE, "#E0A800", fg_color=FG_COLOR)

btn_cli_delete = tk.Button(frame_cli_btns, text="Eliminar"); style_button(btn_cli_delete, COLOR_RED, "#C82333")

btn_cli_clear = tk.Button(frame_cli_btns, text="Limpiar"); style_button(btn_cli_clear, COLOR_PURPLE, "#5A32A3")

for b in (btn_cli_guardar, btn_cli_mostrar, btn_cli_update, btn_cli_delete, btn_cli_clear):

    b.pack(side="left", padx=8)



cols_cli = ("id","nombre","correo","telefono","direccion")

tree_cli = ttk.Treeview(tab_cli, columns=cols_cli, show="headings", selectmode="browse", height=10)

tree_cli.tag_configure('oddrow', background="#F7F7F7")

tree_cli.tag_configure('evenrow', background=FRAME_COLOR)

for c in cols_cli:

    tree_cli.heading(c, text=c.capitalize())

    width = 60 if c == "id" else 100 if c == "telefono" else 250

    tree_cli.column(c, width=width, anchor="w")

tree_cli.column("correo", width=250)

tree_cli.column("direccion", width=300)

tree_cli.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")



# funciones clientes

def listar_clientes():

    for r in tree_cli.get_children(): tree_cli.delete(r)

    rows = db.fetchall("SELECT id,nombre,correo,telefono,direccion FROM clientes ORDER BY id")

    for i, row in enumerate(rows):

        tag = 'evenrow' if i % 2 != 0 else 'oddrow'

        tree_cli.insert("", "end", values=row, tags=(tag,))



def guardar_cliente():

    n = entry_cli_nombre.get().strip(); c = entry_cli_correo.get().strip()

    t = entry_cli_telefono.get().strip(); d = entry_cli_direccion.get().strip()

    if not n or not c:

        messagebox.showwarning("Validación", "Nombre y correo son obligatorios.")

        return

    nuevo_cliente = Cliente(nombre=n, correo=c, telefono=t, direccion=d)

    if nuevo_cliente.guardar(db):

        messagebox.showinfo("OK","Cliente guardado")

        limpiar_cliente() # Limpia los campos después de guardar

        listar_clientes()



def seleccionar_cliente(evt):

    sel = tree_cli.selection()

    if not sel: return

    v = tree_cli.item(sel[0],"values")

    for entry, value in zip([entry_cli_nombre, entry_cli_correo, entry_cli_telefono, entry_cli_direccion], v[1:]):

        entry.config(state='normal')

        entry.delete(0, tk.END)

        entry.insert(0, value)

        entry.config(state='readonly')



def actualizar_cliente():

    sel = tree_cli.selection()

    if not sel:

        messagebox.showwarning("Seleccionar","Selecciona un cliente en la tabla.")

        return

    idc = tree_cli.item(sel[0],"values")[0]

    n = entry_cli_nombre.get().strip(); c = entry_cli_correo.get().strip()

    t = entry_cli_telefono.get().strip(); d = entry_cli_direccion.get().strip()

    if not n or not c:

        messagebox.showwarning("Validación","Nombre y correo son obligatorios.")

        return

    cliente_actualizado = Cliente(nombre=n, correo=c, telefono=t, direccion=d)

    if cliente_actualizado.actualizar(db, idc):

        messagebox.showinfo("OK","Cliente actualizado")

        listar_clientes()



def eliminar_cliente():

    sel = tree_cli.selection()

    if not sel:

        messagebox.showwarning("Seleccionar","Selecciona un cliente en la tabla.")

        return

    idc = tree_cli.item(sel[0],"values")[0]

    if messagebox.askyesno("Confirmar", "Eliminar cliente seleccionado?"):

        if Cliente.eliminar(db, idc):

            messagebox.showinfo("OK","Cliente eliminado")

            listar_clientes()

            limpiar_cliente()



def limpiar_cliente():

    for entry in [entry_cli_nombre, entry_cli_correo, entry_cli_telefono, entry_cli_direccion]:

        entry.config(state='normal')

        entry.delete(0, tk.END)

        entry.config(state='readonly')



btn_cli_guardar.config(command=guardar_cliente)

btn_cli_mostrar.config(command=listar_clientes)

btn_cli_update.config(command=actualizar_cliente)

btn_cli_delete.config(command=eliminar_cliente)

btn_cli_clear.config(command=limpiar_cliente)

tree_cli.bind("<<TreeviewSelect>>", seleccionar_cliente)

listar_clientes()



# ---------------------------

# TAB: CATEGORÍAS

# ---------------------------

tab_cat = ttk.Frame(notebook)

tab_cat.configure(style="TFrame")

notebook.add(tab_cat, text="Secciones")

tk.Label(tab_cat, text="Administración de Secciones", font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)

frame_cat = tk.LabelFrame(tab_cat, text="Categoría", padx=20, pady=15, bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), bd=1, relief="groove"); frame_cat.pack(anchor="w", padx=12, pady=8, fill="x")

tk.Label(frame_cat, text="ID:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=0, column=0, sticky="w", pady=5); entry_cat_id = tk.Entry(frame_cat, width=10, state="readonly"); entry_cat_id.grid(row=0, column=1, padx=6, pady=4, sticky="w")

tk.Label(frame_cat, text="Nombre:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=1,column=0,sticky="w", pady=5); entry_cat_nombre = tk.Entry(frame_cat, width=50, state="readonly"); entry_cat_nombre.grid(row=1,column=1,padx=6,pady=4) # Changed to readonly

tk.Label(frame_cat, text="Descripción:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=2,column=0,sticky="w", pady=5); entry_cat_desc = tk.Entry(frame_cat, width=50, state="readonly"); entry_cat_desc.grid(row=2,column=1,padx=6,pady=4)

frame_cat_btns = tk.Frame(frame_cat, bg=FRAME_COLOR); frame_cat_btns.grid(row=3,column=0,columnspan=2,pady=10)

btn_cat_guardar = tk.Button(frame_cat_btns, text="Guardar"); style_button(btn_cat_guardar, COLOR_GREEN, "#55a058")

btn_cat_mostrar = tk.Button(frame_cat_btns, text="Mostrar"); style_button(btn_cat_mostrar, COLOR_BLUE, "#0069D9")

btn_cat_up = tk.Button(frame_cat_btns, text="Actualizar"); style_button(btn_cat_up, COLOR_ORANGE, "#E0A800", fg_color=FG_COLOR)

btn_cat_del = tk.Button(frame_cat_btns, text="Eliminar"); style_button(btn_cat_del, COLOR_RED, "#C82333")

btn_cat_clear = tk.Button(frame_cat_btns, text="Limpiar"); style_button(btn_cat_clear, COLOR_PURPLE, "#5A32A3")

for b in (btn_cat_guardar,btn_cat_mostrar,btn_cat_up,btn_cat_del,btn_cat_clear): b.pack(side="left", padx=8)



cols_cat = ("id","nombre","descripcion")

tree_cat = ttk.Treeview(tab_cat, columns=cols_cat, show="headings")

tree_cat.tag_configure('oddrow', background="#F7F7F7")

tree_cat.tag_configure('evenrow', background=FRAME_COLOR)

for c in cols_cat: tree_cat.heading(c, text=c.capitalize()); tree_cat.column(c, width=240 if c!="id" else 60)

tree_cat.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")



def listar_categorias():

    for r in tree_cat.get_children(): tree_cat.delete(r)

    rows = db.fetchall("SELECT id,nombre,descripcion FROM categorias ORDER BY id")

    for i, row in enumerate(rows):

        tag = 'evenrow' if i % 2 != 0 else 'oddrow'

        tree_cat.insert("", "end", values=row, tags=(tag,))



def guardar_categoria():

    n = entry_cat_nombre.get().strip()

    d = entry_cat_desc.get().strip()

    if not n:

        messagebox.showwarning("Validación", "Nombre es obligatorio")

        return

    nueva_categoria = Categoria(nombre=n, descripcion=d)

    if nueva_categoria.guardar(db):

        messagebox.showinfo("OK", "Categoría guardada")

        limpiar_categoria() # Limpia los campos después de guardar

        listar_categorias()



def seleccionar_categoria(evt):

    sel = tree_cat.selection()

    if not sel: return

    v = tree_cat.item(sel[0],"values")

    for entry, value in zip([entry_cat_id, entry_cat_nombre, entry_cat_desc], v):

        entry.config(state='normal')

        entry.delete(0, tk.END)

        entry.insert(0, value)

        entry.config(state='readonly') # Set each entry back to readonly



def actualizar_categoria():

    sel = tree_cat.selection()

    if not sel:

        messagebox.showwarning("Seleccionar", "Selecciona una categoría")

        return    

    try:

        idc = int(entry_cat_id.get())

    except (ValueError, TypeError):

        messagebox.showerror("Error", "No se pudo obtener un ID válido del formulario.")

        return

    n = entry_cat_nombre.get().strip()

    d = entry_cat_desc.get().strip()

    if not n:

        messagebox.showwarning("Validación", "Nombre es obligatorio")

        return

    categoria_actualizada = Categoria(nombre=n, descripcion=d)

    if categoria_actualizada.actualizar(db, idc):

        messagebox.showinfo("OK", "Categoría actualizada")

        listar_categorias()

        limpiar_categoria()



def eliminar_categoria():

    sel = tree_cat.selection()

    if not sel:

        messagebox.showwarning("Seleccionar", "Selecciona una categoría")

        return

    idc = tree_cat.item(sel[0], "values")[0]

    if messagebox.askyesno("Confirmar", "Eliminar categoría?"):

        if Categoria.eliminar(db, idc):

            messagebox.showinfo("OK", "Categoría eliminada")

            limpiar_categoria()

            listar_categorias()



def limpiar_categoria():

    for entry in [entry_cat_id, entry_cat_nombre, entry_cat_desc]:

        entry.config(state='normal')

        entry.delete(0, tk.END)

        entry.config(state='readonly') # Set each entry back to readonly



btn_cat_guardar.config(command=guardar_categoria)

btn_cat_mostrar.config(command=listar_categorias)

btn_cat_up.config(command=actualizar_categoria)

btn_cat_del.config(command=eliminar_categoria)

btn_cat_clear.config(command=limpiar_categoria)

tree_cat.bind("<<TreeviewSelect>>", seleccionar_categoria)

listar_categorias()

# ---------------------------

# TAB: PRODUCTOS

# ---------------------------

tab_prod = ttk.Frame(notebook)

tab_prod.configure(style="TFrame")

notebook.add(tab_prod, text="Inventario")

tk.Label(tab_prod, text="Control de Inventario", font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)

frame_prod = tk.LabelFrame(tab_prod, text="Producto", padx=20, pady=15, bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), bd=1, relief="groove"); frame_prod.pack(anchor="w", padx=12, pady=8, fill="x")



# Fila 1: ID y Nombre

tk.Label(frame_prod, text="ID:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=0, column=0, sticky="w", pady=5)

entry_prod_id = tk.Entry(frame_prod, width=10, state='readonly'); entry_prod_id.grid(row=0, column=1, padx=(0, 20), pady=4, sticky="w")

tk.Label(frame_prod, text="Nombre:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=0,column=2,sticky="w", pady=5); 

entry_prod_nombre = tk.Entry(frame_prod,width=40, state="readonly"); entry_prod_nombre.grid(row=0,column=3,padx=6,pady=4, sticky="w")



# Fila 2: Precio y Stock

tk.Label(frame_prod, text="Precio:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=1,column=0,sticky="w", pady=5)

entry_prod_precio = tk.Entry(frame_prod,width=10, state="readonly"); entry_prod_precio.grid(row=1,column=1,padx=(0, 20),pady=4, sticky="w")

tk.Label(frame_prod, text="Stock:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=1,column=2,sticky="w", pady=5)

entry_prod_stock = tk.Entry(frame_prod,width=15, state="readonly"); entry_prod_stock.grid(row=1,column=3,sticky="w",padx=6,pady=4)



# Fila 3: Categoría y Descripción

tk.Label(frame_prod, text="Categoría:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=2,column=0,sticky="w", pady=5)

combo_prod_cat = ttk.Combobox(frame_prod, width=25, state="readonly"); combo_prod_cat.grid(row=2,column=1,columnspan=3,sticky="w",padx=6,pady=4)

tk.Label(frame_prod, text="Descripción:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=3,column=0,sticky="w", pady=5)

entry_prod_desc = tk.Entry(frame_prod,width=60, state="readonly"); entry_prod_desc.grid(row=3,column=1,columnspan=3,padx=6,pady=4, sticky="w")



frame_prod_btns = tk.Frame(frame_prod, bg=FRAME_COLOR); frame_prod_btns.grid(row=4,column=0,columnspan=4,pady=10)

btn_prod_guardar = tk.Button(frame_prod_btns, text="Guardar"); style_button(btn_prod_guardar, COLOR_GREEN, "#55a058")

btn_prod_mostrar = tk.Button(frame_prod_btns, text="Mostrar"); style_button(btn_prod_mostrar, COLOR_BLUE, "#0069D9")

btn_prod_up = tk.Button(frame_prod_btns, text="Actualizar"); style_button(btn_prod_up, COLOR_ORANGE, "#E0A800", fg_color=FG_COLOR)

btn_prod_del = tk.Button(frame_prod_btns, text="Eliminar"); style_button(btn_prod_del, COLOR_RED, "#7E22DF")

btn_prod_clear = tk.Button(frame_prod_btns, text="Limpiar"); style_button(btn_prod_clear, COLOR_PURPLE, "#5A32A3")

for b in (btn_prod_guardar,btn_prod_mostrar,btn_prod_up,btn_prod_del,btn_prod_clear): b.pack(side="left", padx=8)



cols_prod = ("id","nombre","descripcion","precio","stock","categoria", "desc_categoria")

tree_prod = ttk.Treeview(tab_prod, columns=cols_prod, show="headings")

tree_prod.tag_configure('oddrow', background="#F7F7F7")

tree_prod.tag_configure('evenrow', background=FRAME_COLOR)

for c in cols_prod: tree_prod.heading(c, text=c.replace("_"," ").capitalize()); tree_prod.column(c, width=140 if c not in ("id", "precio", "stock") else 60)

tree_prod.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")



def get_category_map():

    """Devuelve un diccionario para mapear nombres de categoría a IDs y viceversa."""

    rows = db.fetchall("SELECT id, nombre FROM categorias")

    name_to_id = {name: id for id, name in rows}

    id_to_name = {id: name for id, name in rows}

    return name_to_id, id_to_name



def listar_productos():

    for r in tree_prod.get_children(): tree_prod.delete(r)

    query = """

        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, 

               COALESCE(c.nombre, 'N/A'), COALESCE(c.descripcion, 'N/A')

        FROM productos p

        LEFT JOIN categorias c ON p.categoria_id = c.id

        ORDER BY p.id

    """

    rows = db.fetchall(query)

    for i, row in enumerate(rows):

        tag = 'evenrow' if i % 2 != 0 else 'oddrow'

        tree_prod.insert("", "end", values=row, tags=(tag,))

    # Actualizar combobox

    _, id_to_name = get_category_map(); combo_prod_cat['values'] = sorted(list(id_to_name.values()))



def guardar_producto():

    name_to_id, _ = get_category_map()

    n = entry_prod_nombre.get().strip(); d = entry_prod_desc.get().strip(); p_str = entry_prod_precio.get().strip(); s_str = entry_prod_stock.get().strip()

    cat_name = combo_prod_cat.get()

    c = name_to_id.get(cat_name)

    if not n or not p_str or not s_str: messagebox.showwarning("Validación","Nombre, precio y stock son oblig."); return

    try:

        p = float(p_str); s = int(s_str)

    except ValueError:

        messagebox.showerror("Error","Precio o stock con formato incorrecto"); return

    

    nuevo_producto = Producto(nombre=n, descripcion=d, precio=p, stock=s, categoria_id=c)

    if nuevo_producto.guardar(db):

        messagebox.showinfo("OK","Producto guardado"); listar_productos(); limpiar_producto()



def seleccionar_producto(evt):

    sel = tree_prod.selection()

    if not sel: return

    v = tree_prod.item(sel[0],"values")

    for entry, value in zip([entry_prod_id, entry_prod_nombre, entry_prod_desc, entry_prod_precio, entry_prod_stock], v[:5]):

        entry.config(state='normal')

        entry.delete(0, tk.END)

        entry.insert(0, value)

        entry.config(state='readonly')

    combo_prod_cat.set(v[5] if v[5] != "N/A" else "")



def actualizar_producto():

    sel = tree_prod.selection()

    if not sel: messagebox.showwarning("Seleccionar","Selecciona un producto"); return

    idp = int(tree_prod.item(sel[0],"values")[0])

    name_to_id, _ = get_category_map()

    n = entry_prod_nombre.get().strip(); d = entry_prod_desc.get().strip()

    p_str = entry_prod_precio.get().strip(); s_str = entry_prod_stock.get().strip()

    cat_name = combo_prod_cat.get()

    c = name_to_id.get(cat_name)

    if not n or not p_str or not s_str:

        messagebox.showwarning("Validación", "Nombre, precio y stock son obligatorios.")

        return

    try:

        p = float(p_str); s = int(s_str)

    except ValueError:

        messagebox.showerror("Error", "Precio o stock con formato incorrecto")

        return

    producto_actualizado = Producto(nombre=n, descripcion=d, precio=p, stock=s, categoria_id=c)

    if producto_actualizado.actualizar(db, idp):

        messagebox.showinfo("OK","Producto actualizado"); listar_productos(); limpiar_producto()



def eliminar_producto():

    sel = tree_prod.selection()

    if not sel: messagebox.showwarning("Seleccionar","Selecciona un producto"); return

    idp = int(tree_prod.item(sel[0],"values")[0])

    if messagebox.askyesno("Confirmar","Eliminar producto?"):

        if Producto.eliminar(db, idp):

            messagebox.showinfo("OK","Producto eliminado"); listar_productos(); limpiar_producto()



def limpiar_producto():

    for entry in [entry_prod_id, entry_prod_nombre, entry_prod_desc, entry_prod_precio, entry_prod_stock]:

        entry.config(state='normal')

        entry.delete(0, tk.END)

        entry.config(state='readonly')

    combo_prod_cat.set('')

btn_prod_guardar.config(command=guardar_producto)

btn_prod_mostrar.config(command=listar_productos)

btn_prod_up.config(command=actualizar_producto)

btn_prod_del.config(command=eliminar_producto)

btn_prod_clear.config(command=limpiar_producto)

tree_prod.bind("<<TreeviewSelect>>", seleccionar_producto)

listar_productos()





# ---------------------------

# TAB: PEDIDOS

# ---------------------------

tab_ped = ttk.Frame(notebook); tab_ped.configure(style="TFrame"); notebook.add(tab_ped, text="Órdenes")

tk.Label(tab_ped, text="Registro de Órdenes", font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)

frame_ped = tk.LabelFrame(tab_ped, text="Pedido", padx=20, pady=15, bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), bd=1, relief="groove"); frame_ped.pack(anchor="w", padx=12, pady=8, fill="x")

tk.Label(frame_ped,text="Cliente ID:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=0,column=0,sticky="w", pady=5); entry_ped_cli = tk.Entry(frame_ped,width=20, state="readonly"); entry_ped_cli.grid(row=0,column=1,padx=6,pady=4)

tk.Label(frame_ped,text="Fecha (YYYY-MM-DD):", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=1,column=0,sticky="w", pady=5); entry_ped_fecha = tk.Entry(frame_ped,width=20, state="readonly"); entry_ped_fecha.grid(row=1,column=1,padx=6,pady=4)

tk.Label(frame_ped,text="Estado:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=2,column=0,sticky="w", pady=5); entry_ped_estado = tk.Entry(frame_ped,width=20, state="readonly"); entry_ped_estado.grid(row=2,column=1,padx=6,pady=4)



frame_ped_btns = tk.Frame(frame_ped, bg=FRAME_COLOR); frame_ped_btns.grid(row=3,column=0,columnspan=2,pady=10)

btn_ped_guardar = tk.Button(frame_ped_btns, text="Guardar"); style_button(btn_ped_guardar, COLOR_GREEN, "#55a058")

btn_ped_mostrar = tk.Button(frame_ped_btns, text="Mostrar"); style_button(btn_ped_mostrar, COLOR_BLUE, "#0069D9")

btn_ped_up = tk.Button(frame_ped_btns, text="Actualizar"); style_button(btn_ped_up, COLOR_ORANGE, "#E0A800", fg_color=FG_COLOR)

btn_ped_del = tk.Button(frame_ped_btns, text="Eliminar"); style_button(btn_ped_del, COLOR_RED, "#C82333")

btn_ped_clear = tk.Button(frame_ped_btns, text="Limpiar"); style_button(btn_ped_clear, COLOR_PURPLE, "#5A32A3")

for b in (btn_ped_guardar,btn_ped_mostrar,btn_ped_up,btn_ped_del,btn_ped_clear): b.pack(side="left", padx=8)



cols_ped = ("id","cliente_id","fecha","estado")

tree_ped = ttk.Treeview(tab_ped, columns=cols_ped, show="headings")

tree_ped.tag_configure('oddrow', background="#F7F7F7")

tree_ped.tag_configure('evenrow', background=FRAME_COLOR)

for c in cols_ped: tree_ped.heading(c, text=c.capitalize()); tree_ped.column(c, width=180 if c!="id" else 60)

tree_ped.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")



def listar_pedidos():

    for r in tree_ped.get_children(): tree_ped.delete(r)

    rows = db.fetchall("SELECT id,cliente_id,fecha,estado FROM pedidos ORDER BY id")

    for i, row in enumerate(rows):

        tag = 'evenrow' if i % 2 != 0 else 'oddrow'

        tree_ped.insert("", "end", values=row, tags=(tag,))



def guardar_pedido():

    try:

        cid = int(entry_ped_cli.get().strip())

    except ValueError:

        messagebox.showerror("Error","Cliente ID debe ser entero"); return

    fecha = entry_ped_fecha.get().strip(); estado = entry_ped_estado.get().strip()

    if not fecha or not estado: messagebox.showwarning("Validación","Fecha y estado oblig."); return

    nuevo_pedido = Pedido(cliente_id=cid, fecha=fecha, estado=estado)

    if nuevo_pedido.guardar(db):

        messagebox.showinfo("OK","Pedido guardado"); listar_pedidos(); limpiar_pedido()



def seleccionar_pedido(evt):

    sel = tree_ped.selection()

    if not sel: return

    v = tree_ped.item(sel[0],"values")

    for entry, value in zip([entry_ped_cli, entry_ped_fecha, entry_ped_estado], v[1:]):

        entry.config(state='normal')

        entry.delete(0, tk.END)

        entry.insert(0, value)

        entry.config(state='readonly')



def actualizar_pedido():

    sel = tree_ped.selection()

    if not sel: messagebox.showwarning("Seleccionar","Selecciona un pedido"); return

    idp = tree_ped.item(sel[0],"values")[0]

    try: cid = int(entry_ped_cli.get().strip())

    except ValueError: messagebox.showerror("Error","Cliente ID debe ser entero"); return

    fecha = entry_ped_fecha.get().strip(); estado = entry_ped_estado.get().strip()

    pedido_actualizado = Pedido(cliente_id=cid, fecha=fecha, estado=estado)

    if pedido_actualizado.actualizar(db, idp):

        messagebox.showinfo("OK","Pedido actualizado"); listar_pedidos(); limpiar_pedido()



def eliminar_pedido():

    sel = tree_ped.selection()

    if not sel: messagebox.showwarning("Seleccionar","Selecciona un pedido"); return

    idp = tree_ped.item(sel[0],"values")[0]

    if messagebox.askyesno("Confirmar","Eliminar pedido?"):

        if Pedido.eliminar(db, idp):

            messagebox.showinfo("OK","Pedido eliminado"); listar_pedidos(); limpiar_pedido()



def limpiar_pedido():

    for entry in [entry_ped_cli, entry_ped_fecha, entry_ped_estado]:

        entry.config(state='normal')

        entry.delete(0, tk.END)

        entry.config(state='readonly')



btn_ped_guardar.config(command=guardar_pedido)

btn_ped_mostrar.config(command=listar_pedidos)

btn_ped_up.config(command=actualizar_pedido)

btn_ped_del.config(command=eliminar_pedido)

btn_ped_clear.config(command=limpiar_pedido)

tree_ped.bind("<<TreeviewSelect>>", seleccionar_pedido)

listar_pedidos()



# ---------------------------

# TAB: DETALLE PEDIDO

# ---------------------------

tab_det = ttk.Frame(notebook); tab_det.configure(style="TFrame"); notebook.add(tab_det, text="Detalle de Órden")

tk.Label(tab_det, text="Detalles de Órdenes", font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)

frame_det = tk.LabelFrame(tab_det, text="Detalle", padx=20, pady=15, bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), bd=1, relief="groove"); frame_det.pack(anchor="w", padx=12, pady=8, fill="x")

tk.Label(frame_det,text="Pedido ID:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=0,column=0,sticky="w", pady=5); entry_det_pedido = tk.Entry(frame_det,width=12, state="readonly"); entry_det_pedido.grid(row=0,column=1,padx=6,pady=4)

tk.Label(frame_det,text="Producto ID:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=1,column=0,sticky="w", pady=5); entry_det_prod = tk.Entry(frame_det,width=12, state="readonly"); entry_det_prod.grid(row=1,column=1,padx=6,pady=4)

tk.Label(frame_det,text="Cantidad:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=2,column=0,sticky="w", pady=5); entry_det_cant = tk.Entry(frame_det,width=12, state="readonly"); entry_det_cant.grid(row=2,column=1,padx=6,pady=4)

tk.Label(frame_det,text="Precio unit.:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=3,column=0,sticky="w", pady=5); entry_det_precio = tk.Entry(frame_det,width=12, state="readonly"); entry_det_precio.grid(row=3,column=1,padx=6,pady=4)



frame_det_btns = tk.Frame(frame_det, bg=FRAME_COLOR); frame_det_btns.grid(row=4,column=0,columnspan=2,pady=10)

btn_det_guardar = tk.Button(frame_det_btns, text="Guardar"); style_button(btn_det_guardar, COLOR_GREEN, "#55a058")

btn_det_mostrar = tk.Button(frame_det_btns, text="Mostrar"); style_button(btn_det_mostrar, COLOR_BLUE, "#0069D9")

btn_det_up = tk.Button(frame_det_btns, text="Actualizar"); style_button(btn_det_up, COLOR_ORANGE, "#E0A800", fg_color=FG_COLOR)

btn_det_del = tk.Button(frame_det_btns, text="Eliminar"); style_button(btn_det_del, COLOR_RED, "#C82333")

btn_det_clear = tk.Button(frame_det_btns, text="Limpiar"); style_button(btn_det_clear, COLOR_PURPLE, "#5A32A3")

for b in (btn_det_guardar,btn_det_mostrar,btn_det_up,btn_det_del,btn_det_clear): b.pack(side="left", padx=8)



cols_det = ("id","pedido_id","producto_id","cantidad","precio_unitario")

tree_det = ttk.Treeview(tab_det, columns=cols_det, show="headings")

tree_det.tag_configure('oddrow', background="#F7F7F7")

tree_det.tag_configure('evenrow', background=FRAME_COLOR)

for c in cols_det: tree_det.heading(c, text=c.capitalize()); tree_det.column(c, width=150 if c!="id" else 60)

tree_det.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")



def listar_detalles():

    for r in tree_det.get_children(): tree_det.delete(r)

    rows = db.fetchall("SELECT id,pedido_id,producto_id,cantidad,precio_unitario FROM detalle_pedido ORDER BY id")

    for i, row in enumerate(rows):

        tag = 'evenrow' if i % 2 != 0 else 'oddrow'

        tree_det.insert("", "end", values=row, tags=(tag,))



def guardar_detalle():

    try:

        pid = int(entry_det_pedido.get().strip()); prid = int(entry_det_prod.get().strip())

        cant = int(entry_det_cant.get().strip()); prec = float(entry_det_precio.get().strip())

    except ValueError:

        messagebox.showerror("Error","IDs y cantidad enteros; precio decimal"); return

    nuevo_detalle = DetallePedido(pedido_id=pid, producto_id=prid, cantidad=cant, precio_unitario=prec)

    if nuevo_detalle.guardar(db):

        messagebox.showinfo("OK","Detalle guardado"); listar_detalles(); limpiar_detalle()



def seleccionar_detalle(evt):

    sel = tree_det.selection()

    if not sel: return

    v = tree_det.item(sel[0],"values")

    for entry, value in zip([entry_det_pedido, entry_det_prod, entry_det_cant, entry_det_precio], v[1:]):

        entry.config(state='normal')

        entry.delete(0, tk.END)

        entry.insert(0, value)

        entry.config(state='readonly')



def actualizar_detalle():

    sel = tree_det.selection()

    if not sel: messagebox.showwarning("Seleccionar","Selecciona un detalle"); return

    idd = tree_det.item(sel[0],"values")[0]

    try:

        pid = int(entry_det_pedido.get().strip()); prid = int(entry_det_prod.get().strip())

        cant = int(entry_det_cant.get().strip()); prec = float(entry_det_precio.get().strip())

    except ValueError:

        messagebox.showerror("Error","Formato incorrecto"); return

    detalle_actualizado = DetallePedido(pedido_id=pid, producto_id=prid, cantidad=cant, precio_unitario=prec)

    if detalle_actualizado.actualizar(db, idd):

        messagebox.showinfo("OK","Detalle actualizado"); listar_detalles(); limpiar_detalle()



def eliminar_detalle():

    sel = tree_det.selection()

    if not sel: messagebox.showwarning("Seleccionar","Selecciona un detalle"); return

    idd = tree_det.item(sel[0],"values")[0]

    if messagebox.askyesno("Confirmar","Eliminar detalle?"):

        if DetallePedido.eliminar(db, idd):

            messagebox.showinfo("OK","Detalle eliminado"); listar_detalles(); limpiar_detalle()



def limpiar_detalle():

    for entry in [entry_det_pedido, entry_det_prod, entry_det_cant, entry_det_precio]:

        entry.config(state='normal')

        entry.delete(0, tk.END)

        entry.config(state='readonly')



btn_det_guardar.config(command=guardar_detalle)

btn_det_mostrar.config(command=listar_detalles)

btn_det_up.config(command=actualizar_detalle)

btn_det_del.config(command=eliminar_detalle)

btn_det_clear.config(command=limpiar_detalle)

tree_det.bind("<<TreeviewSelect>>", seleccionar_detalle)

listar_detalles()



# ---------------------------

# TAB: EMPLEADOS

# ---------------------------

tab_emp = ttk.Frame(notebook); tab_emp.configure(style="TFrame"); notebook.add(tab_emp, text="Personal")

tk.Label(tab_emp, text="Administración de Personal", font=("Georgia", 18, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(15, 10), anchor="w", padx=12)

frame_emp = tk.LabelFrame(tab_emp, text="Empleado", padx=20, pady=15, bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 11), bd=1, relief="groove"); frame_emp.pack(anchor="w", padx=12, pady=8, fill="x")

tk.Label(frame_emp,text="Apellido:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=0,column=0,sticky="w", pady=5); entry_emp_apellido = tk.Entry(frame_emp,width=30, state="readonly"); entry_emp_apellido.grid(row=0,column=1,padx=6,pady=4)

tk.Label(frame_emp,text="Nombre:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=1,column=0,sticky="w", pady=5); entry_emp_nombre = tk.Entry(frame_emp,width=30, state="readonly"); entry_emp_nombre.grid(row=1,column=1,padx=6,pady=4)

tk.Label(frame_emp,text="Fecha Nac.:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=2,column=0,sticky="w", pady=5); entry_emp_fecha = DateEntry(frame_emp,date_pattern="yyyy-mm-dd", state="readonly"); entry_emp_fecha.grid(row=2,column=1,padx=6,pady=4)

tk.Label(frame_emp,text="Foto (ruta):", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=3,column=0,sticky="w", pady=5); entry_emp_foto = tk.Entry(frame_emp,width=40, state="readonly"); entry_emp_foto.grid(row=3,column=1,padx=6,pady=4)

btn_emp_foto = tk.Button(frame_emp, text="Seleccionar...", width=12); btn_emp_foto.grid(row=3,column=2,padx=6)

style_button(btn_emp_foto, ACCENT_COLOR, ACCENT_HOVER_COLOR, fg_color=FRAME_COLOR)

tk.Label(frame_emp,text="Notas:", bg=FRAME_COLOR, fg=FG_COLOR, font=("Calibri", 10)).grid(row=4,column=0,sticky="nw", pady=5); entry_emp_notas = tk.Text(frame_emp,width=50,height=4, state=tk.DISABLED); entry_emp_notas.grid(row=4,column=1,padx=6,pady=4)



frame_emp_btns = tk.Frame(frame_emp, bg=FRAME_COLOR); frame_emp_btns.grid(row=5,column=0,columnspan=3,pady=10)

btn_emp_guardar = tk.Button(frame_emp_btns, text="Guardar"); style_button(btn_emp_guardar, COLOR_GREEN, "#55a058")

btn_emp_mostrar = tk.Button(frame_emp_btns, text="Mostrar"); style_button(btn_emp_mostrar, COLOR_BLUE, "#0069D9")

btn_emp_up = tk.Button(frame_emp_btns, text="Actualizar"); style_button(btn_emp_up, COLOR_ORANGE, "#E0A800", fg_color=FG_COLOR)

btn_emp_del = tk.Button(frame_emp_btns, text="Eliminar"); style_button(btn_emp_del, COLOR_RED, "#C82333")

btn_emp_clear = tk.Button(frame_emp_btns, text="Limpiar"); style_button(btn_emp_clear, COLOR_PURPLE, "#5A32A3")

for b in (btn_emp_guardar,btn_emp_mostrar,btn_emp_up,btn_emp_del,btn_emp_clear): b.pack(side="left", padx=8)



cols_emp = ("id","last_name","first_name","birth_date","photo","notes")

tree_emp = ttk.Treeview(tab_emp, columns=cols_emp, show="headings")

tree_emp.tag_configure('oddrow', background="#F7F7F7")

tree_emp.tag_configure('evenrow', background=FRAME_COLOR)

for c in cols_emp: tree_emp.heading(c, text=c.replace("_"," ").capitalize()); tree_emp.column(c, width=160 if c!="id" else 60)

tree_emp.pack(fill="both", expand=True, padx=12, pady=8, side="bottom")



def seleccionar_foto_empleado():

    archivo = filedialog.askopenfilename(title="Selecciona imagen", filetypes=[("Imágenes","*.jpg *.jpeg *.png *.gif")])

    if not archivo: return

    nombre = os.path.basename(archivo)

    destino = os.path.join(IMAGES_DIR, nombre)

    try:

        copyfile(archivo, destino)

    except Exception as e:

        messagebox.showerror("Error", f"No se pudo copiar la imagen: {e}")

        return

    entry_emp_foto.delete(0,tk.END); entry_emp_foto.insert(0,destino)



def listar_empleados():

    for r in tree_emp.get_children(): tree_emp.delete(r)

    rows = db.fetchall("SELECT id,last_name,first_name,birth_date,photo,notes FROM empleados ORDER BY id")

    for i, row in enumerate(rows):

        tag = 'evenrow' if i % 2 != 0 else 'oddrow'

        tree_emp.insert("", "end", values=row, tags=(tag,))



def guardar_empleado():

    ln = entry_emp_apellido.get().strip(); fn = entry_emp_nombre.get().strip()

    bd = entry_emp_fecha.get().strip(); ph = entry_emp_foto.get().strip(); notes = entry_emp_notas.get("1.0",tk.END).strip()

    if not ln or not fn: messagebox.showwarning("Validación","Apellido y nombre son obligatorios."); return

    

    nuevo_empleado = Empleado(last_name=ln, first_name=fn, birth_date=bd, photo=ph, notes=notes)

    if nuevo_empleado.guardar(db):

        messagebox.showinfo("OK","Empleado guardado"); listar_empleados(); limpiar_empleado()



def seleccionar_empleado(evt):

    sel = tree_emp.selection()

    if not sel: return

    v = tree_emp.item(sel[0],"values")

    for entry, value in zip([entry_emp_apellido, entry_emp_nombre], v[1:3]):

        entry.config(state='normal'); entry.delete(0, tk.END); entry.insert(0, value); entry.config(state='readonly')

    

    try:

        entry_emp_fecha.config(state='normal'); entry_emp_fecha.set_date(v[3]); entry_emp_fecha.config(state='readonly')

    except Exception:

        entry_emp_fecha.config(state='normal'); entry_emp_fecha.delete(0, tk.END); entry_emp_fecha.config(state='readonly')



    entry_emp_foto.config(state='normal'); entry_emp_foto.delete(0, tk.END); entry_emp_foto.insert(0, v[4] or ""); entry_emp_foto.config(state='readonly')

    

    entry_emp_notas.config(state='normal')

    entry_emp_notas.delete("1.0", tk.END)

    entry_emp_notas.insert("1.0", v[5] or "")

    entry_emp_notas.config(state=tk.DISABLED)



def actualizar_empleado():

    sel = tree_emp.selection()

    if not sel: messagebox.showwarning("Seleccionar","Selecciona un empleado"); return

    idd = tree_emp.item(sel[0],"values")[0]

    ln = entry_emp_apellido.get().strip(); fn = entry_emp_nombre.get().strip(); bd = entry_emp_fecha.get().strip()

    ph = entry_emp_foto.get().strip(); notes = entry_emp_notas.get("1.0",tk.END).strip()

    empleado_actualizado = Empleado(last_name=ln, first_name=fn, birth_date=bd, photo=ph, notes=notes)

    if empleado_actualizado.actualizar(db, idd):

        messagebox.showinfo("OK","Empleado actualizado"); listar_empleados()



def eliminar_empleado():

    sel = tree_emp.selection()

    if not sel: messagebox.showwarning("Seleccionar","Selecciona un empleado"); return

    idd = tree_emp.item(sel[0],"values")[0]

    if messagebox.askyesno("Confirmar","Eliminar empleado?"):

        if Empleado.eliminar(db, idd):

            messagebox.showinfo("OK","Empleado eliminado"); listar_empleados(); limpiar_empleado()



def limpiar_empleado():

    for entry in [entry_emp_apellido, entry_emp_nombre, entry_emp_foto]:

        entry.config(state='normal'); entry.delete(0, tk.END); entry.config(state='readonly')

    

    entry_emp_fecha.config(state='normal'); entry_emp_fecha.delete(0, tk.END); entry_emp_fecha.config(state='readonly')

    

    entry_emp_notas.config(state='normal'); entry_emp_notas.delete("1.0", tk.END); entry_emp_notas.config(state=tk.DISABLED)





btn_emp_foto.config(command=seleccionar_foto_empleado)

btn_emp_guardar.config(command=guardar_empleado)

btn_emp_mostrar.config(command=listar_empleados)

btn_emp_up.config(command=actualizar_empleado)

btn_emp_del.config(command=eliminar_empleado)

btn_emp_clear.config(command=limpiar_empleado)

tree_emp.bind("<<TreeviewSelect>>", seleccionar_empleado)

listar_empleados()



# ---------------------------

# Iniciar aplicación

# ---------------------------

def on_closing():

    if messagebox.askokcancel("Salir", "¿Quieres cerrar la aplicación?"):



        db.close()

        root.destroy()



root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

