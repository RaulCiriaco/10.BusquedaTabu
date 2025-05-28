from flask import Flask, render_template, request, jsonify
import tsp_algorithms  # Importamos los algoritmos desde otro archivo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.form
    algoritmo = data['algoritmo']
    
    if algoritmo == "templado_simulado":
        normal_temp = float(data['normal_temp'])
        min_temp = float(data['min_temp'])
        cooling_rate = int(data['cooling_rate'])
        ruta_optima, distancia_total = tsp_algorithms.templado_simulado(normal_temp, min_temp, cooling_rate)
    elif algoritmo == "busqueda_tabu":
        iteraciones = int(data['iteraciones'])
        ruta_optima, distancia_total = tsp_algorithms.busqueda_tabu(iteraciones)

    return jsonify({'ruta': ruta_optima, 'distancia_total': distancia_total})

if __name__ == '__main__':
    app.run(debug=True)
