import cv2

# Open the default camera (0 = laptop's built-in webcam)
camera = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    success, frame = camera.read()

    # If the camera couldn't provide a frame, stop
    if not success:
        print("Could not access the camera.")
        break

    # Display the frame
    cv2.imshow("Laptop Camera", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
camera.release()

# Close all OpenCV windows
cv2.destroyAllWindows()