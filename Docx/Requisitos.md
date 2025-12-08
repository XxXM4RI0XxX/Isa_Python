# Generales
- Estructuras condicionales para toma de decisiones (if)
- Ciclos (while, for)
- Funciones de modularización (CRUD)
- Arreglos (listas, diccionarios) para almacenar información
- Menús interactivos
- Desarrollar habilidades de trabajo en equipo xD
	Para esto ultimo hay 5 roles
	- Líder del proyecto (Coordina y supervisa)
	- Desarrollador de funciones de Entrada
      - Encargado de agregar productos
      - Actualiza el inventario
      - Valida entradas de usuario
	- Desarrollador de funciones de consulta
      - Búsqueda y filtros
      - Visualización de productos
      - Desarrolla reportes
	- Desarrollador de funciones procesamiento
      - Implementa funciones de venta
      - Calcula totales y estadísticas
      - Encargado de las funciones de ordenamiento
	- Responsable de pruebas y documentación
      - Prueba todo el sistema
      - Documenta código y crea el manual de usuario
      - Identifica y reporta errores

# Interfaz
- Un ménu principal, que lleva a diversos submenús dependiendo de la acción elegida
- Después de cada operación se vuelve al submenú correspondiente
- En caso de información errónea del usuario, solo se requiere reingresar el valor

# Estructura de datos
- El inventario es manejado por un diccionario de productos, relacionados con su ID.
- Cada producto es un diccionario relacionado con sus atributos.
- El carrito de compras es una lista que contiene los productos
- El carrito auxiliar es un diccionario que relaciona un ID de producto con la cantidad agregada en el carrito

# Información del producto
- ID
- Nombre
- Categoría (Computadora, accesorio, etc)
- Precio unitario
- Stock
- Proveedor

# Funciones
- ***CRUD de productos***
    - *Mostrar inventario*
      - Se pueden ver todos los productos en una sola lista
      - Los productos se pueden filtrar por: Categoría, disponibilidad o proveedor
      - Los productos se pueden ordenar por: ID, nombre, precio unitario y stock
      - Los productos con *stock* menor a 5 unidades son resaltados de manera llamativa en la lista
      - El inventario muestra el total de piezas
      - El inventario muestra la valuación total de todas las existencias
	- *Agregar producto*
      - Cada producto tiene un ID único e inmutable
      - El sistema requiere ingresar la información completa del producto, caso contrario, se niega el registro del mismo
      - El sistema valída que la información ingresada sea del tipo requerido
	- *Modificar producto*
      - El sistema permite modificar toda la información del producto, excepto ID
      - El sistema válida que la información actualizada sea correcta y coherente (no negativa o nula)
    - *Eliminar producto*
      - La eliminación de productos se realiza producto por producto, para evitar errores
      - El sistema pide confirmación antes de la eliminación del producto
- ***Venta de productos***
    - El sistema crea un carrito de venta donde se agregan los productos a comprar
    - Solo puede existir un carrito por sesión de venta
    - El carrito permite agregar multiples productos, al igual que el mismo producto las veces requeridas
    - El sistema verifica la disponibilidad del producto antes de agregarlo al carrito
    - Se puede vaciar el carrito para comenzar una nueva venta, se pide confirmación antes de completar la acción
    - Al finalizar la venta se genera el ticket de compra, el cual incluye:
      - Fecha de venta
      - Número de venta
      - Productos comprados, con sus cantidades y precios unitarios
      - Total de la compra
    - El inventario se actualiza de manera automática, descontando los productos comprados
    - El sistema vuelve al menú principal una vez completada la venta
- ***Validación***
  - El sistema muestra mensajes de *confirmación*
      - Operación exitosa... y similares
      - Producto no encontrado... y similares
      - Confirmar eliminación... y similares
  - El sistema es capaz de manejar *errores o incoherencias*
    - No se puede vender si no hay stock
    - No se puede registrar precios negativos o en cero
    - No se permite stock negativo

# Funciones avanzadas

- Respaldo de datos (opcional)
- ***Documentación***
- Pruebas unitarias de cada función
- Descripción de cada función (parámetros, retorno, propósito)
- Comentarios y docstrings en el código
- ***Estructura de datos utilizada***
- ***Manual de usuario***
- ***Presentación***
	- Diseño y justificación (porque se eligio ese diseño xd)
- Limitaciones conocidas del sistema

# ***OPCIONAL***
1. Archivos que guarden la información
2. Base de datos
3. Informe estadístico de productos más vendidos
4. Interfaz gráfica