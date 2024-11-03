import ply.yacc as yacc
from Analizador_Lexico import tokens

# Resultado del análisis sintáctico
resultado_gramatica = []
total_lineas = 0
curp = ""
curp1 = ""
nombre = ""

# Definir un diccionario para el contexto semántico
contexto_identificadores = {}

def p_CURP(p):
    '''
    expresion : nombre fecha genero estado
    '''
    global curp,nombre
    # Construcción de la salida final para el CURP completo
    if len(curp.upper() + curp1.upper()) == 17:
        # Ejemplo de CURP de 17 caracteres (sin el dígito verificador final)
        curp_parcial = curp.upper() + curp1.upper()  # Modifica esta cadena para probar otros ejemplos

        # Calcular el dígito verificador
        digito_verificador = calcular_digito_verificador(curp_parcial)

        # Generar CURP completa con el dígito verificador
        curp_completa = curp_parcial + digito_verificador
        curp = curp_completa
        curp_procesada = procesar_curp(curp)
        resultado_gramatica.append(f"OYE {nombre.upper()}")
        p[0] = f"TU CURP ES: {curp_procesada}"
    else:
        p[0] = "Error: CURP no generado correctamente."

def procesar_curp(curp):
    return curp.replace("Ñ", "X")

# Función para calcular el dígito verificador de la CURP
def calcular_digito_verificador(curp):
    # Diccionario de valores asignados a cada letra y número
    valores = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19,
        'K': 20, 'L': 21, 'M': 22, 'N': 23, 'Ñ': 24, 'O': 25, 'P': 26, 'Q': 27, 'R': 28, 'S': 29,
        'T': 30, 'U': 31, 'V': 32, 'W': 33, 'X': 34, 'Y': 35, 'Z': 36
    }
    
    # Pesos específicos para cada posición de la CURP
    pesos = [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

    # Calcular la suma ponderada de cada carácter
    suma = sum(valores[caracter] * peso for caracter, peso in zip(curp, pesos))
    
    # Obtener el residuo de la suma al dividir entre 10
    residuo = suma % 10
    
    # Calcular el dígito verificador
    digito_verificador = 10 - residuo if residuo != 0 else 0
    
    return str(digito_verificador)

def p_nombre(p):
    '''
    nombre : PRIORIDAD IDENTIFICADOR IDENTIFICADOR IDENTIFICADOR
           | PRIORIDAD IDENTIFICADOR IDENTIFICADOR IDENTIFICADOR IDENTIFICADOR
    '''
    global curp,curp1,nombre
    curp1 = ''

    # Aquí puedes manejar la lógica de acuerdo al número de identificadores presentes.
    if len(p) == 5:  # PRIORIDAD + 3 IDENTIFICADORES
        if p[1].lower() == 'nombre':
            # Primera letra del apellido paterno
            nombre_table = p[3][0]  
            curp = nombre_table
            # Primera vocal del apellido paterno
            nombre_table = p[3]  # Nombre completo del apellido paterno
            vocales = "aeiouAEIOU"
            encontradas = [letra for letra in nombre_table if letra in vocales]
            # cosonante de apellido paterno
            nombre_table = p[3]  # Nombre completo del apellido paterno
            vocales = "aeiouAEIOU"
            consonantes = [letra for letra in nombre_table if letra.isalpha() and letra not in vocales]
            # Verificar si la primera letra es una vocal
            if nombre_table[0] in vocales:
                # Si la primera letra es vocal, tomar la primera consonante
                seleccion_consonante = consonantes[0] if consonantes else None
            else:
                # Si la primera letra es consonante, tomar la segunda consonante
                seleccion_consonante = consonantes[1] if len(consonantes) > 1 else None
            # Agregar la consonante seleccionada a curp1
            if seleccion_consonante:
                curp1 += seleccion_consonante
            if encontradas:
                if any(letra in vocales for letra in curp):
                    curp += encontradas[1] if len(encontradas) > 1 else ""
                else:
                    curp += encontradas[0]
            # Primera letra del apellido materno
            nombre_table = p[4][0]
            curp += nombre_table
            nombre_table = p[4]  # Nombre completo del apellido paterno
            vocales = "aeiouAEIOU"
            consonantes = [letra for letra in nombre_table if letra.isalpha() and letra not in vocales]
            # Verificar si la primera letra es una vocal
            if nombre_table[0] in vocales:
                # Si la primera letra es vocal, tomar la primera consonante
                seleccion_consonante = consonantes[0] if consonantes else None
            else:
                # Si la primera letra es consonante, tomar la segunda consonante
                seleccion_consonante = consonantes[1] if len(consonantes) > 1 else None
            # Agregar la consonante seleccionada a curp1
            if seleccion_consonante:
                curp1 += seleccion_consonante
            # Primera letra del primer nombre
            nombre_table = p[2][0]
            curp += nombre_table
            nombre_table = p[2]  # Nombre completo del apellido paterno
            vocales = "aeiouAEIOU"
            consonantes = [letra for letra in nombre_table if letra.isalpha() and letra not in vocales]
            # Verificar si la primera letra es una vocal
            if nombre_table[0] in vocales:
                # Si la primera letra es vocal, tomar la primera consonante
                seleccion_consonante = consonantes[0] if consonantes else None
            else:
                # Si la primera letra es consonante, tomar la segunda consonante
                seleccion_consonante = consonantes[1] if len(consonantes) > 1 else None
            # Agregar la consonante seleccionada a curp1
            if seleccion_consonante:
                curp1 += seleccion_consonante
                nombre = p[2] 
    elif len(p) == 6:  # PRIORIDAD + 4 IDENTIFICADORES
        if p[1].lower() == 'nombre':
            # Primera letra del apellido paterno
            nombre_table = p[4][0]  
            curp = nombre_table
            # Primera vocal del apellido paterno
            nombre_table = p[4]  # Nombre completo del apellido paterno
            vocales = "aeiouAEIOU"
            encontradas = [letra for letra in nombre_table if letra in vocales]
            # cosonante de apellido paterno
            nombre_table = p[4]  # Nombre completo del apellido paterno
            vocales = "aeiouAEIOU"
            consonantes = [letra for letra in nombre_table if letra.isalpha() and letra not in vocales]
            # Verificar si la primera letra es una vocal
            if nombre_table[0] in vocales:
                # Si la primera letra es vocal, tomar la primera consonante
                seleccion_consonante = consonantes[0] if consonantes else None
            else:
                # Si la primera letra es consonante, tomar la segunda consonante
                seleccion_consonante = consonantes[1] if len(consonantes) > 1 else None
            # Agregar la consonante seleccionada a curp1
            if seleccion_consonante:
                curp1 += seleccion_consonante
            if encontradas:
                if any(letra in vocales for letra in curp):
                    curp += encontradas[1] if len(encontradas) > 1 else ""
                else:
                    curp += encontradas[0]
            # Primera letra del apellido materno
            nombre_table = p[5][0]
            curp += nombre_table
            nombre_table = p[5]  # Nombre completo del apellido paterno
            vocales = "aeiouAEIOU"
            consonantes = [letra for letra in nombre_table if letra.isalpha() and letra not in vocales]
            # Verificar si la primera letra es una vocal
            if nombre_table[0] in vocales:
                # Si la primera letra es vocal, tomar la primera consonante
                seleccion_consonante = consonantes[0] if consonantes else None
            else:
                # Si la primera letra es consonante, tomar la segunda consonante
                seleccion_consonante = consonantes[1] if len(consonantes) > 1 else None
            # Agregar la consonante seleccionada a curp1
            if seleccion_consonante:
                curp1 += seleccion_consonante
            # Primera letra del primer nombre
            nombre_table = p[2][0]
            curp += nombre_table
            nombre_table = p[2]  # Nombre completo del apellido paterno
            vocales = "aeiouAEIOU"
            consonantes = [letra for letra in nombre_table if letra.isalpha() and letra not in vocales]
            # Verificar si la primera letra es una vocal
            if nombre_table[0] in vocales:
                # Si la primera letra es vocal, tomar la primera consonante
                seleccion_consonante = consonantes[0] if consonantes else None
            else:
                # Si la primera letra es consonante, tomar la segunda consonante
                seleccion_consonante = consonantes[1] if len(consonantes) > 1 else None
            # Agregar la consonante seleccionada a curp1
            if seleccion_consonante:
                curp1 += seleccion_consonante
                nombre = p[2] + " " + p[3]

    else:
        error_msg = f"Error: combinación inválida de palabras reservadas '{p[1]}' en la declaración."
        resultado_gramatica.append(error_msg)

def p_fecha(p):
    '''
    fecha : PRIORIDAD ENTERO ENTERO ENTERO
    '''
    global curp,curp1
    if p[1].lower() == 'fecha':
        # Añadir los últimos dos dígitos del año al CURP
        if len(p[4]) == 4:
            año = str(p[4])  # Año como número (ej. 1995)        
            mes = str(p[3])  # Mes como número (ej. 07)
            dia = str(p[2])  # Día como número (ej. 15)

        # Añadir año, mes y día en formato YYMMDD
            curp += año[-2:] + mes.zfill(2) + dia.zfill(2)
        
        # Asignar el carácter diferenciador de homonimia y siglo
            if int(p[4]) < 2000:
                curp1 += '0'  # Caracter numérico arbitrario (puede ajustarse entre 0 y 9)
            else:
                curp1 += 'A'  # Caracter alfabético arbitrario (puede ajustarse entre A y J)
        else:
            error_msg = f"Error: Pon bien la fecha '{p[4]}' es yyyy"
            resultado_gramatica.append(error_msg)

            
    else :
        error_msg = f"Error: combinación inválida de palabras reservadas '{p[1]}' en la declaración."
        resultado_gramatica.append(error_msg)

def p_genero(p):
    '''
    genero : PRIORIDAD IDENTIFICADOR
    '''
    global curp
    if p[1].lower() == 'genero':
        if p[2].lower() == 'hombre':
            curp += 'h'
        elif p[2].lower() == 'mujer':
            curp += 'm'
        else:
            error_msg = f"Error: Solo puedes poner Hombre o Mujer -_- ."
            resultado_gramatica.append(error_msg)
                        
    else:
        error_msg = f"Error: combinación inválida de palabras reservadas '{p[1]}' en la declaración."
        resultado_gramatica.append(error_msg)

def p_estado(p):
    '''
    estado : PRIORIDAD IDENTIFICADOR
    '''
    global curp
    if p[1].lower() == 'estado':
        if p[2].lower() == 'chiapas':
            estado ='cs'
            curp += estado
        else:
            error_msg = f"Error: Solo puedes poner chiapas -_- ."
            resultado_gramatica.append(error_msg)

    else:
        error_msg = f"Error: combinación inválida de palabras reservadas '{p[1]}' en la declaración."
        resultado_gramatica.append(error_msg)

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

# Función para realizar el análisis sintáctico y semántico
def realizar_analisis_sintactico(code, total_lineas_param):
    global resultado_gramatica
    global total_lineas

    total_lineas = total_lineas_param
    resultado_gramatica.clear()
    contexto_identificadores.clear()  # Limpiar contexto semántico

    resultado_sintactico = parser.parse(code)

    if resultado_sintactico:
        resultado_gramatica.append(resultado_sintactico)
        
    return resultado_gramatica
