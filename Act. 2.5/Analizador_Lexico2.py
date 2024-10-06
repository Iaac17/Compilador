import ply.lex as lex
from collections import defaultdict
from collections import Counter

# Definir los tokens para el analizador léxico
tokens = (
    'RESERVADA', 'RESERVADO', 'SIMBOLO', 'OPERADOR', 
    'IDENTIFICADOR', 'ENTERO', 'PLUSPLUS',
    'COMDOB', 'DOSPUNTO', 'RESTA', 'COMA' 
    ,'SUMA' , 'PARIZQ', 'PARDER', 'LLAIZQ', 'LLADER'
)

# Expresiones regulares para los tokens
t_COMA = r'\,'
t_PLUSPLUS = r'\+\+'
t_RESTA = r'\-'
t_COMDOB = r'"'
t_DOSPUNTO = r':'
t_SUMA = r'\+'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAIZQ = r'\{'
t_LLADER = r'\}'

# Definir tokens reservados
def t_RESERVADA(t):    
    r'(for|while|do|if|else|program)'
    return t

def t_RESERVADO(t):
    r'(public|static|System|void|out|int|println|read|printf|end)'
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
    contador = Counter()
    lexer.lineno = 1  # Reiniciar el contador de líneas

    for tok in lexer:
        if tok.type == 'RESERVADA':
            contador['Reservada'] += 1
        elif tok.type == 'RESERVADO':
            contador['Reservado'] += 1
        elif tok.type in ['SIMBOLO', 'COMA']:
            contador['Simbolo'] += 1
        elif tok.type == 'IDENTIFICADOR':
            contador['Identificador'] += 1
        elif tok.type == 'ENTERO':
            contador['Numero'] += 1
        elif tok.type in ['PARIZQ', 'PARDER', 'LLAIZQ', 'LLADER']:
            contador['Delimitador'] += 1
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
            
