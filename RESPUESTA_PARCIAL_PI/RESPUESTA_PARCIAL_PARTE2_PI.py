
#PARCIAL 2 - PROBLEMA INTEGRADOR
#Sistema de Gestión de Biblioteca 


from datetime import datetime, timedelta
import os

# ===========================================================================
# EXCEPCIONES PERSONALIZADAS (5 puntos)
# ===========================================================================

class ErrorBiblioteca(Exception):
    #Excepción base para el sistema de biblioteca
    pass


class LibroNoEncontrado(ErrorBiblioteca):
    #Se lanza cuando un libro no existe en el catálogo
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"Libro con ISBN {isbn} no encontrado")


class LibroNoDisponible(ErrorBiblioteca):
    #Se lanza cuando no hay copias disponibles
    def __init__(self, isbn, titulo):
        self.isbn = isbn
        self.titulo = titulo
        super().__init__(f"No hay copias disponibles de '{titulo}'")


class UsuarioNoRegistrado(ErrorBiblioteca):
    #Se lanza cuando el usuario no está registrado
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        super().__init__(f"Usuario con ID '{id_usuario}' no está registrado")


class LimitePrestamosExcedido(ErrorBiblioteca):
    #Se lanza cuando el usuario excede el límite de préstamos
    def __init__(self, id_usuario, limite):
        self.id_usuario = id_usuario
        self.limite = limite
        super().__init__(f"Usuario {id_usuario} excede límite de {limite} préstamos")


class PrestamoVencido(ErrorBiblioteca):
    #Se lanza para operaciones con préstamos vencidos
    def __init__(self, id_prestamo, dias_retraso):
        self.id_prestamo = id_prestamo
        self.dias_retraso = dias_retraso
        super().__init__(f"Préstamo {id_prestamo} está vencido por {dias_retraso} días")


# ===========================================================================
# CLASE PRINCIPAL: SISTEMA BIBLIOTECA (35 puntos)
# ===========================================================================

class SistemaBiblioteca:
    
    #Sistema completo de gestión de biblioteca digital.
    
    #Estructuras de datos:
    # catalogo: {isbn: {'titulo', 'autor', 'anio', 'categoria', 'copias_total', 'copias_disponibles', 'veces_prestado'}}
    # usuarios: {id_usuario: {'nombre', 'email', 'fecha_registro', 'prestamos_activos', 'historial', 'multas_pendientes'}}
    # prestamos: {id_prestamo: {'isbn', 'id_usuario', 'fecha_prestamo', 'fecha_vencimiento', 'fecha_devolucion', 'multa', 'multa_pagada'}}
    
    
    def __init__(self, dias_prestamo=14, multa_por_dia=1.0, limite_prestamos=3):
        
        #Inicializa el sistema.
        
        self.catalogo = {}
        self.usuarios = {}
        self.prestamos = {}
        self.dias_prestamo = int(dias_prestamo)
        self.multa_por_dia = float(multa_por_dia)
        self.limite_prestamos = int(limite_prestamos)
        self._next_prestamo_id = 1

    # ============ GESTIÓN DE CATÁLOGO ============
    
    def _validar_isbn(self, isbn):
        return isinstance(isbn, str) and isbn.isdigit() and len(isbn) == 13

    def agregar_libro(self, isbn, titulo, autor, anio, categoria, copias):
        
        #Agrega un libro al catálogo.
        
        # validaciones
        if not self._validar_isbn(isbn):
            raise ValueError("ISBN debe ser un string de 13 dígitos")
        if not titulo or not autor:
            raise ValueError("Título y autor no pueden estar vacíos")
        anio_actual = datetime.now().year
        if not (1000 <= int(anio) <= anio_actual):
            raise ValueError("Año inválido")
        if int(copias) < 1:
            raise ValueError("Copias debe ser >= 1")
        if isbn in self.catalogo:
            raise KeyError(f"ISBN {isbn} ya existe en el catálogo")
        self.catalogo[isbn] = {
            'titulo': str(titulo),
            'autor': str(autor),
            'anio': int(anio),
            'categoria': str(categoria),
            'copias_total': int(copias),
            'copias_disponibles': int(copias),
            'veces_prestado': 0
        }
        return True
    
    def actualizar_copias(self, isbn, cantidad_cambio):
        
        #Actualiza número de copias (añade o remueve).
        
        if isbn not in self.catalogo:
            raise LibroNoEncontrado(isbn)
        nuevo_total = self.catalogo[isbn]['copias_total'] + int(cantidad_cambio)
        nuevo_disponible = self.catalogo[isbn]['copias_disponibles'] + int(cantidad_cambio)
        if nuevo_total < 0 or nuevo_disponible < 0:
            raise ValueError("Resultado de copias sería negativo")
        self.catalogo[isbn]['copias_total'] = nuevo_total
        self.catalogo[isbn]['copias_disponibles'] = min(nuevo_disponible, nuevo_total)
        return True

    def buscar_libros(self, criterio='titulo', valor='', categoria=None):
        
        #Busca libros por diferentes criterios.
        
        criterio = criterio.lower()
        valor = str(valor).lower()
        resultados = []
        for isbn, info in self.catalogo.items():
            if categoria and info.get('categoria', '').lower() != categoria.lower():
                continue
            match = False
            if criterio == 'titulo':
                match = valor in info['titulo'].lower()
            elif criterio == 'autor':
                match = valor in info['autor'].lower()
            elif criterio == 'anio':
                match = valor == str(info['anio']).lower()
            else:
                # busqueda general en titulo y autor
                match = (valor in info['titulo'].lower()) or (valor in info['autor'].lower())
            if match:
                resultados.append({'isbn': isbn, **info})
        return resultados
    
    # ============ GESTIÓN DE USUARIOS ============
    
    def registrar_usuario(self, id_usuario, nombre, email):
        
        #Registra un nuevo usuario.
        
        if not nombre:
            raise ValueError("Nombre no puede estar vacío")
        if '@' not in email or '.' not in email:
            raise ValueError("Email inválido")
        if id_usuario in self.usuarios:
            raise ValueError("ID de usuario ya existe")
        self.usuarios[id_usuario] = {
            'nombre': nombre,
            'email': email,
            'fecha_registro': datetime.now(),
            'prestamos_activos': [],  # lista de id_prestamo
            'historial': [],  # lista de id_prestamo
            'multas_pendientes': 0.0
        }
        return True

    def obtener_estado_usuario(self, id_usuario):
        
        #Obtiene estado completo del usuario.
        
        if id_usuario not in self.usuarios:
            raise UsuarioNoRegistrado(id_usuario)
        u = self.usuarios[id_usuario]
        total_multas = u['multas_pendientes']
        puede_prestar = (len(u['prestamos_activos']) < self.limite_prestamos) and (total_multas <= 50)
        return {
            'nombre': u['nombre'],
            'prestamos_activos': list(u['prestamos_activos']),
            'puede_prestar': puede_prestar,
            'multas_pendientes': total_multas
        }
    
    # ============ GESTIÓN DE PRÉSTAMOS ============
    
    def _generar_id_prestamo(self):
        pid = self._next_prestamo_id
        self._next_prestamo_id += 1
        return pid

    def prestar_libro(self, isbn, id_usuario):
        
        #Realiza un préstamo.
        
        if id_usuario not in self.usuarios:
            raise UsuarioNoRegistrado(id_usuario)
        if isbn not in self.catalogo:
            raise LibroNoEncontrado(isbn)
        libro = self.catalogo[isbn]
        if libro['copias_disponibles'] <= 0:
            raise LibroNoDisponible(isbn, libro['titulo'])
        usuario = self.usuarios[id_usuario]
        if len(usuario['prestamos_activos']) >= self.limite_prestamos:
            raise LimitePrestamosExcedido(id_usuario, self.limite_prestamos)
        if usuario['multas_pendientes'] > 50:
            raise ValueError(f"Usuario {id_usuario} tiene multas pendientes > 50")
        id_prestamo = self._generar_id_prestamo()
        fecha_prestamo = datetime.now()
        fecha_vencimiento = fecha_prestamo + timedelta(days=self.dias_prestamo)
        self.prestamos[id_prestamo] = {
            'isbn': isbn,
            'id_usuario': id_usuario,
            'fecha_prestamo': fecha_prestamo,
            'fecha_vencimiento': fecha_vencimiento,
            'fecha_devolucion': None,
            'multa': 0.0,
            'multa_pagada': False
        }
        # actualizar estados
        libro['copias_disponibles'] -= 1
        libro['veces_prestado'] += 1
        usuario['prestamos_activos'].append(id_prestamo)
        usuario['historial'].append(id_prestamo)
        return id_prestamo

    def devolver_libro(self, id_prestamo):
        
        #Procesa devolución de libro.
        
        if id_prestamo not in self.prestamos:
            raise KeyError("Préstamo no existe")
        prest = self.prestamos[id_prestamo]
        if prest['fecha_devolucion'] is not None:
            raise ValueError("Préstamo ya fue devuelto")
        fecha_devolucion = datetime.now()
        prest['fecha_devolucion'] = fecha_devolucion
        dias_retraso = max(0, (fecha_devolucion.date() - prest['fecha_vencimiento'].date()).days)
        multa = dias_retraso * self.multa_por_dia
        prest['multa'] = multa
        prest['multa_pagada'] = False if multa > 0 else True
        # actualizar libro y usuario
        isbn = prest['isbn']
        id_usuario = prest['id_usuario']
        if isbn in self.catalogo:
            self.catalogo[isbn]['copias_disponibles'] += 1
            # asegurarse que no sobrepase copias_total
            if self.catalogo[isbn]['copias_disponibles'] > self.catalogo[isbn]['copias_total']:
                self.catalogo[isbn]['copias_disponibles'] = self.catalogo[isbn]['copias_total']
        if id_usuario in self.usuarios:
            u = self.usuarios[id_usuario]
            if id_prestamo in u['prestamos_activos']:
                u['prestamos_activos'].remove(id_prestamo)
            # acumular multa pendiente
            u['multas_pendientes'] += multa
        mensaje = "Devolución procesada"
        if dias_retraso > 0:
            mensaje += f" — {dias_retraso} días de retraso. Multa: {multa:.2f}"
        return {'dias_retraso': dias_retraso, 'multa': multa, 'mensaje': mensaje}

    def renovar_prestamo(self, id_prestamo):
        
        #Renueva préstamo por otros N días (si no está vencido).
        
        if id_prestamo not in self.prestamos:
            raise KeyError("Préstamo no existe")
        prest = self.prestamos[id_prestamo]
        if prest['fecha_devolucion'] is not None:
            raise ValueError("Préstamo ya fue devuelto")
        hoy = datetime.now()
        dias_retraso = max(0, (hoy.date() - prest['fecha_vencimiento'].date()).days)
        if dias_retraso > 0:
            raise PrestamoVencido(id_prestamo, dias_retraso)
        prest['fecha_vencimiento'] = prest['fecha_vencimiento'] + timedelta(days=self.dias_prestamo)
        return True

    # ============ ESTADÍSTICAS Y REPORTES ============
    
    def libros_mas_prestados(self, n=10):
        lst = [(isbn, info['titulo'], info.get('veces_prestado', 0)) for isbn, info in self.catalogo.items()]
        lst.sort(key=lambda x: x[2], reverse=True)
        return lst[:n]

    def usuarios_mas_activos(self, n=5):
        lst = []
        for uid, info in self.usuarios.items():
            total = len(info['historial'])
            lst.append((uid, info['nombre'], total))
        lst.sort(key=lambda x: x[2], reverse=True)
        return lst[:n]

    def estadisticas_categoria(self, categoria):
        total_libros = 0
        total_copias = 0
        copias_prestadas = 0
        libro_mas_popular = None
        max_prestados = -1
        for isbn, info in self.catalogo.items():
            if info.get('categoria', '').lower() == categoria.lower():
                total_libros += 1
                total_copias += info.get('copias_total', 0)
                copias_prestadas += (info.get('copias_total', 0) - info.get('copias_disponibles', 0))
                if info.get('veces_prestado', 0) > max_prestados:
                    max_prestados = info.get('veces_prestado', 0)
                    libro_mas_popular = info.get('titulo')
        tasa_prestamo = (copias_prestadas / total_copias) if total_copias > 0 else 0.0
        return {
            'total_libros': total_libros,
            'total_copias': total_copias,
            'copias_prestadas': copias_prestadas,
            'tasa_prestamo': round(tasa_prestamo, 4),
            'libro_mas_popular': libro_mas_popular
        }

    def prestamos_vencidos(self):
        hoy = datetime.now().date()
        resultados = []
        for pid, info in self.prestamos.items():
            if info['fecha_devolucion'] is None and info['fecha_vencimiento'].date() < hoy:
                dias_retraso = (hoy - info['fecha_vencimiento'].date()).days
                multa_acumulada = dias_retraso * self.multa_por_dia
                isbn = info['isbn']
                titulo = self.catalogo.get(isbn, {}).get('titulo', '')
                resultados.append({
                    'id_prestamo': pid,
                    'isbn': isbn,
                    'titulo': titulo,
                    'id_usuario': info['id_usuario'],
                    'dias_retraso': dias_retraso,
                    'multa_acumulada': multa_acumulada
                })
        return resultados

    def reporte_financiero(self, fecha_inicio=None, fecha_fin=None):
        total_multas = 0.0
        multas_pagadas = 0.0
        multas_pendientes = 0.0
        prestamos_con_multa = 0
        lista_multas = []
        for pid, info in self.prestamos.items():
            if info['multa'] and info['fecha_devolucion']:
                fecha_dev = info['fecha_devolucion']
                if fecha_inicio and fecha_dev < fecha_inicio:
                    continue
                if fecha_fin and fecha_dev > fecha_fin:
                    continue
                total_multas += info['multa']
                prestamos_con_multa += 1
                if info.get('multa_pagada'):
                    multas_pagadas += info['multa']
                else:
                    multas_pendientes += info['multa']
                lista_multas.append(info['multa'])
        promedio_multa = (sum(lista_multas) / len(lista_multas)) if lista_multas else 0.0
        return {
            'total_multas': round(total_multas, 2),
            'multas_pagadas': round(multas_pagadas, 2),
            'multas_pendientes': round(multas_pendientes, 2),
            'prestamos_con_multa': prestamos_con_multa,
            'promedio_multa': round(promedio_multa, 2)
        }

    # ============ UTILIDADES ============
    
    def exportar_catalogo(self, archivo='catalogo.txt'):
        
        #Exporta catálogo a archivo de texto.
        #Formato: ISBN|Título|Autor|Año|Categoría|Copias
        
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                for isbn, info in self.catalogo.items():
                    linea = f"{isbn}|{info['titulo']}|{info['autor']}|{info['anio']}|{info['categoria']}|{info['copias_total']}\n"
                    f.write(linea)
            return True
        except Exception as e:
            raise e

    def importar_catalogo(self, archivo='catalogo.txt'):
        
        #Importa catálogo desde archivo de texto.
        
        resultados = {'exitosos': 0, 'errores': []}
        if not os.path.exists(archivo):
            resultados['errores'].append((None, 'Archivo no existe'))
            return resultados
        with open(archivo, 'r', encoding='utf-8') as f:
            for idx, linea in enumerate(f, start=1):
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split('|')
                if len(partes) != 6:
                    resultados['errores'].append((idx, 'Formato incorrecto'))
                    continue
                isbn, titulo, autor, anio, categoria, copias = partes
                try:
                    if isbn in self.catalogo:
                        resultados['errores'].append((idx, 'Duplicado - no sobrescrito'))
                        continue
                    self.agregar_libro(isbn, titulo, autor, int(anio), categoria, int(copias))
                    resultados['exitosos'] += 1
                except Exception as e:
                    resultados['errores'].append((idx, str(e)))
        return resultados


# ===========================================================================
# CASOS DE PRUEBA BÁSICOS
# ===========================================================================

if __name__ == "__main__":
    print("="*70)
    print(" PRUEBAS DEL SISTEMA DE BIBLIOTECA")
    print("="*70)
    
    # Crear instancia del sistema
    biblioteca = SistemaBiblioteca(dias_prestamo=7, multa_por_dia=2.0, limite_prestamos=3)
    
    # Añadir libros
    try:
        biblioteca.agregar_libro('9783161484100', 'Cien AÃ±os de Soledad', 'Gabriel GarcÃ­a MÃ¡rquez', 1967, 'Novela', 3)
        biblioteca.agregar_libro('9780140449136', 'La Iliada', 'Homero', 800, 'Epica', 2)
    except Exception as e:
        print('Error agregando libros:', e)

    # Registrar usuarios
    try:
        biblioteca.registrar_usuario('u001', 'Ana Perez', 'ana.perez@example.com')
        biblioteca.registrar_usuario('u002', 'Luis Gomez', 'luis.gomez@example.com')
    except Exception as e:
        print('Error registrando usuarios:', e)

    # Realizar prestamos
    try:
        pid1 = biblioteca.prestar_libro('9783161484100', 'u001')
        pid2 = biblioteca.prestar_libro('9783161484100', 'u002')
        print('Prestamos realizados:', pid1, pid2)
    except Exception as e:
        print('Error prestando libro:', e)

    # Forzar devolucion con retraso (simular cambiando fecha de vencimiento)
    biblioteca.prestamos[pid1]['fecha_vencimiento'] = datetime.now() - timedelta(days=3)
    res = biblioteca.devolver_libro(pid1)
    print('Devolucion:', res)

    # Estado usuario
    estado = biblioteca.obtener_estado_usuario('u001')
    print('Estado u001:', estado)

    # Estadisticas
    print('Libros mas prestados:', biblioteca.libros_mas_prestados())
    print('Usuarios mas activos:', biblioteca.usuarios_mas_activos())
    print('Prestamos vencidos:', biblioteca.prestamos_vencidos())

    # Exportar e importar (prueba)
    biblioteca.exportar_catalogo('catalogo_prueba.txt')
    print('\nSistema inicializado y pruebas básicas ejecutadas')
    print('  Revisa las estructuras: biblioteca.catalogo, biblioteca.usuarios, biblioteca.prestamos')
