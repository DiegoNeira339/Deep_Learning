from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image, ImageOps 
import io

app = Flask(__name__)
CORS(app)

try:
    modelo = tf.keras.models.load_model('modelo_reconocimiento_facial.keras')
    print("¡Modelo cargado exitosamente en la API!")
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