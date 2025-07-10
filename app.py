from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd 
import ast
from flask_cors import CORS
import matplotlib.pyplot as plt
import math
import io
import base64

from heuristica import estimar_complejidad_heuristica, calcular_tn

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Página principal
@app.route("/")
def index():
    return render_template("index.html")

# Cargar modelo ML
modelo = joblib.load("modelo_complejidad.pkl")

# ------------------------------------------
# Funciones para extracción de características
# ------------------------------------------
def max_loop_depth(node, depth=0):
    max_depth = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.For, ast.While)):
            max_depth = max(max_depth, max_loop_depth(child, depth + 1))
        else:
            max_depth = max(max_depth, max_loop_depth(child, depth))
    return max_depth

def extraer_features(codigo):
    codigo_limpio = codigo.replace('\xa0', ' ').replace('\t', ' ').replace('\r', '')
    try:
        arbol = ast.parse(codigo_limpio)
    except Exception as e:
        print("Error al parsear el código:", e)
        return {
            "for": 0, "while": 0, "if": 0, "funciones": 0,
            "recursivo": 0, "lineas": len([l for l in codigo_limpio.strip().split("\n") if l.strip()]),
            "profundidad_bucles": 0
        }

    for_count = while_count = if_count = func_count = recursivo = 0
    nombres_funciones = set()
    funciones_recursivas = set()

    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.FunctionDef):
            func_count += 1
            nombres_funciones.add(nodo.name)

    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.For):
            for_count += 1
        elif isinstance(nodo, ast.While):
            while_count += 1
        elif isinstance(nodo, ast.If):
            if_count += 1
        elif isinstance(nodo, ast.Call):
            if hasattr(nodo.func, "id") and nodo.func.id in nombres_funciones:
                funciones_recursivas.add(nodo.func.id)

    if funciones_recursivas:
        recursivo = 1

    profundidad_bucles = max_loop_depth(arbol)
    lineas = len([l for l in codigo_limpio.strip().split("\n") if l.strip()])

    return {
        "for": for_count, "while": while_count, "if": if_count,
        "funciones": func_count, "recursivo": recursivo,
        "lineas": lineas, "profundidad_bucles": profundidad_bucles
    }

# ------------------------------------
# Endpoint: Predecir complejidad
# ------------------------------------
@app.route('/predecir', methods=['POST'])
def predecir():
    datos = request.get_json()
    codigo = datos.get('codigo', '')

    if not codigo.strip():
        return jsonify({"error": "Código vacío"}), 400

    features = extraer_features(codigo)
    input_modelo = pd.DataFrame([features])
    prediccion = modelo.predict(input_modelo)[0]

    equivalencias = {
        "constant": "f(n) = 1",
        "linear": "f(n) = n",
        "logarithmic": "f(n) = log(n)",
        "linear_logarithmic": "f(n) = n * log(n)",
        "quadratic": "f(n) = n²",
        "cubic": "f(n) = n³",
        "exponential": "f(n) = 2ⁿ"
    }

    funcion_equivalente = equivalencias.get(prediccion, "f(n) desconocida")
    heuristica = estimar_complejidad_heuristica(features["for"], features["while"])

    mapa_heuristica_a_modelo = {
        "O(1)": "constant",
        "O(n)": "linear",
        "O(log(n))": "logarithmic",
        "O(n log(n))": "linear_logarithmic",
        "O(n^2)": "quadratic",
        "O(n^3)": "cubic",
        "O(2^n)": "exponential"
    }

    heuristica_clase = mapa_heuristica_a_modelo.get(heuristica, "desconocida")

    advertencia = None
    if heuristica_clase != prediccion:
        advertencia = "⚠ La estimación heurística no coincide con la predicción del modelo. Puede haber un error."

    return jsonify({
        "complejidad_modelo": prediccion,
        "funcion_equivalente": funcion_equivalente,
        "complejidad_heuristica": heuristica,
        "for_niveles": features["for"],
        "while_niveles": features["while"],
        "advertencia": advertencia
    })

# ------------------------------------
# Endpoint: Graficar T(n) vs otras
# ------------------------------------
@app.route("/graficar", methods=["POST"])
def graficar():
    datos = request.get_json()
    for_niveles = datos.get("for", 0)
    while_niveles = datos.get("while", 0)

    x = list(range(1, 13))
    tn = [calcular_tn(n, for_niveles, while_niveles) for n in x]
    logn = [min(math.log(n, 2), 4000) for n in x]
    lineal = x
    nlogn = [min(n * math.log(n, 2), 4000) for n in x]
    cuadrado = [min(n**2, 4000) for n in x]
    cubo = [min(n**3, 4000) for n in x]
    exp2 = [min(2**n, 4000) for n in x]

    plt.figure(figsize=(10, 6))
    plt.plot(x, tn, label="T(n) estimada", linewidth=2, color='black')
    plt.plot(x, logn, label="O(log(n))")
    plt.plot(x, lineal, label="O(n)")
    plt.plot(x, nlogn, label="O(n log n)")
    plt.plot(x, cuadrado, label="O(n²)")
    plt.plot(x, cubo, label="O(n³)")
    plt.plot(x, exp2, label="O(2ⁿ)")

    plt.xlabel("n")
    plt.ylabel("Tiempo estimado")
    plt.title("Comparación de Complejidades")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.read()).decode('utf-8')
    plt.close()

    return jsonify({"grafico": img_b64})

# ------------------------------------
# Ejecutar aplicación
# ------------------------------------
if __name__ == "__main__":
    app.run(debug=True)



