import ast
import math 
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)
import pandas as pd

# Cargar dataset ya generado
df = pd.read_csv("dataset_codecomplex.csv")

# Función para calcular la profundidad máxima de bucles
def max_loop_depth(node, depth=0):
    max_depth = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.For, ast.While)):
            max_depth = max(max_depth, max_loop_depth(child, depth+1))
        else:
            max_depth = max(max_depth, max_loop_depth(child, depth))
    return max_depth

# Función para contar tipos de nodos en el código
def extraer_features(codigo):
    try:
        tree = ast.parse(codigo)
    except:
        return {"for": 0, "while": 0, "if": 0, "funciones": 0, "recursivo": 0, "lineas": codigo.count("\n") + 1, "profundidad_bucles": 0}

    features = {
        "for": 0,
        "while": 0,
        "if": 0,
        "funciones": 0,
        "recursivo": 0,
        "lineas": codigo.count("\n") + 1,
    }

    nombre_funciones = []

    for nodo in ast.walk(tree):
        if isinstance(nodo, ast.For):
            features["for"] += 1
        elif isinstance(nodo, ast.While):
            features["while"] += 1
        elif isinstance(nodo, ast.If):
            features["if"] += 1
        elif isinstance(nodo, ast.FunctionDef):
            features["funciones"] += 1
            nombre_funciones.append(nodo.name)
        elif isinstance(nodo, ast.Call):
            if hasattr(nodo.func, "id") and nodo.func.id in nombre_funciones:
                features["recursivo"] += 1

    # Agrega la profundidad máxima de bucles
    features["profundidad_bucles"] = max_loop_depth(tree)

    return features

def estimar_complejidad_heuristica(for_niveles, while_niveles):
    if for_niveles == 0 and while_niveles == 0:
        return "O(1)"
    elif for_niveles == 0:
        return f"O((log(n))^{while_niveles})"
    elif while_niveles == 0:
        return f"O(n^{for_niveles})"
    else:
        return f"O(n^{for_niveles} * (log(n))^{while_niveles})"

def calcular_tn(n, for_niveles, while_niveles):
    try:
        tn = math.pow(n, for_niveles) * math.pow(math.log(n, 2), while_niveles)
        return min(int(tn), 4000)
    except:
        return 4000

# Aplica la función a cada fila y guarda el nuevo dataset
features_extraidos = df["codigo"].apply(extraer_features)
df_features = pd.DataFrame(features_extraidos.tolist())
df_final = pd.concat([df_features, df["complejidad"]], axis=1)
df_final.to_csv("dataset_entrenamiento.csv", index=False)
print("✅ Dataset con profundidad de bucles guardado como 'dataset_entrenamiento.csv'")

