import ply.yacc as yacc
from Analizador_Lexico2 import tokens

# Resultado del análisis sintáctico
resultado_gramatica = []
variables_declaradas = set()  # Conjunto para almacenar las variables que han sido declaradas
total_lineas = 0

# Regla para la declaración de variables
def p_expresion(p):
    
    '''
    expresion : RESERVADA PARIZQ RESERVADO IDENTIFICADOR OPERADOR ENTERO SIMBOLO IDENTIFICADOR OPERADOR ENTERO SIMBOLO IDENTIFICADOR PLUSPLUS PARDER LLAIZQ RESERVADO SIMBOLO RESERVADO SIMBOLO RESERVADO PARIZQ COMDOB IDENTIFICADOR DOSPUNTO COMDOB SUMA IDENTIFICADOR PARDER SIMBOLO LLADER
              | RESERVADO SIMBOLO RESERVADO SIMBOLO RESERVADO PARIZQ COMDOB IDENTIFICADOR DOSPUNTO COMDOB SUMA IDENTIFICADOR PARDER SIMBOLO 
              | LLAIZQ LLADER
              | RESERVADA IDENTIFICADOR PARIZQ PARDER LLAIZQ declaracion_variables RESERVADO PARIZQ COMDOB IDENTIFICADOR COMDOB PARDER RESERVADO SIMBOLO LLADER 
    '''
    if len(p) == 31:
        p[0] = "Expresión correcta (for-loop)"
    elif len(p) == 16:
            p[0] = "Expresión correcta (Programa de suma)"   
    elif len(p) == 15:
        p[0] = "Expresión correcta (System.out.println)"
    else:
        p[0] = "Expresión correcta (llave de cierre)"

def p_declaracion_variables(p):
    '''
    declaracion_variables : RESERVADO lista_variables SIMBOLO read_variables read_variables uso_variables
    '''
    if p[1] == 'int':  # Detecta declaraciones del tipo 'int'
        p[0] = f"Declaración de variables: {', '.join(p[2])}"

# Regla para la lista de variables en la declaración (como `int a, b, c;`)
def p_lista_variables(p):
    '''
    lista_variables : IDENTIFICADOR
                    | lista_variables COMA IDENTIFICADOR
    '''
    if len(p) == 2:  # Caso base: una sola variable
        variables_declaradas.add(p[1])
        p[0] = [p[1]]  # Retorna una lista con la variable
    else:  # Caso recursivo: varias variables separadas por comas
        variables_declaradas.add(p[3])
        p[0] = p[1] + [p[3]]  # Agrega la nueva variable a la lista existente

# Nueva regla para la instrucción read
def p_read_variables(p):
    '''
    read_variables : RESERVADO IDENTIFICADOR SIMBOLO
    '''
    if p[1] == 'read':  # Detecta la instrucción read
        var = p[2]
        if var not in variables_declaradas:
            p[0] = f"Error en read: La variable '{var}' no está declarada."
            resultado_gramatica.append(p[0])
        else:
            p[0] = f"Lectura de la variable '{var}' en read"
            resultado_gramatica.append(p[0])

# Regla para el uso de variables en expresiones
def p_uso_variables(p):
    '''
    uso_variables : IDENTIFICADOR OPERADOR IDENTIFICADOR SIMBOLO
                  | IDENTIFICADOR OPERADOR ENTERO SIMBOLO
                  | IDENTIFICADOR OPERADOR IDENTIFICADOR SUMA IDENTIFICADOR SIMBOLO
    '''
    var1 = p[1]
    errores = []

    if var1 not in variables_declaradas:
        errores.append(f"Error en operacion: La variable '{var1}' no está declarada.")
    
    # Si es una expresión con otra variable
    if isinstance(p[3], str):  
        var2 = p[3]
        if var2 not in variables_declaradas:
            errores.append(f"Error en operacion: La variable '{var2}' no está declarada.")
    
    # Si es una suma con otra variable
    if len(p) == 7:
        var3 = p[5]
        if var3 not in variables_declaradas:
            errores.append(f"Error en operacion: La variable '{var3}' no está declarada.")
    
    if errores:
        for error in errores:
            resultado_gramatica.append(error)
    else:
        p[0] = "Uso correcto de las variables en la operacion"
        resultado_gramatica.append(p[0])

# Manejo de errores sintácticos
def p_error(p):
    global resultado_gramatica

    if p:
        resultado = f"Error sintáctico en la línea {p.lineno-total_lineas}, posición {p.lexpos}: token inesperado '{p.value}'."
    else:
        resultado = "Error sintáctico: código incompleto o inesperado al final."

    resultado_gramatica.append(resultado)

# Inicializar el parser
parser = yacc.yacc()

# Función para realizar el análisis sintáctico
def realizar_analisis_sintactico(code, total_lineas_param):
    global resultado_gramatica
    global total_lineas
    global variables_declaradas

    total_lineas = total_lineas_param
    resultado_gramatica.clear()
    variables_declaradas.clear()  # Limpiar variables al iniciar un nuevo análisis
    resultado_sintactico = parser.parse(code)

    if resultado_sintactico:
        resultado_gramatica.append(resultado_sintactico)
    return resultado_gramatica

'''
programa suma(){
int a,b,c;
read a;
read b;
c=a+b;
printf("La suma es")
end;
}

for (int i = 1; i <= 5; i++) {
System.out.println ("El valor de la cifra es: " + i);
}
'''
