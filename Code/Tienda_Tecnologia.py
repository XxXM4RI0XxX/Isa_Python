import textwrap
import os, json
from datetime import datetime

def menu_principal(inv):
    while True:

        print(textwrap.dedent("""
            ______Menu______
        1) Realizar venta
        2) Administrar inventario
        3) Generar reporte
        0) Salir"""))

        opt = detectar_valor_entero_positivo("")

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
        print("No hay ningún producto en inventario :o ...")
        return
    carrito = []
    carrito_aux = {}
    while True:

        print(textwrap.dedent("""
                    $$$ Carrito $$$
                1) Agregar producto a carrito
                2) Eliminar producto del carrito
                3) Ver productos en carrito
                4) Vaciar carrito
                5) Pagar carrito
                0) Cancelar venta"""))

        opt = detectar_valor_entero_positivo("")

        if opt == 1:
            agregar_producto_carrito(inv,carrito,carrito_aux)
        elif opt == 2:
            if not carrito:
                print("No hay ningún producto en el carrito ...")
                continue
            eliminar_producto_carrito(inv,carrito,carrito_aux)
        elif opt == 3:
            ver_carrito(carrito,carrito_aux)
        elif opt == 4:
            if not carrito:
                print("No hay ningún producto en el carrito ...")
                continue
            print("Confirmar vaciar carrito [1) Si , otro) Cancelar")
            opt = input("> ")
            if opt == '1':
                vaciar_carrito(inv,carrito,carrito_aux)
                print("¡ Carrito vaciado !")
        elif opt == 5:
            if not carrito:
                print("No hay ningún producto en el carrito ...")
                continue
            finalizar_compra(carrito,carrito_aux)
            break
        else:
            if carrito:
                opt = input("Se vaciará el carrito, ¿Continuar? [1) Si , Otro) No]\n> ")
                if opt == "1":
                    vaciar_carrito(inv,carrito,carrito_aux)
                    break
            break

def agregar_producto_carrito(inv,carr,c_aux):
    ver_inventario(inv)

    id_prod = detectar_valor_entero_positivo("Producto a agregar:")

    if not detectar_existencia_inventario(inv,id_prod):
        return

    prod = None

    for id_p , p in inv.items():
        if id_p == id_prod:
            if p["stock"] < 1:
                print("No hay suficiente inventario para agregar ...")
                return
            prod = p
            p["stock"] -= 1
            break

    if carr.count(prod) == 0:
        carr.append(inv[id_prod])
        c_aux[prod["ID"]] = 1
    else:
        c_aux[prod["ID"]] += 1

    print(f"¡ Producto {inv[id_prod]["nombre"]} agregado con exito !")

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
        print(">>> E406: Producto no existe en carrito ...")
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

    print(f"¡ Producto {inv[id_prod]["nombre"]} eliminado con exito !")

def ver_carrito(carr,c_aux):
    print("--- CARRITO ---")
    if not carr:
        print("No hay ningún producto agregado al carrito ...")
        return
    print("╔" + "═" * 70 + "╗")
    print(f"║{"ID":>3} │ {"Cant":<5} │ {"Nombre":<30} │ {"Precio":<10} │ {"Total":>10}║")
    print(f"╠{"═" * 4:>3}╤{"═" * 7:<5}╤{"═" * 32:<30}╤{"═" * 12:<10}╤{"═" * 11:>10}╣")
    for prod in carr:
        imprimir_producto_carrito(prod,c_aux)
    print(f"╚{"═" * 4:>3}╧{"═" * 7:<5}╧{"═" * 32:<30}╧{"═" * 12:>10}╧{"═" * 11:>10}╝")

def imprimir_carrito(carr,c_aux):
    texto = ""
    for prod in carr:
        texto += f"{prod["ID"]} | {c_aux[prod["ID"]]}  {prod["nombre"]}  ${prod["precio"]} == ${prod["precio"] * c_aux[prod["ID"]]}\n\t"

    return texto

def vaciar_carrito(inv,carr,c_aux):
    if not carr:
        return
    for id_p in c_aux: # Regresar productos al inventario
        p = inv[id_p]
        p["stock"] += c_aux[id_p]

    carr.clear()

def finalizar_compra(carr,c_aux):
    if not carr:
        return

    total = 0

    for prod, (id_prod, cantidad) in zip(carr, c_aux.items()):
        total += prod["precio"] * cantidad

    print(textwrap.dedent(f"""
    Artículos: {len(carr)}
    -----------------------------------------------------
    {imprimir_carrito(carr,c_aux)}-----------------------------------------------------
    Total: ${total}
    ¿Desea completar la compra? [1) Si , Otro) No]"""))

    opt = input("> ")

    if opt != "1":
        print("Compra cancelada...")
        return

    print(" ¡ Compra completada !")

    generar_ticket_venta(carr,c_aux,total)

    carr.clear()

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
    print("--- INVENTARIO ---")
    if not inv:
        print("No hay ningun producto en inventario ...")
        return
    print("╔" + "═" * 112 + "╗")
    print(f"║{"ID":>3} │ {"Nombre":<30} │ {"Proveedor":<30} │ {"Categoria":<20} │{"Precio":>10} │ {"Stock":>5}║")
    print(f"╠{"═"*4:>3}╤{"═"*32:<30}╤{"═"*32:<30}╤{"═"*22:<20}╤{"═"*11:>10}╤{"═"*6:>5}╣")
    for llave, producto in inv.items():
        imprimir_producto_inventario(producto)
    print(f"╚{"═"*4:>3}╧{"═"*32:<30}╧{"═"*32:<30}╧{"═"*22:<20}╧{"═"*11:>10}╧{"═"*6:>5}╝")

def agregar_producto(inv):
    global identificador
    if not inv:
        identificador += 2
    print("[Dejar vacío para cancelar (Excepto al ingresar valores numéricos)]")

    nombre = input("Nombre:\n> ")
    if nombre == "":
        print("Cancelando ...")
        return

    categoria = input("Categoría:\n> ")
    if categoria == "":
        print("Cancelando ...")
        return

    precio = detectar_valor_decimal_positivo("Precio:")

    proveedor = input("Proveedor:\n> ")
    if proveedor == "":
        print("Cancelando ...")
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

    ver_inventario(inv)

def administrar_inventario(inv):
    if not inv:
        print("No hay ningún producto en inventario :o ...")
        return
    while True:
        ver_inventario(inv)
        if not inv:
            return
        id_prod = detectar_valor_entero_positivo("¿Que producto desea modificar? (0 -> cancelar)")

        try:
            producto = inv[id_prod]
        except KeyError:
            if id_prod != 0:
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
            inv.pop(id_prod)
        else: break

def modificar_atributo(prod):
    while True:
        print("->" + prod["nombre"])
        print(textwrap.dedent("""
        ¿Que atributo desea modificar?
        1) Nombre
        2) Categoría
        3) Precio unitario
        4) Proveedor
        5) Aumentar/Disminuir stock ¡¡Verificar stock actual antes de continuar!!
        0) Salir"""))

        opt = detectar_valor_entero_positivo("")

        if opt == 1:
            nuevo_nombre = detectar_cadena_vacia("Nuevo nombre:")
            prod["nombre"] = nuevo_nombre
        elif opt == 2:
            nueva_categoria = detectar_cadena_vacia("Nueva categoria:")
            prod["categoria"] = nueva_categoria
        elif opt == 3:
            nuevo_precio = detectar_valor_decimal_positivo("Nuevo precio:")
            prod["precio"] = nuevo_precio
        elif opt == 4:
            nuevo_proveedor = detectar_cadena_vacia("Nuevo proveedor:")
            prod["proveedor"] = nuevo_proveedor
        elif opt == 5:

            nuevo_stock = detectar_valor_entero("+/- stock:")
            if nuevo_stock == 0:
                print("...Porque?... Cancelando...")
                continue
            elif nuevo_stock < 0 and (prod["stock"] + nuevo_stock) < 0:
                print(">>> E407: No se puede reducir stock no existente...")
                continue
            else:
                prod["stock"] += nuevo_stock
        else:
            break

# TODO relacionado con generación de reportes ////////////////////
def menu_reportes(inv):
    x = 0

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
            print(">>> E404: Producto no encontrado  ...")
            return False

def detectar_cadena_vacia(mensaje_entrada):
    while True:
        if mensaje_entrada != "":
            print(mensaje_entrada)

        cad = input("> ")

        if cad.strip() == "":
            print(">>> E405: Se necesita ingresar un valor ...")
            continue

        return cad

def detectar_valor_entero_positivo(mensaje_entrada):
    while True:
        try:
            if mensaje_entrada != "":
                print(mensaje_entrada)

            val = int(input("> "))

            if val < 0:
                print(">>> E408: Valor incoherente detectado, intente de nuevo ...")
                continue

            return val

        except ValueError:
            print(">>> E401: Valor erróneo ingresado, intente de nuevo ...")
            continue
            
def detectar_valor_entero(mensaje_entrada):
    while True:
        try:
            if mensaje_entrada != "":
                print(mensaje_entrada)

            val = int(input("> "))

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
                print(">>> E408: Valor incoherente detectado, intente de nuevo ...")
                continue

            return val

        except ValueError:
            print(">>> E401: Valor erróneo ingresado, intente de nuevo ...")
            continue

def imprimir_producto_inventario(prod):
    print(f"║{prod["ID"]:>3} │ {prod["nombre"]:<30} │ {prod["proveedor"]:<30} │ {prod["categoria"]:<20} │${prod["precio"]:>10.2f}│ {prod["stock"]:>5}║")

def imprimir_producto_carrito(prod,c_aux):
    print(f"║{prod["ID"]:>3} │ {c_aux[prod["ID"]]:>5} │ {prod["nombre"]:<30} │${prod["precio"]:>10.2f} │${prod["precio"] * c_aux[prod["ID"]]:>10.2f}║")
    #print(f"{prod["ID"]} | {c_aux[prod["ID"]]}  {prod["nombre"]}  ${prod["precio"]} == ${prod["precio"] * c_aux[prod["ID"]]}")

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

global identificador

if __name__ == "__main__":
    inventario = {}
    identificador = obtener_mayor_id(inventario)
    menu_principal(inventario)