import cv2
import mediapipe as mp
import numpy as np
import json
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

# MediaPipe Setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Define which landmarks to exclude (face landmarks)
EXCLUDED_LANDMARKS = list(range(0, 11))  # 0 to 10 inclusive

def generate_frames(camera_id=0):
    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        app.logger.error(f"Error: Could not open camera with ID {camera_id}")
        return

    while True:
        success, image = cap.read()
        if not success:
            app.logger.warning("Ignoring empty camera frame.")
            continue

        # Pose Detection and Landmark Extraction
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Filtered Landmarks
        landmarks = []
        if results.pose_landmarks:
            for id, landmark in enumerate(results.pose_landmarks.landmark):
                if id not in EXCLUDED_LANDMARKS:
                    landmarks.append({
                        'id': id,
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z,
                        'visibility': landmark.visibility
                    })

                    # Display (x, y) coordinates on image (only for non-excluded landmarks)
                    image_height, image_width, _ = image.shape
                    x_px = int(landmark.x * image_width)
                    y_px = int(landmark.y * image_height)
                    cv2.putText(
                        image,
                        str(id) + f' ({x_px}, {y_px})',
                        (x_px + 5, y_px),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        2
                    )

        # Pose Analysis and Feedback (Placeholder)
        feedback = analyze_pose(landmarks)

        # Skeleton Markings (Only Non-Excluded Landmarks)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            # Filter landmarks and connections
            landmark_subset = [lm for i, lm in enumerate(results.pose_landmarks.landmark) if i not in EXCLUDED_LANDMARKS]
            connections_subset = [(a - len(EXCLUDED_LANDMARKS), b - len(EXCLUDED_LANDMARKS)) for a, b in mp_pose.POSE_CONNECTIONS if a not in EXCLUDED_LANDMARKS and b not in EXCLUDED_LANDMARKS]

            mp_drawing.draw_landmarks(
                image,
                landmark_subset,
                connections_subset,
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
            )

        # Prepare Data for Sending
        data = {'landmarks': landmarks, 'feedback': feedback}
        response_data = json.dumps(data)

        # Yield Frame and Data
        _, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
               b'Content-Type: application/json\r\n\r\n' + response_data.encode() + b'\r\n')
    cap.release()


# Placeholder for your pose analysis logic
def analyze_pose(landmarks):
    # ... (Your pose analysis logic here)
    feedback = "This is where your AI-generated feedback would go."
    return feedback

@app.route('/video_feed/<int:camera_id>')
def video_feed(camera_id):
    app.logger.info(f"Connecting to camera with ID {camera_id}")
    return Response(generate_frames(camera_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2000)
