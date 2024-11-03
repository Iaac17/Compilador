import ply.lex as lex
from collections import defaultdict
from collections import Counter

# Definir los tokens para el analizador léxico
tokens = (
    'PRIORIDAD', 'SIMBOLO', 'OPERADOR', 
    'IDENTIFICADOR', 'ENTERO', 
)

# Definir tokens reservados
def t_PRIORIDAD(t):    
    r'( [nN][oO][mM][bB][rR][eE] | [fF][eE][cC][hH][aA] | [gG][eE][nN][eE][rR][oO]  | [eE][sS][tT][aA][dD][oO] | [dD][rR][oO][pP] )'
    return t

def t_OPERADOR(t):
    r'=|<=|>='
    return t

def t_SIMBOLO(t):
    r';|\.'
    return t

def t_ENTERO(t):
    r'\d+'
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-ZñÑ][a-zA-Z0-9ñÑ]*'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # Incrementa el número de líneas correctamente

# Manejo de errores léxicos mejorado
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}, posición {t.lexpos}")
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

def realizar_analisis_lexico(code):
    lexer.input(code)
    tokens_lexico = []
    category_count = defaultdict(int)  # Contador para las categorías
    contador = Counter()
    lexer.lineno = 1  # Reiniciar el contador de líneas

    for tok in lexer:
        if tok.type == 'PRIORIDAD':
            contador['Prioridad'] += 1
        elif tok.type == 'IDENTIFICADOR':
            contador['Identificador'] += 1
        elif tok.type == 'ENTERO':
            contador['Numero'] += 1
        else:
            contador['Desconocido'] += 1

        # Registrar el tipo de token y aumentar el contador de esa categoría
        category_count[tok.type] += 1
        
        # Guardar los detalles del token
        tokens_lexico.append({
            'type': tok.type,
            'value': tok.value,
            'line': tok.lineno,  
            'pos': tok.lexpos
        })        
    # Convertir el defaultdict a una lista de tuplas
    category_count_list = list(category_count.items())
    total_lineas = lexer.lineno - 1 
    
    return tokens_lexico, contador, category_count_list, total_lineas
            