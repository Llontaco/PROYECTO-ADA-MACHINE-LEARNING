

# 🔍 Analizador de Complejidad Algorítmica

¡Bienvenido! Este proyecto es una aplicación web que analiza código Python y estima su complejidad algorítmica usando 🤖 Machine Learning y 🧠 heurísticas. Además, genera un gráfico 📈 comparativo de la función T(n) estimada frente a otras funciones de referencia.

---

## 🚀 Características

- 🤖 **Predicción automática** de la complejidad algorítmica usando ML.
- 🧠 **Estimación heurística** basada en la estructura del código.
- 📈 **Visualización gráfica** de T(n) y comparación con otras funciones.
- ⚠️ **Advertencias** si la heurística y el modelo no coinciden.
- 💻 **Interfaz web moderna** y fácil de usar.

---

## 🛠️ Tecnologías utilizadas

- **Backend:** Python, Flask, Flask-CORS, pandas, scikit-learn, joblib, matplotlib, ast, math, io, base64
- **Frontend:** HTML5, TailwindCSS, JavaScript
- **Sistema operativo:** Windows (compatible con Linux y macOS)

---

## 📦 Instalación

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/tuusuario/analizador-complejidad.git
   cd analizador-complejidad
   ```

2. **Instala las dependencias:**
   ```bash
   pip install flask flask-cors pandas scikit-learn matplotlib
   ```

3. **Asegúrate de tener el modelo entrenado:**
   - El archivo modelo_complejidad.pkl debe estar en la raíz del proyecto.
   - Si necesitas entrenarlo, usa tu script de entrenamiento con tu dataset.

4. **(Opcional) Coloca una imagen de fondo en FISI.jpg para una mejor apariencia.**

---

## ▶️ Uso

1. **Inicia el servidor:**
   ```bash
   python app.py
   ```

2. **Abre tu navegador en:**
   ```
   http://localhost:5000
   ```

3. **Pega tu código Python** en el área de texto y haz clic en **"Predecir Complejidad"**.

4. **Visualiza:**
   - 🧠 La predicción del modelo ML.
   - 🧮 La estimación heurística.
   - 🔁 El número de bucles for y while detectados.
   - ⚠️ Una advertencia si la heurística y el modelo no coinciden.
   - 📈 Un gráfico comparativo de complejidades.

---

## 📝 Ejemplo de entrada y salida

**Entrada:**
```python
for i in range(n):
    for j in range(n):
        print(i, j)
```

**Salida esperada:**
```json
{
  "complejidad_modelo": "quadratic",
  "funcion_equivalente": "f(n) = n²",
  "complejidad_heuristica": "O(n^2)",
  "for_niveles": 2,
  "while_niveles": 0,
  "advertencia": null
}
```

---

## 📚 Créditos

- Desarrollado por [Henry Llontop]  
- Facultad de Ingenieria de Software 

---

## 📄 Licencia

Este proyecto está bajo la licencia UNMSM.

---
