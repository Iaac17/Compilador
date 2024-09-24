from flask import Flask, render_template, request
from Analizador_Lexico2 import realizar_analisis_lexico
from Analizador_sintactico import realizar_analisis_sintactico

# Inicializar la aplicación Flask
app = Flask(__name__)

# Ruta principal que une el análisis léxico y sintáctico
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('code', '')  # Obtener el código desde el formulario
        
        # Realizar análisis léxico y obtener tokens y contadores
        tokens_lexico, category_count_list = realizar_analisis_lexico(code)
        
        # Realizar análisis sintáctico
        resultado_sintactico = realizar_analisis_sintactico(code)

        # Renderizar el template con los resultados
        return render_template('home.html', code=code, tokens=tokens_lexico, category_count=category_count_list, resultado_sintactico=resultado_sintactico )
    
    # Si no se ha enviado un código, mostrar la página sin resultados
    return render_template('home.html', tokens=None, category_count=None, resultado_sintactico=None)

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
