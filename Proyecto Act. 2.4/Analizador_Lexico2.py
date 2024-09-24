import ply.lex as lex
from collections import defaultdict

# Definir los tokens para el analizador léxico
tokens = (
    'RESERVADA', 'RESERVADO', 'DELIMITADOR', 'SIMBOLO', 'OPERADOR',
    'IDENTIFICADOR', 'ENTERO', 'MENORIGUAL', 'PLUSPLUS',
    'COMDOB', 'DOSPUNTO', 'SUMA'
)

# Expresiones regulares para los tokens
t_MENORIGUAL = r'<='
t_PLUSPLUS = r'\+\+'
t_COMDOB = r'"'
t_DOSPUNTO = r':'
t_SUMA = r'\+'

# Definir tokens reservados
def t_RESERVADA(t):    
    r'(for|while|do|if|else)'
    return t

def t_RESERVADO(t):
    r'(public|static|System|void|out|int|println)'
    return t

def t_DELIMITADOR(t):
    r'\(|\)|\{|\}'
    return t

def t_SIMBOLO(t):
    r';|\.'
    return t

def t_OPERADOR(t):
    r'='
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
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Función para realizar el análisis léxico con contador de categorías
def realizar_analisis_lexico(code):
    lexer.input(code)
    tokens_lexico = []
    category_count = defaultdict(int)  # Contador para las categorías
    lexer.lineno = 1
    
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
    
    return tokens_lexico, category_count_list
