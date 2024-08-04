import cv2

# Load classifiers once (no need to reload in the loop)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Open the default camera
cap = cv2.VideoCapture(1)  # 0 is usually the default camera

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

while True:
    # Read a frame
    ret, frame = cap.read()

    # Check if frame was successfully read
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert to grayscale (faster face detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Optimized face detection parameters (adjust for better results)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        # Region of Interest (ROI) for eye detection
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect eyes within the face ROI
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            # Draw eye rectangles
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

    # Display the resulting frame
    cv2.imshow('Face & Eye Detection', frame)  # More descriptive window name

    # Exit on 'Esc' key press
    if cv2.waitKey(1) == 27:  # Wait 1 ms for key press
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# import keyboard
# import time
# import random
#
#
# def type_like_human(text):
#     for char in text:
#         keyboard.write(char)
#
#         # Randomness for typing speed
#         base_delay = 0.01  # Adjust this base value for overall speed
#         randomness = random.uniform(0.05, 0.2)  # Add slight variations
#         delay = base_delay + randomness
#         time.sleep(delay)
#
#
# # Get text input from txt file in current directory
# text_to_type = open('text.txt', 'r').read()
#
# time.sleep(1)
#
# # Start typing
# type_like_human(text_to_type)
