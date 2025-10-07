# Proyecto Final: Calculadora de Expresiones
# Autor: [Tu nombre]

# Operadores permitidos: +, -, *, /, //, %, **

# Solicitar la expresión al usuario
expresion = input("Ingresa una expresión matemática: ")

# Caracteres permitidos
caracteres_permitidos = "0123456789+-*/%.() "

# Verificar que la expresión solo contenga caracteres válidos
if all(caracter in caracteres_permitidos for caracter in expresion):
    try:
        # Evaluar la expresión
        resultado = eval(expresion)
        print("El resultado es:", resultado)

    # Manejar división por cero
    except ZeroDivisionError:
        print("Error: No se puede dividir entre cero.")

    # Manejar cualquier otro tipo de error
    except Exception:
        print("Error: La expresión ingresada no es válida.")
else:
    print("Error: Solo se permiten números, espacios, paréntesis y los operadores +, -, *, /, //, %, **.")
