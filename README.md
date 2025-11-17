# Northwind - Sistema de Gestión

Aplicación de gestión de base de datos Northwind desarrollada con Python y Tkinter, implementando el patrón **MVC (Modelo-Vista-Controlador)**.
Contenido del Repositorio

- ✅ **Proyecto completo con estructura de carpetas organizada** (Patrón MVC)
- ✅ **Scripts de Python con todos los módulos** (Modelos, Vistas, Controladores)
- ✅ **Base de datos** (Script SQL para MySQL: `database/northwind.sql`)
- ✅ **Archivo README** con instrucciones de instalación y uso

## Estructura del Proyecto

```
tarea northwind/
│
├── main.py                          # Archivo principal - Punto de entrada
│
├── models/                          # MODELOS (Lógica de datos)
│   ├── __init__.py
│   ├── base_model.py               # Clase base para modelos
│   ├── cliente.py                  # Modelo Cliente
│   ├── categoria.py                # Modelo Categoria
│   ├── producto.py                 # Modelo Producto
│   ├── pedido.py                   # Modelo Pedido
│   ├── detalle_pedido.py           # Modelo DetallePedido
│   └── empleado.py                 # Modelo Empleado
│
├── views/                          # VISTAS (Interfaz de usuario)
│   ├── __init__.py
│   ├── base_view.py                # Vista base con estilos comunes
│   ├── vista_cliente.py            # Vista de Clientes
│   ├── vista_categoria.py          # Vista de Categorías
│   ├── vista_producto.py           # Vista de Productos
│   ├── vista_pedido.py             # Vista de Pedidos
│   ├── vista_detalle_pedido.py     # Vista de Detalles de Pedido
│   └── vista_empleado.py           # Vista de Empleados
│
├── controllers/                    # CONTROLADORES (Lógica de negocio)
│   ├── __init__.py
│   ├── controlador_cliente.py     # Controlador de Clientes
│   ├── controlador_categoria.py    # Controlador de Categorías
│   ├── controlador_producto.py     # Controlador de Productos
│   ├── controlador_pedido.py       # Controlador de Pedidos
│   ├── controlador_detalle_pedido.py # Controlador de Detalles
│   └── controlador_empleado.py      # Controlador de Empleados
│
├── utils/                          # UTILIDADES
│   ├── __init__.py
│   ├── config.py                   # Configuración (DB_CONFIG, IMAGES_DIR)
│   ├── database.py                 # DatabaseConnector
│   └── database_setup.py           # Funciones para crear tablas
│
├── database/                       # BASE DE DATOS
│   └── northwind.sql               # Script SQL para crear la base de datos
│
├── imagenes_empleados/             # Directorio para fotos de empleados
│
└── northwind_app.py                # Archivo original (legacy)

```

## Patrón MVC

### **Modelos** (`models/`)
- Contienen la lógica de acceso a datos
- Representan las entidades del negocio (Cliente, Producto, etc.)
- Métodos: `guardar()`, `actualizar()`, `eliminar()`

### **Vistas** (`views/`)
- Contienen la interfaz gráfica de usuario
- Componentes Tkinter (Entry, Treeview, Buttons, etc.)
- No contienen lógica de negocio, solo presentación
**Controladores** (`controllers/`)
- Coordinan la interacción entre Modelos y Vistas
- Contienen la lógica de negocio
- Manejan eventos de la interfaz y actualizan modelos/vistas

Instalación

### 1. Requisitos Previos

- Python 3.7 o superior
- MySQL Server instalado y ejecutándose
- Git (para clonar el repositorio)

### 2. Instalar Dependencias

```bash
pip install mysql-connector-python
pip install tkcalendar
```

O usando un archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

#### Opción A: Usando el script SQL

1. Abre MySQL y crea la base de datos:
```sql
CREATE DATABASE IF NOT EXISTS northwind;
```

2. Ejecuta el script SQL:
```bash
mysql -u root -p northwind < database/northwind.sql
```

O desde MySQL:
```sql
USE northwind;
SOURCE database/northwind.sql;
```

#### Opción B: La aplicación crea las tablas automáticamente

Si no ejecutas el script SQL, la aplicación creará las tablas automáticamente al iniciar.

### 4. Configurar Conexión

Edita `utils/config.py` para configurar la conexión a la base de datos:

``python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "tu_contraseña",  # Tu contraseña de MySQL
    "database": "northwind"
}
```

Ejecución
`bash
python main.py
```

La aplicación se iniciará y mostrará la interfaz gráfica con todas las pestañas de gestión.
 Funcionalidades

- ✅ Gestión de Clientes
- ✅ Gestión de Categorías
- ✅ Gestión de Productos
- ✅ Gestión de Pedidos
- ✅ Gestión de Detalles de Pedido
- ✅ Gestión de Empleados (con fotos)

 Características

- ✅ Interfaz moderna con colores suaves
- ✅ Validación de datos
- ✅ Confirmaciones antes de eliminar
- ✅ Tablas con filas alternadas
- ✅ Formularios con campos readonly (se habilitan al editar)
- ✅ Gestión de imágenes para empleados
- ✅ Patrón MVC bien estructurado
- ✅ Código modular y mantenible

Notas

- El archivo `northwind_app.py` es el código original antes de la refactorización MVC
- La aplicación crea automáticamente las tablas si no existen
- Las imágenes de empleados se guardan en la carpeta `imagenes_empleados/`


