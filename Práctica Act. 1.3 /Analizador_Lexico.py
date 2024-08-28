import ply.lex as lex
from flask import Flask, render_template, request
from collections import defaultdict

app = Flask(__name__)

# Definición de tokens y expresiones regulares
reserved = {
    'for': 'FOR',
    'while': 'WHILE',
    'do': 'DO',
    'if': 'IF',
    'else': 'ELSE'
}

reservado = {
    'public': 'PUBLIC',
    'static': 'STATIC',
    'void': 'VOID',
    'int': 'INT'
}

Identificador = {
    'main': 'MAIN',
}

Delimitador = {
    'PABIERTO': '(',
    'PCERRADO': ')',
    'LABIERTO': '{',
    'LCERRADO': '}',
}

Simbolo = {
    'PYC': ';',
    'PUNTO': '.'
}

Operador = {
    'IGUAL': '='
}

Numero = {
    'NUMERO': r'\d'
}

tokens = ['PABIERTO', 'PCERRADO', 'LABIERTO', 'LCERRADO', 'IGUAL', 'NUMERO', 'LETRA', 'PYC', 'PUNTO' ] + \
         list(reserved.values()) + list(reservado.values()) + list(Identificador.values()) 

# Expresiones regulares para los tokens
t_FOR = r'for'
t_WHILE = r'while'
t_DO = r'do'
t_IF = r'if'
t_ELSE = r'else'
t_PUBLIC = r'public'
t_STATIC = r'static'
t_VOID = r'void'
t_MAIN = r'main'
t_INT = r'int'
t_PABIERTO = r'\('
t_PCERRADO = r'\)'
t_LABIERTO = r'\{'
t_LCERRADO = r'\}'
t_PYC = r'\;'
t_IGUAL = r'='
t_NUMERO = r'\d'
t_PUNTO = r'\.'
t_LETRA = r'\b[a-zA-Z]\b'


t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print('Caracter no válido', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('code', '')
        lexer.input(code)

        tokens = []
        lexer.lineno = 1
        category_count = defaultdict(int)

        for tok in lexer:
            if tok.type in reserved.values():
                category = 'Reservada'
                category_count[category] += 1
            elif tok.type in reservado.values():
                category = 'Reservado'
                category_count[category] += 1
            elif tok.type in Identificador.values():
                category = 'Identificador'
                category_count[category] += 1
            elif tok.type == 'LETRA':
                category = 'Identificador'
                category_count[category] += 1               
            elif tok.type in Delimitador.keys():
                category = 'Delimitador'
                category_count[category] += 1
            elif tok.type == 'IGUAL':
                category = 'Operador'
                category_count[category] += 1
            elif tok.type == 'NUMERO':
                category = 'Número'
                category_count[category] += 1
            elif tok.type in Simbolo.keys():
                category = 'Simbolo'
                category_count[category] += 1
            else:
                category = 'Desconocido'
                category_count[category] += 1

            token_info = {
                'category': category,
                'value': tok.value,
                'lineno': tok.lineno,
                'lexpos': tok.lexpos
            }
            tokens.append(token_info)

        category_count_list = [(category, count) for category, count in category_count.items()]

        return render_template('index.html', code=code, tokens=tokens, category_count=category_count_list)

    return render_template('index.html', tokens=None, category_count=None)

if __name__ == '__main__':
    app.run(debug=True)

   # flask --app Analizador_Lexico.py run
"""  
   public static void main ()
{
      int n = 23.23;
}
for
asad
"""
