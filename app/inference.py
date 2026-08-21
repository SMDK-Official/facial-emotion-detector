import os
import json
import base64
import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "emotion_model.keras")
LABELS_PATH = os.path.join(BASE_DIR, "models", "labels.json")
CASCADE_PATH = os.path.join(BASE_DIR, "models", "haarcascade_frontalface_default.xml")

# Initialize global variables for our models
emotion_model = None
label_map = None
face_cascade = None

def load_inference_models():
    """Loads the neural network and face detector into memory once."""
    global emotion_model, label_map, face_cascade
    
    if emotion_model is None:
        print("[INFO] Loading emotion CNN model...")
        emotion_model = load_model(MODEL_PATH)
        
    if label_map is None:
        with open(LABELS_PATH, "r") as f:
            label_map = json.load(f)
            
    if face_cascade is None:
        print("[INFO] Loading Haar Cascade face detector...")
        face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def process_base64_image(base64_string):
    """Converts a web base64 image string into an OpenCV image matrix."""
    # Remove the "data:image/jpeg;base64," header sent by the browser
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
        
    img_data = base64.b64decode(base64_string)
    np_arr = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return image

def predict_emotion(base64_string):
    """Detects a face in the image and predicts its emotion."""
    # Ensure models are loaded
    load_inference_models()
    
    # 1. Decode image and convert to grayscale (Haar cascades need grayscale)
    image = process_base64_image(base64_string)
    if image is None:
        return {"error": "Invalid image data"}
        
    gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. Detect faces
    faces = face_cascade.detectMultiScale(
        gray_frame, 
        scaleFactor=1.3, 
        minNeighbors=5, 
        minSize=(48, 48)
    )
    
    # 3. Handle cases with no face or multiple faces
    if len(faces) == 0:
        return {"status": "no_face_detected"}
        
    # We will process only the largest face found (primary subject)
    # Sort faces by area (width * height) in descending order
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    x, y, w, h = faces[0]
    
    # 4. Crop the face out of the frame
    roi_gray = gray_frame[y:y + h, x:x + w]
    
    # 5. Preprocess the cropped face exactly how we trained the CNN
    roi_resized = cv2.resize(roi_gray, (48, 48))
    roi_normalized = roi_resized / 255.0
    roi_expanded = np.expand_dims(roi_normalized, axis=0) # Add batch dimension
    roi_expanded = np.expand_dims(roi_expanded, axis=-1)  # Add channel dimension
    
    # 6. Predict!
    predictions = emotion_model.predict(roi_expanded, verbose=0)[0]
    best_guess_index = int(np.argmax(predictions))
    confidence = float(predictions[best_guess_index]) * 100
    
    emotion_name = label_map[str(best_guess_index)]
    
    return {
        "status": "success",
        "emotion": emotion_name,
        "confidence": round(confidence, 2),
        "box": {"x": int(x), "y": int(y), "w": int(w), "h": int(h)}
    }