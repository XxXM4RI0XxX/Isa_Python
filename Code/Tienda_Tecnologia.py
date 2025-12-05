import textwrap

def menu_principal(inv):
    while True:

        print(textwrap.dedent("""
        ______Menu______
        1) Realizar venta
        2) Administrar inventario
        3) Generar reporte
        0) Salir"""))

        try:
            opt = int(input(">> "))
        except ValueError:
            print("E400: El valor ingresado es incorrecto\n")
            continue

        if opt == 1:
            menu_ventas(inv)
        elif opt == 2:
            menu_inventario(inv)
        elif opt == 3:
            menu_reportes(inv)
        else:
            break

# TODO relacionado con realización de ventas ///////////////////////
def menu_ventas(inv):
    while True:

        print(textwrap.dedent("""
                    $$$ Carrito $$$
                1) Agregar producto a carrito
                2) Eliminar producto del carrito
                3) Vaciar carrito
                4) Pagar carrito
                0) Cancelar venta"""))

        opt = detectar_valor_entero_positivo("")

        if opt == 1:
            agregar_producto_carrito(inv)
        elif opt == 2:
            eliminar_producto_carrito()
        elif opt == 3:
            x = 0
        elif opt == 4:
            x = 0
        else:
            break

def agregar_producto_carrito(inv):
    x = 0

def eliminar_producto_carrito():
    x = 0

# TODO relacionado con gestion de inventario //////////////////////

def menu_inventario(inv):
    while True:

        print(textwrap.dedent("""
                ◘◘◘ Inventario ◘◘◘
                1) Ver inventario
                2) Agregar nuevo producto
                3) Modificar/Eliminar productos
                0) Salir"""))

        opt = detectar_valor_entero_positivo("")

        if opt == 1:
            ver_inventario(inv)
        elif opt == 2:
            agregar_producto(inv)
        elif opt == 3:
            administrar_inventario(inv)
        else:
            break

def ver_inventario(inv):
    for llave, producto in inv.items():
        print(f"--ID: {llave}--", imprimir_producto(producto))

def agregar_producto(inv):
    global ID
    print("--------------------")

    nombre = input("Nombre: ")

    categoria = input("Categoría: ")

    precio = detectar_valor_decimal_positivo("Precio:")

    proveedor = input("Proveedor: ")

    stock = detectar_valor_entero_positivo("Stock:")

    inv[ID] = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "proveedor": proveedor,
        "stock": stock
    }

    ID += 1

    ver_inventario(inv)

def administrar_inventario(inv):
    while True:

        ver_inventario(inv)
        identf = detectar_valor_entero_positivo("¿Que producto desea modificar? (0 -> cancelar)")

        try:
            producto = inv[identf]
        except KeyError:
            if identf != 0:
                print(">>> E404: Producto no encontrado  ...")
            return

        print(f"Producto: {producto["nombre"]}")

        print(textwrap.dedent("""
        ¿Que acción desea realizar?
        1) Modificar atributo
        2) Eliminar producto
        0) Cancelar operación"""))

        opt = detectar_valor_entero_positivo("")

        if opt == 1:
            modificar_atributo(producto)
        elif opt == 2:
            inv.pop(identf)
        else: break

def modificar_atributo(prod):
    while True:
        print(textwrap.dedent("""
        ¿Que atributo desea modificar?
        1) Nombre
        2) Categoría
        3) Precio unitario
        4) Proveedor
        5) Stock ¡¡Verificar stock actual antes de continuar!!
        0) Salir"""))

        opt = detectar_valor_entero_positivo("")

        if opt == 1:
            nuevo_nombre = input("Nuevo nombre: ")
            prod["nombre"] = nuevo_nombre
        elif opt == 2:
            nueva_categoria = input("Nueva categoria: ")
            prod["categoria"] = nueva_categoria
        elif opt == 3:
            nuevo_precio = detectar_valor_decimal_positivo("Nuevo precio:")
            prod["precio"] = nuevo_precio
        elif opt == 4:
            nuevo_proveedor = input("Nuevo proveedor: ")
            prod["proveedor"] = nuevo_proveedor
        elif opt == 5:
            nuevo_stock = detectar_valor_entero_positivo("Nuevo stock:")
            prod["stock"] = nuevo_stock
        else:
            imprimir_producto(prod)
            break

# TODO relacionado con generación de reportes ////////////////////
def menu_reportes(inv):
    x = 0

# TODO relacionado con ejecución del sistema /////////////////////

global ID

# Regresa el ID mayor del inventario actual para usarlo como referencia para nuevos productos
def obtener_mayor_id(inv):
    if not inv:  # si está vacío
        return -1
    return max(inv.keys())+1

def detectar_valor_entero_positivo(mensaje_entrada):
    while True:
        try:
            if mensaje_entrada != "":
                print(mensaje_entrada)

            val = int(input("> "))

            if val < 0:
                print(">>> E402: Valor incoherente detectado, intente de nuevo ...")
                continue

            return val

        except ValueError:
            print(">>> E401: Valor erróneo ingresado, intente de nuevo ...")
            continue

def detectar_valor_decimal_positivo(mensaje_entrada):
    while True:
        try:
            if mensaje_entrada != "":
                print(mensaje_entrada)

            val = float(input("> "))

            if val < 0.01:
                print(">>> E402: Valor incoherente detectado, intente de nuevo ...")
                continue

            return val

        except ValueError:
            print(">>> E401: Valor erróneo ingresado, intente de nuevo ...")
            continue

def imprimir_producto(prod):
    return textwrap.dedent(f"""
            \tNombre: {prod["nombre"]}
            \tCategoría: {prod["categoria"]}
            \tPrecio unitario: ${prod["precio"]}
            \tProveedor: {prod["proveedor"]}
            Stock: {prod["stock"]} Pz""")

if __name__ == "__main__":
    inventario = {
        1: {
            "nombre": "Laptop Nova 14",
            "categoria": "Computadoras",
            "precio": 15899.00,
            "proveedor": "TechWave",
            "stock": 12
        },
        2: {
            "nombre": "Mouse Óptico Swift",
            "categoria": "Periféricos",
            "precio": 249.50,
            "proveedor": "ClickMaster",
            "stock": 34
        },
        3: {
            "nombre": "SSD UltraFlash 512GB",
            "categoria": "Almacenamiento",
            "precio": 999.99,
            "proveedor": "DataStone",
            "stock": 18
        }}
    ID = obtener_mayor_id(inventario)
    menu_principal(inventario)