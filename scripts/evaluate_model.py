import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

TEST_DIR = "data/raw/test"
MODEL_PATH = "models/emotion_model.keras"
LABELS_PATH = "models/labels.json"

def evaluate():
    # 1. Load Labels & Model
    with open(LABELS_PATH, "r") as f:
        label_map = json.load(f)
    classes = [label_map[str(i)] for i in range(len(label_map))]

    print(f"Loading trained model from {MODEL_PATH}...")
    model = load_model(MODEL_PATH)

    # 2. Test Data Generator (No shuffle to keep indices aligned)
    test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)
    test_generator = test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=(48, 48),
        color_mode="grayscale",
        batch_size=64,
        class_mode="categorical",
        shuffle=False
    )

    # 3. Generate Predictions
    print("Evaluating predictions across test dataset...")
    predictions = model.predict(test_generator)
    y_pred = np.argmax(predictions, axis=1)
    y_true = test_generator.classes

    # 4. Classification Report
    print("\n--- Detailed Classification Report ---")
    report = classification_report(y_true, y_pred, target_names=classes)
    print(report)

    # 5. Confusion Matrix Visualization
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Facial Emotion Confusion Matrix')
    plt.xlabel('Predicted Emotion')
    plt.ylabel('Ground Truth Emotion')
    plt.tight_layout()
    plt.savefig("docs/confusion_matrix.png")
    print("Confusion matrix saved to docs/confusion_matrix.png")

if __name__ == "__main__":
    evaluate()