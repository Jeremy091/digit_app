# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código al contenedor
COPY . .

# Exponemos el puerto 5000 para Flask
EXPOSE 5000

# Comando por defecto al iniciar el contenedor
CMD ["python", "app.py"]
