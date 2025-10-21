"""
PARCIAL 2 - EJERCICIOS
"""

from typing import Tuple, List, Dict, Any
import math
from collections import defaultdict, Counter

# ===========================================================================
# EJERCICIO 1: EXPRESIONES ARITMÉTICAS (10 puntos)
# ===========================================================================

def calculadora_cientifica(operacion: str, a: float, b: float) -> float:
    
    #Realiza operaciones matemáticas con validación.

    #Args:
    # operacion: "suma", "resta", "multiplicacion", "division", "potencia", "modulo"
    # a: Primer número (int o float)
    # b: Segundo número (int o float)

    #Returns:
    # float: Resultado con 2 decimales de precisión

    #Raises:
    # ValueError: Si la operación es inválida o tipos incorrectos
    # ZeroDivisionError: Si intenta dividir por cero
    
    # Validación tipos
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        raise ValueError("Los operandos deben ser int o float")

    op = operacion.lower()
    if op == "suma":
        res = a + b
    elif op == "resta":
        res = a - b
    elif op == "multiplicacion":
        res = a * b
    elif op == "division":
        if b == 0:
            raise ZeroDivisionError("División por cero")
        res = a / b
    elif op == "potencia":
        # potencia permite bases/exp reales
        res = a ** b
    elif op == "modulo":
        if b == 0:
            raise ZeroDivisionError("Módulo por cero")
        res = a % b
    else:
        raise ValueError(f"Operación inválida: {operacion}")

    # Redondear a 2 decimales y devolver float
    return round(float(res), 2)


# ===========================================================================
# EJERCICIO 2: EXPRESIONES LÓGICAS Y RELACIONALES (12 puntos)
# ===========================================================================

class ValidadorPassword:
    #Validador de contraseñas con reglas configurables

    def __init__(self, min_longitud=8, requiere_mayuscula=True,
                 requiere_minuscula=True, requiere_numero=True,
                 requiere_especial=True):
        """
        Inicializa el validador con reglas específicas.
        """
        self.min_longitud = int(min_longitud)
        self.requiere_mayuscula = bool(requiere_mayuscula)
        self.requiere_minuscula = bool(requiere_minuscula)
        self.requiere_numero = bool(requiere_numero)
        self.requiere_especial = bool(requiere_especial)
        # conjunto simple de caracteres especiales (puede ampliarse)
        self._especiales = set("!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~")

    def validar(self, password: str) -> Tuple[bool, List[str]]:
        
        #Valida password según las reglas configuradas.

        #Returns:
        # tuple: (es_valido, lista_de_errores)
        
        errores = []

        if not isinstance(password, str):
            raise ValueError("Password debe ser una cadena de texto")

        if len(password) < self.min_longitud:
            errores.append(f"Longitud mínima: {self.min_longitud}")

        if self.requiere_mayuscula and not any(c.isupper() for c in password):
            errores.append("Debe contener al menos una mayúscula")

        if self.requiere_minuscula and not any(c.islower() for c in password):
            errores.append("Debe contener al menos una minúscula")

        if self.requiere_numero and not any(c.isdigit() for c in password):
            errores.append("Debe contener al menos un número")

        if self.requiere_especial and not any(c in self._especiales for c in password):
            errores.append("Debe contener al menos un carácter especial")

        return (len(errores) == 0, errores)

    def es_fuerte(self, password: str) -> bool:
        
        #Determina si el password es fuerte.
        #Un password fuerte tiene al menos 12 caracteres,
        #mayúsculas, minúsculas, números y caracteres especiales.
    
        if not isinstance(password, str):
            return False
        if len(password) < 12:
            return False
        checks = [
            any(c.isupper() for c in password),
            any(c.islower() for c in password),
            any(c.isdigit() for c in password),
            any(c in self._especiales for c in password)
        ]
        return all(checks)


# ===========================================================================
# EJERCICIO 3: ESTRUCTURAS DE DATOS (15 puntos)
# ===========================================================================

class GestorInventario:
    #Sistema de gestión de inventario

    def __init__(self):
        
        #Inicializa el inventario.
        #Estructura: {codigo: {'nombre': str, 'precio': float, 'cantidad': int, 'categoria': str}}
        
        self._inventario: Dict[str, Dict[str, Any]] = {}

    def agregar_producto(self, codigo: str, nombre: str, precio: float, cantidad: int, categoria: str):
        
        #Agrega un producto al inventario.
        #Raises:
        # ValueError: Si el código ya existe
        
        if codigo in self._inventario:
            raise ValueError(f"Código {codigo} ya existe")
        if precio < 0 or cantidad < 0:
            raise ValueError("Precio y cantidad deben ser no negativos")
        self._inventario[codigo] = {
            'nombre': str(nombre),
            'precio': float(precio),
            'cantidad': int(cantidad),
            'categoria': str(categoria)
        }

    def actualizar_stock(self, codigo: str, cantidad_cambio: int):
        
        #Actualiza el stock de un producto.
        #Raises:
        # ValueError: Si producto no existe o stock resultante sería negativo
        
        if codigo not in self._inventario:
            raise ValueError(f"Producto {codigo} no existe")
        nueva = self._inventario[codigo]['cantidad'] + int(cantidad_cambio)
        if nueva < 0:
            raise ValueError("Stock resultante sería negativo")
        self._inventario[codigo]['cantidad'] = nueva

    def buscar_por_categoria(self, categoria: str) -> List[tuple]:
        
        #Busca productos por categoría.
        #Returns:
        # list: Lista de tuplas (codigo, nombre, precio)
        
        resultado = []
        for codigo, info in self._inventario.items():
            if info['categoria'] == categoria:
                resultado.append((codigo, info['nombre'], info['precio']))
        return resultado

    def productos_bajo_stock(self, limite: int = 10) -> Dict[str, int]:
        
        #Encuentra productos con stock bajo el límite.
        #Returns:
        # dict: {codigo: cantidad} de productos bajo el límite
        
        resultado = {}
        for codigo, info in self._inventario.items():
            if info['cantidad'] < limite:
                resultado[codigo] = info['cantidad']
        return resultado

    def valor_total_inventario(self) -> float:
        
        #Calcula el valor total del inventario.
        #Returns:
        # float: Suma de (precio * cantidad) de todos los productos
        
        total = 0.0
        for info in self._inventario.values():
            total += info['precio'] * info['cantidad']
        return round(total, 2)

    def top_productos(self, n: int = 5) -> List[tuple]:
        
        #Retorna los N productos con mayor valor en inventario.
        #Returns:
        # list: Lista de tuplas (codigo, valor_total) ordenadas descendentemente
        
        valores = []
        for codigo, info in self._inventario.items():
            valor = info['precio'] * info['cantidad']
            valores.append((codigo, round(valor, 2)))
        valores.sort(key=lambda x: x[1], reverse=True)
        return valores[:n]


# ===========================================================================
# EJERCICIO 4: ESTRUCTURAS DE CONTROL (10 puntos)
# ===========================================================================

def es_bisiesto(anio: int) -> bool:
    
    #Determina si un año es bisiesto.
    
    if not isinstance(anio, int):
        raise ValueError("Año debe ser entero")
    if anio % 400 == 0:
        return True
    if anio % 100 == 0:
        return False
    return anio % 4 == 0


def dias_en_mes(mes: int, anio: int) -> int:
    
    #Retorna el número de días en un mes específico.
    #Raises:
    #  ValueError: Si mes es inválido (no está entre 1 y 12)
    
    if not (1 <= mes <= 12):
        raise ValueError("Mes inválido (debe ser 1-12)")
    if mes in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if mes in (4, 6, 9, 11):
        return 30
    # mes == 2
    return 29 if es_bisiesto(anio) else 28


def generar_calendario(mes: int, anio: int, dia_inicio: int = 0) -> str:
    
    #Genera representación string del calendario de un mes.
    #Formato:
    #Lu Ma Mi Ju Vi Sa Do
    # 1  2 ... alineado en 2 espacios por día
    #dia_inicio: 0 = Lunes ... 6 = Domingo
    
    if not (1 <= mes <= 12):
        raise ValueError("Mes inválido (1-12)")
    if not (0 <= dia_inicio <= 6):
        raise ValueError("dia_inicio debe estar entre 0 (Lunes) y 6 (Domingo)")

    dias = dias_en_mes(mes, anio)
    encabezado = "Lu Ma Mi Ju Vi Sa Do"
    # cada dia ocupa 3 caracteres (dos para numero + espacio)
    semanas = []
    semana = ["  "] * 7  # placeholders como strings
    dia_actual = 1
    # llenar primeros espacios según dia_inicio
    idx = dia_inicio
    while dia_actual <= dias:
        semana[idx] = f"{dia_actual:2d}"
        dia_actual += 1
        idx += 1
        if idx == 7:
            semanas.append(semana)
            semana = ["  "] * 7
            idx = 0
    # si quedó semana incompleta, añadirla
    if any(cell.strip() for cell in semana):
        semanas.append(semana)

    # construir string
    lineas = [encabezado]
    for s in semanas:
        lineas.append(" ".join(s))
    return "\n".join(lineas)


# ===========================================================================
# EJERCICIO 5: ESTRUCTURAS DE REPETICIÓN (13 puntos)
# ===========================================================================

def analizar_ventas(ventas: List[Dict[str, Any]]) -> Dict[str, Any]:
    
    #Analiza lista de ventas y genera estadísticas.

    #NOTA: Se asume que 'descuento' en cada venta es un valor entre 0 y 1 que
    #representa el porcentaje (ej. 0.1 = 10%). Si en tu contexto 'descuento' es
    #absoluto, ajustar el cálculo.
    
    total_ventas = 0.0
    total_descuentos = 0.0
    cantidades_por_producto = defaultdict(int)
    venta_mayor = None
    mayor_valor = -math.inf

    for v in ventas:
        producto = v.get('producto')
        cantidad = int(v.get('cantidad', 0))
        precio = float(v.get('precio', 0.0))
        descuento = float(v.get('descuento', 0.0))  # asumido 0..1

        bruto = precio * cantidad
        descuento_valor = bruto * descuento
        neto = bruto - descuento_valor

        total_ventas += neto
        total_descuentos += descuento_valor
        cantidades_por_producto[producto] += cantidad

        if neto > mayor_valor:
            mayor_valor = neto
            venta_mayor = dict(v)
            venta_mayor['total'] = round(neto, 2)

    promedio_por_venta = round(total_ventas / len(ventas), 2) if ventas else 0.0
    total_ventas = round(total_ventas, 2)
    total_descuentos = round(total_descuentos, 2)

    # producto mas vendido por cantidad
    producto_mas_vendido = None
    if cantidades_por_producto:
        producto_mas_vendido = max(cantidades_por_producto.items(), key=lambda x: x[1])[0]

    return {
        'total_ventas': total_ventas,
        'promedio_por_venta': promedio_por_venta,
        'producto_mas_vendido': producto_mas_vendido,
        'venta_mayor': venta_mayor,
        'total_descuentos': total_descuentos
    }


def encontrar_patrones(numeros: List[float]) -> Dict[str, Any]:
    
    #Encuentra patrones en una secuencia de números.
    #Define secuencia ascendente/descendente como tramo contiguo
    #de longitud >= 2 con comparaciones estrictas.
    
    if not numeros:
        return {
            'secuencias_ascendentes': 0,
            'secuencias_descendentes': 0,
            'longitud_max_ascendente': 0,
            'longitud_max_descendente': 0,
            'numeros_repetidos': {}
        }

    asc_count = 0
    desc_count = 0
    max_asc = 0
    max_desc = 0

    i = 0
    n = len(numeros)
    # encontrar secuencias ascendentes
    while i < n - 1:
        # ascendentes
        if numeros[i+1] > numeros[i]:
            length = 2
            j = i + 1
            while j < n - 1 and numeros[j+1] > numeros[j]:
                length += 1
                j += 1
            asc_count += 1
            max_asc = max(max_asc, length)
            i = j  # continuar desde fin de secuencia
        # descendentes
        elif numeros[i+1] < numeros[i]:
            length = 2
            j = i + 1
            while j < n - 1 and numeros[j+1] < numeros[j]:
                length += 1
                j += 1
            desc_count += 1
            max_desc = max(max_desc, length)
            i = j
        else:
            # iguales, no forman asc/desc; avanzar uno
            i += 1

    # contar repetidos (frecuencia >1)
    freq = Counter(numeros)
    repetidos = {num: c for num, c in freq.items() if c > 1}

    return {
        'secuencias_ascendentes': asc_count,
        'secuencias_descendentes': desc_count,
        'longitud_max_ascendente': max_asc,
        'longitud_max_descendente': max_desc,
        'numeros_repetidos': repetidos
    }


def simular_crecimiento(principal: float, tasa_anual: float, anios: int, aporte_anual: float = 0.0) -> List[Dict[str, Any]]:
    
    #Simula crecimiento de inversión con interés compuesto.
    #Se asume que el aporte_anual se añade AL INICIO de cada año y luego
    #se aplica la tasa sobre el balance resultante durante ese año.
    
    if anios < 0:
        raise ValueError("años debe ser no negativo")
    balance = float(principal)
    historial = []
    for anio in range(1, anios + 1):
        # aporte al inicio del año
        balance += aporte_anual
        # interés ganado durante el año
        interes_ganado = balance * float(tasa_anual)
        balance += interes_ganado
        historial.append({
            'anio': anio,
            'balance': round(balance, 2),
            'interes_ganado': round(interes_ganado, 2)
        })
    return historial


# ===========================================================================
# CASOS DE PRUEBA
# ===========================================================================

if __name__ == "__main__":
    print("="*70)
    print(" PRUEBAS DE EJERCICIOS")
    print("="*70)

    print("\nEjercicio 1: Calculadora")
    print("2 + 3 =", calculadora_cientifica("suma", 2, 3))
    print("10 / 4 =", calculadora_cientifica("division", 10, 4))
    print("2^8 =", calculadora_cientifica("potencia", 2, 8))
    try:
        calculadora_cientifica("division", 1, 0)
    except ZeroDivisionError as e:
        print("División por cero correctamente detectada:", e)

    print("\nEjercicio 2: Validador de Password")
    val = ValidadorPassword(min_longitud=8)
    pruebas = ["abc", "Abcdef12", "Abcdef12!", "MuyFuerte123!"]
    for p in pruebas:
        ok, errs = val.validar(p)
        print(f"'{p}': Válido={ok}, Errores={errs}, Es fuerte? {val.es_fuerte(p)}")

    print("\nEjercicio 3: Gestor de Inventario")
    gi = GestorInventario()
    gi.agregar_producto("P001", "Lapiz", 0.5, 50, "Papeleria")
    gi.agregar_producto("P002", "Cuaderno", 2.0, 8, "Papeleria")
    gi.agregar_producto("P003", "Regla", 1.5, 3, "Papeleria")
    print("Por categoría Papeleria:", gi.buscar_por_categoria("Papeleria"))
    print("Bajo stock (<10):", gi.productos_bajo_stock(10))
    print("Valor total inventario:", gi.valor_total_inventario())
    print("Top productos:", gi.top_productos(2))
    gi.actualizar_stock("P002", 5)
    print("P002 stock actualizado:", gi._inventario["P002"]["cantidad"])

    print("\nEjercicio 4: Calendario")
    print("2024 es bisiesto?", es_bisiesto(2024))
    print("Días en Febrero 2024:", dias_en_mes(2, 2024))
    print("Calendario marzo 2025 (suponiendo primo día viernes -> dia_inicio=4):")
    print(generar_calendario(3, 2025, dia_inicio=4))

    print("\nEjercicio 5: Análisis de Datos")
    ventas = [
        {'producto': 'A', 'cantidad': 2, 'precio': 10.0, 'descuento': 0.1},
        {'producto': 'B', 'cantidad': 1, 'precio': 50.0, 'descuento': 0.0},
        {'producto': 'A', 'cantidad': 3, 'precio': 10.0, 'descuento': 0.05},
    ]
    resumen = analizar_ventas(ventas)
    print("Resumen ventas:", resumen)

    numeros = [1,2,3,2,1,1,2,3,4,0]
    patrones = encontrar_patrones(numeros)
    print("Patrones:", patrones)

    sim = simular_crecimiento(1000, 0.05, 3, aporte_anual=100)
    print("Simulación crecimiento:", sim)
