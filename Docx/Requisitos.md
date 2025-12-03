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
Se decidira la estructura de los datos mas adelante xd

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
      - Los productos se muestran con su valor unitario, y valor total de todas las piezas en existencia
      - Los productos con *stock* menor a 5 unidades son resaltados de manera llamativa en la lista
	- *Agregar producto*
      - Cada producto tiene un ID único e inmutable
      - El sistema requiere ingresar la información completa del producto, caso contrario, se niega el registro del mismo
      - El sistema valída que la información ingresada sea del tipo requerido
	- *Modificar producto*
      - El sistema permite modificar toda la información del producto, excepto ID y proveedor
      - El sistema válida que la información actualizada sea correcta y coherente (no negativa o nula)
    - *Eliminar producto*
      - La eliminación de productos se realiza producto por producto, para evitar errores
      - No se puede eliminar un producto que aún tenga stock en inventario
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
- ***Generación de reportes***
    - El sistema permite generar reportes de tanto de ventas como de inventario
    - El reporte de ventas se puede filtrar por un rango de fechas, o una fecha específica. Este reporte contiene:
      - Ventas realizadas en ese rango elegido
      - Productos y cantidades compradas por venta
      - Total de cada venta
      - Un total de los productos comprados y sus cantidades, asi como el total de venta de ese rango de fechas
      - Se puede ordenar por:
        - Número de venta
        - Fecha de venta
        - Total de venta
    - El reporte de inventario se genera tomando en cuenta el inventario actual. Este reporte contiene:
      - Todos los productos registrados en el inventario (aunque no tengan stock)
      - Se muestra cada producto con su precio unitario, stock actual y valor total de stock
      - Se muestra una "valuación total" donde se muestra el valor total de todos los productos en stock
      - Se puede filtrar por disponibilidad
      - Se puede ordenar por:
        - ID de producto
        - Nombre de producto
        - Cantidad en stock (en caso de no estar filtrado por no disponibilidad)
        - Precio unitario y total
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

- ***Respaldo de datos :o*** (opcional xd)
***Documentación***
- Pruebas unitarias de cada función
- Descripción de cada función (parámetros, retorno, propósito)... podrían contar para los docstring xd
- Comentarios y docstrings en el código
- ***Estructura de datos utilizada***
- ***Manual de usuario***
- ***Presentación***
	- Diseño y justificación (porque se eligio ese diseño xd)
- Limitaciones conocidas del sistema

> Hay un cuestionario el cual deben de responder cada integrante del equipo, aqui supongo que depediendo de lo que me diga Isa, puedo generar respuestas con diferentes personalidades xd, o solo las de Isa... Igual el cuestionario se responde al final (QUITAR ESTO XD). Tiene que ir en PDF, incluir ejemplos de código si es necesario

# ***OPCIONAL (Si queda tiempo xd)***
Por complejidad:
1. Archivos que guarden la información
2. Base de datos
3. Informe estadístico de productos más vendidos
4. Interfaz gráfica (si queda muuuucho tiempo nadamás)