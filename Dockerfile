# Dockerfile
FROM python:3.9-slim

# 1) Instalar librerías de sistema necesarias para cv2
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 && \
    rm -rf /var/lib/apt/lists/*

# 2) Directorio de trabajo e instalación de dependencias Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copiar el código de la aplicación
COPY . .

# 4) Exponer el puerto que utiliza Flask
EXPOSE 5000

# 5) Comando por defecto al arrancar
CMD ["python", "app.py"]
