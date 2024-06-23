### Proyecto-M7: Técnicas avanzadas

Para utilizar este proyecto, sigue los siguientes pasos:

1. **Clona el repositorio en tu máquina local:**
   ```sh
   git clone https://github.com/Arsiel15/Proyecto-M7.-T-cnicas-avanzadas.git
   ```

2. **Crea un ambiente virtual:**
   ```sh
   python -m venv venv
   ```

3. **Instala los paquetes de Python necesarios:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Ejecuta el archivo principal:**
   Corre el archivo `.py` llamado `Modelo`.

5. **Ejecución de Ngrok:**
   Se debe de descargar la Setup & Installation de Ngrok, una vez registrados desde el dashboard.
   Desde el ngrok.exe, introducir:
   ```sh
   ngrok http 5000
   ``` 

4. **Ejecuta la aplicación:**
   Luego, ejecuta la aplicación `APP` desde la terminal, utilizando
     ```sh
   python APP.py
   ``` 

7. **Para hacer peticiones al API:**
   Puedes utilizar Postman, colocando el URL que nos proporciona Ngrok y el endpoint `/predict`. Además, se necesita enviar los datos de la encuesta en forma de diccionario con la clave `"datos"`, y en el valor se debe colocar el registro de la encuesta unido por `";"`.

   La respuesta del API es en forma de diccionario, con la clave `"predicciones"` y el valor que contiene una lista con las predicciones de los datos ingresados.
