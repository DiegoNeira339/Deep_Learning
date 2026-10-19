from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image, ImageOps
import cv2 # <-- NUEVA: Librería para visión artificial (OpenCV)
import io
import urllib.request
import os

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DEL DETECTOR DE ROSTROS ---
# Descargamos el modelo de detección de rostros de OpenCV (Haar Cascade) si no existe localmente
cascade_path = "haarcascade_frontalface_default.xml"
if not os.path.exists(cascade_path):
    print("Descargando detector de rostros de OpenCV...")
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml",
        cascade_path
    )
detector_rostros = cv2.CascadeClassifier(cascade_path)

# --- CONFIGURACIÓN DE TU MODELO KERAS ---
try:
    modelo = tf.keras.models.load_model('modelo_reconocimiento_facial.keras')
    print("¡Modelo Keras cargado exitosamente en la API!")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")

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

UMBRAL_CONFIANZA = 0.85 

@app.route('/predecir', methods=['POST'])
def predecir():
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró ninguna imagen en la petición'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        img = ImageOps.exif_transpose(img) 
        
        
        open_cv_image = np.array(img.convert('RGB')) 
        open_cv_image = open_cv_image[:, :, ::-1].copy() 

        gris = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        
        rostros_detectados = detector_rostros.detectMultiScale(
            gris, 
            scaleFactor=1.1, 
            minNeighbors=3, 
            minSize=(30, 30)
        )
        
        if len(rostros_detectados) == 0:
            return jsonify({
                'persona_detectada': 'Error: No se detectó un rostro humano válido.',
                'probabilidad': 0.0
            }), 200
        
        img = img.resize((128, 128))
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0 
        img_array = np.expand_dims(img_array, axis=0) 
        

        predicciones = modelo.predict(img_array)
        indice_clase = np.argmax(predicciones[0])
        probabilidad = float(predicciones[0][indice_clase])
        
        if probabilidad >= UMBRAL_CONFIANZA and indice_clase < len(clases):
            nombre_persona = clases[indice_clase]
        else:
            nombre_persona = "La persona no está en la base de datos."

        return jsonify({
            'persona_detectada': nombre_persona,
            'probabilidad': round(probabilidad * 100, 2)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)