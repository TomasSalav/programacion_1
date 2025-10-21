
#PARCIAL 2 - PROBLEMA INTEGRADOR DE PRÁCTICA
#Sistema de Gestión de Restaurante


from datetime import datetime, time, date
import os

# ===================================================================
# EXCEPCIONES PERSONALIZADAS
# ===================================================================

class ErrorRestaurante(Exception):
    #Excepción base para el sistema de restaurante
    pass


class PlatoNoEncontrado(ErrorRestaurante):
    #Se lanza cuando un plato no existe en el menú
    def __init__(self, codigo_plato):
        self.codigo_plato = codigo_plato
        super().__init__(f"Plato con código '{codigo_plato}' no encontrado en el menú")


class MesaNoDisponible(ErrorRestaurante):
    #Se lanza cuando la mesa está ocupada
    def __init__(self, numero_mesa, hora_disponible=None):
        self.numero_mesa = numero_mesa
        self.hora_disponible = hora_disponible
        msg = f"Mesa {numero_mesa} no disponible"
        if hora_disponible:
            msg += f"; se espera disponible a las {hora_disponible}"
        super().__init__(msg)


class CapacidadExcedida(ErrorRestaurante):
    #Se lanza cuando hay más comensales que capacidad
    def __init__(self, numero_mesa, capacidad, comensales):
        self.numero_mesa = numero_mesa
        self.capacidad = capacidad
        self.comensales = comensales
        super().__init__(f"Capacidad excedida en mesa {numero_mesa}: capacidad {capacidad}, comensales {comensales}")


class PedidoInvalido(ErrorRestaurante):
    #Se lanza para pedidos con problemas
    def __init__(self, razon):
        self.razon = razon
        super().__init__(f"Pedido inválido: {razon}")


# ===================================================================
# CLASE PRINCIPAL: SISTEMA RESTAURANTE
# ===================================================================

class SistemaRestaurante:
    #Sistema completo de gestión de restaurante.

    def __init__(self, num_mesas=10, tasa_impuesto=0.16, propina_sugerida=0.15):
        
        #Inicializa el sistema.

       # Args:
        #   num_mesas: Número total de mesas (se crean mesas numeradas desde 1..num_mesas)
        #   tasa_impuesto: Tasa de impuesto (IVA)
        #   propina_sugerida: Propina sugerida por defecto (porcentaje en formato decimal)
    
        # Menú: dict codigo -> {nombre, categoria, precio, disponible}
        self.menu = {}

        # Mesas: dict numero -> {capacidad, ocupado(bool), comensales(int), hora_reserva(time/datetime or None)}
        self.mesas = {}
        for i in range(1, max(1, num_mesas) + 1):
            self.mesas[i] = {
                'capacidad': 4,     # valor por defecto si no se configura
                'ocupado': False,
                'comensales': 0,
                'hora_reserva': None
            }

        # Pedidos: id -> {mesa, items: {codigo: cantidad}, creado: datetime, pagado: bool, pago_info: dict}
        self.pedidos = {}
        self._prox_id_pedido = 1

        # Ventas históricas (lista de dicts) para reportes diarios:
        # {fecha: date, codigo: str, nombre: str, categoria: str, cantidad: int, precio_unit: float, total: float}
        self.ventas = []

        self.tasa_impuesto = float(tasa_impuesto)
        self.propina_sugerida = float(propina_sugerida)

    # ============ GESTIÓN DE MENÚ ============

    def agregar_plato(self, codigo, nombre, categoria, precio):
        
        #Agrega un plato al menú.

        #Raises: ValueError: 
        # Si validaciones fallan
        # KeyError: Si código ya existe
        
        if not codigo or not isinstance(codigo, str):
            raise ValueError("Código inválido")
        if not nombre or not isinstance(nombre, str):
            raise ValueError("Nombre inválido")
        if not categoria or not isinstance(categoria, str):
            raise ValueError("Categoría inválida")
        try:
            precio = float(precio)
        except Exception:
            raise ValueError("Precio inválido")
        if precio < 0:
            raise ValueError("Precio debe ser no negativo")

        if codigo in self.menu:
            raise KeyError(f"Código '{codigo}' ya existe en el menú")

        self.menu[codigo] = {
            'nombre': nombre,
            'categoria': categoria,
            'precio': precio,
            'disponible': True
        }
        return True

    def cambiar_disponibilidad(self, codigo, disponible):
        
        #Cambia disponibilidad de un plato.

        #Raises:
        # PlatoNoEncontrado: Si código no existe
        
        if codigo not in self.menu:
            raise PlatoNoEncontrado(codigo)
        self.menu[codigo]['disponible'] = bool(disponible)
        return True

    def buscar_platos(self, categoria=None, precio_max=None):
       
        #Busca platos por criterios.

        #Returns:
        # Lista de diccionarios con info de platos disponibles

        resultados = []
        for codigo, info in self.menu.items():
            if not info.get('disponible', False):
                continue
            if categoria and info['categoria'].lower() != categoria.lower():
                continue
            if precio_max is not None:
                try:
                    if info['precio'] > float(precio_max):
                        continue
                except Exception:
                    continue
            resultados.append({
                'codigo': codigo,
                'nombre': info['nombre'],
                'categoria': info['categoria'],
                'precio': info['precio'],
            })
        return resultados

    # ============ GESTIÓN DE MESAS ============

    def configurar_mesa(self, numero, capacidad):
        
        #Configura capacidad de una mesa.

        #Raises:
        # ValueError: Si validaciones fallan
       
        if not isinstance(numero, int) or numero <= 0:
            raise ValueError("Número de mesa inválido")
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError("Capacidad inválida")
        if numero not in self.mesas:
            # crear la mesa si no existe
            self.mesas[numero] = {
                'capacidad': capacidad,
                'ocupado': False,
                'comensales': 0,
                'hora_reserva': None
            }
        else:
            self.mesas[numero]['capacidad'] = capacidad
        return True

    def reservar_mesa(self, numero, comensales, hora):
        
        #Reserva una mesa.

        #Args:numero: 
        # numero de mesa (int)
        # comensales: número de personas (int)
        # hora: objeto time o datetime indicando hora de reserva

        #Raises:
        # MesaNoDisponible: Si mesa ocupada
        # CapacidadExcedida: Si comensales > capacidad
        # ValueError: Si validaciones fallan
    
        if numero not in self.mesas:
            raise ValueError(f"Mesa {numero} no existe")
        if not isinstance(comensales, int) or comensales <= 0:
            raise ValueError("Comensales inválidos")
        if not isinstance(hora, (time, datetime)):
            raise ValueError("Hora inválida (debe ser datetime o time)")

        mesa = self.mesas[numero]
        if mesa['ocupado']:
            raise MesaNoDisponible(numero, mesa.get('hora_reserva'))
        if comensales > mesa['capacidad']:
            raise CapacidadExcedida(numero, mesa['capacidad'], comensales)

        mesa['ocupado'] = True
        mesa['comensales'] = comensales
        mesa['hora_reserva'] = hora
        return True

    def liberar_mesa(self, numero):
        
        #Libera una mesa (termina servicio).

        #Raises:
        # ValueError: Si mesa no existe o no está ocupada
       
        if numero not in self.mesas:
            raise ValueError(f"Mesa {numero} no existe")
        mesa = self.mesas[numero]
        if not mesa['ocupado']:
            raise ValueError(f"Mesa {numero} no está ocupada")
        mesa['ocupado'] = False
        mesa['comensales'] = 0
        mesa['hora_reserva'] = None
        return True

    def mesas_disponibles(self, comensales):
        
        #Lista mesas disponibles para N comensales.

        #Returns:
        # Lista de números de mesa
        
        if not isinstance(comensales, int) or comensales <= 0:
            raise ValueError("Comensales inválidos")
        disponibles = []
        for numero, info in self.mesas.items():
            if not info['ocupado'] and info['capacidad'] >= comensales:
                disponibles.append(numero)
        return disponibles

    # ============ GESTIÓN DE PEDIDOS ============

    def crear_pedido(self, numero_mesa):
        
        #Crea un nuevo pedido para una mesa.

        #Returns:
        # id_pedido: ID único del pedido

        #Raises:
        # ValueError: Si validaciones fallan
        
        if numero_mesa not in self.mesas:
            raise ValueError(f"Mesa {numero_mesa} no existe")
        if not self.mesas[numero_mesa]['ocupado']:
            raise ValueError(f"Mesa {numero_mesa} no está ocupada. Reserve/ocupe la mesa primero.")
        id_pedido = self._prox_id_pedido
        self._prox_id_pedido += 1
        self.pedidos[id_pedido] = {
            'mesa': numero_mesa,
            'items': {},  # codigo -> cantidad
            'creado': datetime.now(),
            'pagado': False,
            'pago_info': None
        }
        return id_pedido

    def agregar_item(self, id_pedido, codigo_plato, cantidad=1):
        
        #Agrega items al pedido.

        #Raises:
        # PedidoInvalido: Si pedido no existe o ya pagado
        # PlatoNoEncontrado: Si plato no existe
        # ValueError: Si plato no disponible
        
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("Pedido no existe")
        pedido = self.pedidos[id_pedido]
        if pedido['pagado']:
            raise PedidoInvalido("Pedido ya fue pagado")
        if codigo_plato not in self.menu:
            raise PlatoNoEncontrado(codigo_plato)
        if not self.menu[codigo_plato].get('disponible', False):
            raise ValueError("Plato no disponible")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("Cantidad inválida")

        pedido['items'][codigo_plato] = pedido['items'].get(codigo_plato, 0) + cantidad
        return True

    def calcular_total(self, id_pedido, propina_porcentaje=None):
        
        #Calcula total del pedido.

        #Returns:
        # dict con subtotal, impuesto, propina, total

        if id_pedido not in self.pedidos:
            raise PedidoInvalido("Pedido no existe")
        pedido = self.pedidos[id_pedido]
        subtotal = 0.0
        detalles = []
        for codigo, cantidad in pedido['items'].items():
            if codigo not in self.menu:
                # Si por alguna razón el plato fue eliminado, lo ignoramos
                continue
            precio_unit = float(self.menu[codigo]['precio'])
            subtotal += precio_unit * cantidad
            detalles.append({'codigo': codigo, 'cantidad': cantidad, 'precio_unit': precio_unit})

        impuesto = round(subtotal * self.tasa_impuesto, 2)
        prop_pct = self.propina_sugerida if propina_porcentaje is None else float(propina_porcentaje)
        propina = round(subtotal * prop_pct, 2)
        total = round(subtotal + impuesto + propina, 2)

        return {
            'subtotal': round(subtotal, 2),
            'impuesto': impuesto,
            'propina': propina,
            'propina_porcentaje': prop_pct,
            'total': total,
            'detalles': detalles
        }

    def pagar_pedido(self, id_pedido, propina_porcentaje=None):
        
        #Procesa pago del pedido.

        #Returns:
        # dict con totales

        #Raises:
        # PedidoInvalido: Si pedido no existe o ya pagado
        
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("Pedido no existe")
        pedido = self.pedidos[id_pedido]
        if pedido['pagado']:
            raise PedidoInvalido("Pedido ya fue pagado")

        totales = self.calcular_total(id_pedido, propina_porcentaje)
        # Registrar ventas por item (fecha = día actual)
        hoy = date.today()
        for item in totales['detalles']:
            codigo = item['codigo']
            cantidad = item['cantidad']
            precio_unit = item['precio_unit']
            nombre = self.menu.get(codigo, {}).get('nombre', 'Desconocido')
            categoria = self.menu.get(codigo, {}).get('categoria', 'Sin categoria')
            self.ventas.append({
                'fecha': hoy,
                'codigo': codigo,
                'nombre': nombre,
                'categoria': categoria,
                'cantidad': cantidad,
                'precio_unit': precio_unit,
                'total': round(precio_unit * cantidad, 2)
            })

        pedido['pagado'] = True
        pedido['pago_info'] = {
            'fecha_pago': datetime.now(),
            'totales': totales
        }

        # Liberar la mesa asociada al pedido
        try:
            self.liberar_mesa(pedido['mesa'])
        except ValueError:
            # si por alguna razón no se puede liberar, no abortamos el pago
            pass

        return totales

    # ============ REPORTES Y ESTADÍSTICAS ============

    def platos_mas_vendidos(self, n=5):
        
        #Retorna los N platos más vendidos del día.

        #Returns:
        # Lista de tuplas (codigo, nombre, cantidad_vendida)
        
        hoy = date.today()
        conteo = {}
        nombres = {}
        for v in self.ventas:
            if v['fecha'] != hoy:
                continue
            codigo = v['codigo']
            conteo[codigo] = conteo.get(codigo, 0) + v.get('cantidad', 0)
            nombres[codigo] = v.get('nombre', nombres.get(codigo))
        orden = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
        resultado = []
        for codigo, cantidad in orden[:n]:
            resultado.append((codigo, nombres.get(codigo, 'Desconocido'), cantidad))
        return resultado

    def ventas_por_categoria(self):
        
        #Calcula ventas totales por categoría.

        #Returns:
        # dict con ventas por categoría
       
        hoy = date.today()
        por_cat = {}
        for v in self.ventas:
            if v['fecha'] != hoy:
                continue
            cat = v.get('categoria', 'Sin categoria')
            por_cat[cat] = por_cat.get(cat, 0.0) + v.get('total', 0.0)
        # redondear
        for k in list(por_cat.keys()):
            por_cat[k] = round(por_cat[k], 2)
        return por_cat

    def reporte_ventas_dia(self):
        
        #Genera reporte completo de ventas del día.

        #Returns:
        # dict con estadísticas completas
        
        hoy = date.today()
        total_ventas = 0.0
        total_items = 0
        pedidos_pagados = 0
        for pedido_id, p in self.pedidos.items():
            if p.get('pagado') and p.get('pago_info'):
                fecha_pago = p['pago_info']['fecha_pago'].date()
                if fecha_pago == hoy:
                    pedidos_pagados += 1
                    total_ventas += p['pago_info']['totales']['total']
        for v in self.ventas:
            if v['fecha'] == hoy:
                total_items += v.get('cantidad', 0)

        return {
            'fecha': hoy,
            'total_ventas': round(total_ventas, 2),
            'total_items_vendidos': total_items,
            'pedidos_pagados': pedidos_pagados,
            'ventas_por_categoria': self.ventas_por_categoria(),
            'platos_mas_vendidos': self.platos_mas_vendidos(10)
        }

    def reporte_ventas_rango(self, fecha_inicio, fecha_fin):
        
        #(Adicional) Reporte de ventas en rango de fechas inclusive.
        
        if not isinstance(fecha_inicio, date) or not isinstance(fecha_fin, date):
            raise ValueError("Fechas deben ser objetos date")
        if fecha_inicio > fecha_fin:
            raise ValueError("fecha_inicio > fecha_fin")
        por_cat = {}
        total = 0.0
        for v in self.ventas:
            if fecha_inicio <= v['fecha'] <= fecha_fin:
                cat = v.get('categoria', 'Sin categoria')
                por_cat[cat] = por_cat.get(cat, 0.0) + v.get('total', 0.0)
                total += v.get('total', 0.0)
        for k in por_cat:
            por_cat[k] = round(por_cat[k], 2)
        return {'total': round(total, 2), 'ventas_por_categoria': por_cat}

    def estado_restaurante(self):
        
        #Estado actual del restaurante.

        #Returns:
        # dict con estado de mesas y pedidos
        
        estado_mesas = {}
        for num, info in self.mesas.items():
            estado_mesas[num] = {
                'capacidad': info['capacidad'],
                'ocupado': info['ocupado'],
                'comensales': info['comensales'],
                'hora_reserva': info['hora_reserva']
            }
        estado_pedidos = {}
        for pid, p in self.pedidos.items():
            estado_pedidos[pid] = {
                'mesa': p['mesa'],
                'items': dict(p['items']),
                'creado': p['creado'],
                'pagado': p['pagado']
            }
        return {
            'mesas': estado_mesas,
            'pedidos': estado_pedidos
        }

    # ============ UTILIDADES ============

    def exportar_menu(self, archivo='menu.txt'):
        
        #Exporta menú a archivo de texto.
        #Formato: Codigo|Nombre|Categoria|Precio|Disponible
        
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                for codigo, info in self.menu.items():
                    linea = f"{codigo}|{info['nombre']}|{info['categoria']}|{info['precio']}|{int(bool(info.get('disponible', False)))}\n"
                    f.write(linea)
            return True
        except Exception as e:
            raise IOError(f"No se pudo exportar menú: {e}")

    def importar_menu(self, archivo='menu.txt'):
        
        #Importa menú desde archivo de texto.

        #Returns:
        # dict con exitosos y errores
        
        exitosos = []
        errores = []
        if not os.path.exists(archivo):
            raise IOError(f"Archivo no encontrado: {archivo}")

        with open(archivo, 'r', encoding='utf-8') as f:
            for i, linea in enumerate(f, start=1):
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split('|')
                if len(partes) != 5:
                    errores.append({'linea': i, 'texto': linea, 'error': 'Formato inválido'})
                    continue
                codigo, nombre, categoria, precio_text, disponible_text = partes
                try:
                    precio = float(precio_text)
                    disponible = bool(int(disponible_text))
                except Exception as e:
                    errores.append({'linea': i, 'texto': linea, 'error': f'Error parseo: {e}'})
                    continue
                # Si el código ya existe, actualizamos los campos en lugar de lanzar error
                if codigo in self.menu:
                    self.menu[codigo].update({
                        'nombre': nombre,
                        'categoria': categoria,
                        'precio': precio,
                        'disponible': disponible
                    })
                    exitosos.append({'linea': i, 'codigo': codigo, 'accion': 'actualizado'})
                else:
                    try:
                        self.menu[codigo] = {
                            'nombre': nombre,
                            'categoria': categoria,
                            'precio': precio,
                            'disponible': disponible
                        }
                        exitosos.append({'linea': i, 'codigo': codigo, 'accion': 'agregado'})
                    except Exception as e:
                        errores.append({'linea': i, 'texto': linea, 'error': str(e)})
        return {'exitosos': exitosos, 'errores': errores}


# ===================================================================
# EJEMPLO DE USO
# ===================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" SISTEMA DE GESTIÓN DE RESTAURANTE (Demo rápido)")
    print("=" * 70)

    restaurante = SistemaRestaurante(num_mesas=5)

    # configurar capacidades
    restaurante.configurar_mesa(1, 2)
    restaurante.configurar_mesa(2, 4)
    restaurante.configurar_mesa(3, 6)

    # agregar platos
    restaurante.agregar_plato("P001", "Sopa del día", "Entradas", 5.50)
    restaurante.agregar_plato("P002", "Ensalada César", "Entradas", 8.00)
    restaurante.agregar_plato("P010", "Filete a la plancha", "Principales", 18.50)
    restaurante.agregar_plato("P020", "Pasta Alfredo", "Principales", 14.00)
    restaurante.agregar_plato("P100", "Tiramisú", "Postres", 6.00)

    # reservar mesa y crear pedido
    restaurante.reservar_mesa(2, 3, datetime.now().time())
    id_p = restaurante.crear_pedido(2)
    restaurante.agregar_item(id_p, "P002", 2)
    restaurante.agregar_item(id_p, "P020", 1)

    print("\n-- Totales antes de pagar --")
    print(restaurante.calcular_total(id_p))

    print("\n-- Procesando pago --")
    tot = restaurante.pagar_pedido(id_p, propina_porcentaje=0.10)
    print(tot)

    print("\n-- Estado del restaurante --")
    import pprint
    pprint.pprint(restaurante.estado_restaurante())

    print("\n-- Reporte ventas del día --")
    pprint.pprint(restaurante.reporte_ventas_dia())
