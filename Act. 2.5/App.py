from flask import Flask, render_template, request
from Analizador_Lexico2 import realizar_analisis_lexico
from Analizador_sintactico import realizar_analisis_sintactico

# Inicializar la aplicación Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    has_error = False  # Inicializa la variable
    if request.method == 'POST':
        code = request.form.get('code', '')  # Obtener el código desde el formulario
        
        # Realizar análisis léxico y obtener tokens, contadores, número total de líneas 
        tokens_lexico, category_count_list, total_lineas= realizar_analisis_lexico(code)
        
        # Realizar análisis sintáctico
        resultado_sintactico = realizar_analisis_sintactico(code, total_lineas)

        # Verifica si hay errores
        if resultado_sintactico and any("Error" in r for r in resultado_sintactico):
            has_error = True  # Si hay algún error, establece la variable en True

        # Renderizar el template con los resultados
        return render_template('home.html', code=code, tokens=tokens_lexico, category_count=category_count_list, resultado_sintactico=resultado_sintactico, has_error=has_error)
    
    # Si no se ha enviado un código, mostrar la página sin resultados
    return render_template('home.html', tokens=None, category_count=None, resultado_sintactico=None, has_error=None)

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
