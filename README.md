# Proyecto-M7.-Tecnicas-avanzadas
Para utilizar este proyecto sigue los siguientes pasos:
1. Clona el repositorio en tú máquina local:
   ```bash
   git clone https://github.com/Arsiel15/Proyecto-M7.-T-cnicas-avanzadas.git

2. Crea un ambiente virtual:
   ```bash
    python -m venv venv

3. Instala los paquetes de Python necesarios:
    ```bash
    pip install -r requirements.txt

4. Correr el archivo .py que se llama Modelo como principal.
5. Luego el APP.
6. Para hacer peticiones al API, se puede utilizar postman, colocando el URL que nos proporciona Ngrok y el endpoint /predict, además se necesita enviar los datos de la encuesta en forma de diccionario con la clave "datos", en el valor se debe colocar el registro de la encuesta unidos por ";".
7. La respuesta del API es en forma de diccionario, con la clave "predicciones" y el valor contiene una lista con las predicciones de los datos ingresados, La respuesta del API es en forma de diccionario, con la clave "predicciones" y el valor contiene una lista con las predicciones de los datos ingresados.
