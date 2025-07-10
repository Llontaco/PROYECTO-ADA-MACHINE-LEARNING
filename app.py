from flask import Flask, request, jsonify
import joblib
import pandas as pd 
import ast
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir CORS para todas las rutas
modelo = joblib.load("modelo_complejidad.pkl")

def max_loop_depth(node, depth=0):
    max_depth = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.For, ast.While)):
            max_depth = max(max_depth, max_loop_depth(child, depth+1))
        else:
            max_depth = max(max_depth, max_loop_depth(child, depth))
    return max_depth

def extraer_features(codigo):
    # Limpia caracteres invisibles y normaliza espacios
    codigo_limpio = (
        codigo.replace('\xa0', ' ')
              .replace('\t', ' ')
              .replace('\r', '')
    )
    try:
        arbol = ast.parse(codigo_limpio)
    except Exception as e:
        print("Error al parsear el código:", e)
        return {
            "for": 0,
            "while": 0,
            "if": 0,
            "funciones": 0,
            "recursivo": 0,
            "lineas": len([l for l in codigo_limpio.strip().split("\n") if l.strip()]),
            "profundidad_bucles": 0
        }

    for_count = 0
    while_count = 0
    if_count = 0
    func_count = 0
    recursivo = 0
    lineas = len([l for l in codigo_limpio.strip().split("\n") if l.strip()])
    nombres_funciones = set()
    funciones_recursivas = set()

    # Primero, recolecta los nombres de las funciones definidas
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.FunctionDef):
            func_count += 1
            nombres_funciones.add(nodo.name)

    # Ahora, cuenta los otros elementos y busca llamadas recursivas
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.For):
            for_count += 1
        elif isinstance(nodo, ast.While):
            while_count += 1
        elif isinstance(nodo, ast.If):
            if_count += 1
        elif isinstance(nodo, ast.Call):
            # Si la función llamada tiene el mismo nombre que alguna función definida, es recursivo
            if hasattr(nodo.func, "id") and nodo.func.id in nombres_funciones:
                funciones_recursivas.add(nodo.func.id)

    if funciones_recursivas:
        recursivo = 1

    # Calcula la profundidad máxima de bucles
    profundidad_bucles = max_loop_depth(arbol)

    return {
        "for": for_count,
        "while": while_count,
        "if": if_count,
        "funciones": func_count,
        "recursivo": recursivo,
        "lineas": lineas,
        "profundidad_bucles": profundidad_bucles
    }

@app.route("/predecir", methods=["POST"])
def predecir():
    data = request.get_json()
    print("Datos recibidos:", data)
    codigo = data.get("codigo", "")
    features = extraer_features(codigo)
    print("Features extraídas:", features)  # <-- Agrega esta línea
    input_modelo = pd.DataFrame([{
        "for": features["for"],
        "while": features["while"],
        "if": features["if"],
        "funciones": features["funciones"],
        "recursivo": features["recursivo"],
        "lineas": features["lineas"],
        "profundidad_bucles": features["profundidad_bucles"]
    }])
    
    prediccion = modelo.predict(input_modelo)[0]
    return jsonify({"complejidad": prediccion})

if __name__ == "__main__":
    app.run(debug=True)

def contar_anidamiento(node, nivel=0):
    max_nivel = nivel
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.For, ast.While)):
            max_nivel = max(max_nivel, contar_anidamiento(child, nivel + 1))
        else:
            max_nivel = max(max_nivel, contar_anidamiento(child, nivel))
    return  max_nivel

anidamiento_max = contar_anidamiento(arbol)