import ply.yacc as yacc
from Analizador_Lexico2 import tokens  # Importar los tokens desde el archivo lexico.py

# Resultado del análisis sintáctico
resultado_gramatica = []

# Definir las reglas gramaticales
def p_expresion(p):
    '''
    expresion : RESERVADA DELIMITADOR RESERVADO IDENTIFICADOR OPERADOR ENTERO SIMBOLO IDENTIFICADOR MENORIGUAL ENTERO SIMBOLO IDENTIFICADOR PLUSPLUS DELIMITADOR DELIMITADOR RESERVADO SIMBOLO RESERVADO SIMBOLO RESERVADO DELIMITADOR COMDOB IDENTIFICADOR DOSPUNTO COMDOB SUMA IDENTIFICADOR DELIMITADOR SIMBOLO DELIMITADOR
              | RESERVADO SIMBOLO RESERVADO SIMBOLO RESERVADO DELIMITADOR COMDOB IDENTIFICADOR DOSPUNTO COMDOB SUMA IDENTIFICADOR DELIMITADOR SIMBOLO 
              | DELIMITADOR DELIMITADOR
    '''
    if len(p) == 31:
        p[0] = "Expresión correcta (for-loop)"
    elif len(p) == 15:
        p[0] = "Expresión correcta (System.out.println)"
    else:
        p[0] = "Expresión correcta (llave de cierre)"

# Manejo de errores sintácticos
def p_error(p):
    global resultado_gramatica
    if p:
        resultado = f"Error sintáctico en el token {p.type} con valor {p.value}"
    else:
        resultado = "Error sintáctico: código incompleto"
    resultado_gramatica.append(resultado)

# Inicializar el parser
parser = yacc.yacc()

# Función para realizar el análisis sintáctico
def realizar_analisis_sintactico(code):
    global resultado_gramatica
    resultado_gramatica.clear()
    resultado_sintactico = parser.parse(code)
    if resultado_sintactico:
        resultado_gramatica.append(resultado_sintactico)
    return resultado_gramatica
