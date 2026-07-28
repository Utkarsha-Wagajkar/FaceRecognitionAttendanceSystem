import cv2
import pickle
from datetime import datetime
from utils import load_face_model
from sklearn.metrics.pairwise import cosine_similarity

from database import attendance_exists, mark_attendance, get_student

# -----------------------------
# Recognition Threshold
# -----------------------------
THRESHOLD = 0.60

# -----------------------------
# Load Trained Model
# -----------------------------
print("Loading trained model...")

with open("trained_model.pkl", "rb") as file:
    trained_data = pickle.load(file)

print("✅ Trained model loaded successfully!")

# -----------------------------
# Load InsightFace
# -----------------------------
print("Loading InsightFace...")

app = load_face_model()

# -----------------------------
# Open Camera
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Could not open the camera.")
    exit()

attendance_done = set()
attendance_message = ""

print("\nOpening Camera...")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    faces = app.get(frame)

    for face in faces:

        x1, y1, x2, y2 = face.bbox.astype(int)
        embedding = face.embedding

        best_match = "Unknown"
        best_student_id = None
        best_score = 0

        # Default values
        student_name = "Unknown"
        student_id = "-"
        department = "-"
        year = "-"

        # -----------------------------
        # Compare with all registered students
        # -----------------------------
        for stored_student_id, data in trained_data.items():

            for stored_embedding in data["embeddings"]:

                score = cosine_similarity(
                    embedding.reshape(1, -1),
                    stored_embedding.reshape(1, -1)
                )[0][0]

                if score > best_score:
                    best_score = score
                    best_match = data["name"]
                    best_student_id = stored_student_id

        # -----------------------------
        # Student Recognized
        # -----------------------------
        if best_score >= THRESHOLD:

            student = get_student(best_student_id)

            if student:
                student_id = student[0]
                student_name = student[1]
                department = student[2]
                year = student[3]

            today = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M:%S")

            if best_student_id not in attendance_done:

                if not attendance_exists(best_student_id, today):

                    mark_attendance(
                        best_student_id,
                        today,
                        current_time
                    )

                    print(f"✅ Attendance Marked : {student_name}")
                    attendance_message = "Attendance Marked"

                else:

                    print(f"⚠ Attendance already marked : {student_name}")
                    attendance_message = "Already Marked"

                attendance_done.add(best_student_id)

        # -----------------------------
        # Unknown Person
        # -----------------------------
        else:

            student_name = "Unknown"
            student_id = "-"
            department = "-"
            year = "-"

        # -----------------------------
        # Draw Rectangle
        # -----------------------------
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # -----------------------------
        # Display Student Information
        # -----------------------------
        cv2.putText(
            frame,
            student_name,
            (x1, y1 - 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"ID : {student_id}",
            (x1, y1 - 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"{department} | {year}",
            (x1, y1 - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

        cv2.putText(
        frame,
        f"Confidence : {best_score*100:.2f}%",
        (x1, y1 - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 0),
        2
    )

    # ---------------------------------------------
    # Attendance Status Message
    # ---------------------------------------------
    if attendance_message:

        color = (0, 255, 0)

        if attendance_message == "Already Marked":
            color = (0, 165, 255)

        cv2.putText(
            frame,
            attendance_message,
            (x1, y2 + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    cv2.imshow("Face Recognition Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()