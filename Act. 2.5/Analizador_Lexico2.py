import ply.lex as lex
from collections import defaultdict

# Definir los tokens para el analizador léxico
tokens = (
    'RESERVADA', 'RESERVADO', 'DELIMITADOR', 'SIMBOLO', 'OPERADOR', 
    'IDENTIFICADOR', 'ENTERO', 'PLUSPLUS',
    'COMDOB', 'DOSPUNTO', 'SUMA', 'RESTA'
)

# Expresiones regulares para los tokens
t_PLUSPLUS = r'\+\+'
t_RESTA = r'\-'
t_COMDOB = r'"'
t_DOSPUNTO = r':'
t_SUMA = r'\+'

# Definir tokens reservados
def t_RESERVADA(t):    
    r'(for|while|do|if|else|program)'
    return t

def t_RESERVADO(t):
    r'(public|static|System|void|out|int|println|read|printf|end)'
    return t

def t_DELIMITADOR(t):
    r'\(|\)|\{|\}'
    return t

def t_SIMBOLO(t):
    r';|\.'
    return t

def t_OPERADOR(t):
    r'=|<=|>='
    return t

def t_ENTERO(t):
    r'\d+'
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z][a-zA-Z0-9\s]*'
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
    lexer.lineno = 1  # Reiniciar el contador de líneas

    for tok in lexer:
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
    
    return tokens_lexico, category_count_list, total_lineas 
