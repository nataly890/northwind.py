"""
Aplicación principal Northwind - Gestión
Patrón MVC (Modelo-Vista-Controlador)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Imports de utilidades
from utils.database import DatabaseConnector
from utils.config import DB_CONFIG
from utils.database_setup import ensure_tables
from views.base_view import BaseView, BG_COLOR

# Imports de vistas
from views.vista_cliente import VistaCliente
from views.vista_categoria import VistaCategoria
from views.vista_producto import VistaProducto
from views.vista_pedido import VistaPedido
from views.vista_detalle_pedido import VistaDetallePedido
from views.vista_empleado import VistaEmpleado

# Imports de controladores
from controllers.controlador_cliente import ControladorCliente
from controllers.controlador_categoria import ControladorCategoria
from controllers.controlador_producto import ControladorProducto
from controllers.controlador_pedido import ControladorPedido
from controllers.controlador_detalle_pedido import ControladorDetallePedido
from controllers.controlador_empleado import ControladorEmpleado


def main():
    """Función principal que inicializa la aplicación"""
    # Crear ventana principal (oculta temporalmente para messageboxes)
    root = tk.Tk()
    root.withdraw()
    
    # Conectar a la base de datos
    db = DatabaseConnector(DB_CONFIG)
    
    if not db.conn:
        # Si la conexión falla, mostramos el error y salimos
        messagebox.showerror("DB Error", "No se pudo conectar a la base de datos.\nLa aplicación se cerrará.")
        root.destroy()
        sys.exit()
    
    # Crear tablas si no existen
    ensure_tables(db)
    
    # Hacer visible la ventana principal
    root.deiconify()
    
    # Configurar ventana principal
    root.title("Northwind - Gestión")
    root.geometry("1200x750")
    root.configure(bg=BG_COLOR)
    
    # Configurar estilos
    BaseView.configure_styles(root)
    
    # Crear notebook (pestañas)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=12, pady=12)
    
    # Crear vistas
    vista_cliente = VistaCliente(notebook)
    vista_categoria = VistaCategoria(notebook)
    vista_producto = VistaProducto(notebook)
    vista_pedido = VistaPedido(notebook)
    vista_detalle_pedido = VistaDetallePedido(notebook)
    vista_empleado = VistaEmpleado(notebook)
    
    # Agregar pestañas al notebook
    notebook.add(vista_cliente.frame, text="Clientes Frecuentes")
    notebook.add(vista_categoria.frame, text="Secciones")
    notebook.add(vista_producto.frame, text="Inventario")
    notebook.add(vista_pedido.frame, text="Órdenes")
    notebook.add(vista_detalle_pedido.frame, text="Detalle de Órden")
    notebook.add(vista_empleado.frame, text="Personal")
    
    # Crear controladores (vinculan vistas con modelos y base de datos)
    controlador_cliente = ControladorCliente(vista_cliente, db)
    controlador_categoria = ControladorCategoria(vista_categoria, db)
    controlador_producto = ControladorProducto(vista_producto, db)
    controlador_pedido = ControladorPedido(vista_pedido, db)
    controlador_detalle_pedido = ControladorDetallePedido(vista_detalle_pedido, db)
    controlador_empleado = ControladorEmpleado(vista_empleado, db)
    
    # Función para cerrar la aplicación
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Quieres cerrar la aplicación?"):
            db.close()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Iniciar el loop principal
    root.mainloop()


if __name__ == "__main__":
    main()

