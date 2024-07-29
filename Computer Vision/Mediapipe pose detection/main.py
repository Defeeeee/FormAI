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

def generate_frames(camera_id=0):
    cap = cv2.VideoCapture(camera_id)

    # Check if camera opened successfully
    if not cap.isOpened():
        app.logger.error(f"Error: Could not open camera with ID {camera_id}")
        return

    while True:
        success, image = cap.read()
        if not success:
            app.logger.warning("Ignoring empty camera frame.")
            continue  # Skip empty frames

        # Pose Detection and Landmark Extraction
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        landmarks = []
        if results.pose_landmarks:
            for landmark in results.pose_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x, 'y': landmark.y, 'z': landmark.z, 'visibility': landmark.visibility
                })

        # Pose Analysis and Feedback (Placeholder)
        feedback = analyze_pose(landmarks)

        # Skeleton Markings (Alternative Method)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            # Custom drawing options
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),  # Red dots
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)  # Green lines
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
    # Replace with your sophisticated pose analysis logic
    # Compare to ideal pose, calculate angles, distances, etc.
    feedback = "This is where your AI-generated feedback would go."
    return feedback

@app.route('/video_feed/<int:camera_id>')
def video_feed(camera_id):
    app.logger.info(f"Connecting to camera waith ID {camera_id}")
    return Response(generate_frames(camera_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2000)
