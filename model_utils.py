# model_utils.py
import numpy as np
import cv2
import imageio
from tensorflow.keras.models import load_model

# 1) Carga del modelo ya entrenado
_model = load_model("digit_model_color_augment.h5")

def preprocess_custom(img):
    # ... copia aquí TU función completa de preprocess_custom ...
    # (incluyendo Otsu, cierre, dilatación, recorte, centrado)
    # y que devuelva un array (28,28,3) normalizado [0,1].
    pass

def predict_image(file_bytes):
    # file_bytes: BytesIO o similar con la imagen subida
    img = imageio.imread(file_bytes, pilmode="RGB")
    proc = preprocess_custom(img)
    X = np.expand_dims(proc, axis=0)
    pred = _model.predict(X)[0]
    return {
      "digit": int(np.argmax(pred)),
      "confidence": float(np.max(pred))
    }
