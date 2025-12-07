import textwrap
import os, json
from datetime import datetime

def menu_principal(inv):
    """
    Este es el menú principal de todo el programa, desde aquí se puede acceder a todas las funciones
    :param inv: El inventario principal
    """
    while True:
        print(textwrap.dedent(f"""
            {NEGRITA}{MORADO}☼ ☼ ☼ MENU ☼ ☼ ☼{BLANCO}
        1) Realizar venta
        2) Administrar inventario
        0) Salir"""))

        opt = detectar_valor_entero_positivo("",3)

        if opt == 1:
            menu_ventas(inv)
        elif opt == 2:
            menu_inventario(inv)
        else:
            break

# TODO relacionado con carrito de ventas ///////////////////////

def menu_ventas(inv):
    """
    El menú de ventas permite el acceso al carrito de compras, el cual se puede llenar y vaciar de productos, y sirve para juntar multiples productos antes de pagar.
    También existe un carrito de compras auxiliar, el cual lleva la cuenta de la cantidad agregada de un solo producto
    :param inv: Inventario principal
    """

    # Verificar que haya existencias en inventario
    if not inv:
        print(f"{AMARILLO}No hay ningún producto en inventario :o ...{BLANCO}")
        return
    carrito = []
    carrito_aux = {}
    while True:

        print(textwrap.dedent(f"""
                    {NEGRITA}{MORADO}$ $ $ VENTA $ $ ${BLANCO}
                1) Agregar producto a carrito
                2) Eliminar producto del carrito
                3) Ver productos en carrito
                4) Vaciar carrito
                5) Pagar carrito
                0) Cancelar venta"""))

        opt = detectar_valor_entero_positivo("",5)

        if opt == 1:
            inv = agregar_producto_carrito(inv,carrito,carrito_aux)
        elif opt == 2:
            if not carrito:
                print(f"{AMARILLO}No hay ningún producto en el carrito ...{BLANCO}")
                continue
            eliminar_producto_carrito(inv,carrito,carrito_aux)
        elif opt == 3:
            ver_carrito(carrito,carrito_aux)
        elif opt == 4:
            if not carrito:
                print(f"{AMARILLO}No hay ningún producto en el carrito ...{BLANCO}")
                continue
            print(f"{AZUL}Confirmar vaciar carrito [1) Si , otro) Cancelar]{BLANCO}")
            opt = input("> ")
            if opt == '1':
                vaciar_carrito(inv,carrito,carrito_aux)
                print(f"{VERDE}¡ Carrito vaciado !{BLANCO}")
        elif opt == 5:
            if not carrito:
                print(f"{AMARILLO}No hay ningún producto en el carrito ...{BLANCO}")
                continue

            if finalizar_compra(carrito,carrito_aux):
                break
        else:
            if carrito:
                opt = input(f"{AZUL}Se vaciará el carrito, ¿Continuar? [1) Si , Otro) No]\n> {BLANCO}")
                if opt == "1":
                    vaciar_carrito(inv,carrito,carrito_aux)
                    print(f"{AMARILLO}Cancelada ...{BLANCO}")
                    break
            print(f"{AMARILLO}Cancelada ...{BLANCO}")
            break

def agregar_producto_carrito(inv,carr,c_aux):
    """
    Permite agregar uno por uno los productos del inventario al carrito de compra, descontando stock del inventario (siempre y cuando haya disponibilidad del producto)
    :param inv: Inventario principal
    :param carr: Carrito de compras principal
    :param c_aux: Carrito de compras auxiliar
    :return: Inventario principal
    """

    # El apartado de filtrado permite aplicar multiples filtros al inventario antes de elegir un producto
    while True:
        ver_productos_inventario(inv)

        id_prod = detectar_id_filtro("Opción ó ID de producto:")
        try:
            if id_prod.upper() == 'F':
                #Crea un inventario auxiliar, el cual solo contiene los productos filtrados
                inv_aux = menu_filtro(inv)
                if not inv_aux:
                    print(f"{AMARILLO}No hubo coincidencias ...{BLANCO}")
                    return inv
                # Se accede de nuevo a la misma función, pero con el inventario filtrado
                agregar_producto_carrito(inv_aux,carr, c_aux)
                return inv
            elif id_prod.upper() == 'O':
                inv = dict(menu_orden(inv))
        except AttributeError:
            if id_prod == 0:
                print(f"{AMARILLO}Cancelando...{BLANCO}")
                return inv
            else:
                break

    if not detectar_existencia_inventario(inv,id_prod):
        return inv

    prod = None

    # Verificar disponibilidad en inventario
    for id_p , p in inv.items():
        if id_p == id_prod:
            if p["stock"] < 1:
                print(f"{AMARILLO}No hay suficiente inventario para agregar ...{BLANCO}")
                return inv
            prod = p
            p["stock"] -= 1
            break

    if carr.count(prod) == 0:
        carr.append(inv[id_prod])
        c_aux[prod["ID"]] = 1
    else:
        # Si el producto ya existe en el carrito principal, solo lo suma al carrito auxiliar
        c_aux[prod["ID"]] += 1

    print(f"{VERDE}¡ Producto {inv[id_prod]["nombre"]} agregado con exito !{BLANCO}")

    return inv

def eliminar_producto_carrito(inv,carr,c_aux):
    """
    Permite eliminar uno por uno los productos agregados al carrito de compras.
    Primero verifica si el producto está agregado al carrito de compras, para después eliminarlo y regresar el stock al inventario
    :param inv: Inventario principal
    :param carr: Carrito de compras
    :param c_aux: Carrito de compras auxiliar
    :return:
    """
    ver_carrito(carr,c_aux)
    if not carr:
        return
    id_prod = detectar_valor_entero_positivo("Producto a eliminar:")

    prod = None

    #Verificar que el producto exista en el carrito
    for p in carr:
        if p["ID"] == id_prod:
            prod = p
            break
    if prod is None:
        print(f"{ROJO}'>>> E406: Producto no existe en carrito ...{BLANCO}")
        return

    # Eliminar de carritos y devolver inventario
    for id_p, p in inv.items():
        if id_p == id_prod:
            p["stock"] += 1
            break
    if c_aux[prod["ID"]] > 1:
        c_aux[prod["ID"]] -= 1
    else:
        c_aux.pop(prod["ID"])
        carr.remove(prod)

    print(f"{VERDE}¡ Producto {inv[id_prod]["nombre"]} eliminado con exito !{BLANCO}")

def ver_carrito(carr,c_aux):
    """
    Permite visualizar todos los productos agregados al carrito de compras.
    También muestra el valor total del carrito y el número de productos agregados.
    :param carr: Carrito de compras
    :param c_aux: Carrito de compras auxiliar
    :return:
    """
    print(f"{NEGRITA}{MORADO}◙ ◙ ◙ CARRITO ◙ ◙ ◙{BLANCO}")
    if not carr:
        print(f"{AMARILLO}No hay ningún producto agregado al carrito ...{BLANCO}")
        return
    imprimir_carrito(carr,c_aux)

    productos , total = total_productos_carrito(carr,c_aux)

    print(f"{CIAN}Productos: {productos}")
    print(f"Total carrito: ${total}{BLANCO}")

def imprimir_carrito(carr,c_aux):
    """
    Muestra en consola visualizar todos los productos en el carrito de compras, acomodados en una tabla con diseño.
    :param carr: Carrito de compras
    :param c_aux: Carrito auxiliar
    """
    print("╔" + "═" * 70 + "╗")
    print(f"║{"ID":>3} │ {"Cant":<5} │ {"Nombre":<30} │ {"Precio":<10} │ {"Total":>10}║")
    print(f"╠{"═" * 4:>3}╤{"═" * 7:<5}╤{"═" * 32:<30}╤{"═" * 12:<10}╤{"═" * 11:>10}╣")
    for prod in carr:
        imprimir_producto_carrito(prod, c_aux)
    print(f"╚{"═" * 4:>3}╧{"═" * 7:<5}╧{"═" * 32:<30}╧{"═" * 12:>10}╧{"═" * 11:>10}╝")

def vaciar_carrito(inv,carr,c_aux):
    """
    Elimina todos los productos agregados al carrito de compras (también vacía el carrito auxiliar), y devuelve el stock al inventario
    :param inv: Inventario principal
    :param carr: Carrito de compras
    :param c_aux: Carrito auxiliar
    :return:
    """
    if not carr:
        return
    for id_p in c_aux:
        p = inv[id_p]
        p["stock"] += c_aux[id_p]

    carr.clear()
    c_aux.clear()

def finalizar_compra(carr,c_aux):
    """
    Muestra todos los productos agregados al carrito de compras, con su cantidad, precio unitario y totales.
    Muestra el total de la compra y pide confirmación para finalizar la venta.
    Una vez finalizada la compra, se genera el ticket de venta
    :param carr: Carrito de compras
    :param c_aux: Carrito auxiliar
    :return: ``True``: Compra completada ``False``: Compra cancelada o carrito vacío
    """
    if not carr:
        return False

    total = 0
    # Consigue el total multiplicando el precio unitario por la cantidad de productos en el carrito auxiliar
    for prod, (id_prod, cantidad) in zip(carr, c_aux.items()):
        total += prod["precio"] * cantidad

    print(f"Artículos: {len(carr)}")

    ver_carrito(carr,c_aux)

    print(f"Total: ${total}")
    print(f"{AZUL}¿Desea completar la compra? [1) Si , Otro) No]{BLANCO}")

    opt = input("> ")

    if opt != "1":
        print(f"{AMARILLO}Compra cancelada...{BLANCO}")
        return False

    print(f"{VERDE}¡ Compra completada !{BLANCO}")

    generar_ticket_venta(carr,c_aux,total)

    carr.clear()

    return True

# TODO relacionado con gestion de inventario //////////////////////

def menu_inventario(inv):
    """
    El menú de inventario permite el acceso a opciones de gestión de inventario (agregar, visualizar, modificar y eliminar productos).
    Muestra el total de piezas en inventario, y el valor neto del mismo.
    Permite filtrar y ordenar los productos en inventario
    :param inv: Inventario principal
    """
    global inventario
    while True:

        total_stock, total_valor = total_stock_inventario(inv)

        print(textwrap.dedent(f"{NEGRITA}{MORADO}◘ ◘ ◘ INVENTARIO ◘ ◘ ◘{BLANCO}"))
        print(f"{CIAN}Total de piezas en inventario: {total_stock} Pz")
        print(f"{CIAN}Valor total del inventario: ${total_valor:.2f}{BLANCO}")
        ver_productos_inventario(inv,False)
        print(f"{AZUL}Opcion: 'A' para agregar un nuevo producto{BLANCO}")

        id_prod = detectar_id_filtro("Opción ó ID de producto:",True)
        try:
            if id_prod.upper() == 'A':
                agregar_producto(inv)
                continue
            elif id_prod.upper() == 'F' and inv:
                inv_aux = menu_filtro(inv)
                if not inv_aux:
                    print(f"{AMARILLO}No hubo coincidencias ...{BLANCO}")
                    return
                menu_inventario(inv_aux) # Regresa de nuevo al menu de inventario, pero con el nuevo inventario filtrado
                break
            elif id_prod.upper() == 'O' and inv:
                inv = menu_orden(inv)
                continue
            else:
                print(f"{ROJO}E000: ERROR DESCONOCIDO !..{BLANCO}")
                return
        # En caso de detectar ID de producto envés de opción
        except AttributeError:
            if id_prod == 0:
                print(f"{AMARILLO}Cancelando...{BLANCO}")
                return

        # Verificar existencia en inventario
        try:
            producto = inv[id_prod]
        except KeyError:
            if id_prod != 0:
                print(f"{ROJO}>>> E404: Producto no encontrado  ...{BLANCO}")
            return

        print(f"\n{NEGRITA}{MORADO}Producto: {producto["nombre"]}{BLANCO}")

        print(textwrap.dedent("""        ¿Que acción desea realizar?
        1) Modificar atributo
        2) Eliminar producto
        0) Cancelar operación"""))

        opt = detectar_valor_entero_positivo("",2)

        if opt == 1:
            modificar_atributo(producto)
        elif opt == 2:
            opt = input(f"{AZUL}¿Seguro desea eliminar {producto["nombre"]} del inventario? [1) Si | Otro) No]{BLANCO}\n> ")
            if opt == "1":
                inventario.pop(id_prod)
                print(f"{VERDE} ¡ Producto eliminado !{BLANCO}\n")
                break
            else:
                print(f"{AMARILLO}Cancelado ...{BLANCO}")
        else:
            print(f"{AMARILLO}Cancelando ...{BLANCO}")
            break

def ver_productos_inventario(inv,titulo=True):
    """
    Permite visualizar todos los productos en inventario, acomodados en una tabla con diseño.
    :param inv: Inventario principal
    :param titulo: Recibe un valor True o False. Sirve para activar o desactivar el título "○ ○ ○ PRODUCTOS ○ ○ ○"
    """
    if titulo:
        print(f"{NEGRITA}{MORADO}○ ○ ○ PRODUCTOS ○ ○ ○{BLANCO}")
    if not inv:
        print(f"{AMARILLO}No hay ningun producto en inventario ...{BLANCO}")
        return
    print("╔" + "═" * 112 + "╗")
    print(f"║{"ID":>3} │ {"Nombre":<30} │ {"Proveedor":<30} │ {"Categoria":<20} │{"Precio":>10} │ {"Stock":>5}║")
    print(f"╠{"═"*4:>3}╤{"═"*32:<30}╤{"═"*32:<30}╤{"═"*22:<20}╤{"═"*11:>10}╤{"═"*6:>5}╣")
    for llave, producto in inv.items():
        imprimir_producto_inventario(producto)
    print(f"╚{"═"*4:>3}╧{"═"*32:<30}╧{"═"*32:<30}╧{"═"*22:<20}╧{"═"*11:>10}╧{"═"*6:>5}╝")
    print(f"{AZUL}Opciones: 'O' para ordenar resultados | 'F' para filtrar resultados | 0 para salir{BLANCO}")

def agregar_producto(inv):
    """
    Agrega un nuevo producto al inventario, se tienen que llenar todos los campos para poder agregarlo exitosamente
    :param inv: Inventario
    """
    # Se utiliza el ID global para saber cuál es el siguiente ID disponible
    global identificador

    # El ID global comienza en -1 cuando no hay ningún producto en inventario
    if not inv:
        identificador += 2

    print("[Dejar vacío para cancelar (Excepto al ingresar valores numéricos)]")

    nombre = input("Nombre:\n> ")
    if nombre == "":
        print(f"{AMARILLO}Cancelando ...{BLANCO}")
        return

    categoria = input("Categoría:\n> ")
    if categoria == "":
        print(f"{AMARILLO}Cancelando ...{BLANCO}")
        return

    precio = detectar_valor_decimal_positivo("Precio:")

    proveedor = input("Proveedor:\n> ")
    if proveedor == "":
        print(f"{AMARILLO}Cancelando ...{BLANCO}")
        return

    stock = detectar_valor_entero_positivo("Stock:")

    inv[identificador] = {
        "ID": identificador,
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "proveedor": proveedor,
        "stock": stock
    }

    identificador += 1

    ver_productos_inventario(inv)

def modificar_atributo(prod):
    """
    Permite el acceso a cada atributo de un producto.
    Muestra su valor actual y permite la modificación individual de cada uno.
    Para modificar el ``stock`` de un producto, se pide aumentar o disminuirlo (No se puede disminuir más stock del que se tiene)
    :param prod: Producto a modificar
    """
    while True:
        print(f"\n{NEGRITA}{MORADO}{prod["nombre"]}{BLANCO}")
        print(textwrap.dedent(f"""        ¿Que atributo desea modificar?
        1) Nombre
        2) Categoría {CIAN}[{prod["categoria"]}]{BLANCO}
        3) Precio unitario {CIAN}[${prod["precio"]}]{BLANCO}
        4) Proveedor {CIAN}[{prod["proveedor"]}]{BLANCO}
        5) Aumentar/Disminuir stock {AMARILLO}¡¡Verificar stock actual antes de continuar!!{BLANCO}
        0) Salir"""))

        opt = detectar_valor_entero_positivo("",5)

        if opt == 1:
            nuevo_nombre = detectar_entrada_vacia(f"Nuevo nombre:")
            prod["nombre"] = nuevo_nombre
        elif opt == 2:
            nueva_categoria = detectar_entrada_vacia(f"Nueva categoria: ")
            prod["categoria"] = nueva_categoria
        elif opt == 3:
            nuevo_precio = detectar_valor_decimal_positivo(f"Nuevo precio: ")
            prod["precio"] = nuevo_precio
        elif opt == 4:
            nuevo_proveedor = detectar_entrada_vacia(f"Nuevo proveedor: ")
            prod["proveedor"] = nuevo_proveedor
        elif opt == 5:
            modificar_stock = detectar_valor_entero(f"+/- stock: {AMARILLO}[{prod["stock"]}]{BLANCO}")
            if modificar_stock == 0:
                print("...Porque?... Cancelando...")
                continue
            # Verificar cantidad de stock si disminuye
            elif modificar_stock < 0 and (prod["stock"] + modificar_stock) < 0:
                print(f"{ROJO}>>> E407: No se puede reducir stock no existente...{BLANCO}")
                continue
            else:
                prod["stock"] += modificar_stock
        else:
            break

# TODO relacionado con búsquedas y filtros

def menu_filtro(inv):
    """
    Este menú permite elegir el criterio de filtrado para los productos del inventario, por coincidencia de palabras o letras.
    :param inv: Inventario principal
    :return:
    """
    inv_aux = {}
    print(f"{NEGRITA}--- FILTRO ---{BLANCO}")
    print(textwrap.dedent("""
            Criterio de filtrado:
            1) Nombre
            2) Proveedor
            3) Categoria
            0) Ninguno"""))

    opt = detectar_valor_entero_positivo("",5)

    if opt == 0:
        return inv
    else:
        texto = detectar_entrada_vacia("Texto a buscar:")
        if opt == 1:
            inv_aux = buscar_productos(inv,texto,"nombre")
        if opt == 2:
            inv_aux = buscar_productos(inv,texto,"proveedor")
        if opt == 3:
            inv_aux = buscar_productos(inv,texto,"categoria")
        return inv_aux

def buscar_productos(inv, texto, criterio):
    """
    Busca coincidencias en el inventario para filtrar productos.
    Guarda en una lista todos los productos que coincidan con el criterio, y los regresa esa lista como un nuevo inventario a consultar.
    :param inv: Inventario principal
    :param texto: Letras o palabras a buscar
    :param criterio: Criterio de búsqueda
    :return: Inventario filtrado
    """
    texto = texto.lower()
    productos = []

    for id_prod, prod in inv.items():
        if texto in prod[criterio].lower():
            productos.append((id_prod, prod))

    return dict(productos)

def menu_orden(inv):
    """
    Permite elegir el criterio de ordenamiento, este orden se mantendrá hasta que se filtre la tabla o se salga de la vista de la tabla.
    :param inv: Inventario principal
    :return: Inventario ordenado
    """
    print(f"{NEGRITA}--- ORDENAR ---{BLANCO}")
    print(textwrap.dedent("""
                Criterio de orden:
                1) Nombre A-Z
                2) Nombre Z-A
                3) Proveedor A-Z
                4) Proveedor Z-A
                5) Categoría A-Z
                6) Categoría Z-A
                7) Precio 0-$
                8) Precio $-0
                9) Stock 0...
                0) Ninguno"""))

    opt = detectar_valor_entero_positivo("")

    if opt == 1:
        inv = ordenar_inventario(inv,"nombre")
    elif opt == 2:
        inv = ordenar_inventario(inv,"nombre",True)
    elif opt == 3:
        inv = ordenar_inventario(inv, "proveedor")
    elif opt == 4:
        inv = ordenar_inventario(inv, "proveedor",True)
    elif opt == 5:
        inv = ordenar_inventario(inv, "categoria")
    elif opt == 6:
        inv = ordenar_inventario(inv, "categoria",True)
    elif opt == 7:
        inv = ordenar_inventario(inv, "precio")
    elif opt == 8:
        inv = ordenar_inventario(inv, "precio",True)
    elif opt == 9:
        inv = ordenar_inventario(inv, "stock")
    else:
        inv = ordenar_inventario(inv)

    return inv

def ordenar_inventario(inv, crit="ID", invertir = False):
    """
    Ordena el inventario por el criterio elegido.
    Convierte el inventario en una lista, la cual es ordenada con el método ``.sort()`` (que incluyen las listas por defecto) en base al criterio elegido.
    :param inv: Inventario principal
    :param crit: Criterio elegido
    :param invertir: Invertir orden
    :return: Inventario reordenado
    """
    inv_ordenado = list(inv.items())

    inv_ordenado.sort(key=lambda prod : prod[1][crit], reverse=invertir)

    # Se convierte la lista ordenada a diccionario, para que sea compatible con todas las funciones del sistema
    return dict(inv_ordenado)

# TODO relacionado con ejecución del sistema /////////////////////

def obtener_mayor_id(inv):
    """
    Regresa el mayor ID del inventario actual para usarlo como referencia para nuevos productos
    :param inv: Inventario principal
    :return: ``ID`` mayor en inventario
    """
    if not inv:  # si está vacío
        return -1
    return max(inv.keys())+1

def detectar_existencia_inventario(inv,id_prod):
    """
    Detecta si el producto tiene disponibilidad en inventario.
    Funciona buscando el ID ingresado en el inventario, si no existe tal ID, regresa un error
    :param inv: Inventario principal
    :param id_prod: ID de producto ingresado
    :return: ``True``: Existe producto en inventario
    ``False``: Error 404
    """
    try:
        prod = inv[id_prod]
        return True
    except KeyError:
        if id != 0:
            print(f"{ROJO}>>> E404: Producto no encontrado  ...{BLANCO}")
            return False

def total_stock_inventario(inv):
    """
    Regresa el total de piezas en inventario, y el valor total del mismo
    :param inv: Inventario principal
    :return: Stock y valor total
    """
    if not inv:
        return 0, 0.00
    else:
        total_stock = 0
        total_valor = 0.00

        for prod in inv.values():
            total_stock += prod["stock"]
            total_valor += prod["precio"] * prod["stock"]

        return total_stock, total_valor

def total_productos_carrito(carr,c_aux):
    """
    Cuenta el total de productos agregados al carrito y su valuación total
    :param carr: Carrito de compras
    :param c_aux: Carrito auxiliar
    :return: Total de productos y su valuación
    """
    total_productos = 0
    total_valor = 0.00

    for prod, cant in zip(carr,c_aux.values()):
        total_productos += cant
        total_valor += prod["precio"] * cant

    return total_productos , total_valor

def detectar_entrada_vacia(mensaje_entrada):
    """
    Garantiza no recibir entradas vacías del usuario
    :param mensaje_entrada: Entrada del usuario
    :return: Entrada no vacía
    """
    while True:
        if mensaje_entrada != "":
            print(mensaje_entrada)

        cad = input("> ")

        if cad.strip() == "":
            print(f"{ROJO}>>> E405: Se necesita ingresar un valor ...{BLANCO}")
            continue

        return cad

def detectar_id_filtro(mensaje_entrada, agregar=False):
    """
    Se usa para elegir productos y opciones de filtrado al mostrar inventario.
    Garantiza la entrada de una opción de menú correcta, al igual que permite unos cuantos caractéres a ser leídos (Usados para las opciones de búsqueda y filtrado)
    :param mensaje_entrada: Mensaje que se va a mostrar para que el usuario ingrese datos
    :param agregar: Por defecto en ``False``. Activa o desactiva la opción de agregar producto
    :return: Opción de menú
    """
    while True:
        entrada = ''
        try:
            if mensaje_entrada != "":
                print(mensaje_entrada)

            entrada = input("> ")
            val = int(entrada)

            if val < 0:
                print(f"{ROJO}>>> E408: Valor incoherente detectado, intente de nuevo ...{BLANCO}")
                continue

            return val

        except ValueError:
            if entrada.upper() == 'F' or entrada.upper() == 'O':
                return entrada
            if agregar and entrada.upper() == 'A':
                return entrada
            else:
                print(f"{ROJO}>>> E401: Valor erróneo ingresado, intente de nuevo ...{BLANCO}")
                continue

def detectar_valor_entero_positivo(mensaje_entrada,valor_maximo = 0):
    """
    Garantiza que el usuario ingrese un valor entero positivo
    :param mensaje_entrada: Mensaje que se va a mostrar para que el usuario ingrese datos
    :param valor_maximo: Este parámetro sirve para garantizar que no se ingresen opciones de menú que no existen
    :return: Valor entero positivo
    """
    while True:
        try:
            if mensaje_entrada != "":
                print(mensaje_entrada)

            val = int(input("> "))

            if val < 0:
                print(f"{ROJO}>>> E408: Valor incoherente detectado, intente de nuevo ...{BLANCO}")
                continue
            elif valor_maximo > 0:
                if val > valor_maximo:
                    print(f"{ROJO}>>> E400: Opción inexistente, intente de nuevo ...{BLANCO}")
                    continue

            return val

        except ValueError:
            print(f"{ROJO}>>> E401: Valor erróneo ingresado, intente de nuevo ...{BLANCO}")
            continue

def detectar_valor_entero(mensaje_entrada):
    """
    Garantiza que el usuario ingrese un valor entero cualquiera
    :param mensaje_entrada: Mensaje que se va a mostrar para que el usuario ingrese datos
    :return: Valor entero
    """
    while True:
        try:
            if mensaje_entrada != "":
                print(mensaje_entrada)

            val = int(input("> "))

            return val

        except ValueError:
            print(f"{ROJO}>>> E401: Valor erróneo ingresado, intente de nuevo ...{BLANCO}")
            continue

def detectar_valor_decimal_positivo(mensaje_entrada):
    """
    Garantiza que el usuario ingrese un valor decimal positivo
    :param mensaje_entrada: Mensaje que se va a mostrar para que el usuario ingrese datos
    :return: Valor decimal positivo
    """
    while True:
        try:
            if mensaje_entrada != "":
                print(mensaje_entrada)

            val = float(input("> "))

            if val < 0.01:
                print(f"{ROJO}>>> E408: Valor incoherente detectado, intente de nuevo ...{BLANCO}")
                continue

            return val

        except ValueError:
            print(f"{ROJO}>>> E401: Valor erróneo ingresado, intente de nuevo ...{BLANCO}")
            continue

# TODO relacionado con impresión en consola

def imprimir_producto_inventario(prod):
    """
    Función específica para mostrar en consola cada producto del inventario.
    Se resaltan en color amarillo los productos con stock menor a 6, y con rojo los productos sin disponibilidad.
    :param prod: Producto a mostrar
    """
    if prod["stock"] > 5:
        print(f"║{prod["ID"]:>3} │ {prod["nombre"]:<30} │ {prod["proveedor"]:<30} │ {prod["categoria"]:<20} │${prod["precio"]:>10.2f}│ {prod["stock"]:>5}║")
    elif prod["stock"] > 0:
        print(f"║{AMARILLO}{prod["ID"]:>3} │ {prod["nombre"]:<30} │ {prod["proveedor"]:<30} │ {prod["categoria"]:<20} │${prod["precio"]:>10.2f}│ {prod["stock"]:>5}{BLANCO}║")
    else:
        print(f"║{ROJO}{prod["ID"]:>3} │ {prod["nombre"]:<30} │ {prod["proveedor"]:<30} │ {prod["categoria"]:<20} │${prod["precio"]:>10.2f}│ {prod["stock"]:>5}{BLANCO}║")

def imprimir_producto_carrito(prod,c_aux):
        """
        Función específica para mostrar en consola cada producto del carrito de compra
        :param prod: Producto a mostrar
        :param c_aux: Carrito auxiliar
        """
        print(f"║{prod["ID"]:>3} │ {c_aux[prod["ID"]]:>5} │ {prod["nombre"]:<30} │${prod["precio"]:>10.2f} │${prod["precio"] * c_aux[prod["ID"]]:>10.2f}║")

def generar_ticket_venta(carr,c_aux,total):
    """
    Genera los tickets de las ventas realizadas durante la ejecución del programa.
    Estos tickets se guardan en archivos JSON, que son guardados en una carpeta llamada ``Tickets_ventas`` que se crea (si no existe aún) en la misma ubicación del código del sistema.
    Cada ticket guarda la fecha de venta, productos comprados y total de la compra.
    :param carr: Carrito de compras
    :param c_aux: Carrito auxiliar
    :param total: Total de la compra
    """
    # Crea la carpeta "Tickets_ventas" si no existe
    os.makedirs("Tickets_venta", exist_ok=True)

    # Ruta y nombre con el que se guarda cada ticket
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"Tickets_ventas/Ticket_{fecha}.json"

    productos = []

    for prod, (id_prod, cantidad) in zip(carr, c_aux.items()):
        productos.append({"ID":prod["ID"],"nombre":prod["nombre"],
                          "categoria":prod["categoria"],"precio":prod["precio"],
                          "proveedor":prod["proveedor"],"cantidad":c_aux[id_prod]})

    ticket = {
        "fecha": fecha,
        "productos": productos,
        "total": total
    }

    # Crear el archivo JSON del ticket de venta
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(ticket, f, ensure_ascii=False, indent=2)

# TODO relacionado con ejecución del código

# ID global para inventario
global identificador

# Inventario de acceso general
global inventario

# Colores para la consola
NEGRITA = "\033[1m"
ROJO = "\033[31m"
VERDE = "\033[32m"
AMARILLO = "\033[33m"
AZUL = "\033[34m"
MORADO = "\033[35m"
CIAN = "\033[36m"
BLANCO = "\033[0m"

def llenar_inventario():
    """
    Llena el inventario principal con productos predefinidos
    :return: Inventario con productos
    """
    inv = {
        1: {"ID": 1, "nombre": "Laptop Nova 14", "categoria": "Computo", "precio": 15899.00, "proveedor": "TechWave",
            "stock": 12},
        2: {"ID": 2, "nombre": "Mouse Óptico Swift", "categoria": "Periferico", "precio": 249.50,
            "proveedor": "ClickMaster", "stock": 34},
        3: {"ID": 3, "nombre": "Teclado RGB Spectra", "categoria": "Periferico", "precio": 799.00,
            "proveedor": "LightKeys", "stock": 20},
        4: {"ID": 4, "nombre": "Monitor VisionPro 27", "categoria": "Computo", "precio": 4299.00,
            "proveedor": "ViewMax", "stock": 8},
        5: {"ID": 5, "nombre": "USB UltraFlash 64GB", "categoria": "Almacenamiento", "precio": 159.99,
            "proveedor": "DataStone", "stock": 50},
        6: {"ID": 6, "nombre": "SSD Quantum 512GB", "categoria": "Almacenamiento", "precio": 999.00,
            "proveedor": "DataStone", "stock": 18},
        7: {"ID": 7, "nombre": "Audífonos StormBass", "categoria": "Audio", "precio": 349.00, "proveedor": "SoundBeat",
            "stock": 15},
        8: {"ID": 8, "nombre": "Bocina ThunderMini", "categoria": "Audio", "precio": 279.00, "proveedor": "SoundBeat",
            "stock": 22},
        9: {"ID": 9, "nombre": "PowerBank Thunder 20k", "categoria": "Energia", "precio": 349.00,
            "proveedor": "ChargeFlow", "stock": 32},
        10: {"ID": 10, "nombre": "Cargador Rápido 45W", "categoria": "Energia", "precio": 199.00,
             "proveedor": "ChargeFlow", "stock": 40},
        11: {"ID": 11, "nombre": "Router Nimbus AX1800", "categoria": "Redes", "precio": 799.00, "proveedor": "NetWave",
             "stock": 14},
        12: {"ID": 12, "nombre": "Cámara Web CrystalView", "categoria": "Periferico", "precio": 459.90,
             "proveedor": "OptiCam", "stock": 27},
        13: {"ID": 13, "nombre": "MicroSD Turbo 128GB", "categoria": "Almacenamiento", "precio": 209.00,
             "proveedor": "MemMaster", "stock": 45},
        14: {"ID": 14, "nombre": "Impresora LaserJet Mini", "categoria": "Oficina", "precio": 2499.00,
             "proveedor": "PrintCore", "stock": 6},
        15: {"ID": 15, "nombre": "Paquete de Tinta CMYK", "categoria": "Oficina", "precio": 599.00,
             "proveedor": "PrintCore", "stock": 25},
        16: {"ID": 16, "nombre": "Tablet FlexiTab 10", "categoria": "Computo", "precio": 3299.00,
             "proveedor": "NovaTech", "stock": 10},
        17: {"ID": 17, "nombre": "Lámpara LED SmartLight", "categoria": "Hogar", "precio": 189.00,
             "proveedor": "BrightHome", "stock": 30},
        18: {"ID": 18, "nombre": "Teclado Mecánico Titan", "categoria": "Periferico", "precio": 1299.00,
             "proveedor": "GearForge", "stock": 12},
        19: {"ID": 19, "nombre": "Mouse Gamer RazorClaw", "categoria": "Periferico", "precio": 699.00,
             "proveedor": "GearForge", "stock": 18},
        20: {"ID": 20, "nombre": "Hub USB-C 7-en-1", "categoria": "Accesorios", "precio": 499.00,
             "proveedor": "LinkBox", "stock": 16}
    }

    return inv

# Código inicial
if __name__ == "__main__":

    inventario = llenar_inventario()

    identificador = obtener_mayor_id(inventario)

    menu_principal(inventario)