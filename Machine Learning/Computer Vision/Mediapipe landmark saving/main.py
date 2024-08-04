import cv2
import mediapipe as mp
import numpy as np


def extract_features_from_video(video_url):
    """Retrieves video from URL and extracts pose features using MediaPipe.

    Args:
        video_url: The URL of the video to process.

    Returns:
        A NumPy array containing the extracted pose features for each frame.
    """
    cap = cv2.VideoCapture(video_url)  # Open video from URL

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose()

    all_features = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # MediaPipe Pose processing
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            # Extract and normalize pose landmarks (33 keypoints)
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark])
            landmarks = landmarks.flatten()  # Flatten for easier storage

            # Further feature engineering (optional)
            # E.g., calculate joint angles, distances, etc.

            all_features.append(landmarks)

        # Draw landmarks and display AFTER processing (inside the loop)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display the processed frame
        cv2.imshow('MediaPipe Pose', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    # Release video resources after the loop
    cap.release()
    cv2.destroyAllWindows()  # Close the display window
    return np.array(all_features)  # Convert to NumPy array


# Example Usage
video_url = ""
pose_features = extract_features_from_video(video_url)
print(pose_features.shape)  # (num_frames, 99) for 33 keypoints
