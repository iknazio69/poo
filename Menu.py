import sqlite3

class ConexionDB:
    def __init__(self):
        self.conexion = sqlite3.connect('inventario.db')
        self.c = self.conexion.cursor()

    def commit(self):
        self.conexion.commit()

    def close(self):
        self.conexion.close()

class Categoria:
    def __init__(self, conexion):
        self.conexion = conexion

    def existe_categoria(self, nombre):
        self.conexion.c.execute("SELECT COUNT(*) FROM categorias WHERE nombre = ?", (nombre,))
        return self.conexion.c.fetchone()[0] > 0

    def agregar(self, nombre):
        if self.existe_categoria(nombre):
            print("La categoría ya existe. No se puede agregar.")
            return
        self.conexion.c.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
        self.conexion.commit()
        print("Categoría agregada con éxito.")

    def listar(self):
        self.conexion.c.execute("SELECT * FROM categorias")
        categorias = self.conexion.c.fetchall()
        for categoria in categorias:
            print(f"ID: {categoria[0]}, Nombre: {categoria[1]}")

    def actualizar(self, id_categoria, nombre):
        self.conexion.c.execute("UPDATE categorias SET nombre = ? WHERE id_categoria = ?", (nombre, id_categoria))
        self.conexion.commit()
        print("Categoría actualizada con éxito.")

    def eliminar(self, id_categoria):
        self.conexion.c.execute("DELETE FROM categorias WHERE id_categoria = ?", (id_categoria,))
        self.conexion.commit()
        print("Categoría eliminada con éxito.")

class Proveedor:
    def __init__(self, conexion):
        self.conexion = conexion

    def existe_proveedor(self, nombre):
        self.conexion.c.execute("SELECT COUNT(*) FROM proveedores WHERE nombre = ?", (nombre,))
        return self.conexion.c.fetchone()[0] > 0

    def agregar(self, nombre, contacto, direccion):
        while len(contacto) != 9 or not contacto.isdigit():
            print("El número de contacto debe tener exactamente 9 dígitos.")
            contacto = input("Contacto del proveedor (nueve dígitos): ")

        if self.existe_proveedor(nombre):
            print("El proveedor ya existe. No se puede agregar.")
            return
        self.conexion.c.execute("INSERT INTO proveedores (nombre, contacto, direccion) VALUES (?, ?, ?)", (nombre, contacto, direccion))
        self.conexion.commit()
        print("Proveedor agregado con éxito.")

    def listar(self):
        self.conexion.c.execute("SELECT * FROM proveedores")
        proveedores = self.conexion.c.fetchall()
        for proveedor in proveedores:
            print(f"ID: {proveedor[0]}, Nombre: {proveedor[1]}, Contacto: {proveedor[2]}, Dirección: {proveedor[3]}")

    def actualizar(self, id_proveedor, nombre, contacto, direccion):
        while len(contacto) != 9 or not contacto.isdigit():
            print("El número de contacto debe tener exactamente 9 dígitos.")
            contacto = input("Nuevo contacto del proveedor (nueve dígitos): ")

        self.conexion.c.execute("UPDATE proveedores SET nombre = ?, contacto = ?, direccion = ? WHERE id_proveedor = ?", (nombre, contacto, direccion, id_proveedor))
        self.conexion.commit()
        print("Proveedor actualizado con éxito.")

    def eliminar(self, id_proveedor):
        self.conexion.c.execute("DELETE FROM proveedores WHERE id_proveedor = ?", (id_proveedor,))
        self.conexion.commit()
        print("Proveedor eliminado con éxito.")

class Producto:
    def __init__(self, conexion):
        self.conexion = conexion

    def existe_producto(self, nombre):
        self.conexion.c.execute("SELECT COUNT(*) FROM productos WHERE nombre = ?", (nombre,))
        return self.conexion.c.fetchone()[0] > 0

    def agregar(self, nombre, precio, stock, id_categoria, id_proveedor):
        if self.existe_producto(nombre):
            print("El producto ya existe. No se puede agregar.")
            return
        precio = int(float(precio))  
        self.conexion.c.execute("INSERT INTO productos (nombre, precio, stock, id_categoria, id_proveedor) VALUES (?, ?, ?, ?, ?)",
                                (nombre, precio, stock, id_categoria, id_proveedor))
        self.conexion.commit()
        print("Producto agregado con éxito.")

    def listar(self):
        self.conexion.c.execute("SELECT * FROM productos")
        productos = self.conexion.c.fetchall()
        for producto in productos:
            precio_formateado = int(producto[2])  
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: {precio_formateado}, Stock: {producto[3]}, ID Categoría: {producto[4]}, ID Proveedor: {producto[5]}")

    def actualizar(self, id_producto, nombre, stock, precio, id_categoria, id_proveedor):
        precio = int(float(precio))
        self.conexion.c.execute("UPDATE productos SET nombre = ?, precio = ?, stock = ?, id_categoria = ?, id_proveedor = ? WHERE id_producto = ?",
                                (nombre, precio, stock, id_categoria, id_proveedor, id_producto))
        self.conexion.commit()
        print("Producto actualizado con éxito.")

    def eliminar(self, id_producto):
        self.conexion.c.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
        self.conexion.commit()
        print("Producto eliminado con éxito.")

class Menu:
    def __init__(self):
        self.conexion = ConexionDB()
        self.categoria = Categoria(self.conexion)
        self.proveedor = Proveedor(self.conexion)
        self.producto = Producto(self.conexion)

    def mostrar_menu(self):
        while True:
            print("\n=== Sistema de Inventario ===")
            print("1. Categorías")
            print("2. Proveedores")
            print("3. Productos")
            print("4. Salir")

            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                self.menu_categorias()
            elif opcion == '2':
                self.menu_proveedores()
            elif opcion == '3':
                self.menu_productos()
            elif opcion == '4':
                self.conexion.close()
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_categorias(self):
        while True:
            print("\n=== Categorías ===")
            print("1. Agregar Categoría")
            print("2. Listar Categorías")
            print("3. Actualizar Categoría")
            print("4. Eliminar Categoría")
            print("5. Regresar")

            opcion_categoria = input("Seleccione una opción: ")

            if opcion_categoria == '1':
                nombre = input("Nombre de la categoría: ")
                self.categoria.agregar(nombre)
            elif opcion_categoria == '2':
                self.categoria.listar()
            elif opcion_categoria == '3':
                id_categoria = int(input("ID de la categoría a actualizar: "))
                nombre = input("Nuevo nombre de la categoría: ")
                self.categoria.actualizar(id_categoria, nombre)
            elif opcion_categoria == '4':
                id_categoria = int(input("ID de la categoría a eliminar: "))
                self.categoria.eliminar(id_categoria)
            elif opcion_categoria == '5':
                break  
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_proveedores(self):
        while True:
            print("\n=== Proveedores ===")
            print("1. Agregar Proveedor")
            print("2. Listar Proveedores")
            print("3. Actualizar Proveedor")
            print("4. Eliminar Proveedor")
            print("5. Regresar")

            opcion_proveedor = input("Seleccione una opción: ")

            if opcion_proveedor == '1':
                nombre = input("Nombre del proveedor: ")
                contacto = input("Contacto del proveedor: ")
                while len(contacto) != 9 or not contacto.isdigit():
                    print("El número de contacto debe tener exactamente 9 dígitos.")
                    contacto = input("Contacto del proveedor: ")
                direccion = input("Dirección del proveedor: ")
                self.proveedor.agregar(nombre, contacto, direccion)
            elif opcion_proveedor == '2':
                self.proveedor.listar()
            elif opcion_proveedor == '3':
                id_proveedor = int(input("ID del proveedor a actualizar: "))
                nombre = input("Nuevo nombre: ")
                contacto = input("Nuevo contacto: ")
                while len(contacto) != 9 or not contacto.isdigit():
                    print("El número de contacto debe tener exactamente 9 dígitos.")
                    contacto = input("Nuevo contacto: ")
                direccion = input("Nueva dirección: ")
                self.proveedor.actualizar(id_proveedor, nombre, contacto, direccion)
            elif opcion_proveedor == '4':
                id_proveedor = int(input("ID del proveedor a eliminar: "))
                self.proveedor.eliminar(id_proveedor)
            elif opcion_proveedor == '5':
                break  
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_productos(self):
        while True:
            print("\n=== Productos ===")
            print("1. Agregar Producto")
            print("2. Listar Productos")
            print("3. Actualizar Producto")
            print("4. Eliminar Producto")
            print("5. Regresar")

            opcion_producto = input("Seleccione una opción: ")

            if opcion_producto == '1':
                nombre = input("Nombre del producto: ")
                precio = input("Precio del producto: ")
                stock = input("Stock del producto: ")
                id_categoria = int(input("ID de la categoría: "))
                id_proveedor = int(input("ID del proveedor: "))
                self.producto.agregar(nombre, precio, stock, id_categoria, id_proveedor)
            elif opcion_producto == '2':
                self.producto.listar()
            elif opcion_producto == '3':
                id_producto = int(input("ID del producto a actualizar: "))
                nombre = input("Nuevo nombre: ")
                precio = input("Nuevo precio: ")
                stock = input("Nuevo stock: ")
                id_categoria = int(input("Nuevo ID de categoría: "))
                id_proveedor = int(input("Nuevo ID de proveedor: "))
                self.producto.actualizar(id_producto, nombre, stock, precio, id_categoria, id_proveedor)
            elif opcion_producto == '4':
                id_producto = int(input("ID del producto a eliminar: "))
                self.producto.eliminar(id_producto)
            elif opcion_producto == '5':
                break  
            else:
                print("Opción no válida. Intente de nuevo.")


menu = Menu()
menu.mostrar_menu()

