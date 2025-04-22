import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import imageio

_model = load_model('digit_model_color_augment.h5')

def preprocess_custom(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) if img.ndim == 3 else img
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    cnts, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    x, y, w, h = cv2.boundingRect(max(cnts, key=cv2.contourArea))
    digit = thresh[y:y+h, x:x+w]
    k = 20.0 / max(w, h)
    digit = cv2.resize(digit, (int(w*k), int(h*k)))
    canvas = np.zeros((28,28), dtype=np.uint8)
    dx, dy = (28 - digit.shape[1]) // 2, (28 - digit.shape[0]) // 2
    canvas[dy:dy+digit.shape[0], dx:dx+digit.shape[1]] = digit
    canvas = canvas.astype('float32') / 255.0
    return np.repeat(canvas[..., None], 3, axis=-1)

def predict_image(file_bytes):
    img = imageio.imread(file_bytes)
    if img.ndim == 4:  # RGBA
        img = img[..., :3]

    proc = preprocess_custom(img)
    X = np.expand_dims(proc, axis=0)
    pred = _model.predict(X, verbose=0)[0]

    digit = int(np.argmax(pred))
    confidence = float(np.max(pred))
    return {"digit": digit, "confidence": confidence}
