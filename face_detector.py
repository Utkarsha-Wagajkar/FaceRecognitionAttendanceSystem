import cv2

# Load the YuNet face detection model
model_path = "models/face_detection_yunet_2023mar.onnx"

# Open the webcam
cap = cv2.VideoCapture(0)

# Get the webcam resolution
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create the face detector
detector = cv2.FaceDetectorYN.create(
    model_path,
    "",
    (width, height)
)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read from webcam.")
        break

    # Tell the detector the current image size
    detector.setInputSize((frame.shape[1], frame.shape[0]))

    # Detect faces
    _, faces = detector.detect(frame)

    # Draw rectangles around detected faces
    if faces is not None:
        for face in faces:
            x, y, w, h = face[:4].astype(int)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()