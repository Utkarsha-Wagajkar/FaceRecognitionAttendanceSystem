import os
import cv2
from database import add_student, student_exists


# -----------------------------
# Get Student ID
# -----------------------------
def get_student_id():

    student_id = input("Enter Student ID: ").strip()

    if student_exists(student_id):

        print("\n❌ Student ID already exists!")
        print("Please enter another Student ID.\n")

        return None

    return student_id


# -----------------------------
# Get Student Information
# -----------------------------
def get_student_information():

    student_name = input("Enter Student Name: ").strip().upper()
    department = input("Enter Department: ").strip().upper()
    year = input("Enter Year (FE/SE/TE/BE): ").strip().upper()

    return student_name, department, year


# -----------------------------
# Create Student Folder
# -----------------------------
def create_student_folder(student_id, student_name):

    folder_name = f"{student_id}_{student_name}"
    dataset_path = os.path.join("dataset", folder_name)

    os.makedirs(dataset_path, exist_ok=True)

    print("\nStudent folder ready!")
    print("Opening camera...\n")

    return dataset_path


# -----------------------------
# Register Student
# -----------------------------
def register_student():

    student_id = get_student_id()

    if student_id is None:
        return None

    student_name, department, year = get_student_information()

    dataset_path = create_student_folder(student_id, student_name)

    return student_id, student_name, department, year, dataset_path


# -----------------------------
# Start Registration
# -----------------------------
result = register_student()

if result is None:
    exit()

student_id, student_name, department, year, dataset_path = result

# -----------------------------
# Load Face Detection Model
# -----------------------------
model_path = "models/face_detection_yunet_2023mar.onnx"

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

detector = cv2.FaceDetectorYN.create(
    model_path,
    "",
    (width, height)
)

image_count = 0

while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to access webcam.")
        break

    detector.setInputSize((frame.shape[1], frame.shape[0]))

    _, faces = detector.detect(frame)

    if faces is not None:

        # Allow only one person
        if len(faces) == 1:

            face = faces[0]

            x, y, w, h = face[:4].astype(int)

            # Draw Rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0,255,0),
                2
            )

            # Crop Face
            face_crop = frame[y:y+h, x:x+w]

            # Save Image
            image_path = os.path.join(
                dataset_path,
                f"{image_count+1}.jpg"
            )

            cv2.imwrite(image_path, face_crop)

            image_count += 1

            cv2.putText(
                frame,
                f"Images Captured : {image_count}/30",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

            cv2.waitKey(150)

        else:

            cv2.putText(
                frame,
                "Only ONE person should be visible!",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,0,255),
                2
            )

    cv2.imshow("Student Registration", frame)

    if image_count >= 30:
        add_student(
    student_id,
    student_name,
    department,
    year
)
        print("\nRegistration Completed Successfully!")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()