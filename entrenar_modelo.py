import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
import joblib
from extraer_features import extraer_features

# Cargar dataset original
df = pd.read_csv("dataset_codecomplex.csv")
df = df.dropna(subset=['complejidad'])

# Extraer features
features = []
for _, fila in df.iterrows():
    codigo = fila['codigo']
    complejidad = fila['complejidad']
    f = extraer_features(codigo)
    f['complejidad'] = complejidad
    features.append(f)

# Guardar dataset procesado
df_final = pd.DataFrame(features)
df_final.to_csv("dataset_entrenamiento.csv", index=False)

# Variables y etiquetas
X = df_final[['for', 'while', 'if', 'funciones', 'recursivo', 'lineas','profundidad_bucles']]
y = df_final['complejidad']

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
modelo = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42)
modelo.fit(X_train, y_train)

# Evaluar modelo
y_pred = modelo.predict(X_test)
print("✅ Precisión:", accuracy_score(y_test, y_pred))
print("📋 Reporte:")
print(classification_report(y_test, y_pred))

# Validación cruzada
scores = cross_val_score(modelo, X, y, cv=5)
print("📊 Validación cruzada:", scores)
print("📊 Promedio:", scores.mean())

# Guardar modelo
joblib.dump(modelo, "modelo_complejidad.pkl")
print("✅ Modelo guardado como modelo_complejidad.pkl")
