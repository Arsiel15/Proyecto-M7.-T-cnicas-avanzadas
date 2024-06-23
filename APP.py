from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import joblib
from funtion import json_df, decode_pred

app = Flask(__name__)
run_with_ngrok(app)  # Iniciar ngrok cuando la app se ejecute

#Carga el modelo de machine learning
modelo = joblib.load('Model.joblib')

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/predict', methods =['POST'] )
def predict():
    try:
        json_data = request.get_json()
        encoded = json_df(json_data)
        #Suponiendo que tu modelo espera un array o similar, ajusta según sea necesario
        prediccion = modelo.predict(encoded)
        resultado = {"prediccion": decode_pred(prediccion.tolist()[0])}  # Convertir a lista si es necesario
        #resultado = {"prediccion": "datos"}
        return jsonify(resultado)
    except Exception as e:
        app.logger.error(f'Error inesperado: {e}')
        return jsonify({'error': 'Error procesando la solicitud'}), 500

if __name__ == '__main__':
    app.run()