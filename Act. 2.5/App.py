from flask import Flask, render_template, request
from Analizador_Lexico2 import realizar_analisis_lexico
from Analizador_sintactico import realizar_analisis_sintactico
# Inicializar la aplicación Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    has_error = False
    if request.method == 'POST':
        code = request.form.get('code', '')
        tokens_lexico, contador, category_count_list, total_lineas = realizar_analisis_lexico(code)
        
        resultado_sintactico = realizar_analisis_sintactico(code, total_lineas)
        
        if resultado_sintactico and any("Error" in r for r in resultado_sintactico):
            has_error = True

        return render_template('home.html', 
                               code=code, 
                               tokens=tokens_lexico, 
                               contador=contador, 
                               category_count=category_count_list, 
                               resultado_sintactico=resultado_sintactico, 
                               has_error=has_error)
    
    return render_template('home.html', tokens=None, category_count=None, contador=None, resultado_sintactico=None, has_error=None)
# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
