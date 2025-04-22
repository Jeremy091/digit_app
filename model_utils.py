# model_utils.py

import numpy as np
import cv2
import imageio
from tensorflow.keras.models import load_model

# Carga tu modelo entrenado
_model = load_model('digit_model_color_augment.h5')


def ensure_white_digit_black_bg(img_gray: np.ndarray) -> np.ndarray:
    """
    Si el fondo es mayoritariamente blanco, invierte para
    que el dígito quede blanco sobre fondo negro.
    """
    # Media de píxeles: si es alta, hay más blanco que negro
    if np.mean(img_gray) > 127:
        img_gray = cv2.bitwise_not(img_gray)
    return img_gray


def preprocess_custom(img_rgb: np.ndarray) -> np.ndarray:
    # 1) Gris
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # 1b) Corrección automática de inversión
    #    Si la media de gris es baja (fondo negro),
    #    invertimos para que fondo sea blanco.
    if np.mean(gray) < 127:
        gray = cv2.bitwise_not(gray)

    # 2) Ecualización CLAHE (opcional, mejora el contraste)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # 3) Umbral Otsu invertido
    _, thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # 4) Encontrar contorno, recortar
    cnts, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    x, y, w, h = cv2.boundingRect(max(cnts, key=cv2.contourArea))
    digit = thresh[y:y+h, x:x+w]

    # 5) Escalar a 20×20
    k = 20.0 / max(w,h)
    digit = cv2.resize(digit, (int(w*k), int(h*k)))

    # 6) Centrar en 28×28
    canvas = np.zeros((28,28), dtype=np.uint8)
    dx, dy = (28-digit.shape[1])//2, (28-digit.shape[0])//2
    canvas[dy:dy+digit.shape[0], dx:dx+digit.shape[1]] = digit

    # 7) Normalizar y convertir a RGB
    canvas = canvas.astype('float32') / 255.0
    return np.repeat(canvas[...,None], 3, axis=-1)


def predict_image(file_bytes: bytes) -> dict:
    """
    Lee bytes de imagen, decodifica con OpenCV, aplica preprocess_custom,
    y devuelve la predicción {'digit': int, 'confidence': float}.
    """
    # 1) Leer imagen desde bytes
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError("No se pudo decodificar la imagen")

    # 2) Convertir a RGB puro
    if img.ndim == 2:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        # BGR o BGRA → RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if img.shape[2] == 3 else cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

    # 3) Preprocesar (binarizar, centrar, normalizar)
    proc = preprocess_custom(img_rgb)

    # 4) Preparar batch y predecir
    X = np.expand_dims(proc, axis=0).astype('float32')
    preds = _model.predict(X, verbose=0)[0]

    return {
        'digit': int(np.argmax(preds)),
        'confidence': float(np.max(preds))
    }
