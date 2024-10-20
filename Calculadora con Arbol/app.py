from flask import Flask, render_template, request, jsonify
import ply.lex as lex
import ply.yacc as yacc

# Configuración del analizador léxico
tokens = [
    'NUMERO', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'
]

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.tipo_numero = 'Decimal'
        t.value = float(t.value)
    else:
        t.tipo_numero = 'Entero'
        t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Caracter no válido: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Reglas del parser
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = ('+', p[1], p[3])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = ('-', p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = ('*', p[1], p[3])

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = ('/', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMERO'
    p[0] = ('NUMERO', p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Error de sintaxis en la entrada!")

parser = yacc.yacc()

# Aplicación Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Función para evaluar el árbol de expresión
def evaluar_arbol(arbol):
    if arbol[0] == 'NUMERO':
        return arbol[1]
    elif arbol[0] == '+':
        return evaluar_arbol(arbol[1]) + evaluar_arbol(arbol[2])
    elif arbol[0] == '-':
        return evaluar_arbol(arbol[1]) - evaluar_arbol(arbol[2])
    elif arbol[0] == '*':
        return evaluar_arbol(arbol[1]) * evaluar_arbol(arbol[2])
    elif arbol[0] == '/':
        return evaluar_arbol(arbol[1]) / evaluar_arbol(arbol[2])
    else:
        raise ValueError("Operación desconocida")

# Ruta para analizar la expresión y generar el árbol de tokens
@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    expresion = data.get('expresion', '')

    lexer.input(expresion)
    tokens = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type == 'PLUS':
            tokens.append({'token': tok.value, 'tipo': 'Operador Suma'})
        elif tok.type == 'MINUS':
            tokens.append({'token': tok.value, 'tipo': 'Operador Resta'})
        elif tok.type == 'TIMES':
            tokens.append({'token': tok.value, 'tipo': 'Operador Multiplicación'})
        elif tok.type == 'DIVIDE':
            tokens.append({'token': tok.value, 'tipo': 'Operador División'})
        elif tok.type == 'LPAREN':
            tokens.append({'token': tok.value, 'tipo': 'Paréntesis Izquierdo'})
        elif tok.type == 'RPAREN':
            tokens.append({'token': tok.value, 'tipo': 'Paréntesis Derecho'})
        elif tok.type == 'NUMERO':
            tokens.append({'token': tok.value, 'tipo': f'Número {tok.tipo_numero}'})
        else:
            tokens.append({'token': tok.value, 'tipo': tok.type})

    try:
        arbol = parser.parse(expresion)  # Parseamos la expresión
        resultado = evaluar_arbol(arbol)  # Calculamos el resultado del árbol
        tokens.append({'token': '=', 'tipo': 'Operador igual'})
        tokens.append({'token': resultado, 'tipo': 'Resultado'})
    except Exception as e:
        tokens.append({'token': str(e), 'tipo': 'Error al calcular resultado'})

    return jsonify(tokens)

# Ruta para mostrar el árbol
@app.route('/arbol')
def arbol():
    expresion = request.args.get('expresion', '')
    return render_template('arbol.html', expresion=expresion)

@app.route('/generar_arbol', methods=['POST'])
def generar_arbol():
    data = request.json
    expresion = data.get('expresion', '')
    try:
        tree = parser.parse(expresion)
        if tree:
            # Convertir el árbol a un formato adecuado para D3.js
            def convertir_a_d3(nodo):
                if nodo[0] == 'NUMERO':
                    return {"tipo": "NUMERO", "valor": nodo[1]}
                else:
                    return {
                        "tipo": nodo[0],
                        "valor": nodo[0],
                        "children": [convertir_a_d3(nodo[1]), convertir_a_d3(nodo[2])]
                    }

            d3_tree = convertir_a_d3(tree)
            return jsonify(d3_tree)
        else:
            return jsonify({"error": "No se pudo generar el árbol."})
    except Exception as e:
        return jsonify({"error": str(e)})
        
if __name__ == '__main__':
    app.run(debug=True)
