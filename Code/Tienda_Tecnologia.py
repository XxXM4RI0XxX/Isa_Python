import textwrap
import os, json
from datetime import datetime

def menu_principal(inv):
    while True:

        print(textwrap.dedent(f"""
            {NEGRITA}{MORADO}☼ ☼ ☼ MENU ☼ ☼ ☼{BLANCO}
        1) Realizar venta
        2) Administrar inventario
        3) Generar reporte
        0) Salir"""))

        opt = detectar_valor_entero_positivo("",3)

        if opt == 1:
            menu_ventas(inv)
        elif opt == 2:
            menu_inventario(inv)
        elif opt == 3:
            menu_reportes(inv)
        else:
            break

# TODO relacionado con carrito de ventas ///////////////////////
def menu_ventas(inv):
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
    while True:
        ver_productos_inventario(inv)

        id_prod = detectar_id_filtro("Opción ó ID de producto:")
        try:
            if id_prod.upper() == 'F':
                inv_aux = menu_filtro(inv)
                if not inv_aux:
                    print(f"{AMARILLO}No hubo coincidencias ...{BLANCO}")
                    return inv
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
        c_aux[prod["ID"]] += 1

    print(f"{VERDE}¡ Producto {inv[id_prod]["nombre"]} agregado con exito !{BLANCO}")

    return inv

def eliminar_producto_carrito(inv,carr,c_aux):
    ver_carrito(carr,c_aux)
    if not carr:
        return
    id_prod = detectar_valor_entero_positivo("Producto a eliminar:")
    
    prod = None
    
    for p in carr:
        if p["ID"] == id_prod:
            prod = p
            break
            
    if prod is None:
        print(f"{ROJO}'>>> E406: Producto no existe en carrito ...{BLANCO}")
        return

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
    print(f"{NEGRITA}{MORADO}◙ ◙ ◙ CARRITO ◙ ◙ ◙{BLANCO}")
    if not carr:
        print(f"{AMARILLO}No hay ningún producto agregado al carrito ...{BLANCO}")
        return
    imprimir_carrito(carr,c_aux)

def imprimir_carrito(carr,c_aux):
    print("╔" + "═" * 70 + "╗")
    print(f"║{"ID":>3} │ {"Cant":<5} │ {"Nombre":<30} │ {"Precio":<10} │ {"Total":>10}║")
    print(f"╠{"═" * 4:>3}╤{"═" * 7:<5}╤{"═" * 32:<30}╤{"═" * 12:<10}╤{"═" * 11:>10}╣")
    for prod in carr:
        imprimir_producto_carrito(prod, c_aux)
    print(f"╚{"═" * 4:>3}╧{"═" * 7:<5}╧{"═" * 32:<30}╧{"═" * 12:>10}╧{"═" * 11:>10}╝")

def vaciar_carrito(inv,carr,c_aux):
    if not carr:
        return
    for id_p in c_aux: # Regresar productos al inventario
        p = inv[id_p]
        p["stock"] += c_aux[id_p]

    carr.clear()

def finalizar_compra(carr,c_aux):
    if not carr:
        return False

    total = 0

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
    global inventario
    while True:
        print(textwrap.dedent(f"{NEGRITA}{MORADO}◘ ◘ ◘ INVENTARIO ◘ ◘ ◘{BLANCO}"))
        ver_productos_inventario(inv,False) # Imprimir inventario
        print(f"{AZUL}Opcion: 'A' para agregar un nuevo producto{BLANCO}")

        id_prod = detectar_id_filtro("Opción ó ID de producto:",True) # Elegir opcion
        try:
            if id_prod.upper() == 'A':
                agregar_producto(inv) # Si la opción es agregar un producto
                continue
            elif id_prod.upper() == 'F' and inv: # Si la opción es Filtrar 'F'
                inv_aux = menu_filtro(inv) # Regresa un inventario auxiliar filtrado
                if not inv_aux:
                    print(f"{AMARILLO}No hubo coincidencias ...{BLANCO}")
                    return inv
                menu_inventario(inv_aux) # Itera de nuevo el menu de inventario con el nuevo inventario filtrado
                break
            elif id_prod.upper() == 'O' and inv: # Ordenar el inventario
                inv = dict(menu_orden(inv))
                continue
            else:
                print(f"{ROJO}E000: ERROR DESCONOCIDO !..{BLANCO}")
                return
        except AttributeError: # En caso de detectar ID de producto envés de opción
            if id_prod == 0: # Si es 0 cancela
                print(f"{AMARILLO}Cancelando...{BLANCO}")
                return inv

        try:
            producto = inv[id_prod] # Verificar existencia en inventario
        except KeyError:
            if id_prod != 0:
                print(f"{ROJO}>>> E404: Producto no encontrado  ...{BLANCO}")
            return inv

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
            break

def ver_productos_inventario(inv,titulo=True):
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
    global identificador
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
            nuevo_nombre = detectar_cadena_vacia(f"Nuevo nombre:")
            prod["nombre"] = nuevo_nombre
        elif opt == 2:
            nueva_categoria = detectar_cadena_vacia(f"Nueva categoria: ")
            prod["categoria"] = nueva_categoria
        elif opt == 3:
            nuevo_precio = detectar_valor_decimal_positivo(f"Nuevo precio: ")
            prod["precio"] = nuevo_precio
        elif opt == 4:
            nuevo_proveedor = detectar_cadena_vacia(f"Nuevo proveedor: ")
            prod["proveedor"] = nuevo_proveedor
        elif opt == 5:

            nuevo_stock = detectar_valor_entero(f"+/- stock: {AMARILLO}[{prod["stock"]}]{BLANCO}")
            if nuevo_stock == 0:
                print("...Porque?... Cancelando...")
                continue
            elif nuevo_stock < 0 and (prod["stock"] + nuevo_stock) < 0:
                print(f"{ROJO}>>> E407: No se puede reducir stock no existente...{BLANCO}")
                continue
            else:
                prod["stock"] += nuevo_stock
        else:
            break

# TODO relacionado con generación de reportes ////////////////////
def menu_reportes(inv):
    x = 0

# TODO relacionado con búsquedas y filtros

def menu_filtro(inv):
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
        texto = detectar_cadena_vacia("Texto a buscar:")
        if opt == 1:
            inv_aux = buscar_productos(inv,texto,"nombre")
        if opt == 2:
            inv_aux = buscar_productos(inv,texto,"proveedor")
        if opt == 3:
            inv_aux = buscar_productos(inv,texto,"categoria")
        return inv_aux

def inventario_filtrado(inv_aux):
    while True:
        ver_productos_inventario(inv_aux,False)
        print(textwrap.dedent(f"""                {NEGRITA}{MORADO}◘ ◘ ◘ INVENTARIO (Filtrado) ◘ ◘ ◘{BLANCO}
                1) Volver a filtrar
                0) Salir"""))

        opt = detectar_valor_entero_positivo("",1)

        if opt == 1:
            inv_aux = menu_filtro(inv_aux)
            if not inv_aux:
                print(f"{AMARILLO}No hubo coincidencias ...{BLANCO}")
                return inv_aux
            inventario_filtrado(inv_aux)
            break
        else:
            break

def buscar_productos(inv, texto, criterio):
    texto = texto.lower()
    resultados = []

    for id_prod, prod in inv.items():
        if texto in prod[criterio].lower():
            resultados.append((id_prod, prod))

    return dict(resultados)

def menu_orden(inv):
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
    inv_ordenado = list(inv.items())

    inv_ordenado.sort(key=lambda prod : prod[1][crit], reverse=invertir)

    return inv_ordenado

# TODO relacionado con ejecución del sistema /////////////////////

# Regresa el ID mayor del inventario actual para usarlo como referencia para nuevos productos
def obtener_mayor_id(inv):
    if not inv:  # si está vacío
        return -1
    return max(inv.keys())+1

def detectar_existencia_inventario(inv,id_prod):
    try:
        prod = inv[id_prod]
        return True
    except KeyError:
        if id != 0:
            print(f"{ROJO}>>> E404: Producto no encontrado  ...{BLANCO}")
            return False

def detectar_cadena_vacia(mensaje_entrada):
    while True:
        if mensaje_entrada != "":
            print(mensaje_entrada)

        cad = input("> ")

        if cad.strip() == "":
            print(f"{ROJO}>>> E405: Se necesita ingresar un valor ...{BLANCO}")
            continue

        return cad

def detectar_id_filtro(mensaje_entrada, agregar=False):
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

def detectar_valor_entero_positivo(mensaje_entrada,valor_maximo = -1):
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
    if prod["stock"] > 5:
        print(f"║{prod["ID"]:>3} │ {prod["nombre"]:<30} │ {prod["proveedor"]:<30} │ {prod["categoria"]:<20} │${prod["precio"]:>10.2f}│ {prod["stock"]:>5}║")
    elif prod["stock"] > 0:
        print(f"║{AMARILLO}{prod["ID"]:>3} │ {prod["nombre"]:<30} │ {prod["proveedor"]:<30} │ {prod["categoria"]:<20} │${prod["precio"]:>10.2f}│ {prod["stock"]:>5}{BLANCO}║")
    else:
        print(f"║{ROJO}{prod["ID"]:>3} │ {prod["nombre"]:<30} │ {prod["proveedor"]:<30} │ {prod["categoria"]:<20} │${prod["precio"]:>10.2f}│ {prod["stock"]:>5}{BLANCO}║")

def imprimir_producto_carrito(prod,c_aux):
        print(f"║{prod["ID"]:>3} │ {c_aux[prod["ID"]]:>5} │ {prod["nombre"]:<30} │${prod["precio"]:>10.2f} │${prod["precio"] * c_aux[prod["ID"]]:>10.2f}║")

def generar_ticket_venta(carr,c_aux,total):
    os.makedirs("Tickets_venta", exist_ok=True)

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"Tickets_venta/Ticket_{fecha}.json"

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

if __name__ == "__main__":
    inventario = {
        1: {
            "ID": 1,
            "nombre": "Router Nimbus AX1800",
            "categoria": "Redes",
            "precio": 799.00,
            "proveedor": "NetWave",
            "stock": 7
        },
        2: {
            "ID": 2,
            "nombre": "Cámara Web CrystalView 1080p",
            "categoria": "Periféricos",
            "precio": 459.90,
            "proveedor": "OptiCam",
            "stock": 3
        },
        3: {
            "ID": 3,
            "nombre": "PowerBank Thunder 20,000mAh",
            "categoria": "Energía",
            "precio": 349.00,
            "proveedor": "ChargeFlow",
            "stock": 1
        }
    }
    identificador = obtener_mayor_id(inventario)
    menu_principal(inventario)