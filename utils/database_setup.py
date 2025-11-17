"""
Utilidad para crear las tablas de la base de datos
"""
def ensure_tables(db):
    """Crea las tablas si no existen"""
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

