import numpy as np
import cv2
from tensorflow.keras.models import load_model

_model = load_model("digit_model_color_augment.h5")

def preprocess_custom(img: np.ndarray) -> np.ndarray:
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Apply Otsu thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Morphological operations
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Find bounding box
    coords = cv2.findNonZero(morph)
    x, y, w, h = cv2.boundingRect(coords)

    digit = morph[y:y+h, x:x+w]

    # Resize and center
    canvas = np.ones((64, 64), dtype=np.uint8) * 0
    digit = cv2.resize(digit, (32, 32))
    start_x = (64 - 32) // 2
    start_y = (64 - 32) // 2
    canvas[start_y:start_y+32, start_x:start_x+32] = digit

    # Normalize and stack
    canvas = canvas.astype('float32') / 255.0
    canvas = np.stack([canvas]*3, axis=-1)

    return canvas

def predict_image(file_bytes_io):
    data = file_bytes_io.read() if hasattr(file_bytes_io, 'read') else file_bytes_io
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError("No se pudo decodificar la imagen")
    
    if img.ndim == 3:
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    proc = preprocess_custom(img)
    X = np.expand_dims(proc, axis=0).astype('float32')

    preds = _model.predict(X)
    digit = int(np.argmax(preds[0]))
    confidence = float(np.max(preds[0]))
    return {"digit": digit, "confidence": confidence}
