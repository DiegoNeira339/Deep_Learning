from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
# Habilitamos CORS para que Next.js (que correrá en otro puerto) pueda comunicarse con la API
CORS(app)

# 1. Cargamos el modelo que nos generó el Colab
try:
    modelo = tf.keras.models.load_model('modelo_reconocimiento_facial.keras')
    print("¡Modelo cargado exitosamente en la API!")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")

# 2. Diccionario de Clases (Nombres de las personas)
# IMPORTANTE: Aquí debes poner los nombres EXACTOS de las carpetas en el mismo orden alfabético 
# en que estaban en tu Drive durante el entrenamiento.
# 2. Diccionario de Clases (Nombres de las carpetas principales del dataset)
clases = [
    "fotografías_evaluacion1_deep_learning_01",
    "fotografías_evaluacion1_deep_learning_02",
    "fotografías_evaluacion1_deep_learning_03",
    "fotografías_evaluacion1_deep_learning_04",
    "fotografías_evaluacion1_deep_learning_05",
    "fotografías_evaluacion1_deep_learning_06",
    "fotografías_evaluacion1_deep_learning_07",
    "fotografías_evaluacion1_deep_learning_08",
    "fotografías_evaluacion1_deep_learning_09",
    "fotografías_evaluacion1_deep_learning_10"
]
@app.route('/predecir', methods=['POST'])
def predecir():
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró ninguna imagen en la petición'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    try:
        # 3. Leemos la imagen enviada por el Frontend
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        
        # 4. Preprocesamiento (Igual que en Colab)
        img = img.resize((128, 128)) # Mismo tamaño que usamos para entrenar
        # Si la imagen viene en RGBA (con transparencia), la pasamos a RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img_array = image.img_to_array(img)
        # Reescalamos los colores de 0-255 a 0-1 (Igual que la capa Rescaling del Colab)
        img_array = img_array / 255.0 
        img_array = np.expand_dims(img_array, axis=0) # Añadimos la dimensión del batch
        
        # 5. Predicción
        predicciones = modelo.predict(img_array)
        indice_clase = np.argmax(predicciones[0]) # Obtenemos el índice con la mayor probabilidad
        probabilidad = float(predicciones[0][indice_clase])
        
        # 6. Mapeamos el índice al nombre de la persona
        if indice_clase < len(clases):
            nombre_persona = clases[indice_clase]
        else:
            nombre_persona = "Desconocido"

        # 7. Retornamos la respuesta al Frontend
        return jsonify({
            'persona_detectada': nombre_persona,
            'probabilidad': round(probabilidad * 100, 2)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Corremos el servidor en el puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=True)