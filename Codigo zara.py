# Inicialización de variables según tabla de especificaciones
capacidad_maxima = 900
stock_tienda = 360
stock_bodega = 500
stock_total = stock_tienda + stock_bodega
espacio_disponible_total = capacidad_maxima - stock_total
demanda_diaria_clientes = 100

# Datos del producto
nombre_producto = "Chaqueta - Blazer"
Talla_producto = "M"
precio_unitario = 150000.0
ubicacion_actual = "Exhibida"
peticiones_talla_cliente = 0
pedidos_cancelados = 0
ventas_realizadas_dia = 0
total_facturado = 0.0

# Estado inicial y alertas
estado_sincronizacion = True
alerta_falta_prenda = False
alerta_agotamiento_talla = False
disponible_para_venta = True

# Ciclo principal del sistema
while True:
    # Evaluación de alertas en tiempo real
    alerta_agotamiento_talla = (stock_tienda == 0)
    alerta_falta_prenda = (stock_total < 100)
    disponible_para_venta = (stock_total > 0)

    print("==================================================")
    print(" SISTEMA DE SINCRONIZACIÓN DE INVENTARIO ZARA")
    print("==================================================")
    print(
        f"Producto actual: {nombre_producto} | Talla: {Talla_producto} | Precio Unitario: ${precio_unitario:,.2f}")
    print(f"Stock en Tienda: {stock_tienda} | Stock en Bodega: {stock_bodega}")
    print(f"Stock Total: {stock_total} / Capacidad Máx: {capacidad_maxima}")
    print(f"Espacio Disponible Total: {espacio_disponible_total}")
    print(
        f"Ubicación Actual: {ubicacion_actual} | Disponible Venta: {disponible_para_venta}")
    print(f"Sincronización activa: {estado_sincronizacion}")
    print(
        f"Métricas Día -> Ventas: {ventas_realizadas_dia} | Total Facturado: ${total_facturado:,.2f}")
    print(
        f"ALERTAS ACTIVAS -> Agotamiento Talla: {alerta_agotamiento_talla} | Falta Prenda: {alerta_falta_prenda}")
    print("--------------------------------------------------")
    print("1. Procesar venta a cliente (Facturación)")
    print("2. Solicitud de talla por cliente")
    print("3. Sincronizar y Reabastecer piso de exhibición (Bodega -> Tienda)")
    print("4. Registrar pedido cancelado")
    print("5. Ver estado de alertas y métricas del día")
    print("6. Salir")
    print("--------------------------------------------------")

    # Validación: Si no hay stock ni en tienda ni en bodega, se detiene el sistema e indica dirigirse a administración
    if stock_tienda == 0 and stock_bodega == 0:
        print(">> [ALERTA CRÍTICA] No hay stock ni en tienda ni en bodega.")
        print(">> Por favor, diríjase a administración para reabastecer stock en bodega o en tienda.")
        break

    try:
        opcion = int(input("Seleccione una opción: "))
    except ValueError:
        print(">> Entrada inválida. Por favor, ingrese un número entero.\n")
        continue

    if opcion == 1:
        # --- PROCESAR VENTA ---
        if stock_tienda == 0 and stock_bodega == 0:
            print(
                ">> [ALERTA CRÍTICA] No hay stock en tienda ni en bodega. Imposible procesar la venta.")
            print(
                ">> Por favor, diríjase a administración para reabastecer stock en bodega o en tienda.")
            break

        try:
            cantidad_compra = int(
                input("Ingrese la cantidad de prendas a comprar: "))
        except ValueError:
            print(">> Error: Ingrese una cantidad válida.\n")
            continue

        if cantidad_compra <= 0:
            print(">> Error: La cantidad debe ser mayor a 0.")
        elif cantidad_compra <= stock_tienda:
            stock_tienda -= cantidad_compra
            stock_total = stock_tienda + stock_bodega
            espacio_disponible_total = capacidad_maxima - stock_total
            ventas_realizadas_dia += cantidad_compra
            monto_venta = cantidad_compra * precio_unitario
            total_facturado += monto_venta
            ubicacion_actual = "Vendida"
            estado_sincronizacion = True

            if stock_tienda == 0:
                alerta_agotamiento_talla = True

            print(">> Venta procesada exitosamente.")
            print(f">> Facturado en esta venta: ${monto_venta:,.2f}")
            print(f">> Total acumulado facturado hoy: ${total_facturado:,.2f}")
            if alerta_agotamiento_talla:
                print(
                    ">> [ALERTA IMPRESA] ¡Atención! Talla agotada en piso de exhibición.")
        else:
            print(
                ">> [ALERTA] Stock suficiente en piso de exhibición NO disponible.")
            if cantidad_compra <= stock_total:
                print(
                    ">> Hay unidades disponibles en BODEGA. Realice un reabastecimiento (Opción 3).")
            else:
                alerta_falta_prenda = True
                print(
                    ">> [ALERTA CRÍTICA DE FALTA DE PRENDA] Sin inventario suficiente ni en tienda ni en bodega.")
                print(
                    ">> Por favor, diríjase a administración para reabastecer stock en bodega o en tienda.")

    elif opcion == 2:
        # --- PETICIÓN DE TALLA ---
        peticiones_talla_cliente += 1
        print(
            f">> Petición de talla registrada. Total peticiones hoy: {peticiones_talla_cliente}")
        if stock_tienda == 0:
            alerta_agotamiento_talla = True
            print(
                ">> [ALERTA DE FALTA DE TALLA] Talla agotada en el piso de exhibición.")

    elif opcion == 3:
        # --- REABASTECIMIENTO Y SINCRONIZACIÓN BODEGA -> TIENDA ---
        if stock_bodega == 0:
            print(
                ">> [ALERTA] No hay stock en bodega para realizar reabastecimiento.")
            print(
                ">> Por favor, diríjase a administración para reabastecer stock en bodega o en tienda.")
            continue

        try:
            cantidad_reabastecer = int(
                input("Ingrese la cantidad de prendas a mover de Bodega a Tienda: "))
        except ValueError:
            print(">> Error: Ingrese una cantidad válida.\n")
            continue

        if cantidad_reabastecer <= 0:
            print(">> Error: La cantidad debe ser mayor a 0.")
        elif cantidad_reabastecer <= stock_bodega:
            stock_bodega -= cantidad_reabastecer
            stock_tienda += cantidad_reabastecer
            stock_total = stock_tienda + stock_bodega
            espacio_disponible_total = capacidad_maxima - stock_total
            ubicacion_actual = "Exhibida"
            estado_sincronizacion = True

            if stock_tienda > 0:
                alerta_agotamiento_talla = False

            print(">> Reabastecimiento exitoso en tiempo real.")
            print(
                f">> Nuevo stock en tienda: {stock_tienda} | Nuevo stock en bodega: {stock_bodega}")
        else:
            print(
                f">> Error: La cantidad supera el stock disponible en bodega ({stock_bodega}).")

    elif opcion == 4:
        # --- REGISTRO DE PEDIDO CANCELADO ---
        pedidos_cancelados += 1
        print(
            f">> Pedido cancelado registrado. Total cancelaciones: {pedidos_cancelados}")

    elif opcion == 5:
        # --- EVALUACIÓN Y REPORTES ---
        alerta_agotamiento_talla = (stock_tienda == 0)
        alerta_falta_prenda = (stock_total < 100)
        disponible_para_venta = (stock_total > 0)

        print("--------------------------------------------------")
        print(" REPORTES Y ALERTAS ")
        print("--------------------------------------------------")
        print(f"Disponible para venta: {disponible_para_venta}")
        print(f"Alerta falta de prenda: {alerta_falta_prenda}")
        print(f"Alerta agotamiento de talla: {alerta_agotamiento_talla}")
        print(f"Peticiones de talla registradas: {peticiones_talla_cliente}")
        print(f"Pedidos cancelados: {pedidos_cancelados}")
        print(f"Ventas realizadas hoy: {ventas_realizadas_dia}")
        print(f"Total facturado: ${total_facturado:,.2f}")
        print(f"Espacio disponible total: {espacio_disponible_total}")
        print("--------------------------------------------------")

    elif opcion == 6:
        print("Saliendo del sistema de sincronización...")
        break

    else:
        print("Opción inválida. Intente de nuevo.")

    print()
