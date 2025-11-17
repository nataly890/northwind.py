"""
Vista base con estilos comunes
"""
import tkinter as tk
from tkinter import ttk

# Colores de la aplicación
BG_COLOR = "#F0F8F7"       # Mint Cream
FG_COLOR = "#4A4A4A"       # Gris oscuro para texto
FRAME_COLOR = "#FFFFFF"    # Blanco para los marcos
ACCENT_COLOR = "#79B4A9"   # Verde menta suave
ACCENT_HOVER_COLOR = "#8AC4B9"  # Menta más claro para hover

COLOR_GREEN = "#66BB6A"    # Verde suave
COLOR_BLUE = "#42A5F5"     # Azul suave
COLOR_ORANGE = "#FFA726"   # Naranja suave
COLOR_RED = "#EF5350"      # Rojo coral suave
COLOR_PURPLE = "#AB47BC"   # Púrpura suave


class BaseView:
    """Clase base para todas las vistas"""
    
    @staticmethod
    def configure_styles(root):
        """Configura los estilos TTK"""
        style = ttk.Style(root)
        style.theme_use("clam")
        
        # Estilo del Notebook (pestañas)
        style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_COLOR, foreground="#6c757d", 
                       padding=[15, 8], font=("Calibri", 11, "bold"), borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", FRAME_COLOR)], 
                 foreground=[("selected", ACCENT_COLOR)])
        
        # Estilo del Treeview (tablas)
        style.configure("Treeview", background=FRAME_COLOR, foreground=FG_COLOR, 
                       fieldbackground=FRAME_COLOR, rowheight=28, font=("Calibri", 11))
        style.configure("Treeview.Heading", background=ACCENT_COLOR, foreground=FRAME_COLOR, 
                       font=("Calibri", 11, "bold"), relief="flat", padding=[0, 5])
        style.map("Treeview.Heading", background=[('active', ACCENT_HOVER_COLOR)])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map('Treeview', background=[('selected', '#DDF0EC')], 
                 foreground=[('selected', FG_COLOR)])
    
    @staticmethod
    def style_button(btn, color, hover_color, fg_color="white"):
        """Aplica estilo a un botón"""
        btn.configure(bg=color, fg=fg_color, activebackground=hover_color, relief="flat", 
                     bd=0, font=("Calibri", 10, "bold"), width=14, borderwidth=0, pady=5)
        btn.bind("<Enter>", lambda e, c=hover_color: e.widget.config(bg=c))
        btn.bind("<Leave>", lambda e, c=color: e.widget.config(bg=c))

