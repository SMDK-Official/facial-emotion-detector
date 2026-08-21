import os
import json
import cv2
import pandas as pd

RAW_DATA_DIR = "data/raw"
TRAIN_DIR = os.path.join(RAW_DATA_DIR, "train")
TEST_DIR = os.path.join(RAW_DATA_DIR, "test")
OUTPUT_LABELS_FILE = "models/labels.json"

def inspect_and_validate_dataset():
    """Validates image integrity and counts samples per class."""
    if not os.path.exists(TRAIN_DIR) or not os.path.exists(TEST_DIR):
        print(f"Error: Dataset directories not found in {RAW_DATA_DIR}")
        print("Please ensure you unzipped the dataset into data/raw/train and data/raw/test")
        return

    # Discover classes dynamically from directory names (alphabetical order)
    classes = sorted([d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))])
    print(f"Discovered {len(classes)} emotion classes: {classes}")

    # Build and save dynamic label mapping
    label_map = {idx: class_name for idx, class_name in enumerate(classes)}
    os.makedirs("models", exist_ok=True)
    with open(OUTPUT_LABELS_FILE, "w") as f:
        json.dump(label_map, f, indent=4)
    print(f"Saved label mapping to {OUTPUT_LABELS_FILE}")

    stats = []
    corrupted_count = 0

    for split_name, split_path in [("train", TRAIN_DIR), ("test", TEST_DIR)]:
        for emotion in classes:
            folder = os.path.join(split_path, emotion)
            files = os.listdir(folder)
            valid_images = 0

            for file in files:
                file_path = os.path.join(folder, file)
                # Verify image can be decoded
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if img is None or img.shape != (48, 48):
                    corrupted_count += 1
                else:
                    valid_images += 1

            stats.append({
                "Split": split_name,
                "Emotion": emotion,
                "Valid Images": valid_images
            })

    df = pd.DataFrame(stats)
    print("\n--- Dataset Distribution Summary ---")
    print(df.to_string(index=False))
    print(f"\nTotal corrupted/unreadable images found: {corrupted_count}")

if __name__ == "__main__":
    inspect_and_validate_dataset()