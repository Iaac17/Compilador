import ply.yacc as yacc
from Analizador_Lexico2 import tokens  

# Resultado del análisis sintáctico
resultado_gramatica = []
total_lineas = 0  

# Definir las reglas gramaticales
def p_expresion(p):
    '''
    expresion : RESERVADA DELIMITADOR RESERVADO IDENTIFICADOR OPERADOR ENTERO SIMBOLO IDENTIFICADOR OPERADOR ENTERO SIMBOLO IDENTIFICADOR PLUSPLUS DELIMITADOR DELIMITADOR RESERVADO SIMBOLO RESERVADO SIMBOLO RESERVADO DELIMITADOR COMDOB IDENTIFICADOR DOSPUNTO COMDOB SUMA IDENTIFICADOR DELIMITADOR SIMBOLO DELIMITADOR
              | RESERVADO SIMBOLO RESERVADO SIMBOLO RESERVADO DELIMITADOR COMDOB IDENTIFICADOR DOSPUNTO COMDOB SUMA IDENTIFICADOR DELIMITADOR SIMBOLO 
              | DELIMITADOR DELIMITADOR
              | RESERVADA IDENTIFICADOR DELIMITADOR DELIMITADOR DELIMITADOR RESERVADO IDENTIFICADOR IDENTIFICADOR IDENTIFICADOR SIMBOLO RESERVADO IDENTIFICADOR SIMBOLO RESERVADO IDENTIFICADOR SIMBOLO IDENTIFICADOR OPERADOR IDENTIFICADOR  SUMA IDENTIFICADOR SIMBOLO RESERVADO DELIMITADOR COMDOB IDENTIFICADOR COMDOB DELIMITADOR RESERVADO SIMBOLO DELIMITADOR 
    '''
    if len(p) == 31:
        p[0] = "Expresión correcta (for-loop)"
    elif len(p) == 32:
            p[0] = "Expresión correcta (Programa de suma)"    
    elif len(p) == 15:
        p[0] = "Expresión correcta (System.out.println)"
    else:
        p[0] = "Expresión correcta (llave de cierre)"

# Manejo de errores sintácticos mejorado
def p_error(p):
    global resultado_gramatica
    global num_saltos_linea  

    if p:
        resultado = f"Error sintáctico en la línea {p.lineno-total_lineas}  posición {p.lexpos}: token inesperado '{p.value}'."
    else:
        resultado = "Error sintáctico: código incompleto o inesperado al final."

    resultado_gramatica.append(resultado)

# Inicializar el parser
parser = yacc.yacc()

def realizar_analisis_sintactico(code, total_lineas_param):
    global resultado_gramatica
    global total_lineas

    total_lineas = total_lineas_param 
    resultado_gramatica.clear()
    resultado_sintactico = parser.parse(code)

    if resultado_sintactico:
        resultado_gramatica.append(resultado_sintactico)
    return resultado_gramatica
