import sqlite3

conexion = sqlite3.connect('inventario.db')
c = conexion.cursor()


c.execute('''
    CREATE TABLE IF NOT EXISTS proveedores (
        id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        contacto TEXT,
        direccion TEXT
    )
''')


c.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
''')


c.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL CHECK(precio > 0),
        stock TEXT NOT NULL DEFAULT 0,  
        id_categoria INTEGER,
        id_proveedor INTEGER,
        FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
        FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
    )
''')



conexion.commit()
conexion.close()
