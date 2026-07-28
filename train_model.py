import os
import cv2
import pickle
from insightface.app import FaceAnalysis

# -----------------------------
# Dataset Path
# -----------------------------
DATASET_PATH = "dataset"

print("Loading InsightFace Model...")

app = FaceAnalysis()
app.prepare(ctx_id=0)

print("✅ Model Loaded Successfully!\n")

# Dictionary to store embeddings
trained_data = {}

print("Reading Dataset...\n")

# -----------------------------
# Read Student Folders
# -----------------------------
for student_folder in os.listdir(DATASET_PATH):

    folder_path = os.path.join(DATASET_PATH, student_folder)

    if not os.path.isdir(folder_path):
        continue

    # Folder format: 101_UTKARSHA
    student_id, student_name = student_folder.split("_", 1)

    print(f"Processing Student: {student_name}")

    embeddings = []

    # -----------------------------
    # Read Images
    # -----------------------------
    for image_name in sorted(os.listdir(folder_path)):

        image_path = os.path.join(folder_path, image_name)

        image = cv2.imread(image_path)

        faces = app.get(image)

        if len(faces) == 0:
            print(f"Skipping {image_name} (No Face Found)")
            continue

        face = faces[0]

        # Get embedding
        embeddings.append(face.embedding)

    trained_data[student_id] = {
        "name": student_name,
        "embeddings": embeddings
    }

print("\n✅ Training Completed!\n")

print("Students Trained:", len(trained_data))

for student_id, data in trained_data.items():
    print(f"\nStudent ID : {student_id}")
    print(f"Name       : {data['name']}")
    print(f"Embeddings : {len(data['embeddings'])}")

# -----------------------------
# Save Trained Data
# -----------------------------
with open("trained_model.pkl", "wb") as file:
    pickle.dump(trained_data, file)

print("\n✅ Trained model saved successfully!")